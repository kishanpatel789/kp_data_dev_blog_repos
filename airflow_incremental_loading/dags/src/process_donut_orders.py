def calculate_hourly_stats(templates_dict):
    from pathlib import Path
    import polars as pl
    
    dir_data = Path("./data")
    dir_input = dir_data / "orders"
    dir_output = dir_data / "hourly_summary"

    file_name = templates_dict["file_name"]

    # read json
    df = pl.read_json(
        dir_input / f"{file_name}.json",
        schema={
            "num_donuts": pl.Int32,
            "order_time": pl.String,
            "user_name": pl.String,
        },
    )
    df = df.with_columns(
        order_time=df["order_time"].str.to_datetime("%a, %d %b %Y %H:%M:%S %Z")
    )

    # calculate hourly summary

    # write as csv
    df.write_csv(dir_output / f"{file_name}.csv")
