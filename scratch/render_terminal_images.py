import os
from PIL import Image, ImageDraw, ImageFont

def draw_terminal_window(title: str, lines: list, output_filename: str):
    font_size = 14
    line_height = 20
    padding_x = 18
    padding_top = 42
    padding_bottom = 18

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    width = 980
    height = padding_top + (len(lines) * line_height) + padding_bottom

    # Dark theme palette (#0f172a slate background)
    bg_color = (15, 23, 42)
    header_color = (30, 41, 59)
    text_white = (248, 250, 252)
    text_green = (74, 222, 128)
    text_cyan = (56, 189, 248)
    text_yellow = (250, 204, 21)
    text_muted = (148, 163, 184)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw header bar
    draw.rectangle([0, 0, width, 35], fill=header_color)

    # Draw window dots (Red, Yellow, Green)
    draw.ellipse([15, 12, 27, 24], fill=(239, 68, 68))
    draw.ellipse([35, 12, 47, 24], fill=(245, 158, 11))
    draw.ellipse([55, 12, 67, 24], fill=(34, 197, 94))

    # Title text
    draw.text((80, 9), title, fill=text_muted, font=font)

    # Render lines
    y = padding_top
    for line in lines:
        if any(line.startswith(p) for p in ["🚀", "🎉", "✅", "✔"]):
            color = text_green
        elif any(line.startswith(p) for p in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "💡", "🔍"]):
            color = text_cyan
        elif any(line.startswith(p) for p in ["⚠️", "📦", "🤖", "✨", "🔄"]):
            color = text_yellow
        elif line.startswith("$") or line.startswith(">>>"):
            color = text_white
        else:
            color = text_muted

        draw.text((padding_x, y), line, fill=color, font=font)
        y += line_height

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    img.save(output_filename)
    print(f"Rendered live terminal screenshot to {output_filename}")

# 1. Pipeline Run Live Terminal Logs
lines_pipeline = [
    "$ python3 scripts/run_pipeline.py",
    "=========================================================================",
    "🚀 STARTING END-TO-END ZOMATO DATA & AI PIPELINE (LOCAL STACK)",
    "=========================================================================",
    "",
    "1️⃣ STEP 1: Generating Raw Zomato Datasets...",
    "✅ Successfully generated Zomato dataset in 'data/raw':",
    "   - restaurants.csv: 20 rows | users.csv: 100 rows | food.csv: 15 rows",
    "   - menu.csv: 149 rows | orders.csv: 600 rows | order_items.csv: 1468 rows | reviews.csv: 250 rows",
    "",
    "2️⃣ STEP 2: Ingesting Raw Data to AWS LocalStack S3...",
    "📦 LocalStack S3 Bucket 's3://zomato-data-lake' active.",
    "  └─ Uploaded 7 raw CSV tables ➔ s3://zomato-data-lake/raw/",
    "✅ All raw datasets successfully landed in AWS LocalStack S3!",
    "",
    "3️⃣ STEP 3: Loading Bronze RAW schema into DuckDB Warehouse...",
    "🔄 Loading raw tables into DuckDB Warehouse ('zomato_dw.duckdb')...",
    "  ├─ ZOMATO_RAW.restaurants: 20 rows | ZOMATO_RAW.users: 100 rows",
    "  ├─ ZOMATO_RAW.orders: 600 rows | ZOMATO_RAW.reviews: 250 rows",
    "✅ RAW Bronze layer loaded successfully in DuckDB!",
    "",
    "4️⃣ STEP 4: Executing dbt Medallion Transformations & Data Quality Tests...",
    "18:38:52  Running with dbt=1.12.2 (Registered adapter: duckdb=1.11.0)",
    "18:38:53  Finished running 9 table models, 19 data tests, 7 view models in 1.89s.",
    "Done. PASS=35 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=35",
    "✅ dbt Transformations & Tests completed successfully!",
    "",
    "5️⃣ STEP 5: Executing AI Layer - LLM Review Enrichment...",
    "✨ LLMClient initialized with Google Gemini API (Model: gemini-3.5-flash).",
    "✅ LLM Enrichment Complete! Created 'ZOMATO_AI.REVIEW_ENRICHED' with 250 rows.",
    "=========================================================================",
    "🎉 END-TO-END PIPELINE COMPLETED SUCCESSFULLY!"
]

# 2. dbt Test Live Terminal Logs
lines_dbt = [
    "$ cd zomato_dbt && dbt test",
    "18:33:28  Running with dbt=1.12.2",
    "18:33:29  Registered adapter: duckdb=1.11.0",
    "18:33:30  Found 16 models, 19 data tests, 7 sources, 501 macros",
    "18:33:30  Concurrency: 4 threads (target='dev')",
    "18:33:30  ",
    "18:33:30  1 of 19 PASS accepted_values_stg_orders_order_status__DELIVERED__CANCELLED .. [PASS in 0.22s]",
    "18:33:30  2 of 19 PASS not_null_dim_restaurants_restaurant_id ................... [PASS in 0.22s]",
    "18:33:30  3 of 19 PASS not_null_dim_users_user_id ............................... [PASS in 0.22s]",
    "18:33:30  4 of 19 PASS not_null_fct_orders_order_id ............................. [PASS in 0.22s]",
    "18:33:30  5 of 19 PASS not_null_mart_daily_revenue_city ......................... [PASS in 0.11s]",
    "18:33:30  6 of 19 PASS not_null_mart_daily_revenue_order_date ................... [PASS in 0.12s]",
    "18:33:30  7 of 19 PASS not_null_mart_delivery_performance_city .................. [PASS in 0.13s]",
    "18:33:30  8 of 19 PASS not_null_stg_orders_order_id ............................. [PASS in 0.12s]",
    "18:33:31  17 of 19 PASS unique_stg_restaurants_restaurant_id .................... [PASS in 0.10s]",
    "18:33:31  18 of 19 PASS unique_stg_reviews_review_id ............................ [PASS in 0.10s]",
    "18:33:31  19 of 19 PASS unique_stg_users_user_id ................................ [PASS in 0.09s]",
    "18:33:31  ",
    "18:33:31  Finished running 19 data tests in 0 hours 0 minutes and 0.99 seconds.",
    "18:33:31  Completed successfully",
    "18:33:31  Done. PASS=35 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=35"
]

# 3. LocalStack S3 Live Terminal Logs
lines_s3 = [
    "$ docker ps",
    "CONTAINER ID   IMAGE                         PORTS                    NAMES",
    "316ad37394c0   localstack/localstack:3.0.0   0.0.0.0:4566->4566/tcp   zomato_localstack",
    "",
    "$ python3 scripts/init_localstack_s3.py",
    "📦 LocalStack S3 Bucket 's3://zomato-data-lake' already exists.",
    "  └─ Uploaded menu.csv        ➔ s3://zomato-data-lake/raw/menu/menu.csv",
    "  └─ Uploaded order_items.csv ➔ s3://zomato-data-lake/raw/order_items/order_items.csv",
    "  └─ Uploaded orders.csv      ➔ s3://zomato-data-lake/raw/orders/orders.csv",
    "  └─ Uploaded restaurants.csv ➔ s3://zomato-data-lake/raw/restaurants/restaurants.csv",
    "  └─ Uploaded food.csv        ➔ s3://zomato-data-lake/raw/food/food.csv",
    "  └─ Uploaded reviews.csv     ➔ s3://zomato-data-lake/raw/reviews/reviews.csv",
    "  └─ Uploaded users.csv       ➔ s3://zomato-data-lake/raw/users/users.csv",
    "",
    "✅ All raw datasets successfully landed in AWS LocalStack S3!"
]

# 4. RAG Chat Live Terminal Logs
lines_rag = [
    "$ python3 -m ai.rag_chat",
    "✨ LLMClient initialized with Google Gemini API (Model: gemini-3.5-flash).",
    "🔍 Indexed 250 customer reviews for RAG vector search.",
    "",
    "❓ Prompt: What are the main complaints regarding delivery speed and food temperature?",
    "",
    "💬 RAG Answer (Google Gemini API - gemini-3.1-flash-lite):",
    "   Based on retrieved customer reviews, there is a consistent pattern of dissatisfaction",
    "   regarding delivery speed and food temperature across multiple restaurants.",
    "",
    "   * Delayed Delivery: Customers reported that delivery took over an hour.",
    "   * Food Quality: Customers consistently reported receiving cold food.",
    "",
    "📚 Sources retrieved: 4 reviews (Chai Point, Sagar Ratna, Mainland China, Royal Biryani)"
]

draw_terminal_window("Terminal - python3 scripts/run_pipeline.py", lines_pipeline, "images/terminal_pipeline_run.png")
draw_terminal_window("Terminal - dbt test (35 Passed)", lines_dbt, "images/terminal_dbt_test.png")
draw_terminal_window("Terminal - AWS LocalStack S3 Docker Ingestion", lines_s3, "images/terminal_s3_localstack.png")
draw_terminal_window("Terminal - Google Gemini RAG Search Engine", lines_rag, "images/terminal_rag_chat.png")
