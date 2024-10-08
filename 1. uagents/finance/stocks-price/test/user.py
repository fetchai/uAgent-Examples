from uagents import Agent, Context, Model


class StockPriceRequest(Model):
    ticker: str


class StockPriceResponse(Model):
    text: str


agent = Agent()


AI_AGENT_ADDRESS = "agent1qft487pu5ashl3ex9h8rzfy5pyvl4vjry8lk47hdq94fl7gqc6w4x2378gp"

prompts = [
    "AMZN",
    "AAPL",
]


@agent.on_event("startup")
async def send_message(ctx: Context):
    for prompt in prompts:
        await ctx.send(AI_AGENT_ADDRESS, StockPriceRequest(ticker=prompt))
        ctx.logger.info(f"Sent prompt to agent: {prompt}")


@agent.on_message(StockPriceResponse)
async def handle_response(ctx: Context, sender: str, msg: StockPriceResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()
