"""
This agent is created to run on agentverse.ai
visit agentverse.ai to create an agent with this code.

This agent is capable of receiving messages and reply to the sender.
"""

from uagents import Agent, Context, Model

agent = Agent(name="alice", seed="YOUR NEW PHRASE")


class Request(Model):
    message: str


@agent.on_message(model=Request)
async def handle_message(ctx: Context, sender: str, msg: Request):
    """Log the received message and reply to the sender"""
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    if sender == 'agent1qvkcrp7hkz692reqw4d87qaky708627gh5kv79fxevjs93jtdacp6a78syj':
        await ctx.send(sender, Request(message="hello there alice"))
    else:
        await ctx.send(sender, Request(message="hello there friend"))


if __name__ == "__main__":
    agent.run()
