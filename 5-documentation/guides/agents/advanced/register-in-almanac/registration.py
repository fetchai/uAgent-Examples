from uagents import Agent, Context, Protocol

agent = Agent(
    name="alice",
    port=8000,
    seed="alice secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_interval(period=3)
async def hi(ctx: Context):
    ctx.logger.info(f"Hello")

agent.run()