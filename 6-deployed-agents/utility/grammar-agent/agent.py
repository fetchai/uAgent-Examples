import os
from enum import Enum

from chat_proto import chat_proto
from grammar import check_grammar
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "grammar-check-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Grammar Agent")


class GrammarCheckRequest(Model):
    text: str


class GrammarCheckResponse(Model):
    corrected_text: str


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


grammar_check_protocol = QuotaProtocol(
    storage_reference=agent.storage,
    name="Grammar Check Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@grammar_check_protocol.on_message(
    model=GrammarCheckRequest, replies=GrammarCheckResponse
)
async def on_message(ctx: Context, sender: str, msg: GrammarCheckRequest):
    ctx.logger.info(f"Received text: {msg.text}")
    try:
        result = check_grammar(msg.text)

        if "error" in result:
            await ctx.send(sender, ErrorMessage(error=result["error"]))
            return

    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))
        return
    await ctx.send(sender, GrammarCheckResponse(corrected_text=result["text"]))


agent.include(grammar_check_protocol)
agent.include(chat_proto, publish_manifest=True)


### Health check related code
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
