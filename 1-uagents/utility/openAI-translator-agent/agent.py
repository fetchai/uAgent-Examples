import os
from enum import Enum

from ai import get_completion
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage, Field

AGENT_SEED = os.getenv("AGENT_SEED", "openai-translator-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "OpenAI Translator Agent")


class TranslationRequest(Model):
    text: str = Field(description="The text to translate")
    language_out: str = Field(description="The output language")
    language_in: str = Field(description="The input language", default="Detect")


class AIEngineTranslationRequest(TranslationRequest):
    pass


class TranslationResponse(Model):
    text: str = Field(description="The translated text")


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="OpenAI-Translation",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(TranslationRequest, replies={TranslationResponse, ErrorMessage})
async def handle_translation(ctx: Context, sender: str, msg: TranslationRequest):
    if msg.language_in == "Detect":
        context = f"Detect the language of the provided text and translate it to {msg.language_out}"
    else:
        context = (
            f"Translate the provided text from {msg.language_in} to {msg.language_out}"
        )
    response = get_completion(context=context, prompt=msg.text)
    if not response:
        await ctx.send(ErrorMessage(error="Error translating text."))
        return
    await ctx.send(sender, TranslationResponse(text=response))


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
