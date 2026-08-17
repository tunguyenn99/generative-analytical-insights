<div align="right">
  <b>🇬🇧 English</b> | <a href="README.vn.md">🇻🇳 Tiếng Việt</a>
</div>

# 📜 Automation & Pipeline Scripts (`scripts/`)

The `scripts/` directory contains Python automation scripts for dataset generation, daily incremental appends, LocalStack S3 ingestion, and end-to-end pipeline execution.

---

## 📁 Directory Structure

```
scripts/
 ├── init_localstack_s3.py               # Uploads raw CSV datasets to AWS LocalStack S3
 ├── load_raw_duckdb.py                  # Loads raw data into DuckDB Bronze schema
 ├── generate_daily_incremental_data.py # Appends daily random rows into raw dataset
 └── run_pipeline.py                     # End-to-end pipeline execution runner
generate_sample_data.py                  # Synthetic Zomato dataset generator (root)
```

---

## ⚙️ Core Scripts

1. **`generate_sample_data.py`**: Generates full synthetic Zomato dataset (7 CSV tables).
2. **`generate_daily_incremental_data.py`**: Appends random daily rows (users, orders, order items, reviews) to dataset.
3. **`init_localstack_s3.py`**: Uploads CSV datasets to AWS LocalStack S3 (`s3://zomato-data-lake/raw/`).
4. **`load_raw_duckdb.py`**: Populates `ZOMATO_RAW` Bronze layer in DuckDB.
5. **`run_pipeline.py`**: Executes the 5-step automated batch pipeline.

---

## 🚀 Execution

Run full end-to-end pipeline:
```bash
python3 scripts/run_pipeline.py
```
