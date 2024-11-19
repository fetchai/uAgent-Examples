from uagents import Agent, Context, Model

class Message(Model):
    message: str

RECIPIENT_ADDRESS = "agent1qvm7v76zs6w2x90xvq99yc5xh7c2thjtm44zc09me556zxnra627gkf4zum"

sigmar = Agent(
    name="sigmar",
    port=8000,
    seed="sigmar secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

@sigmar.on_interval(period=2.0)
async def send_message(ctx: Context):
    await ctx.send(RECIPIENT_ADDRESS, Message(message="hello there slaanesh"))

@sigmar.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

if __name__ == "__main__":
    sigmar.run()