import os

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None:
    raise ValueError("You need to provide an API key for Alpha Vantage.")


class FinancialSentimentRequest(Model):
    ticker: str


class NewsSentiment(Model):
    title: str
    url: str
    summary: str
    overall_sentiment_label: str


class FinancialSentimentResponse(Model):
    summary: list[NewsSentiment]


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = Protocol(name="Financial-Sentiment", version="0.1.0")


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


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


rate_limiter = RateLimiter(agent.storage)


@proto.on_message(
    FinancialSentimentRequest, replies={FinancialSentimentResponse, ErrorMessage}
)
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: FinancialSentimentRequest):
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
    await ctx.send(sender, FinancialSentimentResponse(summary=output))
    ctx.logger.info(f"News sentiment analysis for ticker {msg.ticker} sent.")


agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
