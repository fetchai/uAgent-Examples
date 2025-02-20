from uagents import Agent, Bureau, Context, Model


class Message(Model):
    message: str


alice = Agent(name="alice", seed="alice recovery phrase")
bob = Agent(name="bob", seed="bob recovery phrase")


@alice.on_interval(period=3.0)
async def send_message(ctx: Context):
    await ctx.send(bob.address, Message(message="hello there bob"))


@bob.on_message(model=Message)
async def bob_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(alice.address, Message(message="hello there alice"))


@alice.on_message(model=Message)
async def alice_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")


bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

if __name__ == "__main__":
    bureau.run()
