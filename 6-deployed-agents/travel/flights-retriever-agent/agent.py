"""
Agent information:
---
Mainly relies on https://rapidapi.com/apiheya/api/sky-scrapper.

We should switch to another API that better fits our needs.
We can not filter as much as we should, therefore the request takes longer and we have to filtered in here.
Inefficient and a hogwash.

Missing:
- A plain basic 'limit' query param (it is in v2 but just not working)
- Filter by 'stops'
- Request round-trips (not a big deal).
"""

import os
from enum import Enum

from helpers import (
    NotDirectFlightException,
    create_direct_flight_from_sky_scrapper_response,
    search_flights,
)
from schemas import Flight, FlightsSearchRequest, FlightsSearchResponse
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto

FLIGHTS_SEED = os.getenv("FLIGHTS_SEED", "flights adaptor really secret phrase :)))")
AGENT_NAME = os.getenv("AGENT_NAME", "Flights Retriever Agent")

agent = Agent(name=AGENT_NAME, seed=FLIGHTS_SEED)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Direct-Flights-Search",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(
    model=FlightsSearchRequest, replies={FlightsSearchResponse, ErrorMessage}
)
async def direct_flight_offers(ctx: Context, sender: str, msg: FlightsSearchRequest):
    """
    - Only one-way trip.
    - Only direct flights: API does not filter by number of stops; so we do it.
    ->  Reason: We are looking for atomicity for chaining and composability, so at the moment we are
        aiming for the simpler case.

        In case to accept rounds trips we should return a list of chained flights.
        Same with travels that are not direct.

        The chaining could be in a different service/protocol of the agent or just parametrized in here,
        since we already receive the necessary data in the current request.
    ---

    - Returns all flights available (according to the previous constraints).
    """

    ctx.logger.info(f"Received message from {sender}")
    try:
        flights_raw = search_flights(
            logger=ctx.logger, request=msg, storage=ctx.storage
        )

        # TODO: Rework in general all the exception and cases. In the current state it is impossible to
        #  provide any valid/useful feedback to the client or handle any non-successful casuistic.
        if flights_raw is None:
            # TODO: Manage the exception, that None is artificial and inappropriate.
            # Reply if some problem at connecting requesting to the external API.
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


agent.include(proto, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)


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
