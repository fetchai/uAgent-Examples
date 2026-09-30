import os
from enum import Enum

from agent_health import cached_check, google_geocoding
from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from coordinates import (
    GOOGLE_API_KEY,
    GeolocationRequest,
    GeolocationResponse,
    find_coordinates,
)

AGENT_SEED = os.getenv("AGENT_SEED", "google-geolocation-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Google API Geolocation Agent")


PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Geolocation-Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(GeolocationRequest, replies={GeolocationResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: GeolocationRequest):
    ctx.logger.info(f"Received Address resolution request: {msg.address}")
    try:
        coordinates = await find_coordinates(msg.address)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))
        return

    if "error" in coordinates:
        await ctx.send(sender, ErrorMessage(error=coordinates["error"]))
        return

    await ctx.send(sender, GeolocationResponse(**coordinates))


agent.include(proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: google_geocoding(GOOGLE_API_KEY),
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


if __name__ == "__main__":
    agent.run()
