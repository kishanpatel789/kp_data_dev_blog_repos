FROM python:3.12.9-bookworm

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY api.py /

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["/api.py"]
