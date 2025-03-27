import os
import requests
from uagents import Model

class FinancialSentimentRequest(Model):
    text: str


class FinancialSentimentResponse(Model):
    positive: float
    neutral: float
    negative: float

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    raise ValueError("You need to provide a Hugging Face API token.")


async def get_finbert_sentiment(text) -> FinancialSentimentResponse:
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    payload = {
        "inputs": text,
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    data = response.json()
    if "error" in data:
        raise ValueError(data["error"])

    positive, neutral, negative = 0.0, 0.0, 0.0
    for entry in data[0]:
        if entry["label"] == "positive":
            positive = entry["score"]
        elif entry["label"] == "neutral":
            neutral = entry["score"]
        elif entry["label"] == "negative":
            negative = entry["score"]

    return FinancialSentimentResponse(
        positive=positive, neutral=neutral, negative=negative
    )