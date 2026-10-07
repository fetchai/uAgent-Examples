import os

from agent_health import openai_chat
from ai import ASI1_API_KEY, ASI1_URL, MODEL_NAME
from protocols import chat_proto
from uagents import Agent, Context
from uagents.experimental.health import HealthProtocol, cached_check

AGENT_SEED = os.getenv("AGENT_SEED", "asi1-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "ASI1-Mini Agent")


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

agent.include(chat_proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: openai_chat(
            ASI1_API_KEY,
            model=MODEL_NAME,
            base_url=ASI1_URL,
        ),
    )








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
