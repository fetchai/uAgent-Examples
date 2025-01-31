from uagents import Context


@agent.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f"hello, my name is {agent.name}")
