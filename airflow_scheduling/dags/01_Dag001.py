from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from src.helper import print_context

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

    t2 = PythonOperator(
        task_id="t2",
        python_callable=print_context,
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command='echo "The End"',
    )

    t1 >> t2 >> t3
