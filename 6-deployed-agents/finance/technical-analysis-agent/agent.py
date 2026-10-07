import os
from typing import List

from agent_health import alpha_vantage
from functions import ALPHAVANTAGE_API_KEY, IndicatorSignal, analyze_stock
from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "tech-analysis-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Technical Analysis Agent")


class TechAnalysisRequest(Model):
    ticker: str


class TechAnalysisResponse(Model):
    symbol: str
    analysis: List[IndicatorSignal]


PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Technical-Analysis",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(TechAnalysisRequest, replies={TechAnalysisResponse, ErrorMessage})
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


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: alpha_vantage(ALPHAVANTAGE_API_KEY),
    )








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
