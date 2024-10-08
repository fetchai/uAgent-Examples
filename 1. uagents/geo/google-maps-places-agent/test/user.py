from typing import Any, Optional

from uagents import Model


class Coordinates(Model):
    latitude: float
    longitude: float


class POIAreaRequest(Model):
    loc_search: Coordinates
    radius_in_m: int
    limit: int = 20
    query_string: str
    filter: dict[str, Any] = {}


class POI(Model):
    placekey: str
    location_name: str
    brands: Optional[list[str]] = None
    top_category: Optional[str] = None
    sub_category: Optional[str] = None
    location: Coordinates
    address: str
    city: str
    region: Optional[str] = None
    postal_code: str
    iso_country_code: str
    metadata: Optional[dict[str, Any]] = None


class POIResponse(Model):
    loc_search: Coordinates
    radius_in_m: int
    data_origin: str
    data: list[POI]


from uagents import Agent, Context

agent = Agent()


GMAPS_AGENT_ADDRESS = (
    "agent1qwuqm9r60x89e38h4eletms0sdrdzhvuj5qe8s6kfg60uwtmsgdtwxa5u9u"
)

example_request = POIAreaRequest(
    loc_search=Coordinates(latitude=48.140505822096365, longitude=11.559987118245475),
    radius_in_m=500,
    query_string="coffee shop",
)


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    await ctx.send(GMAPS_AGENT_ADDRESS, example_request)
    ctx.logger.info(f"Sent request to  agent: {example_request}")


@agent.on_message(POIResponse)
async def handle_response(ctx: Context, sender: str, msg: POIResponse):
    ctx.logger.info(f"Received {len(msg.data)} pois from: {sender}")
    for place in msg.data:
        ctx.logger.info(place.location_name)


if __name__ == "__main__":
    agent.run()
