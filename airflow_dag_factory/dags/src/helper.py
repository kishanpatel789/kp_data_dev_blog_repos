import logging

task_logger = logging.getLogger("airflow.task")


def print_context(**context):
    print(context)

    data_interval_start = context["data_interval_start"]
    data_interval_end = context["data_interval_end"]
    logical_date = context["logical_date"]

    task_logger.info(f"{data_interval_start=}")
    task_logger.info(f"{data_interval_end=}")
    task_logger.info(f"{logical_date=}")
