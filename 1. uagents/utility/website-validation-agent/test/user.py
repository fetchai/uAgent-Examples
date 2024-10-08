from uagents import Agent, Context, Model

agent = Agent()

AI_AGENT_ADDRESS = "agent1qfxl5f2dmywt8q3c98fxl50tfhrz6g3mcyl7hp3p5l8fpctc7w45zss2r7n"


class WebsiteValidationInput(Model):
    website_url: str


class GrammarMistake(Model):
    error: str
    solution: str


class WebsiteValidationResponse(Model):
    invalid_links: list[str]
    grammar_mistakes: list[GrammarMistake]


website = "https://fetch.ai"


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    """Send the prompt to the AI agent on startup."""
    await ctx.send(AI_AGENT_ADDRESS, WebsiteValidationInput(website_url=website))
    ctx.logger.info(f"Sent prompt to AI agent: {website}")


@agent.on_message(WebsiteValidationResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteValidationResponse):
    """Do something with the response."""
    ctx.logger.info(f"Received response from: {sender}:")
    ctx.logger.info(msg)


if __name__ == "__main__":
    agent.run()
