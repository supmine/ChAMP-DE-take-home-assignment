from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {"owner": "airflow", "start_date": datetime(2023, 4, 1)}

dag = DAG(
    "etl_dag",
    default_args=default_args,
    description='Take home DE assignment ETL',
    schedule_interval="@once",
)
cmd_command = 'python /home/airflow/documents/main.py /home/airflow/documents/input.csv /home/airflow/documents'

etl_task = BashOperator(
    task_id="etl_bash", bash_command=cmd_command, dag=dag
)

etl_task
