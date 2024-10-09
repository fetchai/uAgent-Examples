import os

from helpers import (
    NotDirectFlightException,
    create_direct_flight_from_sky_scrapper_response,
    search_flights,
)
from quota import RateLimiter
from schemas import Flight, FlightsSearchRequest, FlightsSearchResponse
from uagents import Agent, Context, Protocol
from uagents.models import ErrorMessage

FLIGHTS_SEED = os.getenv("FLIGHTS_SEED")

agent = Agent(
    name="flights_adaptor",
    seed=FLIGHTS_SEED,
)

rate_limiter = RateLimiter(storage=agent.storage)

flights_protocol = Protocol(name="Direct-Flights-Search", version="0.0.1")


@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(agent.address)


@flights_protocol.on_message(
    model=FlightsSearchRequest, replies={FlightsSearchResponse, ErrorMessage}
)
@rate_limiter.wrap
async def direct_flight_offers(ctx: Context, sender: str, msg: FlightsSearchRequest):
    """
    - Only one-way trip.
    - Only direct flights: API does not filter by number of stops

    - Returns all flights available (according to the previous constraints).
    """

    ctx.logger.info(f"Received message from {sender}")
    try:
        flights_raw = search_flights(
            logger=ctx.logger, request=msg, storage=ctx.storage
        )

        if flights_raw is None:
            await ctx.send(
                sender,
                ErrorMessage(error="Error while connecting to the external API."),
            )
            return

        flights: list[Flight] = []
        discarded_flights: int = 0
        for flight in flights_raw["itineraries"]:
            try:
                flights.append(
                    create_direct_flight_from_sky_scrapper_response(itinerary=flight)
                )
            except NotDirectFlightException:
                discarded_flights += 1

        ctx.logger.info(
            f"{len(flights_raw['itineraries'])} total flights retrieved, "
            f"{discarded_flights} discarded, sending {len(flights)} direct flights."
        )

        await ctx.send(sender, FlightsSearchResponse(flights=flights))
    except Exception as exc:
        ctx.logger.exception(exc)
        await ctx.send(sender, ErrorMessage(error="Internal server error."))


agent.include(flights_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
