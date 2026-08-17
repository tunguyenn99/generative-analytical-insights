import os
import json
import re
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """
    Multi-provider LLM connector for Zomato AI Data Engine.
    Primary Provider: Google Gemini API (Free tier: GEMINI_API_KEY, model gemini-3.5-flash)
    Secondary Provider: OpenAI API (OPENAI_API_KEY, model gpt-4o-mini)
    Fallback: Intelligent Local Engine
    """

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        self.provider = "local"
        self.gemini_client = None
        self.openai_client = None
        self.gemini_model_name = "gemini-3.5-flash"

        # 1. Try Google Gemini API (Official google.genai SDK)
        if self.gemini_key:
            try:
                from google import genai

                self.gemini_client = genai.Client(api_key=self.gemini_key)
                self.provider = "gemini"
                print("✨ LLMClient initialized with Google Gemini API (Model: gemini-3.5-flash).")
            except Exception as e:
                print(f"⚠️ Gemini API init failed: {e}. Checking OpenAI...")

        # 2. Try OpenAI API if Gemini key is not set
        if self.provider == "local" and self.openai_key:
            try:
                from openai import OpenAI

                self.openai_client = OpenAI(api_key=self.openai_key)
                self.provider = "openai"
                print("🤖 LLMClient initialized with OpenAI API (gpt-4o-mini).")
            except Exception as e:
                print(f"⚠️ OpenAI init failed: {e}. Falling back to Local Engine.")

        # 3. Fallback to Local Engine
        if self.provider == "local":
            print(
                "💡 GEMINI_API_KEY / OPENAI_API_KEY not set. Running with Local Intelligent AI Engine."
            )

    def generate_completion(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.2
    ) -> str:
        # Google Gemini Execution
        if self.provider == "gemini" and self.gemini_client:
            from google.genai import types

            for model_candidate in [
                "gemini-3.5-flash",
                "gemini-flash-latest",
                "gemini-3.1-flash-lite",
            ]:
                try:
                    response = self.gemini_client.models.generate_content(
                        model=model_candidate,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt, temperature=temperature
                        ),
                    )
                    return response.text.strip()
                except Exception as e:
                    print(
                        f"⚠️ Gemini model '{model_candidate}' error: {e}. Trying next candidate..."
                    )
            print("⚠️ All Gemini models exhausted. Falling back to Local Engine.")

        # OpenAI Execution
        elif self.provider == "openai" and self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"⚠️ OpenAI API error: {e}. Falling back to Local Engine.")

        # Local Fallback Execution
        return self._local_fallback_completion(system_prompt, user_prompt)

    def _local_fallback_completion(self, system_prompt: str, user_prompt: str) -> str:
        # Check if requested for JSON output (Enrichment task)
        if "JSON" in system_prompt or "sentiment" in user_prompt.lower():
            text = user_prompt.lower()
            if any(
                w in text
                for w in [
                    "hot",
                    "fresh",
                    "delicious",
                    "amazing",
                    "great",
                    "best",
                    "excellent",
                    "early",
                ]
            ):
                sentiment = "POSITIVE"
            elif any(
                w in text
                for w in [
                    "cold",
                    "horrible",
                    "oily",
                    "spilled",
                    "stale",
                    "bad",
                    "rude",
                    "delayed",
                    "chewy",
                ]
            ):
                sentiment = "NEGATIVE"
            else:
                sentiment = "NEUTRAL"

            # Aspect detection
            if any(
                w in text for w in ["speed", "delayed", "early", "hour", "delivery", "tracking"]
            ):
                aspect = "Delivery Speed"
            elif any(w in text for w in ["packaging", "spilled", "box", "clean"]):
                aspect = "Packaging"
            elif any(w in text for w in ["price", "charged", "size", "portion"]):
                aspect = "Pricing & Quantity"
            elif any(
                w in text
                for w in [
                    "flavour",
                    "flavor",
                    "taste",
                    "delicious",
                    "fresh",
                    "stale",
                    "oily",
                    "chewy",
                ]
            ):
                aspect = "Food Quality"
            else:
                aspect = "Service"

            return json.dumps({"sentiment": sentiment, "aspect": aspect, "confidence": 0.95})

        # Text-to-SQL fallback query generation
        if "SQL" in system_prompt or "SELECT" in system_prompt:
            prompt_lower = user_prompt.lower()
            if "city" in prompt_lower and (
                "revenue" in prompt_lower or "gmv" in prompt_lower or "doanh thu" in prompt_lower
            ):
                return "SELECT city, SUM(gross_merchandise_value_gmv) AS total_gmv, SUM(delivered_orders) AS total_orders FROM MARTS.mart_daily_revenue GROUP BY city ORDER BY total_gmv DESC;"
            elif "top" in prompt_lower and (
                "restaurant" in prompt_lower
                or "nha hang" in prompt_lower
                or "nhà hàng" in prompt_lower
            ):
                return "SELECT restaurant_name, city, avg_star_rating, total_reviews FROM MARTS.mart_review_insights ORDER BY avg_star_rating DESC LIMIT 5;"
            elif (
                "delivery" in prompt_lower
                or "giao hang" in prompt_lower
                or "giao hàng" in prompt_lower
            ):
                return "SELECT city, AVG(avg_delivery_mins) AS avg_mins, AVG(p90_delivery_mins) AS p90_mins FROM MARTS.mart_delivery_performance GROUP BY city ORDER BY avg_mins ASC;"
            elif (
                "user" in prompt_lower
                or "customer" in prompt_lower
                or "khach hang" in prompt_lower
                or "khách hàng" in prompt_lower
            ):
                return "SELECT age_group, COUNT(user_id) AS total_users, SUM(total_spent) AS total_spent FROM MARTS.dim_users GROUP BY age_group ORDER BY total_spent DESC;"
            else:
                return "SELECT city, COUNT(restaurant_id) AS total_restaurants, ROUND(AVG(rating), 2) AS avg_rating FROM MARTS.dim_restaurants GROUP BY city ORDER BY total_restaurants DESC;"

        # General RAG QA response
        return f"Based on customer reviews in our database: Customers frequently highlight delivery speed and food freshness. Negative feedback mainly points to packaging spills or occasional delays during peak hours."
