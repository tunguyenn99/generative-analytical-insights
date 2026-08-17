import json
import os
from datetime import datetime
import duckdb

DB_PATH = "data/warehouse/zomato_dw.duckdb"
OUTPUT_DIR = "data/observability"


def run_data_observability_audit():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        print(f"⚠️ Database '{DB_PATH}' not found!")
        return

    con = duckdb.connect(DB_PATH, read_only=True)
    print("🔍 === Data Observability & Statistical Anomaly Audit ===")

    # 1. Check Data Freshness
    freshness_df = con.execute(
        """
        SELECT
            MAX(order_timestamp) AS latest_order_time,
            ROUND(DATEDIFF('hour', MAX(order_timestamp), CURRENT_TIMESTAMP), 1) AS hours_since_last_order
        FROM STAGING.stg_orders;
    """
    ).fetchdf()

    latest_time = str(freshness_df["latest_order_time"].iloc[0])
    hours_lag = float(freshness_df["hours_since_last_order"].iloc[0])
    print(f"  ├─ 🕒 Data Freshness Check: Latest order at '{latest_time}' ({hours_lag} hours ago)")

    # 2. Z-Score Anomaly Detection on Daily Revenue GMV
    anomaly_df = con.execute(
        """
        WITH stats AS (
            SELECT
                AVG(gross_merchandise_value_gmv) AS mean_gmv,
                STDDEV(gross_merchandise_value_gmv) AS std_gmv,
                AVG(cancellation_rate_pct) AS mean_cancel_rate,
                STDDEV(cancellation_rate_pct) AS std_cancel_rate
            FROM MARTS.mart_daily_revenue
        )
        SELECT
            r.order_date,
            r.city,
            r.gross_merchandise_value_gmv,
            r.cancellation_rate_pct,
            ROUND((r.gross_merchandise_value_gmv - s.mean_gmv) / NULLIF(s.std_gmv, 0), 2) AS gmv_z_score,
            ROUND((r.cancellation_rate_pct - s.mean_cancel_rate) / NULLIF(s.std_cancel_rate, 0), 2) AS cancel_z_score
        FROM MARTS.mart_daily_revenue r, stats s
        WHERE ABS((r.gross_merchandise_value_gmv - s.mean_gmv) / NULLIF(s.std_gmv, 0)) > 2.0
           OR ABS((r.cancellation_rate_pct - s.mean_cancel_rate) / NULLIF(s.std_cancel_rate, 0)) > 2.0;
    """
    ).fetchdf()

    anomalies = []
    if not anomaly_df.empty:
        print(f"  ├─ ⚠️ Detected {len(anomaly_df)} Statistical Anomalies (|z-score| > 2.0):")
        for _, row in anomaly_df.iterrows():
            anomalies.append(
                {
                    "date": str(row["order_date"]),
                    "city": str(row["city"]),
                    "gmv": float(row["gross_merchandise_value_gmv"]),
                    "gmv_z_score": float(row["gmv_z_score"]),
                    "cancellation_rate": float(row["cancellation_rate_pct"]),
                    "cancel_z_score": float(row["cancel_z_score"]),
                }
            )
            print(
                f"  │    ├─ [{row['order_date']}] {row['city']}: GMV=₹{row['gross_merchandise_value_gmv']} (z={row['gmv_z_score']}), Cancel Rate={row['cancellation_rate_pct']}% (z={row['cancel_z_score']})"
            )
    else:
        print("  ├─ ✅ No Statistical Anomalies Detected in Gold Marts (|z-score| <= 2.0).")

    con.close()

    # 3. Generate OpenLineage Standard Event Metadata Payload
    openlineage_event = {
        "eventType": "COMPLETE",
        "eventTime": datetime.now().isoformat() + "Z",
        "producer": "https://github.com/tunguyenn99/generative-analytical-insights",
        "schemaURL": "https://openlineage.io/spec/1-0-5/OpenLineage.json#/$defs/RunEvent",
        "job": {
            "namespace": "zomato_data_engineering",
            "name": "zomato_medallion_pipeline_observability",
        },
        "inputs": [
            {
                "namespace": "s3://zomato-data-lake",
                "name": "raw/orders",
                "facets": {"schema": {"fields": [{"name": "order_id", "type": "INTEGER"}]}},
            },
            {
                "namespace": "s3://zomato-data-lake",
                "name": "raw/reviews",
                "facets": {"schema": {"fields": [{"name": "review_id", "type": "INTEGER"}]}},
            },
        ],
        "outputs": [
            {
                "namespace": "duckdb://data/warehouse/zomato_dw.duckdb",
                "name": "MARTS.mart_daily_revenue",
                "facets": {
                    "dataQualityMetrics": {
                        "freshnessHoursLag": hours_lag,
                        "anomaliesDetectedCount": len(anomalies),
                    }
                },
            }
        ],
    }

    event_path = os.path.join(OUTPUT_DIR, "openlineage_events.json")
    with open(event_path, "w") as f:
        json.dump(openlineage_event, f, indent=2)

    print(f"  └─ 📑 Saved OpenLineage event metadata to '{event_path}'.")
    print("✅ Data Observability & Lineage Audit Complete!")


if __name__ == "__main__":
    run_data_observability_audit()
