from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.datasets import Dataset

my_dataset = Dataset("/opt/airflow/my_file.txt")


with DAG(
    dag_id="02_DatasetExample",
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
        bash_command="pwd && echo 'Keep it secret' > /opt/airflow/my_file.txt",
        outlets=[my_dataset],
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command='sleep 5 && echo "The End"',
    )

    t1 >> t2 >> t3
