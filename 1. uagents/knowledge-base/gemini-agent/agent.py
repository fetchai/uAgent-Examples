import os

from ai import get_completion
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "gemini-test-agent")


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
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

text_proto = Protocol(name="LLM-Text-Response", version="0.1.0")
code_proto = Protocol(name="LLM-Code-Generator", version="0.1.0")


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


rate_limiter = RateLimiter(agent.storage)


@text_proto.on_message(TextPrompt, replies={Response, ErrorMessage})
@rate_limiter.wrap
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
@rate_limiter.wrap
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

if __name__ == "__main__":
    agent.run()
