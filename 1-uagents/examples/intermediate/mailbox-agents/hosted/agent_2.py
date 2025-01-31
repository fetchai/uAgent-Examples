from uagents import Context, Model


class Message(Model):
    message: str


# Copy ALICE_ADDRESS generated in agent_1.py
ALICE_ADDRESS = "agent1qfa53drat8rzau90u4494gx5mhj3v87tm4t5cuzkd7gkegxcm5vx5pku7kf"


@agent.on_interval(period=2.0)
async def send_message(ctx: Context):
    ctx.logger.info("Sending message to alice")
    await ctx.send(ALICE_ADDRESS, Message(message="hello there alice"))


@agent.on_message(model=Message, replies=set())
async def on_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
