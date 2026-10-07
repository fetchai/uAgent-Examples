import os

from agent_health import openai_models
from ai import MODEL_ENGINE, OPENAI_API_KEY, get_completion
from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "finance_qa_agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Finance Q&A Agent")

PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


class FinanceQA(Model):
    question: str


class Response(Model):
    text: str


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Finance-QA",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(model=FinanceQA, replies={Response, ErrorMessage})
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
