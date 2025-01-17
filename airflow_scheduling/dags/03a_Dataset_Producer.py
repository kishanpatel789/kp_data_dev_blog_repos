from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

from src.datasets import my_dataset

with DAG(
    dag_id="03a_Dataset_Producer",
    start_date=datetime(2025, 1, 1),
    schedule="45 15 * * 4",
    catchup=False,
    tags=["dataset"],
) as dag:

    start = EmptyOperator(task_id="start")

    create_dataset = BashOperator(
        task_id="create_dataset",
        bash_command=f"echo 'Keep it secret, Keep it safe' > {my_dataset.uri}",
        outlets=[my_dataset],
    )

    end = EmptyOperator(task_id="end")

    start >> create_dataset >> end
