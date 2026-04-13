# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

This is a local ELT pipeline using Airflow, PostgreSQL, and dbt — all running in Docker.

## Rules

Detailed guidance is split into rule files in `.claude/rules/`:

- [architecture.md](rules/architecture.md) — pipeline stages, Airflow DAG structure, service startup order
- [docker.md](rules/docker.md) — stack commands, networking, volume mounts, Dockerfile notes
- [databases.md](rules/databases.md) — connection details for all three Postgres instances
- [dbt.md](rules/dbt.md) — dbt commands, model dependency graph, macros

## Running Tests

```bash
# Activate conda environment first
conda activate data-engineering-db

# Run all integration tests
pytest tests/ -v
```
