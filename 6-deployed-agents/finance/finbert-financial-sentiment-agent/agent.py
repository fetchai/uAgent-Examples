import os
from enum import Enum

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "<finbert-sentiment-agent>")
AGENT_NAME = os.getenv("AGENT_NAME", "Finbert Financial Sentiment Agent")

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("You need to provide a Hugging Face API token.")

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
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


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Financial-Sentiment",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


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


@proto.on_message(
    FinancialSentimentRequest, replies={FinancialSentimentResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: FinancialSentimentRequest):
    ctx.logger.info(f"Got request to get finbert sentiment from {sender}")
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


### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.

    For example, check if the agent can connect to a third party API,
    check if the agent has enough resources, etc.
    """
    condition = True  # TODO: logic here
    return bool(condition)


class HealthCheck(Model):
    pass


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class AgentHealth(Model):
    agent_name: str
    status: HealthStatus


health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)


@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
