import json
import os
from enum import Enum
from typing import Any

from ai import get_text_completion
from chat_proto import chat_proto
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit, AccessControlList
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "openai-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "OpenAI Agent")
BYPASS_RATE_LIMIT = set([item for item in os.getenv("BYPASS_RATE_LIMIT", "").split(",") if item])

class ContextPrompt(Model):
    context: str
    text: str


class Response(Model):
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
    name="LLM-Context-Response",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6, acl=acl),
)

struct_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Structured-Response",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6, acl=acl),
)


@proto.on_message(ContextPrompt, replies={Response, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: ContextPrompt):
    response = get_text_completion(context=msg.context, prompt=msg.text)
    await ctx.send(sender, Response(text=response))


@struct_proto.on_message(
    StructuredOutputPrompt, replies={StructuredOutputResponse, ErrorMessage}
)
async def handle_structured_request(
    ctx: Context, sender: str, msg: StructuredOutputPrompt
):
    response = get_text_completion(
        context="", prompt=msg.prompt, response_schema=msg.output_schema
    )
    await ctx.send(sender, StructuredOutputResponse(output=json.loads(response)))


agent.include(proto, publish_manifest=True)
agent.include(struct_proto, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)


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
