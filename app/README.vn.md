<div align="right">
  <a href="README.md">🇬🇧 English</a> | <b>🇻🇳 Tiếng Việt</b>
</div>

# 🖥️ Giao Diện Web Streamlit (`app/`)

Thư mục `app/` chứa mã nguồn ứng dụng web đa trang **Streamlit** cho hệ thống phân tích Zomato AI.

---

## 📁 Cấu Trúc Thư Mục

```
app/
 ├── app.py                   # Màn hình trang chủ Executive Overview
 └── pages/
      ├── 1_📊_Analytics_Dashboard.py     # BI Analytics & Chỉ số hoạt động
      ├── 2_💬_Review_RAG_Assistant.py    # Trợ lý trí tuệ nhân tạo RAG Q&A
      └── 3_🤖_Text_to_SQL_Query.py       # Studio truy vấn SQL ngôn ngữ tự nhiên
```

---

## 🎨 Tổng Quan Các Màn Hình

1. **`app.py`**: Màn hình trang chủ Executive Overview hiển thị KPI tổng quan và trạng thái hoạt động thời gian thực của pipeline.
2. **`1_📊_Analytics_Dashboard.py`**: Màn hình BI Analytics trực quan hóa xu hướng doanh thu GMV, tỷ lệ hủy đơn, xếp hạng nhà hàng và SLA thời gian giao hàng.
3. **`2_💬_Review_RAG_Assistant.py`**: Trợ lý trí tuệ nhân tạo RAG tra cứu đánh giá khách hàng theo câu hỏi tự nhiên.
4. **`3_🤖_Text_to_SQL_Query.py`**: Studio chuyển đổi câu hỏi tự nhiên thành câu lệnh SQL DuckDB và tự động vẽ biểu đồ trực quan.

---

## 🚀 Khởi Động Web App

```bash
streamlit run app/app.py
```
Truy cập ứng dụng tại địa chỉ: **`http://localhost:8501`**
