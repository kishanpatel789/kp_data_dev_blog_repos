# %%
import csv
import time
from collections import Counter
from typing import List, Dict, Any, Optional

import requests

from config import API_SERVER, CSV_DIR, CONTROL
from schemas import schemas


# %%
def generate_column_names(table_schema: Dict[str, Any]) -> List[str]:
    """
    Translate a dictionary describing API endpoint into a list of column names.

    Args:
        table_schema (Dict[str, Any]): Dictionary representing the API endpoint and relevant attributes.

    Returns:
        List[str]: List of columns to represent the API scraped data as a relational table.
    """

    if not isinstance(table_schema, dict):
        raise TypeError(
            f"Input 'table_schema' must be a dictionary. Received type '{type(table_scheam)}'."
        )

    column_names = ["id"]
    if table_schema.get("id_ref") is not None:
        column_names.append(table_schema["id_ref"] + "_id")
    column_names.extend(table_schema["attributes"])

    return column_names


def generate_sub_column_names(table: str, array_attribute: str) -> List[str]:
    """
    Generate column names to represented nested arrays from API output.

    Args:
        table (str): Name of base table.
        array_attribute (str): Key of the nested array key-value pair in the API response.

    Returns:
        List[str]: List of columns to represent the sub-table populated with a nested array in the API response.
    """

    sub_column_names = [f"{table}_id", array_attribute]

    return sub_column_names


def make_api_get_request(
    url: str, payload: Optional[Dict[str, str]] = None, max_retries: int = 5
) -> Dict[str, Any]:
    """
    Make a GET request to the RESTAPI endpoint and return the results. Exponential backoff is implemented to handle 429 errors.

    Args:
        url (str): URL of API endpoint
        payload (Optional[Dict[str, str]], optional): A dictionary of key-values to be converted into the URL query component. Defaults to None.
        max_retries (int, optional): The maximum number of request attempts when facing 429 errors. Defaults to 5.

    Raises:
        Exception: Raises exception when maximum retry attempts have been reached.

    Returns:
        Dict[str, Any]: A dictionary representing the JSON response from the API endpoint.
    """

    retry_delay = 1  # 1 second
    for _ in range(max_retries):
        try:
            response = requests.get(url, params=payload)
            print(f"Called '{response.request.url}'")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            if response.status_code == 429:
                print("Reached rate limit and received 429 error. Will try again...")
                time.sleep(retry_delay)
                retry_delay *= 2  # double the delay for next attempt
            else:
                raise
    raise Exception("Maximum retry attempts reached. Try again in an hour.")


def write_to_csv(
    response_json: Dict[str, Any],
    table: str,
    table_schema: Dict[str, Any],
    column_names: List[str],
) -> None:
    """
    Loop through records in API response and write to CSV file. For nested attributes identified in `table_schema`, also write a sub-file.

    Args:
        response_json (Dict[str, Any]): Dictionary representing response from API.
        table (str): Name of table.
        table_schema (Dict[str, Any]): Dictionary representing the API endpoint and relevant attributes.
        column_names (List[str]): List of columns to represent the API scraped data as a relational table.
    """

    # initialize counter to track number of records written
    record_counter = Counter()

    # open csv file to append
    csv_file_name = f"{table}.csv"
    with open(CSV_DIR / csv_file_name, "at", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=column_names, quoting=csv.QUOTE_ALL)

        for record in response_json["data"]:
            # write base csv
            row = dict(id=record["id"])
            if table_schema.get("id_ref") is not None:
                id_ref_key = table_schema["id_ref"] + "_id"
                id_ref_value = record["relationships"][table_schema["id_ref"]]["data"][
                    "id"
                ]
                row.update({id_ref_key: id_ref_value})
            row.update({k: record["attributes"][k] for k in table_schema["attributes"]})
            writer.writerow(row)
            record_counter[csv_file_name] += 1

            # write array attributes as sub csv
            if table_schema.get("array_attributes") is not None:
                for array_attribute in table_schema["array_attributes"]:
                    sub_csv_file_name = f"{table}_{array_attribute}.csv"
                    with open(CSV_DIR / sub_csv_file_name, "at", newline="") as f_sub:
                        sub_column_names = generate_sub_column_names(
                            table, array_attribute
                        )
                        sub_writer = csv.DictWriter(
                            f_sub, fieldnames=sub_column_names, quoting=csv.QUOTE_ALL
                        )

                        for value in record["attributes"][array_attribute]:
                            sub_row = {
                                sub_column_names[0]: record["id"],
                                sub_column_names[1]: value,
                            }

                            sub_writer.writerow(sub_row)
                            record_counter[sub_csv_file_name] += 1

        # output written record counts
        for file_name, record_count in record_counter.items():
            print(f"    Wrote {record_count:,} records to '{file_name}'")


def call_and_write(
    table: str,
    table_schema: Dict[str, Any],
    column_names: List[str],
    url: Optional[str] = None,
) -> None:
    """
    Call API endpoint and write output to CSV. Use API's pagination to make any follow-up API calls as needed.

    Args:
        table (str): Name of table.
        table_schema (Dict[str, Any]): Dictionary representing the API endpoint and relevant attributes.
        column_names (List[str]): List of columns to represent the API scraped data as a relational table.
        url (Optional[str], optional): Initial URL of API endpoint. Defaults to None.
    """

    # create base url
    if url is None:
        url = f"{API_SERVER}/{table_schema['api_endpoint']}"
    url_payload = table_schema.get("api_query")

    # call api as many times as needed
    while url is not None:
        r_json = make_api_get_request(url, url_payload)

        # write to csv file
        write_to_csv(r_json, table, table_schema, column_names)

        # get ready for next page
        url = r_json["links"].get("next")
        url_payload = None


# %%
def main():
    """
    Loop through endpoint descriptions in `schemas.py`. For each endpoint, call the API and write output to CSV files.
    """

    # identify endpoints to read into tables
    tables_to_get = [k for k, v in CONTROL.items() if v == 1]

    for table in tables_to_get:
        print(f"\n============= {table} =============")
        table_schema = schemas[table]

        # identify final table columns
        column_names = generate_column_names(table_schema)

        # initialize base csv file
        with open(CSV_DIR / f"{table}.csv", "wt", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_names, quoting=csv.QUOTE_ALL)
            writer.writeheader()

        # initialize sub-attribute csv files
        if table_schema.get("array_attributes") is not None:
            for array_attribute in table_schema["array_attributes"]:
                with open(
                    CSV_DIR / f"{table}_{array_attribute}.csv", "wt", newline=""
                ) as f:
                    sub_column_names = generate_sub_column_names(table, array_attribute)
                    writer = csv.DictWriter(
                        f, fieldnames=sub_column_names, quoting=csv.QUOTE_ALL
                    )
                    writer.writeheader()

        # for endpoints requiring reference IDs, generate custom API URL
        if table_schema.get("id_ref") is not None:
            with open(CSV_DIR / f"{table_schema['id_ref']}.csv", "rt", newline="") as f:
                reader_column_names = generate_column_names(
                    schemas[f"{table_schema['id_ref']}"]
                )
                reader = csv.DictReader(f, fieldnames=reader_column_names)
                _ = next(reader)  # read header

                for ref_row in reader:
                    print(f"Preparing for reference '{ref_row['slug']}'")

                    api_endpoint = table_schema["api_endpoint"].format(
                        rel_id=ref_row["id"]
                    )
                    url = f"{API_SERVER}/{api_endpoint}"

                    call_and_write(table, table_schema, column_names, url)
        else:
            call_and_write(table, table_schema, column_names)


# %%
if __name__ == "__main__":
    # create csv directory if needed
    if not CSV_DIR.exists():
        print(f"Creating directory: '{CSV_DIR}'.")
        CSV_DIR.mkdir(parents=True)

    main()
