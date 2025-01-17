from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from src.helper import print_context

with DAG(
    dag_id="02a_Timedelta",
    start_date=datetime(2025, 1, 1),
    schedule=timedelta(minutes=10),
    catchup=False,
    tags=["timedelta"],
) as dag:

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end

with DAG(
    dag_id="02b_Timedelta_Frequency",
    start_date=datetime(2025, 1, 1),
    schedule=timedelta(days=4),
    catchup=False,
    tags=["timedelta"],
) as dag:

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end
