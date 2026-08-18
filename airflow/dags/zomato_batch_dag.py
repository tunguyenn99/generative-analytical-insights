import os
import sys
from datetime import datetime, timedelta

# Ensure project root is in sys.path and set working directory context
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from airflow.operators.python import PythonOperator

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


def task_generate_raw_data():
    os.chdir(PROJECT_ROOT)
    from generate_sample_data import generate_zomato_dataset

    generate_zomato_dataset()


def task_upload_localstack_s3():
    os.chdir(PROJECT_ROOT)
    from scripts.init_localstack_s3 import upload_raw_data_to_s3

    upload_raw_data_to_s3()


def task_load_raw_duckdb():
    os.chdir(PROJECT_ROOT)
    from scripts.load_raw_duckdb import load_raw_tables

    load_raw_tables()


def task_enrich_reviews():
    os.chdir(PROJECT_ROOT)
    from ai.enrich_reviews import enrich_reviews_pipeline

    enrich_reviews_pipeline()


def task_data_observability():
    os.chdir(PROJECT_ROOT)
    from scripts.data_observability import run_data_observability_audit

    run_data_observability_audit()


if AIRFLOW_AVAILABLE:
    with DAG(
        "zomato_end_to_end_batch",
        default_args=default_args,
        description=(
            "End-to-End Zomato AI Data Pipeline (LocalStack S3 -> DuckDB -> dbt"
            " -> LLM AI -> Observability)"
        ),
        schedule="@daily",
        catchup=False,
    ) as dag:

        t1_gen_data = PythonOperator(
            task_id="1_generate_raw_data",
            python_callable=task_generate_raw_data,
        )

        t2_s3_upload = PythonOperator(
            task_id="2_upload_localstack_s3",
            python_callable=task_upload_localstack_s3,
        )

        t3_raw_duckdb = PythonOperator(
            task_id="3_load_raw_duckdb",
            python_callable=task_load_raw_duckdb,
        )

        t4_dbt_build = BashOperator(
            task_id="4_dbt_build_medallion",
            bash_command=f"cd {PROJECT_ROOT}/zomato_dbt && dbt build --profiles-dir .",
        )

        t5_enrich_reviews = PythonOperator(
            task_id="5_llm_enrich_reviews",
            python_callable=task_enrich_reviews,
        )

        t6_observability = PythonOperator(
            task_id="6_data_observability_audit",
            python_callable=task_data_observability,
        )

        (
            t1_gen_data
            >> t2_s3_upload
            >> t3_raw_duckdb
            >> t4_dbt_build
            >> t5_enrich_reviews
            >> t6_observability
        )
