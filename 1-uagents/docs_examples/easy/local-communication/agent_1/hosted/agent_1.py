from uagents import Context, Model

# NOTE: Run agent1.py before running agent2.py


class Message(Model):
    message: str


@agent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    # send the response
    await ctx.send(sender, Message(message="Hello there alice."))
