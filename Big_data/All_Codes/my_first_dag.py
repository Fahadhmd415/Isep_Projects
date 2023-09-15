import os
import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


from lib.source_to_raw_1 import source_to_raw_1
from lib.source_to_raw_2 import source_to_raw_2

from lib.raw_to_formatted_1 import raw_to_formatted_1
from lib.raw_to_formatted_2 import raw_to_formatted_2

from lib.produce_usage import produce_usage

from lib.index_to_elastic import index_to_elastic

default_args = {
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=15),
}

with DAG(
        'my_first_dag',
        default_args=default_args,
        description='A first DAG',
        schedule=None,
        start_date=datetime(2023, 5, 5),
        catchup=False,
        tags=['example'],
) as dag:
    dag.doc_md = """
        This is my first DAG in Airflow.
        I can write documentation in Markdown here with **bold text** or __bold text__.
    """


    source_to_raw_1 = PythonOperator(
        task_id='source_to_raw_1',
        python_callable=source_to_raw_1,
    )

    raw_to_formatted_1 = PythonOperator(
        task_id='raw_to_formatted_1',
        python_callable=raw_to_formatted_1,

    )

    source_to_raw_2 = PythonOperator(
        task_id='source_to_raw_2',
        python_callable=source_to_raw_2,
    )

    raw_to_formatted_2 = PythonOperator(
        task_id='raw_to_formatted_2',
        python_callable=raw_to_formatted_2,
    )

    produce_usage = PythonOperator(
        task_id='produce_usage',
        python_callable=produce_usage,
    )

    index_to_elastic = PythonOperator(
        task_id='index_to_elastic',
        python_callable=index_to_elastic,
    )

    source_to_raw_1 >> raw_to_formatted_1 >> produce_usage
    source_to_raw_2 >> raw_to_formatted_2 >> produce_usage
    produce_usage >> index_to_elastic
