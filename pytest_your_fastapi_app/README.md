# Pytest Your Fastapi App

**Objective**: This project implements testing on a Fastapi application. The API provides CRUD operations to a recipe database stored in SQLite. 

Project Start: 2024.11.18

## Project Outline
- This project is an extract from a larger application for managing recipes. It's purpose is to highlight the use of pytest for testing a FastAPI application. 
- Associated blog post can be found here: https://kpdata.dev/blog/pytest-your-fastapi-app/

## Setup Instructions
- This project can be run locally: 
  - Download or clone the repository to a local computer. 
  - Create a virtual environment for python 3.12:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## How to Run FastAPI Application
- Set up a "production" version of the database in SQLite. Run the following command in the `scripts` folder:

  ```bash
  python seed_db.py
  ```

  - This command will initialize a database `recipe.db` and load the seed data found in the CSV files within the `seed_data` folder. 
- Run the FastAPI application on a uvicorn worker by executing the following command in the project root folder: 
  
  ```bash
  uvicorn api.main:app --port 8001
  ```

- HTTP requests (GET, POST, etc) can now be made against the endpoints at `http://127.0.0.1:8001`.
  - The OpenAPI UI can be accessed at `http://127.0.0.1:8001/docs` to interact with the API more conveniently.
  - The UI gives documentation for each endpoint and allows API calls through a GUI instead of alternatives like Postman or curl commands.

## How to Test Application
- In the project root folder, execute the following:

  ```bash
  pytest -v api/tests/ 
  ```

  - The terminal should list each test along with its PASS/FAIL status. 