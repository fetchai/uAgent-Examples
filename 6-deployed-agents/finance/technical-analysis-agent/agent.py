import os
from enum import Enum
from typing import List

from functions import IndicatorSignal, analyze_stock
from uagents import Agent, Context, Model
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
agent = Agent(
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
