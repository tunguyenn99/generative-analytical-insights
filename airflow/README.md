<div align="center">

# ⏱️ Apache Airflow Orchestration (`airflow/`)

<p align="center">
  <a href="#-english-version"><b>🇬🇧 English Version</b></a> | <a href="#-tiếng-việt-version"><b>🇻🇳 Tiếng Việt Version</b></a>
</p>

---

</div>

<a name="-english-version"></a>
# 🇬🇧 Apache Airflow Orchestration (English)

The `airflow/` directory contains Apache Airflow DAG definitions for automated batch scheduling and daily incremental data ingestion for the Zomato data engineering pipeline.

---

## 📁 Directory Structure

```
airflow/
 └── dags/
      ├── zomato_batch_dag.py                # Main batch orchestration DAG definition
      └── zomato_daily_incremental_dag.py    # Daily scheduled incremental ingestion DAG
```

---

## 🔄 DAG Workflows

### 1. Main Batch DAG (`zomato_batch_dag`)
```
[1_generate_raw_data] ➔ [2_upload_localstack_s3] ➔ [3_load_raw_duckdb] ➔ [4_dbt_build_medallion] ➔ [5_llm_enrich_reviews]
```

### 2. Daily Incremental DAG (`zomato_daily_incremental_dag`)
```
[1_generate_incremental_data] ➔ [2_upload_localstack_s3] ➔ [3_load_raw_duckdb] ➔ [4_dbt_medallion_build]
```

---

<hr>

<a name="-tiếng-việt-version"></a>
# 🇻🇳 Điều Phối Dữ Liệu Apache Airflow (Tiếng Việt)

Thư mục `airflow/` chứa các định nghĩa Airflow DAGs định kỳ điều phối luồng dữ liệu tự động cho dự án Zomato Data Engineering.

---

## 🔄 Danh Sách DAGs

1. **`zomato_batch_dag`**: DAG điều phối toàn bộ chuỗi batch từ tạo dữ liệu thô ➔ tải lên S3 ➔ nạp DuckDB ➔ dbt build ➔ Gemini LLM enrichment.
2. **`zomato_daily_incremental_dag`**: DAG điều phối phát sinh dữ liệu ngẫu nhiên mới hàng ngày (`0 0 * * *`) và làm mới các tầng Medallion trong DuckDB.
