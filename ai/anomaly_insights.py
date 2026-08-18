import json
import os
import sys

# Ensure root path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import duckdb
from ai.llm_client import LLMClient

DB_PATH = "data/warehouse/zomato_dw.duckdb"


def generate_anomaly_narrative(anomalies=None):
    if anomalies is not None:
        if hasattr(anomalies, "to_json"):
            records_json = anomalies.to_json(orient="records")
        elif isinstance(anomalies, list):
            records_json = json.dumps(anomalies)
        else:
            records_json = str(anomalies)
    else:
        if not os.path.exists(DB_PATH):
            print(f"⚠️ Database '{DB_PATH}' not found!")
            return "⚠️ Database not found for anomaly extraction."

        con = duckdb.connect(DB_PATH, read_only=True)

        # Extract top anomalies (|z-score| > 2.0)
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
               OR ABS((r.cancellation_rate_pct - s.mean_cancel_rate) / NULLIF(s.std_cancel_rate, 0)) > 2.0
            ORDER BY ABS((r.gross_merchandise_value_gmv - s.mean_gmv) / NULLIF(s.std_gmv, 0)) DESC
            LIMIT 5;
        """
        ).fetchdf()

        con.close()

        if anomaly_df.empty:
            print("✅ No significant anomalies found for AI narrative synthesis.")
            return "✅ No significant statistical anomalies detected in the current warehouse run."

        records_json = anomaly_df.to_json(orient="records")

    llm = LLMClient()
    system_prompt = (
        "You are a Senior Data Operations Analyst at Zomato. "
        "Analyze the provided statistical metric anomalies (Z-score > 2.0 for GMV and Cancellation Rates) "
        "and generate a concise Executive Anomaly Narrative report with root cause hypotheses and operational recommendations. "
        "Provide your response in both English and Vietnamese."
    )
    user_prompt = f"Anomalous Metrics Records:\n{records_json}"

    narrative = llm.generate_completion(system_prompt, user_prompt)

    print("\n🤖 === Gemini LLM Executive Anomaly Analysis ===")
    print(narrative)
    print("=================================================\n")
    return narrative


if __name__ == "__main__":
    generate_anomaly_narrative()
