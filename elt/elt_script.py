
# a built-in midule lets you run terminal commands from within 
# a python script 
import subprocess
import os



source_config= {
    "host": "localhost", # where the postgres database is running
    "port": "5433",
    "database": "source_db",
    "user": "postgres",
    "password": "secret"
}

destination_config = {
    "host": "localhost", # where the postgres database is running
    "port": "5434",
    "database": "destination_db",
    "user": "postgres",
    "password": "secret"
}




# function that run pg_dump then psql to copy the database from source to destination
def run_elt(source, destination):
    dump_command= [
        "pg_dump",
        "-h", source["host"],
        "-p", source["port"],
        "-U", source["user"],
        "-d", source["database"],
        "-f", "data_dump.sql", # the dump fill will be saved in the current directory with the name data_dump.sql
        "-w" # this flag tells pg_dump to use the password from the environment variable PGPASSWORD
    ]

    # set the environment variable PGPASSWORD to avoid password prompt
    subprocess_env= {
        **os.environ, # include the existing environment variables
        "PGPASSWORD": source["password"]
    }


    # use psql to load the dumped sql file into the destination database
    load_command= [
        "psql",
        "-h", destination["host"],
        "-p", destination["port"],
        "-U", destination["user"],
        "-d", destination["database"],
        "-f", "data_dump.sql",# the dump file that we want to load into the destination database
        "-a" # echo all input from the file to the terminal for debugging purposes
    ]

    # run pg_dump to create the dump file
    subprocess.run(dump_command, env=subprocess_env, check=True)
    
    # run psql to load the dump file into the destination database
    subprocess.run(load_command, env=subprocess_env, check=True)

if __name__ == "__main__":
    # only run the ELT process if this script is executed directly (not imported as a module)
    run_elt(source_config, destination_config)