import os

from agent_health import google_geocoding
from coordinates import (
    GOOGLE_API_KEY,
    GeolocationRequest,
    GeolocationResponse,
    find_coordinates,
)
from uagents import Context
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

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








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
