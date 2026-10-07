import os

from agent_health import openai_models
from ai import MODEL_ENGINE, OPENAI_API_KEY, get_completion
from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage, Field

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
agent = ChatAgent(
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


async def translate(
    ctx: Context, sender: str, request: TranslationRequest
) -> str | None:
    if request.language_in == "Detect":
        context = f"Detect the language of the provided text and translate it to {request.language_out}"
    else:
        context = f"Translate the provided text from {request.language_in} to {request.language_out}"
    response = get_completion(context=context, prompt=request.text)
    return response


@proto.on_message(TranslationRequest, replies={TranslationResponse, ErrorMessage})
async def handle_translation(ctx: Context, sender: str, msg: TranslationRequest):
    response = await translate(ctx, sender, msg)
    if not response:
        await ctx.send(ErrorMessage(error="Error translating text."))
        return
    await ctx.send(sender, TranslationResponse(text=response))


agent.include(proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: openai_models(OPENAI_API_KEY, model=MODEL_ENGINE),
    )








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
