from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model

class Message(Model):
    message: str

slaanesh = Agent(
    name="slaanesh",
    port=8001,
    seed="slaanesh secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(slaanesh.wallet.address())

@slaanesh.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    await ctx.send(sender, Message(message="hello there sigmar"))

if __name__ == "__main__":
    slaanesh.run()