import os

from ai import get_completion
from ai_engine import UAgentResponse, UAgentResponseType
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage, Field

AGENT_SEED = os.getenv("AGENT_SEED")


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
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

rate_limiter = RateLimiter(agent.storage)

translate_proto = Protocol(name="OpenAI-Translation", version="0.1.0")
ai_engine_translate_proto = Protocol(
    name="AIEngine-OpenAI-Translation", version="0.1.0"
)


async def translate(
    ctx: Context, sender: str, request: TranslationRequest
) -> str | None:
    if not rate_limiter.add_request(sender):
        await ctx.send(
            sender, ErrorMessage(error="Rate limit exceeded. Try again later.")
        )
        return None
    if request.language_in == "Detect":
        context = f"Detect the language of the provided text and translate it to {request.language_out}"
    else:
        context = f"Translate the provided text from {request.language_in} to {request.language_out}"
    response = get_completion(context=context, prompt=request.text)
    return response


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(f"Agent address: {agent.address}")


@translate_proto.on_message(TranslationRequest, replies={TranslationResponse})
@rate_limiter.wrap
async def handle_translation(ctx: Context, sender: str, msg: TranslationRequest):
    response = await translate(ctx, sender, msg)
    if response:
        await ctx.send(sender, TranslationResponse(text=response))


@ai_engine_translate_proto.on_message(
    AIEngineTranslationRequest, replies={UAgentResponse}
)
async def handle_ai_engine_translation(
    ctx: Context, sender: str, msg: TranslationRequest
):
    response = await translate(ctx, sender, msg)
    if response:
        await ctx.send(
            sender, UAgentResponse(type=UAgentResponseType.FINAL, message=response)
        )


agent.include(translate_proto, publish_manifest=True)
agent.include(ai_engine_translate_proto, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
