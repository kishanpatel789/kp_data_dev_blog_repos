from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from src.helper import print_context

# cron basic
with DAG(
    dag_id="01a_Cron_Basic",
    start_date=datetime(2025, 1, 1),
    schedule="30 5 * * *",
    catchup=False,
    tags=["cron"],
):

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end

# cron preset
with DAG(
    dag_id="01b_Cron_Preset",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["cron"],
):

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end


# cron extended
with DAG(
    dag_id="01c_Cron_DayOfWeekHash",
    start_date=datetime(2025, 1, 1),
    schedule="0 13 * * 5#2",
    catchup=False,
    tags=["cron"],
):

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end


with DAG(
    dag_id="01d_Cron_StepValues",
    start_date=datetime(2025, 1, 1),
    schedule="*/10 * * * *",
    catchup=False,
    tags=["cron"],
):

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end
