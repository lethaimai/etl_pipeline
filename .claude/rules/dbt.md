# dbt Project

The dbt project lives in `custom_postgres/` and targets `destination_db` on port 5434.
`~/.dbt/profiles.yml` must have a `custom_postgres` profile pointing there.

## Commands

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

## Model dependency graph

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

All models materialize as **tables** (global default in `dbt_project.yml`).

## Macros

`macros/film_ratings_macro.sql` — `user_rating_bucket(col)` buckets a numeric rating into:
- `Excellent` (≥ 4.5)
- `Good` (≥ 4.0)
- `Average` (≥ 3.0)
- `Poor` (< 3.0)

Used in `models/film_ratings.sql`.
