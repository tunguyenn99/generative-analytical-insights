# 🍕 Zomato AI & Data Engineering Intelligence Platform

An end-to-end modern batch data engineering and generative AI analytics platform. Built locally with **AWS LocalStack S3**, **DuckDB Data Warehouse**, **dbt Medallion Architecture**, **Apache Airflow**, **Google Gemini AI (`gemini-3.5-flash`)**, and an interactive multi-page **Streamlit Web Application**.

---

## 📐 Architecture Diagram & Data Flow (Excalidraw Format)

![Data Architecture Diagram](images/architecture_diagram.png)

### 🔄 End-to-End Data Pipeline Flow:
1. **Raw Data Generation**: Synthetic relational Zomato datasets generated across 7 tables (`restaurants`, `users`, `food`, `menu`, `orders`, `order_items`, `reviews`).
2. **Data Landing Lake (AWS LocalStack S3)**: Emulated AWS S3 storage (`s3://zomato-data-lake/raw/`) managed via Docker Compose.
3. **Analytical Data Warehouse (DuckDB)**: Embedded high-performance OLAP data warehouse (`data/warehouse/zomato_dw.duckdb`).
4. **Transformations & Quality Governance (dbt Core)**: Medallion Architecture (Bronze Raw ➔ Silver Staging ➔ Gold Business Marts) with 35+ automated data quality tests (`dbt test`).
5. **Generative AI Layer (Google Gemini API - Free Tier)**: Natural language review sentiment enrichment, Vector RAG search, and Text-to-SQL query synthesis using `gemini-3.5-flash`.
6. **Web Dashboard & User Interface (Streamlit)**: Multi-page UI featuring real-time KPIs, Plotly BI charts, RAG Q&A, and Text-to-SQL Query Studio.

---

## 🖥️ Application UI & Web Interfaces

### 1. 🏠 System Overview & Pipeline Status
![System Overview Dashboard](images/overview_dashboard.png)
- **Executive KPIs**: Real-time aggregation of Total Orders (600), Gross Revenue (₹ 742,069.00), Active Restaurants (20), and Enriched Customer Reviews (250).
- **Pipeline Health**: Live status tracking for AWS LocalStack S3, DuckDB Warehouse, dbt Model Tests (35/35 PASSED), and LLM Review Enrichment.

---

### 2. 📊 BI Analytics Dashboard
![BI Analytics Dashboard](images/analytics_dashboard.png)
- **Daily GMV Trend**: Interactive line chart showing daily revenue broken down by city.
- **Cancellation Rates**: City-level cancellation percentages for operational monitoring.
- **Top Restaurants by GMV**: Ranked by gross merchandise value and star rating.
- **Delivery Lead Time SLA**: Hour-of-day comparison between median (P50) and 90th percentile (P90) delivery duration in minutes.

---

### 3. 💬 Review RAG Intelligence Assistant
![Review RAG Assistant](images/rag_assistant.png)
- **Vector Search & LLM Synthesis**: Combines TF-IDF vector similarity over customer reviews with **Google Gemini (`gemini-3.5-flash`)** response generation.
- **Grounded Insights**: Produces structured answers with exact quotes, star ratings, and restaurant citations.

---

### 4. 🤖 Text-to-SQL Natural Language Query Studio
![Text-to-SQL Query Studio](images/text_to_sql_studio.png)
- **Natural Language to DuckDB SQL**: Converts English and Vietnamese questions directly into read-only SQL queries.
- **Auto Data & Visual Charts**: Executes SQL against the `MARTS` schema and automatically renders interactive data tables and visual Plotly bar charts.

---

## 💻 Backend Pipeline Execution & Terminal Outputs

### 1. 🚀 End-to-End Pipeline Execution (`scripts/run_pipeline.py`)
![Pipeline Terminal Run](images/terminal_pipeline_run.png)

### 2. 📦 AWS LocalStack S3 Data Landing Ingestion
![AWS LocalStack S3 Terminal](images/terminal_s3_localstack.png)

### 3. 🧪 dbt Medallion Model Transformations & Quality Tests (35/35 PASSED)
![dbt Test Terminal](images/terminal_dbt_test.png)

### 4. 🧠 Google Gemini RAG Search Engine Execution (`ai/rag_chat.py`)
![Gemini RAG Terminal](images/terminal_rag_chat.png)

---

## 🛠️ Technology Stack & Architecture Comparison

| Pipeline Component | Production Cloud Standard | Local Production Stack | Rationale & Advantage |
| :--- | :--- | :--- | :--- |
| **Data Lake Storage** | AWS S3 (Cloud) | **AWS LocalStack S3** | Zero cloud cost, full AWS S3 API compatibility via boto3 |
| **Data Warehouse** | Snowflake / Redshift | **DuckDB** | Zero setup, ultra-fast vectorised in-memory analytical SQL engine |
| **Transformation Engine** | dbt Cloud / dbt-snowflake | **`dbt-duckdb`** | Full SQL modularity, lineage graph, data quality tests, schema documentation |
| **Generative AI Model** | OpenAI GPT-4o | **Google Gemini (`gemini-3.5-flash`)** | **Free tier access**, 1M token context window, fast sentiment & RAG synthesis |
| **Orchestration** | Managed Airflow (MWAA) | **Apache Airflow (DAGs)** | Automated batch scheduling with step-by-step dependency DAGs |
| **Frontend UI** | Metabase / Tableau | **Streamlit + Plotly** | Custom Python web application with glassmorphic dark mode styling |

---

## 💡 Architectural Deep-Dive: Text-to-SQL vs. dbt MetricFlow

| Criteria | 🤖 Generative Text-to-SQL (Chosen Approach) | 📐 dbt MetricFlow / Semantic Layer |
| :--- | :--- | :--- |
| **Query Flexibility** | **Unrestricted Ad-hoc Natural Language**: Can answer arbitrary questions across any dimensions and tables. | **Restricted to Pre-defined Metrics**: Can only query metrics explicitly defined in `semantic_models` YML files. |
| **User Experience** | **Conversational UI**: Non-technical users ask questions in natural language (English/Vietnamese). | **API / Code Driven**: Requires GraphQL/dbt Semantic Layer API or CLI commands. |
| **Infrastructure Cost** | **Zero Extra Infrastructure Cost**: Runs locally against DuckDB using free-tier LLM APIs. | **Requires dbt Cloud / Proxy**: Production deployment requires dbt Cloud Semantic Layer API or custom proxy host. |
| **Setup Overhead** | **Low Setup**: Prompt engineering + schema context injection from dbt `schema.yml`. | **High Setup**: Requires writing hundreds of lines of YAML for dimensions, entities, and measure aggregations. |
| **Best Used For** | Exploratory analytics, self-service business Q&A, unstructured data synthesis. | Standardized executive KPI reporting, fixed dashboard metrics, single-source-of-truth governance. |

> **Production Recommendation**: In enterprise environments, the ideal architecture combines both: **dbt MetricFlow** governs core KPIs, while **Text-to-SQL** operates on top of dbt Gold Marts to allow flexible natural language exploration!

---

## 🏛️ Medallion Architecture (dbt Data Layers)

```
data/warehouse/zomato_dw.duckdb
 ├── ZOMATO_RAW (Bronze)       --> Direct raw table load from LocalStack S3 / CSVs
 ├── STAGING (Silver)          --> Type casting, cleaned columns, normalized schemas
 │    ├── stg_restaurants.sql
 │    ├── stg_users.sql
 │    ├── stg_food.sql
 │    ├── stg_orders.sql
 │    ├── stg_order_items.sql
 │    └── stg_reviews.sql
 └── MARTS (Gold)              --> Star schema dimensional models & analytical business marts
      ├── dim_restaurants.sql
      ├── dim_users.sql
      ├── dim_food.sql
      ├── mart_daily_revenue.sql
      ├── mart_delivery_performance.sql
      └── mart_review_insights.sql
```

---

## 🚀 Quick Start Guide

### 1. Prerequisite Setup & Credentials
Clone the repository and create your virtual environment:
```bash
git clone https://github.com/tunguyenn99/generative-analytical-insights.git
cd generative-analytical-insights

# Install python dependencies
pip install -r requirements.txt
```

Set up your `.env` file with your free Google Gemini API Key (obtained from [Google AI Studio](https://aistudio.google.com/app/apikey)):
```bash
cp .env.example .env
# Edit .env and add your key:
# GEMINI_API_KEY=your_gemini_api_key_here
```

---

### 2. Start AWS LocalStack S3 (Docker)
```bash
docker compose up -d localstack
```

---

### 3. Run End-to-End Pipeline
Execute data generation, S3 upload, DuckDB loading, dbt medallion compilation/tests, and Gemini AI review enrichment:
```bash
python3 scripts/run_pipeline.py
```

---

### 4. Launch Streamlit Web Application
```bash
streamlit run app/app.py
```
Open **`http://localhost:8501`** in your browser to explore the dashboard!

---

## 🧪 Testing & Data Quality
Run dbt data quality checks manually:
```bash
cd zomato_dbt
dbt test
```
All **35 data tests** (uniqueness, non-null, referential integrity) pass cleanly.
