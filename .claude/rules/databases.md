# Database Connections

| Service | Host (from host machine) | Port | Database | User | Password |
|---|---|---|---|---|---|
| source_postgres | localhost | 5433 | source_db | postgres | secret |
| destination_postgres | localhost | 5434 | destination_db | postgres | secret |
| airflow metadata | internal only | — | airflow | airflow | airflow |

Within the Docker network, containers reach each other by service name (e.g. `source_postgres`, `destination_postgres`) on port `5432`.

## Source schema

`source_db` contains: `users`, `films`, `film_category`, `actors`, `film_actors`.
Seeded by `source_db_init/init.sql` on first container start.

## Destination schema

`destination_db` starts empty; the ELT script populates it with a full dump from `source_db`. dbt then transforms the data in place.
