# Docker Stack

## Starting and stopping

```bash
# Start all services
docker compose up --build -d

# Tear down
docker compose down

# Tail logs for a service
docker compose logs -f webserver
docker compose logs -f scheduler
```

## Services

| Service | Purpose | Port |
|---|---|---|
| source_postgres | Holds raw source data | 5433 |
| destination_postgres | Holds copied + transformed data | 5434 |
| postgres | Airflow internal metadata DB | internal only |
| init-airflow | One-time setup, then exits | — |
| webserver | Airflow UI | 8080 |
| scheduler | Runs DAG tasks | — |

## Networking

All services share the `elt_network` bridge network (compose-prefixed name: `etl_pipeline_elt_network`).

The `scheduler` container mounts `/var/run/docker.sock` so the Airflow `DockerOperator` can launch sibling containers on the host Docker engine.

The dbt `DockerOperator` task uses `network_mode="host"` so the dbt container can reach `destination_postgres` via `localhost:5434`.

## Custom Dockerfile

The root `Dockerfile` extends `apache/airflow:2.9.3` and adds:
- `postgresql-client` — needed by `elt_script.py` to run `pg_dump`/`psql`
- `apache-airflow-providers-docker` — needed by the `DockerOperator`

## Volume mounts (host → container)

| Host path | Container path | Used by |
|---|---|---|
| `./airflow/dags/` | `/opt/airflow/dags/` | webserver, scheduler |
| `./elt/` | `/opt/airflow/elt/` | scheduler |
| `./custom_postgres/` | `/dbt` | dbt DockerOperator container |
| `~/.dbt/` | `/root/.dbt/` | dbt DockerOperator container |
| `/var/run/docker.sock` | `/var/run/docker.sock` | scheduler |
