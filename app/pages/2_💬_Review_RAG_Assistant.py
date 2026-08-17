import os
import sys
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ai.rag_chat import ReviewRAGSystem

st.set_page_config(page_title="Review RAG Assistant", page_icon="💬", layout="wide")

st.title("💬 Review RAG Intelligence Assistant")
st.markdown(
    "*Ask questions directly against customer reviews powered by Vector Search & LLM Retrieval*"
)


@st.cache_resource
def get_rag_system():
    return ReviewRAGSystem()


rag = get_rag_system()

st.sidebar.markdown("### 💡 Example Prompts:")
example_prompts = [
    "What do customers say about delivery speed and delays?",
    "Any complaints regarding food packaging or spilled gravy?",
    "Which restaurants get praised for authentic biryani and hot food?",
    "What are the most common reasons for 1-star ratings?",
]

for prompt in example_prompts:
    if st.sidebar.button(prompt):
        st.session_state["user_input"] = prompt

query_text = st.text_input(
    "Type your query regarding customer feedback:",
    value=st.session_state.get("user_input", ""),
    placeholder="e.g. What are the main customer complaints about food packaging?",
)

if st.button("🔎 Search & Generate Answer", type="primary") and query_text:
    with st.spinner("Retrieving relevant customer reviews & generating answer..."):
        response = rag.answer_query(query_text)

        st.markdown("### 🤖 AI Synthesized Insights")
        st.info(response["answer"])

        st.markdown("### 📚 Source Customer Reviews Retrieved")
        if response["sources"]:
            sources_df = pd.DataFrame(response["sources"])
            st.dataframe(
                sources_df[
                    [
                        "restaurant_name",
                        "city",
                        "star_rating",
                        "llm_sentiment",
                        "llm_aspect",
                        "review_text",
                        "relevance_score",
                    ]
                ],
                use_container_width=True,
            )
        else:
            st.warning("No matching sources found.")
