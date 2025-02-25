# Airflow Incremental Loading

**Objective**: This repo demonstrates incremental loading in Apache Airflow. 

Project Start: 2025.02.05

## Architecture
- Technologies Used
  - Apache Airflow
  - Docker - used to run Airflow locally
  - Python packages
    - FastAPI and Faker: for simulating a data source
    - Polars: for managing data files

## Setup Instructions
- Local Setup
  - Download or clone the repository to a local computer. 
- Airflow on Docker
  - The following instructions assume Docker is already installed on the local machine. 
  - In the directory `./airflow_incremental_loading/` create additional airflow files to be used as volumes by Docker: 
    ```
    mkdir -p ./logs ./plugins ./config
    ```
  - In the directory `./airflow_incremental_loading/` create a file `.env` by running the following commands: 
    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > .env    
    ```
    - Docker will automatically pick up this `.env` file when building Airflow resources. 
  - Create and start the Airflow containers by executing following two commands in a terminal when in the directory `./airflow_incremental_loading/`:
    ```bash
    docker compose up airflow-init
    docker compose up
    ```
    - In addition to the Airflow containers, this will start a container that runs a FastAPI app, called "Donut App". The app is exposed to the host at `localhost:8000`. 

## How to Run
- After completing setup described above, go to the Airflow UI at `localhost:8080`. Log in with the following credentials:
  - Username: `airflow`
  - Password: `airflow`
- In the Airflow UI, there should be two dags available. 
  - `001_incremental_dag`: A simple DAG with a bash command that prints the `logical_date`, `data_interval_start`, and `data_interval_end` template variables. 
  - `002_process_donut_orders`: A two-task DAG that reads and summarizes donut orders. DAG is designed to incrementaly pull one day's worth of data from an API.
    1. `get_orders`: Pull orders from the API and save them locally as a JSON file. 
    2. `process_orders`: Read saved JSON orders, aggregate them to a hourly summary, and save locally as a CSV file. 
- The Donut App API documentation can be found at `localhost:8000/docs`. 
  ![Donut Order API](./presentation/images/DonutOrderAPI.jpeg)
  