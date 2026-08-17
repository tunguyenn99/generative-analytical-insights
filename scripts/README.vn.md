<div align="right">
  <a href="README.md">🇬🇧 English</a> | <b>🇻🇳 Tiếng Việt</b>
</div>

# 📜 Kịch Bản Tự Động Hóa & Pipeline (`scripts/`)

Thư mục `scripts/` chứa các script Python thực thi nạp và phát sinh dữ liệu tự động cho hệ thống.

---

## 📁 Cấu Trúc Thư Mục

```
scripts/
 ├── init_localstack_s3.py               # Tải dữ liệu thô lên AWS LocalStack S3
 ├── load_raw_duckdb.py                  # Nạp dữ liệu vào DuckDB Bronze layer
 ├── generate_daily_incremental_data.py # Sinh dữ liệu phát sinh hàng ngày
 └── run_pipeline.py                     # Thực thi toàn bộ pipeline tự động
generate_sample_data.py                  # Khởi tạo tập dữ liệu mẫu ban đầu (root)
```

---

## ⚙️ Chi Tiết Kịch Bản

1. **`generate_sample_data.py`**: Khởi tạo tập dữ liệu mẫu ban đầu gồm 7 bảng thô.
2. **`generate_daily_incremental_data.py`**: Tự động tạo và nối thêm dữ liệu giao dịch ngẫu nhiên theo ngày hiện tại.
3. **`init_localstack_s3.py`**: Đồng bộ dữ liệu thô vào LocalStack S3 Bucket.
4. **`load_raw_duckdb.py`**: Nạp dữ liệu thô vào DuckDB Bronze layer.
5. **`run_pipeline.py`**: Chạy toàn bộ pipeline tự động từ A-Z.

---

## 🚀 Thực Thi

Chạy toàn bộ pipeline tự động:
```bash
python3 scripts/run_pipeline.py
```
