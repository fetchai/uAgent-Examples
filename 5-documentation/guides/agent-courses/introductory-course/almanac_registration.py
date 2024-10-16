from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Protocol

agent = Agent(
    name="alice",
    port=8000,
    seed="alice secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(agent.wallet.address())


@agent.on_interval(period=3)
async def hi(ctx: Context):
    ctx.logger.info(f"Hello")


agent.run()