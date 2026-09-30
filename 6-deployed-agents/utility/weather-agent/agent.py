import os
from enum import Enum

from agent_health import cached_check, weather_api
from uagents import Agent, Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from weather import API_KEY, get_weather, WeatherForecastRequest, WeatherForecastResponse

AGENT_SEED = os.getenv("AGENT_SEED", "weather-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Weather Agent")


PORT = 8000
agent = ChatAgent(
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
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(
        ctx,
        lambda: weather_api(API_KEY),
        cache_key="weather_api_health",
    )


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
        if await agent_is_healthy(ctx):
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
