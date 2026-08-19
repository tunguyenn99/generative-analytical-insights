import os
import sys
import streamlit as st

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(
    page_title="Zomato Generative Analytical Insights",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Premium Custom Dark Glassmorphism Styling
st.markdown(
    """
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        text-align: center;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-lbl {
        font-size: 0.95rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-tag {
        background: #0284c7;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Multi-Page Navigation Structure
pages = {
    "📌 INTRODUCTION": [
        st.Page(
            "pages/0_🏠_Executive_Overview.py",
            title="Executive Overview",
            icon="🏠",
            default=True,
        ),
    ],
    "📊 INSIGHTS & ANALYTICS": [
        st.Page(
            "pages/1_📊_Analytics_Dashboard.py",
            title="BI Analytics Dashboard",
            icon="📊",
        ),
    ],
    "🤖 GENERATIVE AI": [
        st.Page(
            "pages/2_💬_Review_RAG_Assistant.py",
            title="Review RAG Assistant",
            icon="💬",
        ),
        st.Page(
            "pages/3_🤖_Text_to_SQL_Query.py",
            title="Text-to-SQL Query Studio",
            icon="🤖",
        ),
    ],
    "🛡️ GOVERNANCE & OBSERVABILITY": [
        st.Page(
            "pages/4_🚨_Data_Observability.py",
            title="Data Observability & Audit",
            icon="🚨",
        ),
    ],
}

# Sidebar Branding Header
with st.sidebar:
    st.markdown("## 🍕 Zomato AI Engine")
    st.caption("End-to-End Modern Data & Generative AI Platform")
    st.divider()

pg = st.navigation(pages)
pg.run()
