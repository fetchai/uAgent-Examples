from typing import Optional

from uagents import Agent, Context, Model


class GeoParkingRequest(Model):
    latitude: float
    longitude: float
    radius_in_meters: int
    max_results: int


class CarPark(Model):
    name: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float


class GeoParkingResponse(Model):
    carparks: list[CarPark]


agent = Agent()


AI_AGENT_ADDRESS = "agent1qdvtet4wpgq02sv2n0hvgv5xr99sfmzny9jkg4hamn5zq6fpseq46g9vhzp"

latitude = 35.7174747
longitude = 139.7941792
radius = 100
max_results = 5


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(
        AI_AGENT_ADDRESS,
        GeoParkingRequest(
            latitude=latitude,
            longitude=longitude,
            radius_in_meters=radius,
            max_results=max_results,
        ),
    )


@agent.on_message(GeoParkingResponse)
async def handle_response(ctx: Context, sender: str, msg: GeoParkingResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.carparks)


if __name__ == "__main__":
    agent.run()
