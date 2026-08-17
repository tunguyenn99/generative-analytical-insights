<div align="right">
  <b>🇬🇧 English</b> | <a href="README.vn.md">🇻🇳 Tiếng Việt</a>
</div>

# ☁️ AWS LocalStack Infrastructure (`aws/`)

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

## 🚀 Commands

Start LocalStack S3 container:
```bash
docker compose up -d localstack
```

Verify S3 bucket creation using Boto3 or AWS CLI:
```bash
python3 scripts/init_localstack_s3.py
```
