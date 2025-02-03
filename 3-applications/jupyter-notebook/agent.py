from uagents import Agent, Context, Model

agent = Agent(
    name="jupyter_test_agent",
    seed="AGENTcwefewfwerfg_2_SEED",
    endpoint=["http://127.0.0.1:8009/submit"],
    port=8009,
)

SECOND_AGENT_ADDRESS = (
    "agent1qdwgulp6q2jw93u3yhh9teectdjaxvrmmwl900cs33vz4skkawstg3q74n4"
)


class ResponseMessage(Model):
    text: str


@agent.on_event("startup")
async def on_startup(ctx: Context):
    message = ResponseMessage(text="Hello from first agent")
    await ctx.send(SECOND_AGENT_ADDRESS, message)


@agent.on_message(model=ResponseMessage)
async def handle_message(ctx: Context, sender: str, msg: ResponseMessage):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")


agent.run()
