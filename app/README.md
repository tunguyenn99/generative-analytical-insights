# 🖥️ Streamlit Web Application (`app/`)

The `app/` directory contains the multi-page **Streamlit** user interface and interactive web dashboard for the Zomato AI & Data Engineering platform.

---

## 📁 Directory Structure

```
app/
 ├── app.py                   # Main entry point & System Overview Home Page
 └── pages/
      ├── 1_📊_Analytics_Dashboard.py     # BI Plotly analytics & operational KPIs
      ├── 2_💬_Review_RAG_Assistant.py    # Generative AI Vector RAG review Q&A
      └── 3_🤖_Text_to_SQL_Query.py       # Natural language to DuckDB SQL Studio
```

---

## 🎨 Pages Overview

### 1. `app.py` - Executive Overview & Pipeline Monitor
- Displays top-level KPIs (Total Orders, Gross GMV, Active Restaurants, LLM Enriched Reviews).
- Real-time pipeline health check cards for LocalStack S3, DuckDB Warehouse, dbt Tests, and LLM API.

### 2. `1_📊_Analytics_Dashboard.py` - BI Analytics
- Interactive Plotly visualizations:
  - Daily GMV trend breakdown by city.
  - Cancellation rates by city.
  - Top 10 restaurants by GMV and rating.
  - Delivery lead time SLA (P50 vs P90) by hour of day.

### 3. `2_💬_Review_RAG_Assistant.py` - Review RAG Intelligence
- Natural language query box for customer review exploration.
- Combines TF-IDF vector similarity search over reviews with Google Gemini synthesis.
- Displays grounded answer markdown and source review metadata with relevance scores.

### 4. `3_🤖_Text_to_SQL_Query.py` - Text-to-SQL Studio
- Translates natural language questions (English/Vietnamese) into DuckDB SQL queries.
- Executes read-only queries against `MARTS` schema.
- Displays formatted data table and auto-generated Plotly bar charts.

---

## 🚀 Running the App

Start the Streamlit application:
```bash
streamlit run app/app.py
```
Open **`http://localhost:8501`** in your web browser.
