import os
from enum import Enum

from agent_health import cached_check, openai_chat
from ai import ASI1_API_KEY, ASI1_URL, MODEL_NAME
from protocols import chat_proto
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol

AGENT_SEED = os.getenv("AGENT_SEED", "asi1-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "ASI1-Mini Agent")


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

agent.include(chat_proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: openai_chat(
            ASI1_API_KEY,
            model=MODEL_NAME,
            base_url=ASI1_URL,
        ),
    )


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
        if await agent_is_healthy(ctx):
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
