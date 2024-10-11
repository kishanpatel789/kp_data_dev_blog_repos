"""
# Super Cool Python Runner
- This dag runs a python file and should be executed with run-time configuration.
- The target python file must be located in AWS S3 and contain a `main()` function.
"""

import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.models.param import Param
from src.python_runner import (
    process_parameters,
    run_python_file,
    STANDARD_PACKAGES,
)

params = {
    "python_file_path": Param(
        "",
        description="Enter the path to the python file. Should be in format of 's3://<bucket-name>/<path-to-file>.py'",
        type="string",
        minLength=0,
    ),
    "extra_packages": Param(
        [],
        description=f"Enter any additional python packages required for the python file. Each package should be entered on a separate line without quotation.\nStandard packages: {STANDARD_PACKAGES}",
        type="array",
        items={"type": "string"},
    ),
    "kw_args": Param(
        {},
        description="Enter any arguments needed by the python file's main() function as key-value pairs. Input should be a python dictionary that passes JSON parsing",
        type="object",
    ),
    "system_site_packages": Param(
        True,
        description="Inherit packages from global site-packages directory",
        type="boolean",
    ),
}

with DAG(
    dag_id="02_better_dag",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 9, 1, tz="UTC"),
    catchup=False,
    tags=["level:amazing", "usability:high"],
    render_template_as_native_obj=True,
    params=params,
    doc_md=__doc__,
) as dag:

    process_parameters_py = PythonOperator(
        task_id="process_parameters_py",
        python_callable=process_parameters,
        op_args=[
            "{{ params.python_file_path }}",
            "{{ params.extra_packages }}",
            "{{ params.kw_args }}",
        ],
    )

    run_python_file_py = PythonVirtualenvOperator(
        task_id="run_python_file_py",
        python_callable=run_python_file,
        requirements="{{task_instance.xcom_pull(task_ids='process_parameters_py', key='final_packages_str')}}",
        python_version="3.12",
        system_site_packages="{{ params.system_site_packages }}",
        op_args=[
            "{{ params.python_file_path }}",
            "{{ task_instance.xcom_pull(task_ids='process_parameters_py', key='final_packages') }}",
            "{{ params.kw_args }}",
        ],
        venv_cache_path="/home/airflow/venv-cache",
    )
    run_python_file_py.template_fields = (
        "op_kwargs",
        "op_args",
        "requirements",
        "system_site_packages",
    )

    process_parameters_py >> run_python_file_py
