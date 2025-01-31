import os
from enum import Enum

from ai import get_completion
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "finance_qa_agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Finance Q&A Agent")

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


class FinanceQA(Model):
    question: str


class Response(Model):
    text: str


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Finance-QA",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(model=FinanceQA, replies={Response, ErrorMessage})
async def finance_qa_query(ctx: Context, sender: str, msg: FinanceQA):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")

    try:
        response = get_completion(prompt=msg.question)
        result = response.strip()
    except Exception as exc:
        ctx.logger.warning(exc)
        await ctx.send(sender, ErrorMessage(error=str(exc)))
        return

    await ctx.send(sender, Response(text=result))


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
