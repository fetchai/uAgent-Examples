import os
from enum import Enum

from ai import get_completion
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "gemini-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Google Gemini Agent")


class TextPrompt(Model):
    text: str


class CodePrompt(Model):
    text: str


class TextResponse(Model):
    text: str


class Response(Model):
    text: str


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

text_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Text-Response",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)
code_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Code-Generator",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@text_proto.on_message(TextPrompt, replies={Response, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: TextPrompt):
    response = get_completion(msg.text, False)
    if response is None:
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
    await ctx.send(sender, Response(text=response))


@code_proto.on_message(CodePrompt, replies={Response, ErrorMessage})
async def handle_codegen_request(ctx: Context, sender: str, msg: CodePrompt):
    response = get_completion(msg.text, True)
    if response is None:
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
    await ctx.send(sender, Response(text=response))


agent.include(text_proto, publish_manifest=True)
agent.include(code_proto, publish_manifest=True)


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
