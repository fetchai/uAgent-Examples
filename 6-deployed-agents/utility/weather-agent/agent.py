import os
from enum import Enum

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "weather-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Weather Agent")
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
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Weather-Agent-Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


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


@proto.on_message(
    WeatherForecastRequest, replies={WeatherForecastResponse, ErrorMessage}
)
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
