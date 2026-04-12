FROM apache/airflow:2.9.3
USER root

RUN apt-get update && \
    apt-get install -y postgresql-client docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
