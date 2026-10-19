import os

from agent_health import asi1_chat
from ai import ASI1_API_KEY, ASI1_URL, MODEL_NAME, generate_image
from models import ImageRequest, ImageResponse
from protocols import chat_proto, store_image
from uagents import Agent, Context
from uagents.experimental.health import HealthProtocol, cached_check
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "asi1-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "ASI1 Agent")


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

agent.include(chat_proto, publish_manifest=True)


async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: asi1_chat(
            ASI1_API_KEY,
            model=MODEL_NAME,
            base_url=ASI1_URL,
        ),
        cache_key="health_asi1_api",
    )


health_protocol = HealthProtocol(
    agent_name=agent.name,
    check=agent_is_healthy,
)
agent.include(health_protocol, publish_manifest=True)


@agent.on_message(ImageRequest, replies={ImageResponse, ErrorMessage})
async def handle_image_request(
    ctx: Context,
    sender: str,
    msg: ImageRequest,
) -> None:
    try:
        image = generate_image(msg.prompt)
        _, uri, _ = store_image(ctx, sender, image)
        await ctx.send(sender, ImageResponse(image_url=uri))
    except Exception as error:
        ctx.logger.error(f"Image generation failed: {error}")
        await ctx.send(sender, ErrorMessage(error=str(error)))


if __name__ == "__main__":
    agent.run()
