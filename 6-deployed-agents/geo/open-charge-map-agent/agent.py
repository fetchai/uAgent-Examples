import os
from enum import Enum

from api_adapter import OCMAPI, Unit
from models import POI, Coordinates, POIAreaRequest, POIResponse
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "super secret seed for the open charge map agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Open Charge Map Agent")
OCM_API_KEY = os.getenv("OCM_API_KEY")
if not OCM_API_KEY:
    raise ValueError("You need to provide an API key for OpenChargeMap")

ocm_api = OCMAPI(OCM_API_KEY)


KEYWORDS = [
    "Charging Station",
    "Charging Stations",
    "Charging Station Near Me",
    "Electric Vehicle Charger",
    "EV Charger",
]

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Points-Of-Interest-Search",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@agent.on_event("startup")
async def introduce(ctx: Context):
    """
    This function is called when the agent starts up.

    If not available in the storage, the agent retrieves reference data
    from the API which includes the list of countries, operators, etc.
    """
    if not ctx.storage.has("reference_data"):
        data = ocm_api.get_reference_data()
        ctx.storage.set("reference_data", data)
        ctx.logger.info("Reference data retrieved")


def get_charger_info(
    latitude: float, longitude: float, radius: int = 1, limit: int = 100
):
    res = ocm_api.get_chargers(
        latitude=latitude,
        longitude=longitude,
        distance=radius,
        distanceunit=Unit.KM,
        maxresults=limit,
        compact=False,
    )
    pois = []
    if res:
        for charger in res:
            pois.append(
                POI(
                    placekey=charger["UUID"] or "",
                    location_name=charger["AddressInfo"]["Title"]
                    if charger["AddressInfo"]
                    else "",
                    brands=[charger["OperatorInfo"]["Title"]]
                    if charger["OperatorInfo"]
                    else [],
                    top_category="Automotive Services",
                    sub_category="Charging Station",
                    # naics_code=336320,  # check https://www.naics.com/search/
                    location=Coordinates(
                        latitude=charger["AddressInfo"]["Latitude"],
                        longitude=charger["AddressInfo"]["Longitude"],
                    ),
                    address=charger["AddressInfo"]["AddressLine1"]
                    if charger["AddressInfo"]
                    else "",
                    city=charger["AddressInfo"]["Town"]
                    if charger["AddressInfo"]
                    else "",
                    region=charger["AddressInfo"]["StateOrProvince"]
                    if charger["AddressInfo"]
                    else "",
                    postal_code=charger["AddressInfo"]["Postcode"]
                    if charger["AddressInfo"]
                    else "",
                    iso_country_code=charger["AddressInfo"]["Country"]["ISOCode"]
                    if charger["AddressInfo"]
                    else "",
                    metadata={  # add more metadata if necessary
                        "UsageCost": charger["UsageCost"] or "",
                        "status": charger["StatusType"]["Title"]
                        if charger["StatusType"]
                        else "",
                    },
                )
            )
    return pois


@proto.on_message(POIAreaRequest, replies={POIResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: POIAreaRequest):
    if not any(query in msg.query_string for query in KEYWORDS):
        return

    try:
        pois = get_charger_info(
            latitude=msg.loc_search.latitude,
            longitude=msg.loc_search.longitude,
            radius=msg.radius_in_m / 1000,
            limit=msg.limit,
        )
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return

    if not pois:
        await ctx.send(sender, ErrorMessage(error="No results found"))
        return

    await ctx.send(
        sender,
        POIResponse(
            loc_search=Coordinates(
                latitude=msg.loc_search.latitude,
                longitude=msg.loc_search.longitude,
            ),
            radius_in_m=msg.radius_in_m,
            data_origin=agent.name,
            data=pois,
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
