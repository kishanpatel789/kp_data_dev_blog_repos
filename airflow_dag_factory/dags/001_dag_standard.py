from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from src.helper import print_context

with DAG(
    dag_id="001_dag_standard",
    start_date=datetime(2025, 3, 1),
    schedule="30 5 * * *",
    catchup=False,
    tags=["standard"],
):

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end
