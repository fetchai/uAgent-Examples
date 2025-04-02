import os
import time
from enum import Enum

import openai
import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "ticker-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Company Ticker Resolver Agent")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None or OPENAI_API_KEY is None:
    raise ValueError("You need to provide an API keys for Alpha Vantage and OpenAi.")


class TickerRequest(Model):
    company: str


class TickerResponse(Model):
    ticker: str


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Company-Ticker-Resolver",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def get_verified_ticker(company_name) -> str:
    """
    Fetches ticker symbols for a given company name and verifies the most relevant one using OpenAI's GPT-4 model.

    Args:
        company_name (str): The name of the company to search for.

    Returns:
        str: The verified ticker symbol.
    """
    # Fetch ticker symbols using Alpha Vantage API
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={ALPHAVANTAGE_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        raise
    except requests.exceptions.RequestException as e:
        raise ValueError("Request exception happened.") from e

    data = response.json()

    # Collect the first 5 ticker symbols
    ticker_list = []
    for i in range(min(5, len(data.get("bestMatches", [])))):
        ticker = data.get("bestMatches")[i].get("1. symbol")
        ticker_list.append(ticker)

    if not ticker_list:
        return "No ticker symbols found."

    # Verify the correct ticker using OpenAI's gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an agent to provide tickers for a given company name. You will get 5 best matching tickers in a list and you have to verify which ticker is right. Just respond always with a ticker. For example: TSLA for Tesla, AAPL for Apple, etc. If the list is empty check ticker for {company_name } and return ticker",
            },
            {
                "role": "user",
                "content": f"ticker_list : {str(ticker_list)} company name : {company_name}",
            },
        ],
    )

    # Extract and return the verified ticker
    verified_ticker = response.choices[0].message.content
    return verified_ticker


@proto.on_message(TickerRequest, replies={TickerResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: TickerRequest):
    ctx.logger.info(f"Received Ticker request for company: {msg.company}")
    cache = ctx.storage.get(msg.company)
    if cache:
        if int(time.time()) - cache["timestamp"] < 86400:
            ctx.logger.info(f"Sending cached data for company: {msg.company}")
            await ctx.send(sender, TickerResponse(ticker=cache["ticker"]))
            return

    try:
        ticker = get_verified_ticker(msg.company)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    await ctx.send(sender, TickerResponse(ticker=ticker))
    ctx.logger.info(f"Ticker for company {msg.company} sent.")
    to_store = {"ticker": ticker, "timestamp": int(time.time())}
    ctx.storage.set(msg.company, to_store)


agent.include(proto, publish_manifest=True)


# Health check related code
def agent_is_healthy():
    return True


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
        agent_is_healthy()
        status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
