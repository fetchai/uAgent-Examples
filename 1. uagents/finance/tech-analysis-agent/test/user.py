from uagents import Agent, Context, Model


class TechAnalysisRequest(Model):
    ticker: str


class IndicatorSignal(Model):
    indicator: str
    latest_value: float
    previous_value: float
    signal: str


class TechAnalysisResponse(Model):
    symbol: str
    analysis: list[IndicatorSignal]


agent = Agent()


AI_AGENT_ADDRESS = "agent1qgeg7agnrg4agztkefvllk0gdc0gzrge62zsy9f5ysj3nemzptyyu59q3ju"

ticker = "AMZN"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, TechAnalysisRequest(ticker=ticker))
    ctx.logger.info(f"Sent prompt to AI agent: {ticker}")


@agent.on_message(TechAnalysisResponse)
async def handle_response(ctx: Context, sender: str, msg: TechAnalysisResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.analysis)


if __name__ == "__main__":
    agent.run()
