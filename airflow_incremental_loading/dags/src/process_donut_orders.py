def calculate_hourly_stats(templates_dict):
    from pathlib import Path
    import logging

    import polars as pl

    logger = logging.getLogger("airflow.task")
    dir_input = Path("./data/orders")
    dir_output = Path("./data/hourly_summary")
    if not dir_output.exists():
        dir_output.mkdir()

    path_input = dir_input / f"{templates_dict['file_name']}.json"
    path_output = dir_output / f"{templates_dict['file_name']}.csv"

    # read json
    logger.info(f"Reading file '{path_input}'...")
    df = pl.read_json(
        path_input,
        schema={
            "num_donuts": pl.Int32,
            "order_time": pl.Datetime,
            "user_name": pl.String,
        },
    )
    logger.info(f"    Read {df.height:,} rows from .json file")

    # calculate hourly summary
    logger.info("Calculating hourly summary...")
    df_out = (
        df.with_columns(date_hour=df["order_time"].dt.truncate("1h"))
        .group_by("date_hour")
        .agg(pl.col("num_donuts").sum())
        .sort("date_hour")
    )
    logger.info(f"    Aggregated to {df_out.height:,} rows in hourly summary")

    # write as csv
    df_out.write_csv(path_output)
    logger.info(f"Saved file '{path_output}'")
