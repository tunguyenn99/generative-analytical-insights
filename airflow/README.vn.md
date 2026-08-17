<div align="right">
  <a href="README.md">🇬🇧 English</a> | <b>🇻🇳 Tiếng Việt</b>
</div>

# ⏱️ Điều Phối Dữ Liệu Apache Airflow (`airflow/`)

Thư mục `airflow/` chứa các định nghĩa Airflow DAGs định kỳ điều phối luồng dữ liệu tự động cho dự án Zomato Data Engineering.

---

## 📁 Cấu Trúc Thư Mục

```
airflow/
 └── dags/
      ├── zomato_batch_dag.py                # DAG chạy batch toàn bộ quy trình
      └── zomato_daily_incremental_dag.py    # DAG chạy phát sinh dữ liệu hàng ngày
```

---

## 🔄 Danh Sách DAGs

1. **`zomato_batch_dag`**: DAG điều phối toàn bộ chuỗi batch từ tạo dữ liệu thô ➔ tải lên S3 ➔ nạp DuckDB ➔ dbt build ➔ Gemini LLM enrichment.
2. **`zomato_daily_incremental_dag`**: DAG điều phối phát sinh dữ liệu ngẫu nhiên mới hàng ngày (`0 0 * * *`) và làm mới các tầng Medallion trong DuckDB.

---

## ⚙️ Kiểm Tra Cú Pháp

```bash
python3 airflow/dags/zomato_batch_dag.py
python3 airflow/dags/zomato_daily_incremental_dag.py
```
