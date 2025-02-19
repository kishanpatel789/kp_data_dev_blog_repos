FROM python:3.12.9-bookworm

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY api.py /code/api.py

EXPOSE 8000

CMD ["fastapi", "run", "api.py", "--port", "8000"]
