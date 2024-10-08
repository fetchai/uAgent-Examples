from uagents import Agent, Context, Model


class CompanyOverviewRequest(Model):
    ticker: str


class CompanyOverviewResponse(Model):
    overview: dict[str, str]


agent = Agent()


AI_AGENT_ADDRESS = "agent1qvfwtemphj4443sprwhqk0hywskp2txscuzayc6ymem3990ca7ehjcwsygh"

ticker = "AMZN"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, CompanyOverviewRequest(ticker=ticker))
    ctx.logger.info(f"Sent prompt to AI agent: {ticker}")


@agent.on_message(CompanyOverviewResponse)
async def handle_response(ctx: Context, sender: str, msg: CompanyOverviewResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.overview)


if __name__ == "__main__":
    agent.run()
