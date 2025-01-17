from datetime import datetime
import pendulum

from airflow import DAG
from airflow.timetables.events import EventsTimetable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from src.helper import print_context

my_events = EventsTimetable(
    event_dates=[
        pendulum.datetime(2025, 1, 1), # MLK Jr Day
        pendulum.datetime(2025, 1, 20), # MLK Jr Day
        pendulum.datetime(2025, 2, 17), # Presidents' Day
        pendulum.datetime(2025, 5, 26), # Memorial Day
        pendulum.datetime(2025, 6, 19), # Juneteenth
        pendulum.datetime(2025, 7, 4), # Independence Day
        pendulum.datetime(2025, 7, 31), # Harry Potter's Birthday
        pendulum.datetime(2025, 9, 1), # Labor Day
        pendulum.datetime(2025, 11, 11), # Veterans Day
        pendulum.datetime(2025, 11, 27), # Thanksgiving Day
        pendulum.datetime(2025, 12, 25), # Christmas Day
    ],
    description="My events",
    restrict_to_events=False,
)

with DAG(
    dag_id="04_TimetableEvents",
    start_date=datetime(2025, 1, 1),
    schedule=my_events,
    catchup=False,
    tags=["timetable"],
) as dag:

    start = EmptyOperator(task_id="start")

    print_context_py = PythonOperator(
        task_id="print_context_py",
        python_callable=print_context,
    )

    end = EmptyOperator(task_id="end")

    start >> print_context_py >> end
