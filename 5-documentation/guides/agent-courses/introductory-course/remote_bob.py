from uagents import Agent, Context, Model


class Message(Model):
    message: str


agent = Agent(
    name="bob",
    port=8001,
    seed="bob secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)


@agent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    await ctx.send(sender, Message(message="hello there alice"))


if __name__ == "__main__":
    agent.run()