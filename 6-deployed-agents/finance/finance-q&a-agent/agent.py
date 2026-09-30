import os
from enum import Enum

from agent_health import cached_check, openai_models
from ai import MODEL_ENGINE, OPENAI_API_KEY, get_completion
from uagents import Agent, Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "finance_qa_agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Finance Q&A Agent")

PORT = 8000
agent = ChatAgent(
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
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: openai_models(OPENAI_API_KEY, model=MODEL_ENGINE),
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
