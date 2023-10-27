from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 27),
    'retries': 1,
}

dag = DAG(
    'postgres_test',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@daily',
)

# Create Table Task
create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres',  # replace with your connection id
    sql="""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
        );
    """,
    dag=dag,
)

# Insert Data Task
insert_data = PostgresOperator(
    task_id='insert_data',
    postgres_conn_id='postgres',  # replace with your connection id
    sql="""
        INSERT INTO test_table (name)
        VALUES ('John Doe'), ('Jane Doe');
    """,
    dag=dag,
)

# Select Data Task
select_data = PostgresOperator(
    task_id='select_data',
    postgres_conn_id='postgres',  # replace with your connection id
    sql="SELECT * FROM test_table;",
    dag=dag,
)

# Set Task Dependencies
create_table >> insert_data >> select_data
