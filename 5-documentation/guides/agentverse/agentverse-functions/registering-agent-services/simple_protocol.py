from uagents import Context, Model, Protocol
from ai_engine import UAgentResponse, UAgentResponseType

simples = Protocol(name="simples", version="1.1")


class Request(Model):
    message: str


@simples.on_message(model=Request, replies={UAgentResponse})
async def handle_message(ctx: Context, sender: str, msg: Request):
    await ctx.send(sender, UAgentResponse(message="0", type=UAgentResponseType.FINAL))