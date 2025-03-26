import os
from enum import Enum

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "geolocation-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Geolocation Agent")

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

if OPENCAGE_API_KEY is None:
    raise ValueError("You need to provide an API key for Open Cage.")


class GeolocationRequest(Model):
    address: str


class GeolocationResponse(Model):
    latitude: float
    longitude: float


PORT = 8000
agent = Agent(
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


async def find_coordinates(address) -> dict:
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {"q": address, "key": OPENCAGE_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        data = response.json()

        # Check if results are available in the response
        if "results" in data:
            return {
                "latitude": data["results"][0]["geometry"]["lat"],
                "longitude": data["results"][0]["geometry"]["lng"],
            }

        return {"error": "Address not found in the response."}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request failed: {str(req_err)}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {str(err)}"}


@proto.on_message(GeolocationRequest, replies={GeolocationResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: GeolocationRequest):
    ctx.logger.info(f"Received Address resolution request: {msg.address}")
    cache = ctx.storage.get(msg.address) or None
    if cache:
        await ctx.send(sender, GeolocationResponse(**cache))
        return

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
    ctx.storage.set(msg.address, coordinates)


agent.include(proto, publish_manifest=True)


### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.

    For example, check if the agent can connect to a third party API,
    check if the agent has enough resources, etc.
    """
    condition = True  # TODO: logic here
    return bool(condition)


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
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
