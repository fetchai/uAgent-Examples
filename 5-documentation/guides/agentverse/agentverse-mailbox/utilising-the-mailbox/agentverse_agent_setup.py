from uagents import Agent, Context, Model


class Message(Model):
    message: str


# Copy ALICE_ADDRESS generated in mailbox_agent.py
ALICE_ADDRESS = "agent1qfa53drat8rzau90u4494gx5mhj3v87tm4t5cuzkd7gkegxcm5vx5pku7kf"

# Generate a second seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now let's create the Agentverse agent
agent = Agent(
    name="bob",
    seed=SEED_PHRASE,
    endpoint="http://127.0.0.1:8001/submit",
)


@agent.on_interval(period=2.0)
async def send_message(ctx: Context):
    ctx.logger.info("Sending message to alice")
    await ctx.send(ALICE_ADDRESS, Message(message="hello there alice"))


@agent.on_message(model=Message, replies=set())
async def on_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")


if __name__ == "__main__":
    agent.run()