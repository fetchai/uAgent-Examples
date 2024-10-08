import os

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "weather-agent")
API_KEY = os.getenv("WEATHERAPI_KEY")


class WeatherForecastRequest(Model):
    location: str


class WeatherForecastResponse(Model):
    location: str
    temp: float
    condition: str
    humidity: float
    wind_speed: float


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

weather_proto = Protocol(name="Weather-Agent-Protocol", version="0.1.0")

rate_limiter = RateLimiter(agent.storage)


async def get_weather(location) -> dict:
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=no"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

    weather_data = response.json()

    if "error" in weather_data:
        return {"error": weather_data["error"]["message"]}

    return {
        "location": location,
        "temp": weather_data["current"]["temp_c"],
        "condition": weather_data["current"]["condition"]["text"],
        "humidity": weather_data["current"]["humidity"],
        "wind_speed": weather_data["current"]["wind_kph"],
    }


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


@weather_proto.on_message(
    WeatherForecastRequest, replies={WeatherForecastResponse, ErrorMessage}
)
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: WeatherForecastRequest):
    ctx.logger.info(f"Received Address: {msg.location}")
    try:
        weather_forecast = await get_weather(msg.location)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))

    if "error" in weather_forecast:
        await ctx.send(sender, ErrorMessage(error=weather_forecast["error"]))
        return
    await ctx.send(sender, WeatherForecastResponse(**weather_forecast))


agent.include(weather_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
