"""
This agent is created to run on agentverse.ai
visit agentverse.ai to create an agent with this code.

This agent will send a message to agent Bob as soon as its starts.
"""
from uagents import Agent, Context, Model

agent = Agent()


class Request(Model):
    message: str


@agent.on_message(model=Request)
async def handle_message(ctx: Context, sender: str, msg: Request):
    """Log the received message along with its sender"""
    ctx.logger.info(f"Received message from {sender}: {msg.message}")


@agent.on_event("startup")
async def send_message(ctx: Context):
    """Send a message to agent Bob by specifying its address"""
    ctx.logger.info(f"Just about to send a message to Bob")

    await ctx.send('agent1qwy8xp40thujt9ftmg4ug0qj8n6ln3n4wgjadrymxesshh2egge462cczye',
                   Request(message="hello there bob"))
    ctx.logger.info(f"Message has been sent to Bob")


if __name__ == "__main__":
    agent.run()
