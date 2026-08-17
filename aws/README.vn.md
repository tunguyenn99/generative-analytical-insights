<div align="right">
  <a href="README.md">🇬🇧 English</a> | <b>🇻🇳 Tiếng Việt</b>
</div>

# 🇻🇳 Hạ Tầng AWS LocalStack (`aws/`)

Thư mục `aws/` chứa kịch bản cấu hình và khởi tạo container **AWS LocalStack** phục vụ giả lập dịch vụ đám mây AWS S3 ở môi trường local offline.

---

## 📁 Cấu Trúc Thư Mục

```
aws/
 └── localstack_init.sh     # Shell script tự động khởi tạo S3 buckets
```

---

## 🏗️ Thông Số Cấu Hình

- **Docker Container**: `localstack/localstack:3.0.0`
- **Dịch vụ Giả Lập**: AWS S3 Data Lake
- **Endpoint URL**: `http://localhost:4566`
- **Khu vực (Region)**: `us-east-1`
- **S3 Bucket Path**: `s3://zomato-data-lake/raw/`

---

## 🚀 Câu Lệnh Thực Thi

Khởi chạy container LocalStack S3:
```bash
docker compose up -d localstack
```

Khởi tạo bucket và nạp dữ liệu thô:
```bash
python3 scripts/init_localstack_s3.py
```
