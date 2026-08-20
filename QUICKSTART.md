# 🚀 Master Setup & Execution Guide (All Tools & Modules)

This comprehensive guide details how to set up, configure, and execute **every tool, pipeline, and module** in the **Zomato AI & Data Engineering Intelligence Platform** from scratch using Bash.

---

## 📑 Table of Contents
1. [Prerequisites & System Setup](#1-prerequisites--system-setup)
2. [Environment Configuration (.venv & .env)](#2-environment-configuration-venv--env)
3. [Infrastructure & Cloud Emulation (AWS LocalStack S3)](#3-infrastructure--cloud-emulation-aws-localstack-s3)
4. [Apache Airflow Orchestration Setup](#4-apache-airflow-orchestration-setup)
5. [End-to-End Pipeline Execution](#5-end-to-end-pipeline-execution)
6. [dbt Core Medallion & Documentation Tools](#6-dbt-core-medallion--documentation-tools)
7. [Generative AI & LLM Tools Execution](#7-generative-ai--llm-tools-execution)
8. [Data Observability & OpenLineage Governance](#8-data-observability--openlineage-governance)
9. [Daily Incremental Data Generation](#9-daily-incremental-data-generation)
10. [Streamlit Multi-Page Web Application](#10-streamlit-multi-page-web-application)
11. [Code Quality & CI/CD Governance (Pre-Commit, Black, SQLFluff)](#11-code-quality--cicd-governance-pre-commit-black-sqlfluff)

---

## 1. Prerequisites & System Setup

Ensure the following tools are installed on your Linux / macOS / WSL machine:
- **Python 3.10+** (Verify: `python3 --version`)
- **Git** (Verify: `git --version`)
- **Docker & Docker Compose** (Verify: `docker compose version`)
- *(Optional)* **AWS CLI** (For inspecting LocalStack S3 buckets)

Clone the repository and enter the project directory:
```bash
git clone https://github.com/tunguyenn99/generative-analytical-insights.git
cd generative-analytical-insights
```

---

## 2. Environment Configuration (.venv & .env)

### A. Create & Activate Virtual Environment (`.venv`)
```bash
# Create python virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### B. Configure Environment Variables (`.env`)
Copy the template file `.env.example` to `.env`:
```bash
cp .env.example .env
```

Open `.env` in your text editor and add your **Google Gemini API Key** (Get free key at [https://ai.google.dev/](https://ai.google.dev/)):
```env
GEMINI_API_KEY=your_gemini_api_key_here
DUCKDB_PATH=data/warehouse/zomato_dw.duckdb
OPENLINEAGE_URL=http://localhost:5000
```

### C. Install All Dependencies
```bash
pip install -r requirements.txt
```

---

## 3. Infrastructure & Cloud Emulation (AWS LocalStack S3)

### A. Start AWS LocalStack S3 Container
```bash
docker compose up -d
```

### B. Initialize S3 Bucket & Landing Zone Data
```bash
python3 scripts/init_localstack_s3.py
```

### C. Verify S3 Bucket Contents via AWS CLI (Optional)
```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://zomato-data-lake/raw/
```

---

## 4. Apache Airflow Orchestration Setup

### A. Export Airflow Home Directory
```bash
export AIRFLOW_HOME=$(pwd)/airflow
```

### B. Run Airflow Standalone
```bash
airflow standalone
```
> Access Airflow UI at **[http://localhost:8080](http://localhost:8080)** to view and trigger DAGs:
> - `zomato_end_to_end_batch`: Full batch ingestion & transformation pipeline.
> - `zomato_daily_incremental_ingestion`: Daily incremental batch schedule.

---

## 5. End-to-End Pipeline Execution

### A. One-Command Master Execution
To execute the complete data & AI pipeline automatically:
```bash
python3 scripts/run_pipeline.py
```

### B. Step-by-Step Manual Pipeline Execution
If you prefer running each pipeline step manually:
```bash
# Step 1: Generate synthetic raw Zomato datasets (2024-2026)
python3 generate_sample_data.py

# Step 2: Load raw tables into DuckDB warehouse (Bronze RAW schema)
python3 scripts/load_raw_duckdb.py

# Step 3: Run dbt Medallion transformations & tests
cd zomato_dbt && dbt build --profiles-dir . && cd ..

# Step 4: Run AI review enrichment (Sentiment & Aspect extraction)
python3 ai/enrich_reviews.py

# Step 5: Run Data Observability & OpenLineage audit
python3 scripts/data_observability.py
```

---

## 6. dbt Core Medallion & Documentation Tools

Navigate to the dbt project folder:
```bash
cd zomato_dbt
```

### A. dbt Build (Models + Tests)
```bash
dbt build --profiles-dir .
```

### B. dbt Test Only
```bash
dbt test --profiles-dir .
```

### C. dbt Interactive Documentation Site
Generate and serve the interactive dbt schema lineage docs site:
```bash
dbt docs generate --profiles-dir .
dbt docs serve --port 8088 --profiles-dir .
```
> Open browser at **[http://localhost:8088](http://localhost:8088)** to view full DAG lineage and schema documentation.

### D. Verify dbt Semantic Layer
```bash
cd ..
python3 scripts/verify_semantic_layer.py
```

---

## 7. Generative AI & LLM Tools Execution

All AI tools support **Google Gemini API (`gemini-3.5-flash`)** with automatic fallback to the **Local Engine**:

### A. LLM Review Sentiment Enrichment
```bash
python3 ai/enrich_reviews.py
```

### B. Review Vector RAG Search Assistant (CLI Mode)
```bash
python3 ai/rag_chat.py
```

### C. Text-to-SQL Query Synthesizer (CLI Mode)
```bash
python3 ai/text_to_sql.py
```

### D. Gemini AI Root-Cause Anomaly Analysis
```bash
python3 ai/anomaly_insights.py
```

---

## 8. Data Observability & OpenLineage Governance

Run data freshness SLA checks, Z-score outlier detection, and OpenLineage metadata logging:
```bash
python3 scripts/data_observability.py
```
> Output JSON metadata is saved at `data/observability/openlineage_events.json`.

---

## 9. Daily Incremental Data Generation

Simulate a daily batch data ingestion cycle (appends new orders & reviews to raw datasets):
```bash
python3 scripts/generate_daily_incremental_data.py
```

---

## 10. Streamlit Multi-Page Web Application

Launch the interactive multi-page web app:
```bash
streamlit run app/app.py
```
or:
```bash
python3 -m streamlit run app/app.py
```
> Open browser at **[http://localhost:8501](http://localhost:8501)** to access:
> - 🏠 **Executive Overview**: System Status & Pipeline KPIs.
> - 📊 **BI Analytics**: GMV Trends, Cancellation Rates, Top Restaurants, SLA Durations.
> - 💬 **Review RAG Assistant**: Vector Similarity & LLM Sentiment Search.
> - 🤖 **Text-to-SQL Studio**: Natural Language SQL Query Engine.
> - 🚨 **Data Observability**: Anomaly Scatter Plots & Gemini AI Incident Synthesis.

---

## 11. Code Quality & CI/CD Governance (Pre-Commit, Black, SQLFluff)

### A. Install Pre-Commit Hooks
```bash
pre-commit install
```

### B. Run Black Code Formatter
```bash
black .
```

### C. Run SQLFluff Linter (DuckDB Dialect)
```bash
sqlfluff lint zomato_dbt/models --dialect duckdb
```

### D. Run All Pre-Commit Checks Manually
```bash
pre-commit run --all-files
```
