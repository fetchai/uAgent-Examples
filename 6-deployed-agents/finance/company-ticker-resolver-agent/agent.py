import asyncio
import os
import time

import requests
from agent_health import alpha_vantage, asi1_chat
from openai import OpenAI
from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "ticker-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Company Ticker Resolver Agent")

ASI1_API_KEY = os.getenv("ASI1_API_KEY", "")
ASI1_BASE_URL = os.getenv("ASI1_BASE_URL", "https://api.asi1.ai/v1")
ASI1_MODEL = os.getenv("ASI1_MODEL", "asi1")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None or not ASI1_API_KEY:
    raise ValueError("You need to provide API keys for Alpha Vantage and ASI:One.")

asi1_client = OpenAI(api_key=ASI1_API_KEY, base_url=ASI1_BASE_URL)


class TickerRequest(Model):
    company: str


class TickerResponse(Model):
    ticker: str


PORT = 8000
agent = ChatAgent(
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
    Fetches ticker symbols for a given company name and verifies the most relevant
    one using ASI:One.

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

    # Verify the correct ticker using ASI:One.
    response = asi1_client.chat.completions.create(
        model=ASI1_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Select the ticker that best matches the company name from the "
                    "provided candidates. Return exactly one candidate ticker and "
                    "nothing else."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Company: {company_name}\nCandidate tickers: {ticker_list}"
                ),
            },
        ],
        max_tokens=16,
    )

    verified_ticker = (response.choices[0].message.content or "").strip().upper()
    matching_ticker = next(
        (ticker for ticker in ticker_list if ticker.upper() == verified_ticker),
        None,
    )
    if matching_ticker is None:
        raise ValueError(f"ASI:One returned an unexpected ticker: {verified_ticker!r}")
    return matching_ticker


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
async def agent_is_healthy(ctx: Context) -> bool:
    asi1_ok, alpha_vantage_ok = await asyncio.gather(
        cached_check(
            ctx,
            lambda: asi1_chat(
                ASI1_API_KEY,
                model=ASI1_MODEL,
                base_url=ASI1_BASE_URL,
            ),
            cache_key="health_asi1_api",
        ),
        cached_check(
            ctx,
            lambda: alpha_vantage(ALPHAVANTAGE_API_KEY),
            cache_key="health_alpha_vantage",
        ),
    )
    return asi1_ok and alpha_vantage_ok


health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
