import os

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("You need to provide an API key for Google Geocode")


class GeolocationRequest(Model):
    address: str


class GeolocationResponse(Model):
    latitude: float
    longitude: float


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

rate_limiter = RateLimiter(agent.storage)

proto = Protocol(name="Geolocation-Protocol", version="0.1.0")


async def find_coordinates(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_API_KEY}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        data = response.json()

        # Check if results are available in the response
        if "results" in data:
            return {
                "latitude": data["results"][0]["geometry"]["location"]["lat"],
                "longitude": data["results"][0]["geometry"]["location"]["lng"],
            }

        return {"error": "Address not found in the response."}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request failed: {str(req_err)}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {str(err)}"}


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


@proto.on_message(GeolocationRequest, replies={GeolocationResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: GeolocationRequest):
    ctx.logger.info(f"Received Address resolution request: {msg.address}")
    cache = ctx.storage.get(msg.address) or None
    if cache:
        await ctx.send(sender, GeolocationResponse(**cache))
        return

    await inner_handle_request(ctx, sender, msg)


@rate_limiter.wrap
async def inner_handle_request(ctx: Context, sender: str, msg: GeolocationRequest):
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

if __name__ == "__main__":
    agent.run()
