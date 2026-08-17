# ⏱️ Apache Airflow Orchestration (`airflow/`)

The `airflow/` directory contains Apache Airflow DAG definitions for automated batch scheduling of the Zomato data engineering pipeline.

---

## 📁 Directory Structure

```
airflow/
 └── dags/
      └── zomato_batch_dag.py     # Main batch orchestration DAG definition
```

---

## 🔄 DAG Workflow (`zomato_batch_dag`)

```
[t1_gen_data] ➔ [t2_s3_upload] ➔ [t3_raw_duckdb] ➔ [t4_dbt_build] ➔ [t5_enrich_reviews]
```

### DAG Tasks Breakdown:
1. **`t1_gen_data`** (`PythonOperator`): Generates synthetic raw CSV datasets into `data/raw/`.
2. **`t2_s3_upload`** (`PythonOperator`): Ingests raw CSVs into AWS LocalStack S3 bucket `s3://zomato-data-lake/raw/`.
3. **`t3_raw_duckdb`** (`PythonOperator`): Loads S3 CSV files into DuckDB `ZOMATO_RAW` Bronze schema.
4. **`t4_dbt_build`** (`BashOperator`): Executes `dbt build` (compilation, medallion transformations, and 35 data tests).
5. **`t5_enrich_reviews`** (`PythonOperator`): Runs Google Gemini AI sentiment and topic extraction on review dataset.

---

## ⚙️ Execution & Triggering

To test DAG execution locally without running full Airflow webserver:
```bash
python3 scripts/run_pipeline.py
```
Or with Airflow CLI:
```bash
airflow dags test zomato_batch_pipeline 2026-08-18
```
