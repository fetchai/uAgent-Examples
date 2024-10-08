import os

from uagents import Agent, Context, Model


class WebSearchRequest(Model):
    query: str


class WebSearchResult(Model):
    title: str
    url: str
    content: str


class WebSearchResponse(Model):
    query: str
    results: list[WebSearchResult]


agent = Agent()

AI_AGENT_ADDRESS = "agent1qgzp6fglff9zrtt09ra0r0qwk5jhh0t0tuxpjl0jvqq384hdfly4zfvl7jt"

prompt = "What is a Fetch.ai agent?"


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    """Send the prompt to the AI agent on startup."""
    await ctx.send(AI_AGENT_ADDRESS, WebSearchRequest(query=prompt))
    ctx.logger.info(f"Sent prompt to AI agent: {prompt}")


@agent.on_message(WebSearchResponse)
async def handle_response(ctx: Context, sender: str, msg: WebSearchResponse):
    """Do something with the response."""
    ctx.logger.info(f"Received response from: {sender}")
    ctx.logger.info(msg.results)


if __name__ == "__main__":
    agent.run()
