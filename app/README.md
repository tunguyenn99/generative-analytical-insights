<div align="center">

# 🖥️ Streamlit Web Application (`app/`)

<p align="center">
  <a href="#-english-version"><b>🇬🇧 English Version</b></a> | <a href="#-tiếng-việt-version"><b>🇻🇳 Tiếng Việt Version</b></a>
</p>

---

</div>

<a name="-english-version"></a>
# 🇬🇧 Streamlit Web Application (English)

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

<hr>

<a name="-tiếng-việt-version"></a>
# 🇻🇳 Giao Diện Web Streamlit (Tiếng Việt)

Thư mục `app/` chứa mã nguồn ứng dụng web đa trang **Streamlit** cho hệ thống phân tích Zomato AI.

---

## 🎨 Tổng Quan Các Màn Hình

1. **`app.py`**: Màn hình trang chủ Executive Overview hiển thị KPI tổng quan và trạng thái hoạt động thời gian thực của pipeline.
2. **`1_📊_Analytics_Dashboard.py`**: Màn hình BI Analytics trực quan hóa xu hướng doanh thu GMV, tỷ lệ hủy đơn, xếp hạng nhà hàng và SLA thời gian giao hàng.
3. **`2_💬_Review_RAG_Assistant.py`**: Trợ lý trí tuệ nhân tạo RAG tra cứu đánh giá khách hàng theo câu hỏi tự nhiên.
4. **`3_🤖_Text_to_SQL_Query.py`**: Studio chuyển đổi câu hỏi tự nhiên thành câu lệnh SQL DuckDB và tự động vẽ biểu đồ trực quan.

---

## 🚀 Khởi Động Web App

```bash
streamlit run app/app.py
```
Truy cập ứng dụng tại địa chỉ: **`http://localhost:8501`**
