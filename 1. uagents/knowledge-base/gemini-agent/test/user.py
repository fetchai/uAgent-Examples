from uagents import Agent, Context, Model


class TextPrompt(Model):
    text: str


class CodePrompt(Model):
    text: str


class TextResponse(Model):
    text: str


class Response(Model):
    text: str


agent = Agent()


AI_AGENT_ADDRESS = "agent1qfcg434qzr8xkf2c8ej08w634rgcqh7fkz94c73ljalh3lffp6y4qg99569"

prompts = [
    "What is the square root of 123456789?",
    "What is the tower of Hanoi problem? Write a recursive solution in Python.",
]


@agent.on_event("startup")
async def send_message(ctx: Context):
    for prompt in prompts:
        await ctx.send(
            AI_AGENT_ADDRESS,
            CodePrompt(
                code_generation=True,
                text=prompt,
            ),
        )
        ctx.logger.info(f"Sent prompt to AI agent: {prompt}")


@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()
