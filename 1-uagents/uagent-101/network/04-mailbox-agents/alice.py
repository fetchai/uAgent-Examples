from uagents import Agent, Context, Model


class Message(Model):
    message: str


ALICE_SEED = "put_your_seed_phrase_here"

print(f"Your agent's address is: {Agent(seed=ALICE_SEED).address}")

agent = Agent(
    name="alice",
    seed=ALICE_SEED,
    mailbox=True,
)


@agent.on_message(model=Message, replies={Message})
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(sender, Message(message="Hello there bob"))


if __name__ == "__main__":
    agent.run()
