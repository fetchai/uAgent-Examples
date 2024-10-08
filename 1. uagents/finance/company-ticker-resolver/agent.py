import os
import time

import openai
import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "ticker-agent")
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
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = Protocol(name="Company-Ticker-Resolver", version="0.1.0")


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


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


rate_limiter = RateLimiter(agent.storage)


@proto.on_message(TickerRequest, replies={TickerResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: TickerRequest):
    ctx.logger.info(f"Received Ticker request for company: {msg.company}")
    cache = ctx.storage.get(msg.company)
    if cache:
        if int(time.time()) - cache["timestamp"] < 86400:
            ctx.logger.info(f"Sending cached data for company: {msg.company}")
            await ctx.send(sender, TickerResponse(overview=cache["ticker"]))
            return

    await inner_handle_request(ctx, sender, msg)


@rate_limiter.wrap
async def inner_handle_request(ctx: Context, sender: str, msg: TickerRequest):
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

if __name__ == "__main__":
    agent.run()
