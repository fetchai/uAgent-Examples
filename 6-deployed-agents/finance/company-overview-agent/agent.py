import os
import time
from enum import Enum

from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from functions import CompanyOverviewResponse, CompanyOverviewRequest, fetch_overview_json

AGENT_SEED = os.getenv("AGENT_SEED", "company-overview")
AGENT_NAME = os.getenv("AGENT_NAME", "Company Overview Agent")


PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Company-Overview",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(
    CompanyOverviewRequest, replies={CompanyOverviewResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: CompanyOverviewRequest):
    ctx.logger.info(f"Received company overview request for ticker: {msg.ticker}")
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
