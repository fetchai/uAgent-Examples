from ai_engine import UAgentResponse, UAgentResponseType

class Request(Model):
    message: str

@agent.on_message(model=UAgentResponse)
async def handle_message(ctx: Context, sender: str, msg: UAgentResponse):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

@agent.on_interval(period=3.0)
async def send_message(ctx: Context):
    await ctx.send('YOUR AGENT ADDRESS', Request(message="hello there bob"))
    ctx.logger.info(f"Message has been sent to basically zero")