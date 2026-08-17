<div align="right">
  <a href="README.md">🇬🇧 English</a> | <b>🇻🇳 Tiếng Việt</b>
</div>

# 🏛️ Mô Hình Biến Đổi dbt Medallion (`zomato_dbt/`)

Thư mục `zomato_dbt/` chứa mã nguồn dbt Core kết nối `dbt-duckdb` quản lý quá trình biến đổi dữ liệu chuẩn Medallion Architecture, kiểm thử chất lượng và tài liệu hóa schema (`docs.md`).

---

## 📁 Cấu Trúc Thư Mục

```
zomato_dbt/
 ├── dbt_project.yml        # Cấu hình dự án dbt
 ├── profiles.yml           # Kết nối cơ sở dữ liệu DuckDB
 └── models/
      ├── docs.md           # Khối tài liệu mô tả cho dbt catalog
      ├── staging/          # Silver Layer: Mô hình chuẩn hóa dữ liệu
      │    ├── schema.yml
      │    ├── stg_restaurants.sql
      │    ├── stg_users.sql
      │    ├── stg_food.sql
      │    ├── stg_orders.sql
      │    ├── stg_order_items.sql
      │    └── stg_reviews.sql
      └── marts/            # Gold Layer: Các bảng phân tích kinh doanh
           ├── schema.yml
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
