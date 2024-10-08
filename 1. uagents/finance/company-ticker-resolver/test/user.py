from uagents import Agent, Context, Model


class TickerRequest(Model):
    company: str


class TickerResponse(Model):
    ticker: str


agent = Agent()


AI_AGENT_ADDRESS = "agent1qdx686denardc7uaf7jwmfq8vlv25llgve66gykm2f4n9xew6kpywtp7cg2"

company = "Amazon"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, TickerRequest(company=company))
    ctx.logger.info(f"Sent prompt to AI agent: {company}")


@agent.on_message(TickerResponse)
async def handle_response(ctx: Context, sender: str, msg: TickerResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.ticker)


if __name__ == "__main__":
    agent.run()
