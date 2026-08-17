import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ai.text_to_sql import TextToSQLEngine

st.set_page_config(page_title="Text-to-SQL Query Studio", page_icon="🤖", layout="wide")

st.title("🤖 Text-to-SQL Natural Language Query Studio")
st.markdown("*Query your Medallion Data Warehouse in plain English or Vietnamese!*")


@st.cache_resource
def get_sql_engine():
    return TextToSQLEngine()


engine = get_sql_engine()

st.sidebar.markdown("### 💡 Sample Questions:")
samples = [
    "Tổng doanh thu GMV và số đơn hàng theo từng thành phố?",
    "Cho tôi xem 5 nhà hàng có điểm đánh giá cao nhất?",
    "Phân tích thời gian giao hàng trung bình và p90 theo từng thành phố?",
    "Số lượng người dùng và tổng chi tiêu theo từng nhóm tuổi?",
]

for sample in samples:
    if st.sidebar.button(sample):
        st.session_state["sql_user_input"] = sample

user_q = st.text_input(
    "Enter your question for the Data Warehouse:",
    value=st.session_state.get("sql_user_input", ""),
    placeholder="e.g. Total revenue and orders by city?",
)

if st.button("🚀 Execute Query", type="primary") and user_q:
    with st.spinner("Generating SQL query & executing against DuckDB..."):
        res = engine.execute_query(user_q)

        if res["success"]:
            st.markdown("### 🔮 Generated DuckDB SQL Query:")
            st.code(res["sql"], language="sql")

            df = res["data"]
            st.markdown(f"### 📊 Query Results ({len(df)} rows):")
            st.dataframe(df, use_container_width=True)

            # Auto chart rendering for 2+ column numeric data
            num_cols = df.select_dtypes(include=["number"]).columns
            str_cols = df.select_dtypes(include=["object", "category", "string"]).columns

            if len(num_cols) >= 1 and len(str_cols) >= 1:
                st.markdown("### 📈 Auto Visual Analytics")
                fig = px.bar(
                    df,
                    x=str_cols[0],
                    y=num_cols[0],
                    color=str_cols[0],
                    title=f"{num_cols[0]} by {str_cols[0]}",
                    template="plotly_dark",
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"❌ Error: {res['error']}")
            if res["sql"]:
                st.code(res["sql"], language="sql")
