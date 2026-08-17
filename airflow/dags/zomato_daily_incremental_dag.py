import os
from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.operators.bash import BashOperator

    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False

default_args = {
    "owner": "data_engineering_team",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def task_incremental_data():
    from scripts.generate_daily_incremental_data import generate_daily_incremental_data

    generate_daily_incremental_data()


def task_upload_s3():
    from scripts.init_localstack_s3 import upload_raw_data_to_s3

    upload_raw_data_to_s3()


def task_load_duckdb():
    from scripts.load_raw_duckdb import load_raw_tables

    load_raw_tables()


if AIRFLOW_AVAILABLE:
    with DAG(
        "zomato_daily_incremental_ingestion",
        default_args=default_args,
        description="Daily Incremental Batch Ingestion & dbt Medallion Refresh",
        schedule_interval="0 0 * * *",
        catchup=False,
    ) as dag:

        t1_incremental = PythonOperator(
            task_id="1_generate_incremental_data",
            python_callable=task_incremental_data,
        )

        t2_s3_upload = PythonOperator(
            task_id="2_upload_localstack_s3",
            python_callable=task_upload_s3,
        )

        t3_duckdb = PythonOperator(
            task_id="3_load_raw_duckdb",
            python_callable=task_load_duckdb,
        )

        t4_dbt_build = BashOperator(
            task_id="4_dbt_medallion_build",
            bash_command="cd zomato_dbt && dbt build --profiles-dir .",
        )

        t1_incremental >> t2_s3_upload >> t3_duckdb >> t4_dbt_build
