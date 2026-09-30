import os
from enum import Enum

from agent_health import cached_check, openai_models
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, external_storage
from models import (
    OPENAI_API_KEY,
    OPENAI_IMAGE_MODEL,
    ImageRequest,
    ImageResponse,
    generate_image,
)

AGENT_SEED = os.getenv("AGENT_SEED", "image-generator-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Image Generator Agent")

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Image-Generator",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)

@proto.on_message(ImageRequest, replies={ImageResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: ImageRequest):
    ctx.logger.info(f"Received Image request")
    try:
        image = generate_image(msg.image_description)
        asset_id = external_storage.create_asset(
            name=f"img_{ctx.session}",
            content=image,
            mime_type="image/png",
        )
        external_storage.set_permissions(asset_id=asset_id, agent_address=sender)
        image_url = f"agent-storage://{external_storage.storage_url}/{asset_id}"

    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    await ctx.send(sender, ImageResponse(image_url=image_url))


agent.include(proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: openai_models(OPENAI_API_KEY, model=OPENAI_IMAGE_MODEL),
    )


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
        if await agent_is_healthy(ctx):
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
