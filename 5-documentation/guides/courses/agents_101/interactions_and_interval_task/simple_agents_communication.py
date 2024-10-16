from uagents import Agent, Context, Bureau

alice = Agent(name="alice", seed="alice recovery phrase")
bob = Agent(name="bob", seed="bob recovery phrase")


@alice.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'Hello, my name is {alice.name}')


@bob.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'Hello, my name is {bob.name}')


bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

if __name__ == "__main__":
    bureau.run()