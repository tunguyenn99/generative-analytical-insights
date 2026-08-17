# 🏛️ dbt Medallion Transformation Pipeline (`zomato_dbt/`)

The `zomato_dbt/` directory contains the dbt Core project configured with `dbt-duckdb` for data modeling, Medallion Architecture transformations, schema documentation, and automated data quality testing.

---

## 📁 Directory Structure

```
zomato_dbt/
 ├── dbt_project.yml        # Main dbt project configuration
 ├── profiles.yml           # DuckDB database connection profile
 └── models/
      ├── staging/          # Silver Layer: Cleaned, type-casted staging models
      │    ├── schema.yml
      │    ├── stg_restaurants.sql
      │    ├── stg_users.sql
      │    ├── stg_food.sql
      │    ├── stg_orders.sql
      │    ├── stg_order_items.sql
      │    └── stg_reviews.sql
      └── marts/            # Gold Layer: Analytical business marts & dimensions
           ├── schema.yml
           ├── dim_restaurants.sql
           ├── dim_users.sql
           ├── dim_food.sql
           ├── fct_orders.sql
           ├── mart_daily_revenue.sql
           ├── mart_delivery_performance.sql
           └── mart_review_insights.sql
```

---

## 🏆 Medallion Architecture Layers

### 🥉 Bronze Layer (`ZOMATO_RAW`)
Raw table ingests loaded directly into DuckDB from AWS LocalStack S3 CSV data files.

### 🥈 Silver Layer (`STAGING`)
- Type casting (e.g. `TIMESTAMP`, `DECIMAL`, `INTEGER`).
- Column standardization and renaming.
- Input validation and null handling.

### 🥇 Gold Layer (`MARTS`)
- **Dimensions**: `dim_restaurants`, `dim_users`, `dim_food`.
- **Fact Table**: `fct_orders`.
- **Business Marts**:
  - `mart_daily_revenue`: Daily city-level GMV, total orders, and average order value.
  - `mart_delivery_performance`: City and hour-of-day delivery SLAs (median P50 vs 90th percentile P90).
  - `mart_review_insights`: Rating aggregations and sentiment summaries.

---

## 🧪 Data Quality Tests (35 Assertions)

Run tests manually:
```bash
cd zomato_dbt
dbt test
```

Includes:
- **`unique`** on primary keys (`restaurant_id`, `user_id`, `order_id`, `review_id`).
- **`not_null`** on mandatory analytical attributes.
- **`relationships`** testing referential integrity between orders, users, and restaurants.
- **`accepted_values`** for `order_status` (`DELIVERED`, `CANCELLED`).
