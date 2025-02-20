import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd

default_args = {
    'owner': 'adam',
    'start_date': dt.datetime(2024, 1, 11),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=10),
}

with DAG('load_fp_datas',
         default_args=default_args,
         schedule_interval='10-30/10 9 * * 6',    
         catchup = False,
         ) as dag:

    get_FP_data = BashOperator(task_id='get_FP_data', bash_command='python /opt/airflow/ETL/final_project_extract_transform.py')
    
    load_FP_data = BashOperator(task_id='load_FP_data', bash_command='python /opt/airflow/ETL/final_project_load.py')
    
    load_to_sheet = BashOperator(task_id='load_to_sheet', bash_command='python /opt/airflow/ETL/mongo_to_sheet.py')

get_FP_data >> load_FP_data >> load_to_sheet
