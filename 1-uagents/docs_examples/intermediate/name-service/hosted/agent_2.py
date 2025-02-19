from uagents import Context, Model


class Message(Model):
    message: str


@agent.on_interval(period=5)
async def alice_interval_handler(ctx: Context):
    bob_name = "bob-0.agent"
    ctx.logger.info(f"Sending message to {bob_name}...")
    await ctx.send(bob_name, Message(message="Hello there bob."))
