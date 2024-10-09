import os

from ai import get_completion
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")

PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


class FinanceQA(Model):
    question: str


class Response(Model):
    text: str


finance_qa_protocol = Protocol(name="Finance-Questions-&-Answers", version="0.1.0")

rate_limiter = RateLimiter(agent.storage)


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(agent.address)


@finance_qa_protocol.on_message(model=FinanceQA, replies={Response, ErrorMessage})
@rate_limiter.wrap
async def finance_qa_query(ctx: Context, sender: str, msg: FinanceQA):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")

    try:
        response = get_completion(prompt=msg.question)
        result = response.strip()
    except Exception as exc:
        ctx.logger.warning(exc)
        await ctx.send(sender, ErrorMessage(error=str(exc)))
        return

    await ctx.send(sender, Response(text=result))


agent.include(finance_qa_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
