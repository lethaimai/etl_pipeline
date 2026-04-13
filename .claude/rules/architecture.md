# Architecture

This is a local ELT pipeline with three stages orchestrated by Airflow.

## Pipeline stages

1. **Extract & Load** — `elt/elt_script.py`
   Uses `pg_dump` to dump `source_db` to a SQL file, then `psql` to load it into `destination_db`. Runs as a `PythonOperator` task inside the Airflow container.

2. **Transform** — dbt (`custom_postgres/`)
   Runs as a `DockerOperator` task that spins up `ghcr.io/dbt-labs/dbt-postgres:1.8.2` as a sibling container with `custom_postgres/` mounted at `/dbt`.

3. **Orchestration** — Airflow DAG (`airflow/dags/elt_dag.py`)
   DAG id: `elt_and_dbt_dag`. Task order: `run_elt_script` → `dbt_run`.
   `schedule_interval=None` — triggered manually from the Airflow UI at `http://localhost:8080`.

## Airflow setup

- Runs Airflow 2.9.3 with `SequentialExecutor`
- Metadata DB is a dedicated `postgres` service (internal, not exposed)
- `init-airflow` service runs `airflow db migrate` and creates the admin user on first start, then exits
- `webserver` and `scheduler` both depend on `init-airflow` completing successfully before they start
- Airflow UI credentials: `airflow` / `password`
