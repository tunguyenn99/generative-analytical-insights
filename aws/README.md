<div align="center">

# ☁️ AWS LocalStack Infrastructure (`aws/`)

<p align="center">
  <a href="#-english-version"><b>🇬🇧 English Version</b></a> | <a href="#-tiếng-việt-version"><b>🇻🇳 Tiếng Việt Version</b></a>
</p>

---

</div>

<a name="-english-version"></a>
# 🇬🇧 AWS LocalStack Infrastructure (English)

The `aws/` directory contains configuration scripts and docker setup for local cloud infrastructure emulation using **AWS LocalStack S3**.

---

## 📁 Directory Structure

```
aws/
 └── localstack_init.sh     # Initialization shell script to auto-create S3 buckets
```

---

## 🏗️ LocalStack Service Details

- **Docker Image**: `localstack/localstack:3.0.0`
- **Service**: AWS S3 Emulation
- **Endpoint**: `http://localhost:4566`
- **Region**: `us-east-1`
- **Access Credentials**: Dummy credentials (`aws_access_key_id=test`, `aws_secret_access_key=test`) for local offline development.

---

## 🪣 S3 Data Lake Bucket Layout

```text
s3://zomato-data-lake/
 └── raw/
      ├── restaurants/restaurants.csv
      ├── users/users.csv
      ├── food/food.csv
      ├── menu/menu.csv
      ├── orders/orders.csv
      ├── order_items/order_items.csv
      └── reviews/reviews.csv
```

---

<hr>

<a name="-tiếng-việt-version"></a>
# 🇻🇳 Hạ Tầng AWS LocalStack (Tiếng Việt)

Thư mục `aws/` chứa kịch bản cấu hình và khởi tạo container **AWS LocalStack** phục vụ giả lập dịch vụ đám mây AWS S3 ở môi trường local offline.

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
