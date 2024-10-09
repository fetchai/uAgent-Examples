import os

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")

HF_BEARER_TOKEN = os.getenv("HF_BEARER_TOKEN")
if not HF_BEARER_TOKEN:
    raise ValueError("You need to provide a Hugging Face API token.")

PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


class FinancialSentimentRequest(Model):
    text: str


class FinancialSentimentResponse(Model):
    positive: float
    neutral: float
    negative: float


proto = Protocol(name="Financial-Sentiment", version="0.1.0")


async def get_finbert_sentiment(text) -> FinancialSentimentResponse:
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": f"Bearer {HF_BEARER_TOKEN}"}

    payload = {
        "inputs": text,
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    data = response.json()

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


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


rate_limiter = RateLimiter(agent.storage)


@proto.on_message(
    FinancialSentimentRequest, replies={FinancialSentimentResponse, ErrorMessage}
)
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: FinancialSentimentRequest):
    ctx.logger.info(f"Got request to get finbert sentiment for the text {msg.text}")
    try:
        sentiment = await get_finbert_sentiment(msg.text)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return

    await ctx.send(sender, sentiment)


agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
