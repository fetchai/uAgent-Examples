from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model


class Message(Model):
    message: str


agent = Agent(
    name="agent 2",
    port=8001,
    seed="",
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(agent.wallet.address())


@agent.on_event("startup")
async def start(ctx: Context):
    ctx.logger.info(f"agent address is {agent.address}")


@agent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    await ctx.send(sender, Message(message="hello there"))


if __name__ == "__main__":
    agent.run()
