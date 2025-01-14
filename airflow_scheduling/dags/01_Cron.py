from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from src.helper import print_context

# cron basic
with DAG(
    dag_id="01a_Cron_Basic",
    schedule="30 5 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cron"],
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo 'Begin'",
    )

    t2 = PythonOperator(
        task_id="t2",
        python_callable=print_context,
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command="echo 'The End'",
    )

    t1 >> t2 >> t3

# cron preset
with DAG(
    dag_id="01b_Cron_Preset",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cron"],
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo 'Begin'",
    )

    t2 = PythonOperator(
        task_id="t2",
        python_callable=print_context,
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command="echo 'The End'",
    )

    t1 >> t2 >> t3

# cron extended
with DAG(
    dag_id="01c_Cron_DayOfWeekHash",
    schedule="0 13 * * 5#2",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cron"],
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo 'Begin'",
    )

    t2 = PythonOperator(
        task_id="t2",
        python_callable=print_context,
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command="echo 'The End'",
    )

    t1 >> t2 >> t3

with DAG(
    dag_id="01d_Cron_StepValues",
    schedule="*/10 * * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cron"],
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo 'Begin'",
    )

    t2 = PythonOperator(
        task_id="t2",
        python_callable=print_context,
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command="echo 'The End'",
    )

    t1 >> t2 >> t3
