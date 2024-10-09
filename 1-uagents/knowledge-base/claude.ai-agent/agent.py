import os

from ai import get_completion
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")


class TextPrompt(Model):
    text: str


class TextResponse(Model):
    text: str


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = Protocol(name="LLM-Text-Response", version="0.1.0")


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


rate_limiter = RateLimiter(agent.storage)


@proto.on_message(TextPrompt, replies={TextResponse, ErrorMessage})
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: TextPrompt):
    response = get_completion(msg.text)
    if response is None:
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
    await ctx.send(sender, TextResponse(text=response))


agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
