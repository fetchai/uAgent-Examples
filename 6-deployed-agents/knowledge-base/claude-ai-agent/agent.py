import os
from enum import Enum
from typing import Any

from agent_health import anthropic_models, cached_check
from uagents import Agent, Context, Model
from uagents.experimental.quota import AccessControlList, QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from ai import ANTHROPIC_API_KEY, MODEL_ENGINE, get_structured_response, get_text_completion
from chat_proto import chat_proto

AGENT_SEED = os.getenv("AGENT_SEED", "claude-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Claude.ai Agent")
BYPASS_RATE_LIMIT = set(
    [item for item in os.getenv("BYPASS_RATE_LIMIT", "").split(",") if item]
)


class TextPrompt(Model):
    text: str


class TextResponse(Model):
    text: str


class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    output: dict[str, Any]


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

acl = AccessControlList(
    default=False,
    bypass_rate_limit=BYPASS_RATE_LIMIT,
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Text-Response",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6, acl=acl),
)

struct_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Structured-Response",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6, acl=acl),
)


@proto.on_message(TextPrompt, replies={TextResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: TextPrompt):
    response = get_text_completion(msg.text)
    if response is None:
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
    await ctx.send(sender, TextResponse(text=response))


@struct_proto.on_message(
    StructuredOutputPrompt, replies={StructuredOutputResponse, ErrorMessage}
)
async def handle_structured_request(
    ctx: Context, sender: str, msg: StructuredOutputPrompt
):
    response = get_structured_response(msg.prompt, msg.output_schema)
    if response is None:
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
    await ctx.send(sender, StructuredOutputResponse(output=response))


agent.include(proto, publish_manifest=True)
agent.include(struct_proto, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: anthropic_models(ANTHROPIC_API_KEY, model=MODEL_ENGINE),
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
