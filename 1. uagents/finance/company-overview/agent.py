import os
import time

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "company-overview")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None:
    raise ValueError("You need to provide an API key for Alpha Vantage.")


class CompanyOverviewRequest(Model):
    ticker: str


class CompanyOverviewResponse(Model):
    overview: dict[str, str]


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = Protocol(name="Company-Overview", version="0.1.0")


def fetch_overview_json(ticker: str) -> dict:
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

    data = response.json()

    if not data or "Symbol" not in data:
        return {"error": "No valid data found in the response."}

    return data


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


rate_limiter = RateLimiter(agent.storage)


@proto.on_message(
    CompanyOverviewRequest, replies={CompanyOverviewResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: CompanyOverviewRequest):
    ctx.logger.info(f"Received company overview request for ticker: {msg.ticker}")
    cache = ctx.storage.get(msg.ticker) or None
    if cache:
        if int(time.time()) - cache["timestamp"] < 86400:
            cache.pop("timestamp")
            ctx.logger.info(f"Sending cached data for ticker: {msg.ticker}")
            await ctx.send(sender, CompanyOverviewResponse(overview=cache))
            return

    await inner_handle_request(ctx, sender, msg)


@rate_limiter.wrap
async def inner_handle_request(ctx: Context, sender: str, msg: CompanyOverviewRequest):
    try:
        ctx.logger.info(f"Fetching company overview for ticker: {msg.ticker}")
        output_json = fetch_overview_json(msg.ticker)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    await ctx.send(sender, CompanyOverviewResponse(overview=output_json))
    if "error" not in output_json:
        output_json["timestamp"] = int(time.time())
        ctx.storage.set(msg.ticker, output_json)


agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
