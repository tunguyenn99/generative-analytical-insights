<div align="center">

# 🤖 Generative AI Layer (`ai/`)

<p align="center">
  <a href="#-english-version"><b>🇬🇧 English Version</b></a> | <a href="#-tiếng-việt-version"><b>🇻🇳 Tiếng Việt Version</b></a>
</p>

---

</div>

<a name="-english-version"></a>
# 🇬🇧 Generative AI Layer (English)

The `ai/` directory houses the Generative AI engine and intelligence modules for the Zomato AI & Data Engineering platform. Powered by **Google Gemini API (`gemini-3.5-flash`)**, this layer enriches unstructured review data, provides RAG retrieval, and generates read-only SQL queries from natural language.

---

## 📁 Directory Structure

```
ai/
 ├── __init__.py
 ├── llm_client.py         # Multi-provider LLM connector (Gemini -> OpenAI -> Local Fallback)
 ├── enrich_reviews.py     # Batch review sentiment & aspect extraction pipeline
 ├── rag_chat.py           # Vector RAG search engine over customer reviews
 └── text_to_sql.py        # Text-to-SQL engine with schema context & security guard
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
- **Security Guard**: Enforces strict read-only execution (blocking `DROP`, `DELETE`, `UPDATE`, `INSERT`).

---

<hr>

<a name="-tiếng-việt-version"></a>
# 🇻🇳 Tầng Trí Tuệ Nhân Tạo Generative AI (Tiếng Việt)

Thư mục `ai/` chứa toàn bộ mã nguồn xử lý AI và trí tuệ nhân tạo cho hệ thống. Được vận hành bởi **Google Gemini API (`gemini-3.5-flash`)**, tầng này chịu trách nhiệm bóc tách sentiment đánh giá khách hàng, tìm kiếm tri thức Vector RAG và tự động sinh câu lệnh SQL từ ngôn ngữ tự nhiên.

---

## ⚙️ Các Module Chính

1. **`llm_client.py`**: Module kết nối LLM đa mô hình với cơ chế tự động xoay vòng Gemini model (`gemini-3.5-flash` ➔ `gemini-flash-latest` ➔ `gemini-3.1-flash-lite`) chống nghẽn API quota.
2. **`enrich_reviews.py`**: Pipeline làm giàu dữ liệu đánh giá thô, trích xuất sentiment (`POSITIVE`, `NEGATIVE`, `NEUTRAL`) và khía cạnh dịch vụ (`Food Quality`, `Delivery Speed`, `Packaging`, `Price`).
3. **`rag_chat.py`**: Công cụ truy vấn RAG dựa trên TF-IDF Vector Search và kết hợp tổng hợp câu trả lời từ Gemini.
4. **`text_to_sql.py`**: Công cụ dịch thuật ngôn ngữ tự nhiên thành câu lệnh SQL DuckDB kèm màng chắn an toàn SQL Guard (chỉ cho phép lệnh `SELECT`).

---

## 🚀 Lệnh Thực Thi Terminal

Chạy RAG chat trực tiếp trên terminal:
```bash
python3 -m ai.rag_chat
```

Chạy pipeline làm giàu sentiment đánh giá:
```bash
python3 ai/enrich_reviews.py
```
