from datetime import datetime
from airflow import DAG
import uuid
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 10, 25),
}

with DAG('postgres_dag', 
         default_args=default_args, 
         schedule_interval='*/1 * * * *',  # This schedules the DAG to run every minute
         catchup=False) as dag:
    
    

    create_table = PostgresOperator(
        task_id='create_table',
        sql='''CREATE TABLE new_table(
            custom_id integer NOT NULL, timestamp TIMESTAMP NOT NULL, user_id VARCHAR (50) NOT NULL
            );''',
    )
    
    insert_row = PostgresOperator(
    task_id='insert_row',
    sql='INSERT INTO new_table VALUES(%s, %s, %s)',
    trigger_rule=TriggerRule.ALL_DONE,
    parameters=(uuid.uuid4().int % 123456789, datetime.now(), uuid.uuid4().hex[:10])
)

    create_table >> insert_row


    # run_sql = PostgresOperator(
    #     task_id='run_sql',
    #     postgres_conn_id='postgres',  # Use the connection ID you created
    #     sql='SELECT * FROM races;',
    # )
