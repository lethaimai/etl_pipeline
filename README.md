# ELT Pipeline

A local ELT (Extract, Load, Transform) pipeline built with Apache Airflow, PostgreSQL, and dbt — all running in Docker.

## What it does

1. **Extract & Load** — copies data from a source PostgreSQL database to a destination PostgreSQL database using `pg_dump` and `psql`
2. **Transform** — runs dbt models to transform the raw data into analytics-ready tables
3. **Orchestrate** — Apache Airflow schedules and monitors the full pipeline

## Architecture

```
source_db (postgres:5433)
        ↓  pg_dump / psql
destination_db (postgres:5434)
        ↓  dbt
transformed tables (films, actors, film_ratings, specific_movie)
```

All orchestrated by Airflow at `http://localhost:8080`.

## Prerequisites

- Docker Desktop
- Git
- conda (or any Python virtual environment)
- dbt-postgres (`pip install dbt-postgres`)

## Project Structure

```
etl_pipeline/
├── airflow/
│   └── dags/
│       └── elt_dag.py          # Airflow DAG
├── custom_postgres/
│   ├── models/                 # dbt SQL models
│   ├── macros/                 # dbt macros
│   └── dbt_project.yml         # dbt project config
├── elt/
│   └── elt_script.py           # Extract & Load script
├── source_db_init/
│   └── init.sql                # Source database seed data
├── tests/
│   └── test_elt.py             # Integration tests
├── Dockerfile                  # Custom Airflow image
├── docker-compose.yaml         # All services
└── requirements.txt            # Python dependencies
```

## Setup

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/etl_pipeline.git
cd etl_pipeline
```

**2. Create conda environment:**
```bash
conda create -n data-engineering-db python=3.11
conda activate data-engineering-db
pip install -r requirements.txt
```

**3. Create dbt profiles file at `~/.dbt/profiles.yml`:**
```yaml
custom_postgres:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5434
      dbname: destination_db
      user: postgres
      password: secret
      schema: public
```

**4. Start all services:**
```bash
docker compose up --build -d
```

**5. Verify all services are running:**
```bash
docker compose ps
```

## Running the Pipeline

1. Open `http://localhost:8080` in your browser
2. Log in with `airflow` / `password`
3. Find `elt_and_dbt_dag` and click the play button ▶ to trigger it manually
4. Watch the tasks run: `run_elt_script` → `dbt_run`

## Running Tests

```bash
conda activate data-engineering-db
pytest tests/ -v
```

## Database Connections

| Database | Host | Port | User | Password |
|---|---|---|---|---|
| source_db | localhost | 5433 | postgres | secret |
| destination_db | localhost | 5434 | postgres | secret |

## dbt Models

| Model | Description |
|---|---|
| `films` | Raw films data |
| `actors` | Raw actors data |
| `film_actors` | Raw film-actor relationships |
| `film_ratings` | Joins films + actors, adds rating category |
| `specific_movie` | Filtered view of PG-13 films |
