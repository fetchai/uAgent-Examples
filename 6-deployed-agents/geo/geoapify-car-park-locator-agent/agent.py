import os
from typing import List, Optional

import requests
from agent_health import geoapify
from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "<geoapi-car-park-agent>")
AGENT_NAME = os.getenv("AGENT_NAME", "Geoapify Car Park Locator Agent")
GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
URL = "https://api.geoapify.com/v2/places"

if GEOAPIFY_KEY is None:
    raise ValueError("You need to provide an API key for Geoapify.")


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
    carparks: List[CarPark]


PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="CarParking-Search",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def format_data(api_response) -> list[CarPark]:
    formatted_data = []
    if "features" not in api_response:
        return formatted_data
    for place in api_response["features"]:
        formatted_data.append(
            CarPark(
                name=place["properties"].get("name"),
                address=place["properties"].get("formatted"),
                latitude=place["geometry"]["coordinates"][1],
                longitude=place["geometry"]["coordinates"][0],
            )
        )
    return formatted_data


def get_data(latitude, longitude, radius, max_results) -> dict:
    """
    Retrieves data from the Geoapify API for Car Parking.
    Args:
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.
        miles_radius (float): The radius in miles for searching car parks.
    Returns:
        list or None: A list of Car Parking data if successful, or None if the request fails.
    """
    params = {
        "categories": "parking.cars",
        "filter": f"circle:{longitude},{latitude},{radius}",
        "bias": f"proximity:{longitude},{latitude}",
        "limit": max_results,
        "apiKey": GEOAPIFY_KEY,
    }
    try:
        response = requests.get(url=URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.Timeout as e:
        print(
            "Request timed out. Check your internet connection or try again later.",
            str(e),
        )
    except requests.RequestException as e:
        print("An error occurred during the request:", str(e))
    except Exception as e:
        print("An unexpected error occurred:", str(e))
    return {}


@proto.on_message(model=GeoParkingRequest, replies={GeoParkingResponse, ErrorMessage})
async def on_message(ctx: Context, sender: str, msg: GeoParkingRequest):
    try:
        response = get_data(
            msg.latitude, msg.longitude, msg.radius_in_meters, msg.max_results
        )
        formatted_data = format_data(response)

        if not formatted_data:
            await ctx.send(sender, ErrorMessage(error="No car parks found."))
            return
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))
        return

    await ctx.send(sender, GeoParkingResponse(carparks=formatted_data))


agent.include(proto, publish_manifest=True)


### Health check related code
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: geoapify(GEOAPIFY_KEY),
    )








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
