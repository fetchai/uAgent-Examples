from uagents import Agent, Context, Model
from uagents.models import Field


class TranslationRequest(Model):
    text: str = Field(description="The text to translate")
    language_out: str = Field(description="The output language")
    language_in: str = Field(description="The input language", default="Detect")


class TranslationResponse(Model):
    text: str = Field(description="The translated text")


agent = Agent()


AI_AGENT_ADDRESS = "agent1qtgce4lemgh3gprtn648dte75earej6exz292vl6qek9xhfetgzgsy8peun"


request = TranslationRequest(
    text="I need some donuts",
    language_in="english",
    language_out="dutch",
)


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, request)


@agent.on_message(TranslationResponse)
async def handle_response(ctx: Context, sender: str, msg: TranslationResponse):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")


if __name__ == "__main__":
    agent.run()
