import os

from functions import IndicatorSignal, analyze_stock
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")


class TechAnalysisRequest(Model):
    ticker: str


class TechAnalysisResponse(Model):
    symbol: str
    analysis: list[IndicatorSignal]


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

rate_limiter = RateLimiter(agent.storage)

proto = Protocol(name="Technical-Analysis", version="0.1.0")


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


@proto.on_message(TechAnalysisRequest, replies={TechAnalysisResponse, ErrorMessage})
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: TechAnalysisRequest):
    ctx.logger.info(f"Received technical analysis request for ticker: {msg.ticker}")
    try:
        output = analyze_stock(msg.ticker)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    if not output:
        await ctx.send(
            sender,
            ErrorMessage(
                error="No technical analysis data available for the requested ticker."
            ),
        )
        return
    await ctx.send(sender, TechAnalysisResponse(symbol=msg.ticker, analysis=output))


agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
