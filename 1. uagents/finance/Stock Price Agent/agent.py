import os

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None:
    raise ValueError("You need to provide an API key for Alpha Vantage.")


class StockPriceRequest(Model):
    ticker: str


class StockPriceResponse(Model):
    text: str


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = Protocol("Stocks-Price", version="0.1.0")

rate_limiter = RateLimiter(agent.storage)


async def get_stock_price(symbol) -> str:
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHAVANTAGE_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

    data = response.json()

    if "Time Series (1min)" in data:
        latest_time = sorted(data["Time Series (1min)"].keys())[0]
        latest_data = data["Time Series (1min)"][latest_time]
        current_price = latest_data["1. open"]
        return current_price

    return "Error: Unable to fetch stock price."


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


@proto.on_message(StockPriceRequest, replies={StockPriceResponse, ErrorMessage})
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: StockPriceRequest):
    ctx.logger.info(f"Received Price request for ticker : {msg.ticker}")
    try:
        price = await get_stock_price(msg.ticker)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    await ctx.send(sender, StockPriceResponse(text=price))


agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
