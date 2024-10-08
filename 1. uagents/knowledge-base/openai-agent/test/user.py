from uagents import Agent, Context, Model


class ContextPrompt(Model):
    context: str
    text: str


class Response(Model):
    text: str


agent = Agent(
    name="user",
    endpoint="http://localhost:8000/submit",
)


AI_AGENT_ADDRESS = "agent1q09xe6rk6lqcnchdrkcn92ma4wlmjyty3v2yzxlxdx4jylq2fcfa2rv458x"


code = """
    def do_something():
        for i in range(10)
            pass
    """

prompt = ContextPrompt(
    context="Find and fix the bug in the provided code snippet",
    text=code,
)


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, prompt)


@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")


if __name__ == "__main__":
    agent.run()
