import json
import os
from typing import Any

from agent_health import gemini_models
from ai import GEMINI_API_KEY, MODEL_ENGINE, get_completion, get_text_completion
from chat_proto import chat_proto
from uagents import Agent, Context, Model
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import AccessControlList, QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "gemini-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Google Gemini Agent")
BYPASS_RATE_LIMIT = set([item for item in os.getenv("BYPASS_RATE_LIMIT", "").split(",") if item])


class TextPrompt(Model):
    text: str


class CodePrompt(Model):
    text: str


class TextResponse(Model):
    text: str


class CodeResponse(Model):
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

text_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Text-Response",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6, acl=acl),
)

code_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Code-Generator",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6, acl=acl),
)

struct_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="LLM-Structured-Response",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6, acl=acl),
)


@text_proto.on_message(TextPrompt, replies={TextResponse, ErrorMessage})
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


@code_proto.on_message(CodePrompt, replies={CodeResponse, ErrorMessage})
async def handle_codegen_request(ctx: Context, sender: str, msg: CodePrompt):
    response = get_text_completion(msg.text, True)
    if response is None:
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
    await ctx.send(sender, CodeResponse(text=response))


@struct_proto.on_message(
    StructuredOutputPrompt, replies={StructuredOutputResponse, ErrorMessage}
)
async def handle_structured_request(
    ctx: Context, sender: str, msg: StructuredOutputPrompt
):
    response = get_completion([{"type": "text", "text": msg.prompt}], response_schema=msg.output_schema)
    if response is None:
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
    await ctx.send(sender, StructuredOutputResponse(output=json.loads(response)))


agent.include(text_proto, publish_manifest=True)
agent.include(code_proto, publish_manifest=True)
agent.include(struct_proto, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: gemini_models(GEMINI_API_KEY, model=MODEL_ENGINE),
    )








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
