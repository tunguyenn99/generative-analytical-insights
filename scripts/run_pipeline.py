import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import subprocess
from generate_sample_data import generate_zomato_dataset
from scripts.init_localstack_s3 import upload_raw_data_to_s3
from scripts.load_raw_duckdb import load_raw_tables
from ai.enrich_reviews import enrich_reviews_pipeline

def run_full_pipeline():
    print("=========================================================================")
    print("🚀 STARTING END-TO-END ZOMATO DATA & AI PIPELINE (LOCAL STACK)")
    print("=========================================================================\n")

    # Step 1: Data Generation
    print("1️⃣ STEP 1: Generating Raw Zomato Datasets...")
    generate_zomato_dataset()
    print()

    # Step 2: AWS LocalStack Ingestion
    print("2️⃣ STEP 2: Ingesting Raw Data to AWS LocalStack S3...")
    upload_raw_data_to_s3()
    print()

    # Step 3: Raw DuckDB Loading
    print("3️⃣ STEP 3: Loading Bronze RAW schema into DuckDB Warehouse...")
    load_raw_tables()
    print()

    # Step 4: dbt Medallion Transformations & Tests
    print("4️⃣ STEP 4: Executing dbt Medallion Transformations & Data Quality Tests...")
    dbt_dir = os.path.abspath("zomato_dbt")
    result = subprocess.run(["dbt", "build", "--profiles-dir", "."], cwd=dbt_dir)
    if result.returncode != 0:
        print("❌ dbt build failed!")
        sys.exit(1)
    print("✅ dbt Transformations & Tests completed successfully!\n")

    # Step 5: LLM Review Enrichment
    print("5️⃣ STEP 5: Executing AI Layer - LLM Review Enrichment...")
    enrich_reviews_pipeline()
    print()

    print("=========================================================================")
    print("🎉 END-TO-END PIPELINE COMPLETED SUCCESSFULLY!")
    print("=========================================================================")
    print("💡 Next Step: Launch the Streamlit Web Application:")
    print("   streamlit run app/app.py")
    print("=========================================================================\n")

if __name__ == "__main__":
    run_full_pipeline()
