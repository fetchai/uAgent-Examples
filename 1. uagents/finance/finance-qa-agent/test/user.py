from uagents import Agent, Context, Model

agent = Agent()

AI_AGENT_ADDRESS = "agent1qfha7nyvvxsdqlaljy32vmx50h6c4hssxtx5yxywdxe4fcw62u766xdn5x7"


class FinanceQA(Model):
    question: str


class Response(Model):
    text: str


question = FinanceQA(question="What is a stock?")


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    """Send the prompt to the AI agent on startup."""
    await ctx.send(AI_AGENT_ADDRESS, question)
    ctx.logger.info(f"Sent question to Finance QA agent: {question.question}")


@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    """Do something with the response."""
    ctx.logger.info(f"Received response from: {sender}: {msg.text}")


if __name__ == "__main__":
    agent.run()
