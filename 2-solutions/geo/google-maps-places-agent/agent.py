"""
This agent connects the Google Places API to the point_of_interest protocol.
Note that the googlemaps module supports all of the Google Maps APIS
(including geocoding or directions) so this agent could easily be extended
to support other protocols as well.
"""

import os
from enum import Enum

from client import Client
from communication import POIAreaRequest, POIResponse
from logic import find_pois
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_NAME = os.getenv("AGENT_NAME", "Google Maps Places Agent")

agent = Agent(
    name=AGENT_NAME,
    seed="Google Places Agent secret very crypto much safe 3",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Points-Of-Interest-Search",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("You need to provide an API key for Google Places")

gmaps = Client(GOOGLE_API_KEY)


@proto.on_message(model=POIAreaRequest, replies={POIResponse, ErrorMessage})
async def handle_poi_request(ctx: Context, sender: str, msg: POIAreaRequest):
    ctx.logger.info(f"Got request from {sender} for: {msg.query_string}")

    response = await find_pois(
        client=gmaps,
        ctx=ctx,
        query_string=msg.query_string,
        lat=msg.loc_search.latitude,
        lng=msg.loc_search.longitude,
        radius_in_m=msg.radius_in_m,
        limit=msg.limit,
    )

    ctx.logger.info(f"returning: len{response} places")
    await ctx.send(
        sender,
        POIResponse(
            loc_search=msg.loc_search,
            radius_in_m=msg.radius_in_m,
            data_origin="Google Places API",
            data=response,
        ),
    )


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
