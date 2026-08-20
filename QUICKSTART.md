# 🚀 Comprehensive Step-by-Step Setup Guide

This guide will walk you from zero to running the complete **Zomato AI & Data Engineering Intelligence Platform** locally using Bash, Python virtual environment (`.venv`), environment variables (`.env`), dbt Core, DuckDB, Google Gemini AI, and Streamlit.

---

## 📋 Prerequisites

Make sure you have installed on your machine:
- **Python 3.10+** (Check via `python3 --version`)
- **Git** (Check via `git --version`)
- *(Optional)* **Docker & Docker Compose** (For running AWS LocalStack S3 container)

---

## 🛠️ Step 1: Clone Repository & Navigate to Directory

Open your Linux / macOS Terminal or WSL Bash and run:

```bash
git clone https://github.com/tunguyenn99/generative-analytical-insights.git
cd generative-analytical-insights
```

---

## 🐍 Step 2: Create & Activate Python Virtual Environment (`venv`)

Create a isolated Python environment named `.venv`:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment on Linux/macOS/WSL:
source .venv/bin/activate

# (Optional) Verify that active python points to .venv:
which python3
```

---

## 🔑 Step 3: Configure Environment Variables (`.env`)

Create your `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Open `.env` in your text editor (e.g. `nano .env` or VSCode) and add your **Google Gemini API Key** (Free tier available at [https://ai.google.dev/](https://ai.google.dev/)):

```env
GEMINI_API_KEY=your_gemini_api_key_here
DUCKDB_PATH=data/warehouse/zomato_dw.duckdb
OPENLINEAGE_URL=http://localhost:5000
```

> 💡 *Note: If you do not have a Gemini API key, the platform will automatically fall back to the built-in Local AI Engine.*

---

## 📦 Step 4: Install Dependencies

Upgrade `pip` and install all required Python libraries:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*(Optional for developers)* Enable automated pre-commit code formatting hooks:
```bash
pre-commit install
```

---

## 🐳 Step 5: (Optional) Launch Infrastructure via Docker

If you want to emulate AWS S3 storage using LocalStack:

```bash
docker compose up -d
```

---

## ⚙️ Step 6: Run End-to-End Data & AI Pipeline

You can run the entire pipeline with a single command:

```bash
python3 scripts/run_pipeline.py
```

### 🔄 What `run_pipeline.py` automatically executes:
1. **Raw Data Generation**: Generates 1,500 synthetic orders & 500 reviews across 2024–2026 (`generate_sample_data.py`).
2. **LocalStack S3 Ingestion**: Uploads CSV files to S3 bucket `s3://zomato-data-lake/raw/` (`scripts/init_localstack_s3.py`).
3. **DuckDB Raw Loading**: Loads Bronze `RAW` schema tables into `data/warehouse/zomato_dw.duckdb` (`scripts/load_raw_duckdb.py`).
4. **dbt Medallion Transformations & Tests**: Executes `dbt build` across Bronze ➔ Silver ➔ Gold schemas with 35+ data tests.
5. **Generative AI Enrichment**: Runs sentiment & aspect classification on customer reviews (`ai/enrich_reviews.py`).
6. **Data Observability Audit**: Runs SLA freshness check, OpenLineage telemetry logging, and Z-score anomaly detection (`scripts/data_observability.py`).

---

## 🌐 Step 7: Launch Interactive Streamlit Web Application

Start the multi-page Streamlit web app:

```bash
streamlit run app/app.py
```

or:

```bash
python3 -m streamlit run app/app.py
```

After running, open your web browser at:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🧪 Handy Commands Quick Reference

| Action | Command |
| :--- | :--- |
| **Run Daily Incremental Data Job** | `python3 scripts/generate_daily_incremental_data.py` |
| **Run dbt Models & Quality Tests** | `cd zomato_dbt && dbt build --profiles-dir . && cd ..` |
| **Run RAG Assistant CLI Query** | `python3 ai/rag_chat.py` |
| **Run Code Format & SQL Linter** | `pre-commit run --all-files` |
