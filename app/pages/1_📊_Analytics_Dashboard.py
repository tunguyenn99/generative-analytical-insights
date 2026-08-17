import os
import duckdb
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Zomato Analytics Dashboard", page_icon="📊", layout="wide")

st.title("📊 Zomato Business Analytics Dashboard")
st.markdown("*Real-time Insights from Medallion Data Warehouse (`MARTS` Schema)*")

DB_PATH = "data/warehouse/zomato_dw.duckdb"

if not os.path.exists(DB_PATH):
    st.error("Database not found!")
    st.stop()

con = duckdb.connect(DB_PATH)

# Filter options
cities_df = con.execute("SELECT DISTINCT city FROM MARTS.dim_restaurants ORDER BY city;").fetchdf()
selected_city = st.sidebar.selectbox("Select City Filter", ["All Cities"] + list(cities_df["city"]))

# 1. GMV & Daily Revenue
query_rev = "SELECT * FROM MARTS.mart_daily_revenue"
if selected_city != "All Cities":
    query_rev += f" WHERE city = '{selected_city}'"
query_rev += " ORDER BY order_date ASC;"

df_rev = con.execute(query_rev).fetchdf()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Gross Merchandise Value (GMV) Trend")
    fig_gmv = px.line(
        df_rev,
        x="order_date",
        y="gross_merchandise_value_gmv",
        color="city" if selected_city == "All Cities" else None,
        title="Daily GMV (₹) Over Time",
        labels={"gross_merchandise_value_gmv": "GMV (₹)", "order_date": "Order Date"},
        template="plotly_dark",
    )
    st.plotly_chart(fig_gmv, use_container_width=True)

with col2:
    st.subheader("📦 Order Cancellation Rate (%)")
    fig_cancel = px.bar(
        df_rev.groupby("city", as_index=False)["cancellation_rate_pct"].mean(),
        x="city",
        y="cancellation_rate_pct",
        color="cancellation_rate_pct",
        color_continuous_scale="Reds",
        title="Average Cancellation Rate by City",
        labels={"cancellation_rate_pct": "Cancellation Rate (%)", "city": "City"},
        template="plotly_dark",
    )
    st.plotly_chart(fig_cancel, use_container_width=True)

# 2. Restaurant Performance & SLA
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.subheader("🏆 Top Restaurants by GMV")
    query_rest = "SELECT name, city, rating, total_orders, total_gmv FROM MARTS.dim_restaurants"
    if selected_city != "All Cities":
        query_rest += f" WHERE city = '{selected_city}'"
    query_rest += " ORDER BY total_gmv DESC LIMIT 10;"

    df_rest = con.execute(query_rest).fetchdf()
    fig_rest = px.bar(
        df_rest,
        x="total_gmv",
        y="name",
        orientation="h",
        color="rating",
        color_continuous_scale="Viridis",
        title="Top 10 Restaurants by GMV & Star Rating",
        labels={"total_gmv": "Total GMV (₹)", "name": "Restaurant"},
        template="plotly_dark",
    )
    fig_rest.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_rest, use_container_width=True)

with col4:
    st.subheader("⏱️ Delivery Lead Time SLA (p90 vs p50)")
    query_sla = "SELECT city, order_hour, avg_delivery_mins, p50_delivery_mins, p90_delivery_mins FROM MARTS.mart_delivery_performance"
    if selected_city != "All Cities":
        query_sla += f" WHERE city = '{selected_city}'"
    query_sla += " ORDER BY order_hour ASC;"

    df_sla = con.execute(query_sla).fetchdf()
    fig_sla = px.line(
        df_sla,
        x="order_hour",
        y=["p50_delivery_mins", "p90_delivery_mins"],
        title="Delivery Lead Time (Minutes) by Hour of Day",
        labels={"value": "Delivery Duration (Mins)", "order_hour": "Hour of Day (0-23)"},
        template="plotly_dark",
    )
    st.plotly_chart(fig_sla, use_container_width=True)

con.close()
