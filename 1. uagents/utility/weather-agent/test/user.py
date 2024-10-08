from uagents import Agent, Context, Model


class WeatherForecastRequest(Model):
    location: str


class WeatherForecastResponse(Model):
    location: str
    temp: float
    condition: str
    humidity: float
    wind_speed: float


agent = Agent()

AI_AGENT_ADDRESS = "agent1qvazkaq9h68nahpuu3dludwv0rl44sgwdjzpknm6wmkk4ahd4mtgsg7psj0"

location = "London"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, WeatherForecastRequest(location=location))
    ctx.logger.info(f"Sent request to weather agent: {location}")


@agent.on_message(WeatherForecastResponse)
async def handle_response(ctx: Context, sender: str, msg: WeatherForecastResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg)


if __name__ == "__main__":
    agent.run()
