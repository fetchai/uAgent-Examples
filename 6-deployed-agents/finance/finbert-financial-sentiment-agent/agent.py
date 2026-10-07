import os

from agent_health import huggingface_account
from finbert import (
    HUGGINGFACE_API_KEY,
    FinancialSentimentRequest,
    FinancialSentimentResponse,
    get_finbert_sentiment,
)
from uagents import Context
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "<finbert-sentiment-agent>")
AGENT_NAME = os.getenv("AGENT_NAME", "Finbert Financial Sentiment Agent")

PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Financial-Sentiment",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(
    FinancialSentimentRequest, replies={FinancialSentimentResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: FinancialSentimentRequest):
    ctx.logger.info(f"Got request to get finbert sentiment from {sender}")
    try:
        sentiment = await get_finbert_sentiment(msg.text)
    except Exception as err:
        ctx.logger.error(f"FinBERT provider request failed: {err}")
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
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: huggingface_account(HUGGINGFACE_API_KEY),
    )








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
