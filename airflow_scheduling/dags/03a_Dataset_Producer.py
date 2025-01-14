from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

from src.datasets import my_dataset

with DAG(
    dag_id="03a_Dataset_Producer",
    schedule="45 15 * * 4",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["dataset"],
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo 'Begin'",
    )

    t2 = BashOperator(
        task_id="t2",
        bash_command=f"pwd && echo 'Keep it secret, Keep it safe' > {my_dataset.uri}",
        outlets=[my_dataset],
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command="echo 'The End'",
    )

    t1 >> t2 >> t3
