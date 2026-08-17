# 📜 Automation & Pipeline Scripts (`scripts/`)

The `scripts/` directory contains Python automation scripts for data generation, LocalStack S3 landing ingestion, and pipeline execution.

---

## 📁 Directory Structure

```
scripts/
 ├── init_localstack_s3.py    # Uploads raw CSV datasets to AWS LocalStack S3
 └── run_pipeline.py          # End-to-end pipeline execution runner
generate_sample_data.py       # Synthetic Zomato dataset generator (in root)
```

---

## ⚙️ Script Descriptions

### 1. `generate_sample_data.py`
- Generates 7 synthetic Zomato datasets into `data/raw/`:
  - `restaurants.csv` (20 rows)
  - `users.csv` (100 rows)
  - `food.csv` (15 rows)
  - `menu.csv` (149 rows)
  - `orders.csv` (600 rows)
  - `order_items.csv` (1468 rows)
  - `reviews.csv` (250 rows)

### 2. `init_localstack_s3.py`
- Connects to AWS LocalStack S3 endpoint at `http://localhost:4566`.
- Ensures bucket `s3://zomato-data-lake` exists.
- Uploads all 7 CSV files into `s3://zomato-data-lake/raw/<table_name>/`.

### 3. `run_pipeline.py`
- Complete end-to-end pipeline runner executing all 5 steps sequentially:
  1. Data Generation
  2. LocalStack S3 Upload
  3. DuckDB RAW Bronze Ingestion
  4. dbt Medallion Build & Data Tests
  5. Gemini LLM Review Enrichment

---

## 🚀 Execution

Run full end-to-end pipeline:
```bash
python3 scripts/run_pipeline.py
```
