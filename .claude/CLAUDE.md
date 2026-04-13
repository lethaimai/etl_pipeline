# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

This is a local ELT pipeline using Airflow, PostgreSQL, and dbt — all running in Docker.

## Project Overview

A local ELT (Extract, Load, Transform) pipeline that:
1. Extracts data from a source PostgreSQL database using `pg_dump`
2. Loads it into a destination PostgreSQL database using `psql`
3. Transforms the data using dbt models
4. Orchestrates all steps using Apache Airflow

## Architecture

### Pipeline stages

1. **Extract & Load** — `elt/elt_script.py`
   Uses `pg_dump` to dump `source_db` to a SQL file, then `psql` to load it into `destination_db`. Runs as a `PythonOperator` task inside the Airflow container.

2. **Transform** — dbt (`custom_postgres/`)
   Runs as a `DockerOperator` task that spins up `ghcr.io/dbt-labs/dbt-postgres:1.8.2` as a sibling container with `custom_postgres/` mounted at `/dbt`.

3. **Orchestration** — Airflow DAG (`airflow/dags/elt_dag.py`)
   DAG id: `elt_and_dbt_dag`. Task order: `run_elt_script` → `dbt_run`.
   `schedule_interval=None` — triggered manually from the Airflow UI at `http://localhost:8080`.

### Airflow setup

- Runs Airflow 2.9.3 with `SequentialExecutor`
- Metadata DB is a dedicated `postgres` service (internal, not exposed)
- `init-airflow` service runs `airflow db migrate` and creates the admin user on first start, then exits
- `webserver` and `scheduler` both depend on `init-airflow` completing successfully before they start
- Airflow UI credentials: `airflow` / `password`

## How to Run

```bash
# Start all services
docker compose up --build -d

# Tear down
docker compose down

# Tail logs for a service
docker compose logs -f webserver
docker compose logs -f scheduler
```

Then open `http://localhost:8080`, log in with `airflow` / `password`, and manually trigger `elt_and_dbt_dag`.

## Database Connections

| Service | Host (from host machine) | Port | Database | User | Password |
|---|---|---|---|---|---|
| source_postgres | localhost | 5433 | source_db | postgres | secret |
| destination_postgres | localhost | 5434 | destination_db | postgres | secret |
| airflow metadata | internal only | — | airflow | airflow | airflow |

Within the Docker network, containers reach each other by service name (e.g. `source_postgres`, `destination_postgres`) on port `5432`.

## dbt Commands

```bash
# Run all models
dbt run --profiles-dir ~/.dbt --project-dir custom_postgres

# Run a single model
dbt run --profiles-dir ~/.dbt --project-dir custom_postgres --select film_ratings

# Full refresh (drop and recreate all tables)
dbt run --profiles-dir ~/.dbt --project-dir custom_postgres --full-refresh

# Test connection
dbt debug --profiles-dir ~/.dbt --project-dir custom_postgres
```

## dbt Model dependency graph

```
source(destination_db.films)
source(destination_db.actors)
source(destination_db.film_actors)
        ↓
films.sql / actors.sql / film_actors.sql   ← thin source wrappers
        ↓
film_ratings.sql     ← joins all three; applies user_rating_bucket macro
specific_movie.sql   ← filtered view of PG-13 films
```

## Running Tests

```bash
# Activate conda environment first
conda activate data-engineering-db

# Run all integration tests
pytest tests/ -v
```

Tests verify that after running `elt_script.py`:
- All 5 tables exist in `destination_db`
- The `films` table has the correct columns
- All tables have rows
