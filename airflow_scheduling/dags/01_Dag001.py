from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="01_Dag001",
    schedule=timedelta(minutes=10),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["kp-data-dev"],
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command='echo "Begin"',
    )

    t2 = BashOperator(
        task_id="t2",
        bash_command="echo '{{data_interval_start}} {{data_interval_end}}' && echo '{{logical_date}}'",
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command='echo "The End"',
    )

    t1 >> t2 >> t3
