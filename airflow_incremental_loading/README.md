# Airflow Incremental Loading

**Objective**: This repo demonstrates incremental loading in Apache Airflow. 

Project Start: 2025.02.05

## Architecture
- Technologies Used
  - Apache Airflow
  - Docker - used to run Airflow locally

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
  - Run the Airflow containers by executing following two commands in a terminal when in the directory `./airflow_incremental_loading/`:
    ```bash
    docker compose up airflow-init
    docker compose up
    ```

## How to Run
- After completing setup described above, go to the Airflow UI at `localhost:8080`. Log in with the following credentials:
  - Username: `airflow`
  - Password: `airflow`

TODO: complete run steps