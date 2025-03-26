import os
from enum import Enum
from typing import List

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "tech-sentiment-agent-alphavantage123")
AGENT_NAME = os.getenv("AGENT_NAME", "Financial News Sentiment Agent")

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None:
    raise ValueError("You need to provide an API key for Alpha Vantage.")


class FinancialNewsSentimentRequest(Model):
    ticker: str


class NewsSentiment(Model):
    title: str
    url: str
    summary: str
    overall_sentiment_label: str


class FinancialNewsSentimentResponse(Model):
    summary: List[NewsSentiment]


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Financial-News-Sentiment",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def fetch_news_sentiment_json(ticker) -> list[NewsSentiment]:
    """
    Fetches news sentiment data for a given ticker symbol and returns it as a JSON object.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        str: A JSON-formatted string containing the news title, URL, and overall sentiment label.
    """
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHAVANTAGE_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        raise
    except requests.exceptions.RequestException as e:
        raise ValueError("Request exception happened.") from e

    data = response.json()

    if not data or "feed" not in data:
        raise ValueError("No valid data found in the response.")

    news_list = []

    for article in data["feed"]:
        news_list.append(
            NewsSentiment(
                title=article.get("title"),
                url=article.get("url"),
                summary=article.get("summary"),
                overall_sentiment_label=article.get("overall_sentiment_label"),
            )
        )

    return news_list


@proto.on_message(
    FinancialNewsSentimentRequest,
    replies={FinancialNewsSentimentResponse, ErrorMessage},
)
async def handle_request(ctx: Context, sender: str, msg: FinancialNewsSentimentRequest):
    ctx.logger.info(
        f"Received news sentiment analysis request for ticker: {msg.ticker}"
    )
    try:
        output = fetch_news_sentiment_json(msg.ticker)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error=f"An error occurred while processing the request: {err}."
            ),
        )
        return
    await ctx.send(sender, FinancialNewsSentimentResponse(summary=output))
    ctx.logger.info(f"News sentiment analysis for ticker {msg.ticker} sent.")


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
