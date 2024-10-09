"""
This agent connects the Google Places API to the point_of_interest protocol.
Note that the googlemaps module supports all of the Google Maps APIS
(including geocoding or directions) so this agent could easily be extended
to support other protocols as well.
"""

import os

from client import Client
from communication import POIAreaRequest, POIResponse
from logic import find_pois
from quota import RateLimiter
from uagents import Agent, Context, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")

agent = Agent(
    name="GooglePlacesAgent",
    seed=AGENT_SEED,
)

proto = Protocol(name="Points-Of-Interest-Search", version="0.1.0")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("You need to provide an API key for Google Places")

gmaps = Client(GOOGLE_API_KEY)

rate_limiter = RateLimiter(agent.storage)


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


@proto.on_message(model=POIAreaRequest, replies={POIResponse, ErrorMessage})
@rate_limiter.wrap
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

if __name__ == "__main__":
    agent.run()
