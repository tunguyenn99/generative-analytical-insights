<div align="center">

# 🍕 Zomato AI & Data Engineering Intelligence Platform

<p align="center">
  <a href="#-english-version"><b>🇬🇧 English Version</b></a> | <a href="#-tiếng-việt-version"><b>🇻🇳 Tiếng Việt Version</b></a>
</p>

---

</div>

<a name="-english-version"></a>
# 🇬🇧 Zomato AI & Data Engineering Platform (English)

An end-to-end modern batch data engineering and generative AI analytics platform. Built locally with **AWS LocalStack S3**, **DuckDB Data Warehouse**, **dbt Medallion Architecture**, **Apache Airflow**, **Google Gemini AI (`gemini-3.5-flash`)**, **Pre-Commit / CI Quality Governance**, and an interactive multi-page **Streamlit Web Application**.

---

## 📐 Architecture Diagram & Data Flow (Excalidraw Format)

![Data Architecture Diagram](images/architecture_diagram.png)

### 🔄 End-to-End Data Pipeline Flow:
1. **Raw Data Generation & Daily Incremental Ingestion**: Synthetic relational Zomato datasets generated across 7 tables (`restaurants`, `users`, `food`, `menu`, `orders`, `order_items`, `reviews`) plus scheduled daily incremental random batch ingestion (`scripts/generate_daily_incremental_data.py`).
2. **Data Landing Lake (AWS LocalStack S3)**: Emulated AWS S3 storage (`s3://zomato-data-lake/raw/`) managed via Docker Compose.
3. **Analytical Data Warehouse (DuckDB)**: Embedded high-performance OLAP data warehouse (`data/warehouse/zomato_dw.duckdb`).
4. **Transformations & Quality Governance (dbt Core)**: Medallion Architecture (Bronze Raw ➔ Silver Staging ➔ Gold Business Marts) with 35+ automated data quality tests (`dbt test`) and full schema documentation (`docs.md`).
5. **Code Quality & CI/CD Automation**: Automated pre-commit hooks (**Black** code formatter, **SQLFluff** SQL linter with DuckDB dialect) and GitHub Actions CI workflows (`ci_pipeline.yml`, `daily_incremental_pipeline.yml`).
6. **Generative AI Layer (Google Gemini API - Free Tier)**: Natural language review sentiment enrichment, Vector RAG search, and Text-to-SQL query synthesis using `gemini-3.5-flash`.
7. **Web Dashboard & User Interface (Streamlit)**: Multi-page UI featuring real-time KPIs, Plotly BI charts, RAG Q&A, and Text-to-SQL Query Studio.

---

## 🖥️ Application UI & Web Interfaces

### 1. 🏠 System Overview & Pipeline Status
![System Overview Dashboard](images/overview_dashboard.png)
- **Executive KPIs**: Real-time aggregation of Total Orders, Gross Revenue, Active Restaurants, and Enriched Customer Reviews.
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
| **Code Governance & CI** | GitHub Actions / Pre-Commit | **Black + SQLFluff** | Enforces consistent Python code formatting and DuckDB SQL linting |
| **Generative AI Model** | OpenAI GPT-4o | **Google Gemini (`gemini-3.5-flash`)** | **Free tier access**, 1M token context window, fast sentiment & RAG synthesis |
| **Orchestration** | Managed Airflow (MWAA) | **Apache Airflow (DAGs)** | Automated batch & daily incremental scheduling with step-by-step dependency DAGs |
| **Frontend UI** | Metabase / Tableau | **Streamlit + Plotly** | Custom Python web application with glassmorphic dark mode styling |

---

## 🏛️ Medallion Architecture (dbt Data Layers)

```
data/warehouse/zomato_dw.duckdb
 ├── ZOMATO_RAW (Bronze)       --> Direct raw table load from LocalStack S3 / CSVs
 ├── STAGING (Silver)          --> Type casted, sanitized staging views (stg_restaurants, stg_orders, etc.)
 ├── MARTS (Gold)              --> Business analytical marts (dim_restaurants, fct_orders, mart_daily_revenue, etc.)
 └── ZOMATO_AI (Enriched)      --> Gemini LLM review sentiment & aspect enrichment (REVIEW_ENRICHED)
```

---

<hr>

<a name="-tiếng-việt-version"></a>
# 🇻🇳 Zomato AI & Data Engineering Platform (Tiếng Việt)

Platform phân tích dữ liệu batch hiện đại và trí tuệ nhân tạo Generative AI end-to-end. Dự án được phát triển hoàn toàn ở môi trường Local tích hợp **AWS LocalStack S3**, **DuckDB Data Warehouse**, **dbt Medallion Architecture**, **Apache Airflow**, **Google Gemini AI (`gemini-3.5-flash`)**, **Pre-Commit / CI Quality Governance**, và ứng dụng web đa trang **Streamlit**.

---

## 📐 Sơ Đồ Kiến Trúc & Luồng Dữ Liệu (Chuẩn Excalidraw)

![Data Architecture Diagram](images/architecture_diagram.png)

### 🔄 Quy Trình Tự Động Hóa End-to-End:
1. **Khởi Tạo Dữ Liệu & Daily Incremental**: Tự động sinh dữ liệu thô Zomato qua 7 bảng (`restaurants`, `users`, `food`, `menu`, `orders`, `order_items`, `reviews`) và chạy job phát sinh dữ liệu ngẫu nhiên hàng ngày (`scripts/generate_daily_incremental_data.py`).
2. **Lưu Trữ Dữ Liệu Thô (AWS LocalStack S3)**: Giả lập AWS S3 (`s3://zomato-data-lake/raw/`) chạy qua Docker Compose.
3. **Kho Dữ Liệu Phân Tích (DuckDB)**: Embedded OLAP Data Warehouse tốc độ cao (`data/warehouse/zomato_dw.duckdb`).
4. **Biến Đổi & Kiểm Duyệt Chất Lượng (dbt Core)**: Mô hình Medallion (Bronze Raw ➔ Silver Staging ➔ Gold Business Marts) đi kèm 35+ data quality assertions (`dbt test`) và tài liệu schema chuẩn (`docs.md`).
5. **Chuẩn Hóa Mã Nguồn & CI/CD**: Kiểm tra mã nguồn tự động qua Pre-commit hooks (**Black** Python formatter, **SQLFluff** SQL linter với dialect DuckDB) và GitHub Actions Workflows (`ci_pipeline.yml`, `daily_incremental_pipeline.yml`).
6. **Tầng Trí Tuệ Nhân Tạo (Google Gemini API - Free Tier)**: Phân tích cảm xúc đánh giá khách hàng, tìm kiếm vector RAG và chuyển đổi câu hỏi tự nhiên thành câu lệnh SQL (`gemini-3.5-flash`).
7. **Giao Diện Web Phân Tích (Streamlit)**: Ứng dụng web đa trang hiển thị chỉ số KPI thời gian thực, biểu đồ Plotly, RAG Q&A và Text-to-SQL Query Studio.

---

## 🖥️ Màn Hình Giao Diện Web

### 1. 🏠 Executive Overview & Pipeline Health
![System Overview Dashboard](images/overview_dashboard.png)
- **KPI Tổng Quan**: Tổng đơn hàng, Doanh thu Gross GMV, Nhà hàng đối tác, và số lượng đánh giá được AI làm giàu.
- **Trạng Thái Pipeline**: Kiểm tra kết nối thời gian thực tới LocalStack S3, DuckDB Warehouse, dbt Tests (35/35 PASSED), và Gemini LLM API.

---

### 2. 📊 BI Analytics Dashboard
![BI Analytics Dashboard](images/analytics_dashboard.png)
- **Xu Hướng GMV Hàng Ngày**: Biểu đồ đường tương tác hiển thị doanh thu theo từng thành phố.
- **Tỷ Lệ Hủy Đơn**: Theo dõi phần trăm đơn hủy theo khu vực.
- **Top Nhà Hàng Theo GMV**: Xếp hạng nhà hàng doanh thu cao nhất.
- **Thời Gian Giao Hàng SLA**: So sánh thời gian giao trung vị (P50) và percentile 90 (P90) theo khung giờ trong ngày.

---

### 3. 💬 Review RAG Intelligence Assistant
![Review RAG Assistant](images/rag_assistant.png)
- **Tìm Kiếm Vector & Tổng Hợp LLM**: Kết hợp TF-IDF similarity trên đánh giá khách hàng với **Google Gemini (`gemini-3.5-flash`)**.
- **Câu Trả Lời Minh Bạch**: Trích dẫn chính xác trích dẫn đánh giá, số sao và tên nhà hàng.

---

### 4. 🤖 Text-to-SQL Natural Language Query Studio
![Text-to-SQL Query Studio](images/text_to_sql_studio.png)
- **Truy Vấn Ngôn Ngữ Tự Nhiên sang SQL**: Chuyển đổi câu hỏi tiếng Anh/tiếng Việt thành câu lệnh SQL DuckDB (chế độ Read-only).
- **Trực Quan Hóa Tự Động**: Thực thi SQL trên schema `MARTS` và tự động vẽ biểu đồ cột Plotly.

---

## 🚀 Hướng Dẫn Chạy Dự Án

### 1. Khởi Động Hạ Tầng LocalStack S3
```bash
docker compose up -d localstack
python3 scripts/init_localstack_s3.py
```

### 2. Chạy Toàn Bộ Pipeline End-to-End
```bash
python3 scripts/run_pipeline.py
```

### 3. Mở Giao Diện Web Streamlit
```bash
streamlit run app/app.py
```
Truy cập web tại: **`http://localhost:8501`**
