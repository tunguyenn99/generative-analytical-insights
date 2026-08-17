<div align="right">
  <b>🇬🇧 English</b> | <a href="README.vn.md">🇻🇳 Tiếng Việt</a>
</div>

# 🤖 Generative AI Layer (`ai/`)

The `ai/` directory houses the Generative AI engine and intelligence modules for the Zomato AI & Data Engineering platform. Powered by **Google Gemini API (`gemini-3.5-flash`)**, this layer enriches unstructured review data, provides RAG retrieval, generates read-only SQL queries via dbt Semantic Layer, and synthesizes executive anomaly narratives.

---

## 📁 Directory Structure

```
ai/
 ├── __init__.py
 ├── llm_client.py         # Multi-provider LLM connector (Gemini -> OpenAI -> Local Fallback)
 ├── enrich_reviews.py     # Batch review sentiment & aspect extraction pipeline
 ├── rag_chat.py           # Vector RAG search engine over customer reviews
 ├── text_to_sql.py        # Text-to-SQL engine with dbt Semantic Layer metrics & SQL Guard
 └── anomaly_insights.py   # AI Executive Anomaly Narrative & Root-Cause Analysis
```

---

## ⚙️ Core Modules

### 1. `llm_client.py` - Unified Multi-Provider LLM Client
- **Primary Provider**: **Google Gemini API** (`gemini-3.5-flash`) via the official `google-genai` SDK.
- **Resilience**: Features automatic model rotation (`gemini-3.5-flash` ➔ `gemini-flash-latest` ➔ `gemini-3.1-flash-lite`) and local fallback if API quota is exhausted.

### 2. `enrich_reviews.py` - Review Sentiment & Topic Extraction
- Processes customer reviews from `ZOMATO_RAW.reviews`.
- Extracts `llm_sentiment` (`POSITIVE`, `NEGATIVE`, `NEUTRAL`) and `llm_aspect` (`Food Quality`, `Delivery Speed`, `Packaging`, `Price`, `Customer Service`).
- Saves results into DuckDB table `ZOMATO_AI.REVIEW_ENRICHED`.

### 3. `rag_chat.py` - Retrieval-Augmented Generation (RAG)
- Vector similarity search over customer reviews using TF-IDF and cosine distance.
- Grounded answers synthesized by Google Gemini with exact star ratings, quote snippets, and citations.

### 4. `text_to_sql.py` - Natural Language Text-to-SQL Studio
- Translates plain English or Vietnamese questions into DuckDB SQL queries against the Gold `MARTS` schema.
- **dbt Semantic Layer Context**: Integrates dbt MetricFlow metric definitions (`gmv_metric`, `order_volume_metric`, `cancellation_rate_metric`).
- **Security Guard**: Enforces strict read-only execution (blocking `DROP`, `DELETE`, `UPDATE`, `INSERT`).

### 5. `anomaly_insights.py` - AI Anomaly Narrative Analysis
- Reads statistical metric outliers (|z-score| > 2.0) detected by `scripts/data_observability.py`.
- Synthesizes executive anomaly root-cause reports in English and Vietnamese.

---

## 🚀 CLI Commands

Run RAG chat directly from terminal:
```bash
python3 -m ai.rag_chat
```

Run AI Anomaly Narrative Analysis:
```bash
python3 ai/anomaly_insights.py
```
