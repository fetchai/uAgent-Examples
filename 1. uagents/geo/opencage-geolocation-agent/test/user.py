from uagents import Agent, Context, Model


class GeolocationRequest(Model):
    address: str


class GeolocationResponse(Model):
    latitude: float
    longitude: float


agent = Agent()


AI_AGENT_ADDRESS = "agent1qfxdgszajw64694ut0kwwfkerel2s5p8j9saw7evp2sgcqe86hqswy34gg3"


address = "Kings Cross Station, London"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, GeolocationRequest(address=address))
    ctx.logger.info(f"Sent address to Geolocation agent: {address}")


@agent.on_message(GeolocationResponse)
async def handle_response(ctx: Context, sender: str, msg: GeolocationResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")


if __name__ == "__main__":
    agent.run()
