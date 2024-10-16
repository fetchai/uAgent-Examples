from uagents import Agent, Context

agent = Agent(name="agent", seed="alice recovery phrase")


@agent.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {agent.name}')


if __name__ == "__main__":
    agent.run()