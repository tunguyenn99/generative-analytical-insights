import os
import duckdb

DB_PATH = "data/warehouse/zomato_dw.duckdb"
DATA_DIR = "data/raw"


def load_raw_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = duckdb.connect(DB_PATH)

    # Ensure raw schema exists
    con.execute("CREATE SCHEMA IF NOT EXISTS ZOMATO_RAW;")

    tables = ["restaurants", "users", "food", "menu", "orders", "order_items", "reviews"]

    print(f"🔄 Loading raw tables into DuckDB Warehouse ('{DB_PATH}')...")
    for table in tables:
        csv_path = os.path.join(DATA_DIR, f"{table}.csv")
        if os.path.exists(csv_path):
            con.execute(
                f"""
                CREATE OR REPLACE TABLE ZOMATO_RAW.{table} AS
                SELECT * FROM read_csv_auto('{csv_path}', header=True);
            """
            )
            count = con.execute(f"SELECT COUNT(*) FROM ZOMATO_RAW.{table};").fetchone()[0]
            print(f"  ├─ ZOMATO_RAW.{table}: {count} rows loaded")
        else:
            print(f"  ⚠️ File {csv_path} not found!")

    con.close()
    print("✅ RAW Bronze layer loaded successfully in DuckDB!")


if __name__ == "__main__":
    load_raw_tables()
