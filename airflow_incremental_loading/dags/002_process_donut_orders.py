from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonVirtualenvOperator

from src.process_donut_orders import calculate_hourly_stats


with DAG(
    dag_id="002_process_donut_orders",
    start_date=datetime(2025, 2, 1),
    schedule="@daily",
    max_active_runs=4,
    catchup=True,
):

    get_orders = BashOperator(
        task_id="get_orders",
        bash_command=(
            "mkdir -p $AIRFLOW_HOME/data/orders && "
            "curl -sSo $AIRFLOW_HOME/data/orders/{{ data_interval_start | ds }}.json "
            "'http://orders_api:8000/orders?"
            "start_date={{ data_interval_start | ds }}&"
            "end_date={{ data_interval_end | ds }}'"
        ),
    )

    process_orders = PythonVirtualenvOperator(
        task_id="process_orders",
        python_callable=calculate_hourly_stats,
        requirements=["polars==1.21.0"],
        system_site_packages=True,
        templates_dict={"file_name": "{{ data_interval_start | ds }}"},
        venv_cache_path=Path("/home/airflow/venv-cache"),
    )

    get_orders >> process_orders
