import os
import duckdb
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ai.llm_client import LLMClient

DB_PATH = "data/warehouse/zomato_dw.duckdb"


class ReviewRAGSystem:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.llm = LLMClient()
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.reviews_data = []
        self.tfidf_matrix = None
        self._index_reviews()

    def _index_reviews(self):
        if not os.path.exists(self.db_path):
            print(f"⚠️ Warehouse database '{self.db_path}' not found!")
            return

        con = duckdb.connect(self.db_path)
        try:
            df = con.execute("""
                SELECT 
                    e.review_id,
                    r.name AS restaurant_name,
                    r.city,
                    e.review_text,
                    e.star_rating,
                    e.llm_sentiment,
                    e.llm_aspect
                FROM ZOMATO_AI.REVIEW_ENRICHED e
                JOIN MARTS.dim_restaurants r ON e.restaurant_id = r.restaurant_id
            """).fetchdf()
        except Exception:
            # Fallback to STAGING.stg_reviews if ZOMATO_AI isn't built yet
            df = con.execute("""
                SELECT 
                    e.review_id,
                    r.name AS restaurant_name,
                    r.city,
                    e.review_text,
                    e.star_rating,
                    'UNKNOWN' AS llm_sentiment,
                    'General' AS llm_aspect
                FROM STAGING.stg_reviews e
                JOIN MARTS.dim_restaurants r ON e.restaurant_id = r.restaurant_id
            """).fetchdf()
        finally:
            con.close()

        if df.empty:
            print("⚠️ No review documents found for indexing.")
            return

        self.reviews_data = df.to_dict(orient="records")
        corpus = [
            f"{r['restaurant_name']} ({r['city']}): {r['review_text']} [Aspect: {r['llm_aspect']}]"
            for r in self.reviews_data
        ]
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        print(f"🔍 Indexed {len(self.reviews_data)} customer reviews for RAG vector search.")

    def search_similar_reviews(self, query: str, top_k: int = 5):
        if not self.reviews_data or self.tfidf_matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            item = dict(self.reviews_data[idx])
            item["relevance_score"] = round(score, 4)
            results.append(item)

        return results

    def answer_query(self, user_question: str, top_k: int = 4):
        retrieved_reviews = self.search_similar_reviews(user_question, top_k=top_k)

        if not retrieved_reviews:
            return {
                "answer": "No relevant reviews found in the dataset to answer your query.",
                "sources": [],
            }

        context_blocks = []
        for i, rev in enumerate(retrieved_reviews, 1):
            context_blocks.append(
                f"Review #{i} [{rev['restaurant_name']} - {rev['city']}] ({rev['star_rating']}⭐, Sentiment: {rev['llm_sentiment']}):\n"
                f"\"{rev['review_text']}\""
            )

        context_str = "\n\n".join(context_blocks)
        system_prompt = (
            "You are an AI Analytics Assistant for Zomato food delivery. "
            "Answer the user's question strictly based on the provided retrieved customer reviews. "
            "Cite specific restaurants, ratings, and quotes when appropriate."
        )
        user_prompt = (
            f"Retrieved Customer Reviews Context:\n{context_str}\n\nUser Question: {user_question}"
        )

        llm_response = self.llm.generate_completion(system_prompt, user_prompt)

        return {"answer": llm_response, "sources": retrieved_reviews}


if __name__ == "__main__":
    rag = ReviewRAGSystem()
    result = rag.answer_query(
        "What are the main complaints regarding delivery speed and cold food?"
    )
    print("\n💬 RAG Answer:\n", result["answer"])
    print("\n📚 Sources retrieved:", len(result["sources"]))
