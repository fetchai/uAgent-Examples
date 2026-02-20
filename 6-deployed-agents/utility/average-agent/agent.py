import os
import statistics
from enum import Enum

from average import get_statistics
from messages import Prompt, Response
from uagents import Agent, Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "average-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Average Agent")


PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage, name="Average-Statistics", version="0.1.0"
)


@proto.on_message(Prompt, replies={Response, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: Prompt):
    try:
        math = get_statistics(msg)
    except statistics.StatisticsError as s_err:
        await ctx.send(sender, ErrorMessage(error=str(s_err)))
        return
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    await ctx.send(sender, math)


agent.include(proto, publish_manifest=True)


# Health Check code
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
    await ctx.send(
        sender, AgentHealth(agent_name=AGENT_NAME, status=HealthStatus.HEALTHY)
    )


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
