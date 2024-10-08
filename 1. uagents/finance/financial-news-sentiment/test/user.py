from uagents import Agent, Context, Model


class FinancialSentimentRequest(Model):
    ticker: str


class NewsSentiment(Model):
    title: str
    url: str
    summary: str
    overall_sentiment_label: str


class FinancialSentimentResponse(Model):
    summary: list[NewsSentiment]


agent = Agent()


AI_AGENT_ADDRESS = "agent1q06j56crj8rcu38fsrajcnph0xgwhkevm9wwea4kh0fjl0pz3hgfk7g6hqg"

ticker = "AAPL"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, FinancialSentimentRequest(ticker=ticker))
    ctx.logger.info(f"Sent prompt to AI agent: {ticker}")


@agent.on_message(FinancialSentimentResponse)
async def handle_response(ctx: Context, sender: str, msg: FinancialSentimentResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.summary)


if __name__ == "__main__":
    agent.run()
