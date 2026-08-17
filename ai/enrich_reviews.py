import os
import json
import duckdb
from ai.llm_client import LLMClient

DB_PATH = "data/warehouse/zomato_dw.duckdb"


def enrich_reviews_pipeline():
    print(f"🤖 Starting LLM Review Enrichment Pipeline on '{DB_PATH}'...")
    con = duckdb.connect(DB_PATH)
    llm = LLMClient()

    # Ensure schema ZOMATO_AI exists
    con.execute("CREATE SCHEMA IF NOT EXISTS ZOMATO_AI;")

    # Fetch reviews
    reviews_df = con.execute("""
        SELECT review_id, order_id, user_id, restaurant_id, review_text, star_rating, review_date 
        FROM STAGING.stg_reviews;
    """).fetchdf()

    if reviews_df.empty:
        print("⚠️ No reviews found in ZOMATO_STAGING.stg_reviews!")
        con.close()
        return

    print(f"  ├─ Processing {len(reviews_df)} customer reviews...")

    system_prompt = "You are an AI data enrichment assistant. Classify sentiment (POSITIVE, NEUTRAL, NEGATIVE) and aspect (Food Quality, Delivery Speed, Packaging, Pricing & Quantity, Service) into valid JSON format."

    enriched_records = []
    for _, row in reviews_df.iterrows():
        user_prompt = f"Review text: '{row['review_text']}'. Star rating: {row['star_rating']}."
        response_str = llm.generate_completion(system_prompt, user_prompt)

        try:
            parsed = json.loads(response_str)
            sentiment = parsed.get("sentiment", "NEUTRAL")
            aspect = parsed.get("aspect", "Food Quality")
        except Exception:
            sentiment = (
                "POSITIVE"
                if row["star_rating"] >= 4
                else ("NEGATIVE" if row["star_rating"] <= 2 else "NEUTRAL")
            )
            aspect = "Food Quality"

        enriched_records.append(
            (
                int(row["review_id"]),
                int(row["order_id"]),
                int(row["user_id"]),
                int(row["restaurant_id"]),
                str(row["review_text"]),
                int(row["star_rating"]),
                sentiment,
                aspect,
                row["review_date"],
            )
        )

    # Register temp table and create ZOMATO_AI.REVIEW_ENRICHED
    con.execute("DROP TABLE IF EXISTS ZOMATO_AI.REVIEW_ENRICHED;")
    con.execute("""
        CREATE TABLE ZOMATO_AI.REVIEW_ENRICHED (
            review_id INT,
            order_id INT,
            user_id INT,
            restaurant_id INT,
            review_text VARCHAR,
            star_rating INT,
            llm_sentiment VARCHAR,
            llm_aspect VARCHAR,
            review_date TIMESTAMP
        );
    """)

    con.executemany(
        """
        INSERT INTO ZOMATO_AI.REVIEW_ENRICHED 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
        enriched_records,
    )

    count = con.execute("SELECT COUNT(*) FROM ZOMATO_AI.REVIEW_ENRICHED;").fetchone()[0]
    con.close()
    print(f"✅ LLM Enrichment Complete! Created 'ZOMATO_AI.REVIEW_ENRICHED' with {count} rows.")


if __name__ == "__main__":
    enrich_reviews_pipeline()
