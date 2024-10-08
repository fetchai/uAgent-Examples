from uagents import Agent, Context, Model


class TextPrompt(Model):
    text: str


class TextResponse(Model):
    text: str


agent = Agent()


AI_AGENT_ADDRESS = "agent1q2hc6jmrqr9ncxm69u0ss4rlhqq65z2fwt2xkm9hugwxx66t3jllxwtceav"

prompts = [
    "How is the weather in London today?",
    "Compare the inflation rates of the past years in various European countries.",
]


@agent.on_event("startup")
async def send_message(ctx: Context):
    for prompt in prompts:
        await ctx.send(AI_AGENT_ADDRESS, TextPrompt(text=prompt))
        ctx.logger.info(f"[Sent prompt to AI agent]: {prompt}")


@agent.on_message(TextResponse)
async def handle_response(ctx: Context, sender: str, msg: TextResponse):
    ctx.logger.info(f"[Received response from ...{sender[-8:]}]:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()
