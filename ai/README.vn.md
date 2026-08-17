<div align="right">
  <a href="README.md">🇬🇧 English</a> | <b>🇻🇳 Tiếng Việt</b>
</div>

# 🤖 Tầng Trí Tuệ Nhân Tạo Generative AI (`ai/`)

Thư mục `ai/` chứa toàn bộ mã nguồn xử lý AI và trí tuệ nhân tạo cho hệ thống. Được vận hành bởi **Google Gemini API (`gemini-3.5-flash`)**, tầng này chịu trách nhiệm bóc tách sentiment đánh giá khách hàng, tìm kiếm tri thức Vector RAG, tự động sinh câu lệnh SQL tích hợp dbt Semantic Layer và viết báo cáo phân tích bất thường chỉ số (AI Anomaly Narrative).

---

## 📁 Cấu Trúc Thư Mục

```
ai/
 ├── __init__.py
 ├── llm_client.py         # Module kết nối LLM đa mô hình
 ├── enrich_reviews.py     # Pipeline phân tích cảm xúc & khía cạnh đánh giá
 ├── rag_chat.py           # Công cụ tìm kiếm RAG Vector Search
 ├── text_to_sql.py        # Studio truy vấn SQL ngôn ngữ tự nhiên (dbt Semantic Layer)
 └── anomaly_insights.py   # Báo cáo AI phân tích bất thường chỉ số vận hành
```

---

## ⚙️ Các Module Chính

1. **`llm_client.py`**: Module kết nối LLM đa mô hình với cơ chế tự động xoay vòng Gemini model (`gemini-3.5-flash` ➔ `gemini-flash-latest` ➔ `gemini-3.1-flash-lite`) chống nghẽn API quota.
2. **`enrich_reviews.py`**: Pipeline làm giàu dữ liệu đánh giá thô, trích xuất sentiment (`POSITIVE`, `NEGATIVE`, `NEUTRAL`) và khía cạnh dịch vụ.
3. **`rag_chat.py`**: Công cụ truy vấn RAG dựa trên TF-IDF Vector Search và kết hợp tổng hợp câu trả lời từ Gemini.
4. **`text_to_sql.py`**: Công cụ dịch thuật ngôn ngữ tự nhiên thành câu lệnh SQL DuckDB tích hợp ngữ cảnh dbt MetricFlow Semantic Layer và màng chắn SQL Guard.
5. **`anomaly_insights.py`**: Công cụ phân tích tự động các điểm bất thường chỉ số (`z-score > 2.0`) được phát hiện từ Data Observability và tạo báo cáo root-cause bằng Gemini.

---

## 🚀 Lệnh Thực Thi Terminal

Chạy RAG chat trực tiếp trên terminal:
```bash
python3 -m ai.rag_chat
```

Chạy AI Anomaly Narrative Analysis:
```bash
python3 ai/anomaly_insights.py
```
