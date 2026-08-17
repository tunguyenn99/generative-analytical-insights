<div align="center">

# 📜 Automation & Pipeline Scripts (`scripts/`)

<p align="center">
  <a href="#-english-version"><b>🇬🇧 English Version</b></a> | <a href="#-tiếng-việt-version"><b>🇻🇳 Tiếng Việt Version</b></a>
</p>

---

</div>

<a name="-english-version"></a>
# 🇬🇧 Automation & Pipeline Scripts (English)

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

<hr>

<a name="-tiếng-việt-version"></a>
# 🇻🇳 Kịch Bản Tự Động Hóa & Pipeline (Tiếng Việt)

Thư mục `scripts/` chứa các script Python thực thi nạp và phát sinh dữ liệu tự động cho hệ thống.

---

## ⚙️ Chi Tiết Kịch Bản

1. **`generate_sample_data.py`**: Khởi tạo tập dữ liệu mẫu ban đầu gồm 7 bảng thô.
2. **`generate_daily_incremental_data.py`**: Tự động tạo và nối thêm dữ liệu giao dịch ngẫu nhiên theo ngày hiện tại.
3. **`init_localstack_s3.py`**: Đồng bộ dữ liệu thô vào LocalStack S3 Bucket.
4. **`load_raw_duckdb.py`**: Nạp dữ liệu thô vào DuckDB Bronze layer.
5. **`run_pipeline.py`**: Chạy toàn bộ pipeline tự động từ A-Z.
