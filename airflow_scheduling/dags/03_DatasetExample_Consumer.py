from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

from src.datasets import my_dataset

with DAG(
    dag_id="03_DatasetExample_Consumer",
    schedule=my_dataset,
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
        bash_command="cat /opt/airflow/my_file.txt",
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command='rm /opt/airflow/my_file.txt',
    )

    t1 >> t2 >> t3
