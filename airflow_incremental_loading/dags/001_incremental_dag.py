from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="001_incremental_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@weekly",
):
    bash_task = BashOperator(
        task_id="bash_task",
        bash_command="echo {{logical_date}} - {{data_interval_start}} - {{data_interval_end}}",
    )

    bash_task
