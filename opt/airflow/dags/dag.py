from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 10, 25),
}

with DAG('postgres_dag', 
         default_args=default_args, 
         schedule_interval='*/1 * * * *',  # This schedules the DAG to run every minute
         catchup=False) as dag:

    run_sql = PostgresOperator(
        task_id='run_sql',
        postgres_conn_id='postgres_default',  # Use the connection ID you created
        sql='SELECT * FROM your_table;',
    )
