from pathlib import Path

from airflow import DAG
from airflow.configuration import conf as airflow_conf
from dagfactory import load_yaml_dags

config_dir = Path(airflow_conf.get("core", "dags_folder")) / "configs"
load_yaml_dags(globals_dict=globals(), dags_folder=str(config_dir))

