
from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

import csv
import requests
import json

default_args = {
            "owner": "airflow",
            "start_date": datetime(2019, 1, 1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "youremail@host.com",
            "retries": 1,
            "retry_delay": timedelta(minutes=5)
        }

with DAG(dag_id="test_kerberos_conn", schedule_interval="0 1 * * *", default_args = default_args, ) as dag:
    
    start = DummyOperator(task_id='start_task', retries=3)
    
    start_Bash = BashOperator(
        task_id='start_Bash',
        bash_command="echo hello BashOperator",
        retries=3
    )

    test_kerberos = BashOperator(
        task_id="test_kerberos",
        bash_command="""
        echo $HADOOP_HOME
        klist
        hdfs dfs -ls /user
        echo "$(AIRFLOW_HOME)"
        hdfs dfs -put $AIRFLOW_HOME/dags/files/forex_currencies.csv /tmp
        hdfs dfs -ls /tmp
        """,
        retries=3
    )

#Flow
start >> start_Bash >> test_kerberos
