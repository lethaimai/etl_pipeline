FROM apache/airflow:2.9.3
USER root

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install apache-airflow-providers-docker


