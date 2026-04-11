import pytest 
import psycopg2


# write the dest_connection fixture 
@pytest.fixture 
def dest_connection():
    # connects to destination_db on localhost:5434 
    connection= psycopg2.connect(
        host="localhost",
        port=5434,
        database="destination_db",
        user="postgres",
        password="secret")
    
    # hand the connection to the test function
    yield connection
    # close the connection after the test is done
    connection.close()


# write test 1 that should contains these steps:
# 1. create a cursor from dest_connection
# 2. execute the SQL query to get all tables names from information_schma.tables 
# 3. check that all 5 tables exist: films, actors, users, film_actors, film_category by using asserrt
def test_destination_tables_exist(dest_connection):
    cursor= dest_connection.cursor()
    cursor.execute(
        "SELECT table_name " \
        "FROM information_schema.tables " \
        "WHERE table_schema='public';"
    )

    # fet all the tables names from cursor into a list of tuples
    tables= cursor.fetchall()
    # extract the table names from the list of tuples into a list of strings
    table_names= [table[0] for table in tables]
    expected_tables= ["films", "actors", "users", "film_actors", "film_category"]
    missing_tables= [expected_table for expected_table in expected_tables if expected_table not in table_names]
    assert not missing_tables, (
        f"Missing tables in destination database: {', '.join(missing_tables)}"
    )


# write test 2 that checks the films table has the right columns
def test_destination_films_columns(dest_connection):
    cursor= dest_connection.cursor()
    cursor.execute(
        "SELECT column_name "\
        "FROM information_schema.columns " \
        "WHERE table_schema='public' AND table_name='films';"
    ) 

    columns= cursor.fetchall()
    column_names= [column[0] for column in columns]
    expected_columns= ["film_id", "title", "release_date", "price", "rating", "user_rating"]
    missing_columns= [expected_column for expected_column in expected_columns if expected_column not in column_names]
    assert not missing_columns, (
        f"Missing columns in films table: {', '.join(missing_columns)}"
    )
    

# write test 3 that checks that each table has rows (count > 0)
def test_destination_tables_have_rows(dest_connection):
    cursor= dest_connection.cursor()
    tables= ["films", "actors", "users", "film_actors", "film_category"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count= cursor.fetchone()[0]
        assert count > 0, f"Table {table} is empty in destination database"


