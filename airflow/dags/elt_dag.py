from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator 
from datetime import datetime
import sys 
sys.path.insert(0, "/opt/airflow/elt")
from elt_script import run_elt



# define source_config and destination_config but with Docker network hostnames this time (not localhost)
source_config= {
    "host": "source_postgres", # where the postgres database is running
    "port": "5432",
    "database": "source_db",
    "user": "postgres",
    "password": "secret"
}

destination_config= {
    "host": "destination_postgres", # where the postgres database is running
    "port": "5432",
    "database": "destination_db",
    "user": "postgres",
    "password": "secret"
}

with DAG(
    dag_id= "elt_and_dbt_dag",
    description= "Run the elt_script.py that copies data from source to destination, then run dbt transformations",
    start_date= datetime(2026, 4, 10),
    schedule_interval= None, # set to None to only run the DAG when triggered manually
    catchup= False,
    tags= ["elt_and_dbt"]
) as dag:
    
    task1 = PythonOperator(
        task_id= "run_elt_script",
        python_callable= run_elt,
        op_kwargs= {
            "source": source_config,
            "destination": destination_config
        }
    )

    task2 = DockerOperator(
        task_id= "dbt_run",
        image= "ghcr.io/dbt-labs/dbt-postgres:1.8.2",
        command= "run --profiles-dir /root/.dbt --project-dir /dbt",
        network_mode= "elt_pipeline_elt_network", # use the same Docker network as the postgres containers to allow connectivity
        auto_remove= True
    )

    task1 >> task2 # set the task dependencies so that task2 runs after task1

