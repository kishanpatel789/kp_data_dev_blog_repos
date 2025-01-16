from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

from src.datasets import my_dataset

with DAG(
    dag_id="03b_Dataset_Consumer",
    schedule=my_dataset,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["dataset"],
) as dag:

    start = EmptyOperator(task_id="start")

    read_dataset = BashOperator(
        task_id="read_dataset",
        bash_command=f"cat {my_dataset.uri}",
    )

    remove_dataset = BashOperator(
        task_id="remove_dataset",
        bash_command="src/remove_file.bash",
        env={"FILE_PATH": my_dataset.uri},
    )

    end = EmptyOperator(task_id="end")

    start >> read_dataset >> remove_dataset >> end
