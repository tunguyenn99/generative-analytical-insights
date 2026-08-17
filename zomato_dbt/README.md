<div align="center">

# 🏛️ dbt Medallion Transformation Pipeline (`zomato_dbt/`)

<p align="center">
  <a href="#-english-version"><b>🇬🇧 English Version</b></a> | <a href="#-tiếng-việt-version"><b>🇻🇳 Tiếng Việt Version</b></a>
</p>

---

</div>

<a name="-english-version"></a>
# 🇬🇧 dbt Medallion Transformation Pipeline (English)

The `zomato_dbt/` directory contains the dbt Core project configured with `dbt-duckdb` for data modeling, Medallion Architecture transformations, schema documentation (`docs.md`), and automated data quality testing.

---

## 📁 Directory Structure

```
zomato_dbt/
 ├── dbt_project.yml        # Main dbt project configuration
 ├── profiles.yml           # DuckDB database connection profile
 └── models/
      ├── docs.md           # Markdown documentation blocks for dbt catalog
      ├── staging/          # Silver Layer: Cleaned, type-casted staging models
      │    ├── schema.yml   # Staging schema definitions & tests
      │    ├── stg_restaurants.sql
      │    ├── stg_users.sql
      │    ├── stg_food.sql
      │    ├── stg_orders.sql
      │    ├── stg_order_items.sql
      │    └── stg_reviews.sql
      └── marts/            # Gold Layer: Analytical business marts & dimensions
           ├── schema.yml   # Gold Marts schema definitions & tests
           ├── dim_restaurants.sql
           ├── dim_users.sql
           ├── dim_date.sql
           ├── dim_food.sql
           ├── fct_orders.sql
           ├── fct_order_items.sql
           ├── mart_daily_revenue.sql
           ├── mart_delivery_performance.sql
           └── mart_review_insights.sql
```

---

## 🏆 Medallion Architecture Layers

### 🥉 Bronze Layer (`ZOMATO_RAW`)
Raw table ingests loaded directly into DuckDB from AWS LocalStack S3 CSV data files.

### 🥈 Silver Layer (`STAGING`)
- Type casting (`TIMESTAMP`, `DECIMAL`, `INTEGER`).
- Column standardization and cleaning.

### 🥇 Gold Layer (`MARTS`)
- **Dimensions**: `dim_restaurants`, `dim_users`, `dim_date`, `dim_food`.
- **Fact Tables**: `fct_orders`, `fct_order_items`.
- **Business Marts**: `mart_daily_revenue`, `mart_delivery_performance`, `mart_review_insights`.

---

## 🧪 Data Quality Tests (35 Assertions) & Docs

Run tests manually:
```bash
cd zomato_dbt
dbt build
```

Generate schema documentation catalog:
```bash
dbt docs generate
```

---

<hr>

<a name="-tiếng-việt-version"></a>
# 🇻🇳 Mô Hình Biến Đổi dbt Medallion (Tiếng Việt)

Thư mục `zomato_dbt/` chứa mã nguồn dbt Core kết nối `dbt-duckdb` quản lý quá trình biến đổi dữ liệu chuẩn Medallion Architecture, kiểm thử chất lượng và tài liệu hóa schema (`docs.md`).

---

## 🏆 Các Tầng Kiến Trúc Medallion

1. **Bronze Layer (`ZOMATO_RAW`)**: Tầng dữ liệu thô nạp từ S3 CSVs.
2. **Silver Layer (`STAGING`)**: Tầng chuẩn hóa kiểu dữ liệu, làm sạch tên cột và xử lý giá trị khuyết thiếu.
3. **Gold Layer (`MARTS`)**: Tầng dữ liệu phân tích kinh doanh gồm bảng Chiều (Dimensions), Bảng Sự kiện (Fact) và các bảng Báo cáo (Marts).

---

## 🧪 Kiểm Thử & Tạo Tài Liệu Schema

Thực thi biến đổi và kiểm thử 35 data assertions:
```bash
cd zomato_dbt
dbt build
```

Sinh trang web tài liệu dbt catalog:
```bash
dbt docs generate
```
