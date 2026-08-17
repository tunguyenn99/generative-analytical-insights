import os
import re
import duckdb
import pandas as pd
from ai.llm_client import LLMClient

DB_PATH = "data/warehouse/zomato_dw.duckdb"

SCHEMA_DOCUMENTATION = """
Available Data Warehouse Tables & Views in DuckDB (Zomato Project):

1. MARTS.mart_daily_revenue:
   - order_date (DATE)
   - city (VARCHAR: 'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', etc.)
   - total_orders (INT)
   - delivered_orders (INT)
   - cancelled_orders (INT)
   - gross_merchandise_value_gmv (DOUBLE)
   - average_order_value_aov (DOUBLE)
   - cancellation_rate_pct (DOUBLE)

2. MARTS.mart_delivery_performance:
   - city (VARCHAR)
   - order_hour (INT: 0 to 23)
   - total_deliveries (INT)
   - avg_delivery_mins (DOUBLE)
   - p50_delivery_mins (DOUBLE)
   - p90_delivery_mins (DOUBLE)

3. MARTS.mart_review_insights:
   - restaurant_id (INT)
   - restaurant_name (VARCHAR)
   - city (VARCHAR)
   - total_reviews (INT)
   - avg_star_rating (DOUBLE)
   - positive_reviews_count (INT)
   - neutral_reviews_count (INT)
   - negative_reviews_count (INT)

4. MARTS.dim_restaurants:
   - restaurant_id (INT), name (VARCHAR), city (VARCHAR), rating (DOUBLE), votes (INT), cost_for_two (INT), cuisine (VARCHAR), total_orders (INT), total_gmv (DOUBLE)

5. MARTS.dim_users:
   - user_id (INT), name (VARCHAR), email (VARCHAR), age (INT), age_group (VARCHAR), gender (VARCHAR), city (VARCHAR), signup_date (DATE), total_orders_placed (INT), total_spent (DOUBLE)

6. MARTS.fct_orders:
   - order_id (INT), user_id (INT), restaurant_id (INT), order_timestamp (TIMESTAMP), delivery_timestamp (TIMESTAMP), order_status (VARCHAR: 'DELIVERED', 'CANCELLED'), is_delivered (BOOLEAN), total_amount (DOUBLE), delivery_duration_mins (INT)

dbt Semantic Layer Metrics Definitions (MetricFlow Standard):
- gmv_metric: SUM(gross_merchandise_value_gmv) on MARTS.mart_daily_revenue
- order_volume_metric: SUM(total_orders) on MARTS.mart_daily_revenue
- cancellation_rate_metric: AVG(cancellation_rate_pct) on MARTS.mart_daily_revenue
"""


class TextToSQLEngine:

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.llm = LLMClient()

    def generate_sql(self, natural_language_query: str) -> str:
        system_prompt = (
            "You are an expert SQL Generator for DuckDB Data Warehouse. "
            "Convert the user's natural language question into a clean, valid DuckDB SQL query. "
            "Leverage the dbt Semantic Layer Metrics definitions when available. "
            "Return ONLY the executable SQL query string inside ```sql ... ``` block or as plain SQL text. "
            "IMPORTANT: Use SELECT statements ONLY. Do not attempt to modify, drop, or alter database tables."
            f"\n\nDatabase Schema Documentation & Semantic Metrics:\n{SCHEMA_DOCUMENTATION}"
        )
        user_prompt = f"Question: {natural_language_query}"

        raw_response = self.llm.generate_completion(system_prompt, user_prompt)

        # Clean markdown code blocks if present
        sql_match = re.search(r"```sql\s*(.*?)\s*```", raw_response, re.DOTALL)
        if sql_match:
            sql_query = sql_match.group(1).strip()
        else:
            sql_query = raw_response.strip()

        # Remove trailing semicolon or markdown backticks
        sql_query = sql_query.replace("```", "").strip()
        return sql_query

    def validate_sql(self, sql_query: str) -> bool:
        """Enforces SELECT-only security guard."""
        sql_clean = sql_query.upper().strip()
        if not sql_clean.startswith("SELECT") and not sql_clean.startswith("WITH"):
            return False
        forbidden_keywords = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "TRUNCATE",
            "CREATE",
        ]
        for kw in forbidden_keywords:
            if re.search(rf"\b{kw}\b", sql_clean):
                return False
        return True

    def execute_query(self, natural_language_query: str):
        sql_query = self.generate_sql(natural_language_query)

        if not self.validate_sql(sql_query):
            return {
                "success": False,
                "error": "Query rejected by Security Guard. Only SELECT read queries are permitted.",
                "sql": sql_query,
                "data": None,
            }

        try:
            con = duckdb.connect(self.db_path)
            df = con.execute(sql_query).fetchdf()
            con.close()
            return {
                "success": True,
                "error": None,
                "sql": sql_query,
                "data": df,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "sql": sql_query,
                "data": None,
            }


if __name__ == "__main__":
    engine = TextToSQLEngine()
    res = engine.execute_query("Cho tôi xem 5 nhà hàng có doanh thu GMV cao nhất?")
    print("\n🔮 Generated SQL:\n", res["sql"])
    print("\n📊 Query Result:\n", res["data"])
