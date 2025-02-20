# Import the required classes
from uagents import Agent, Context

agent = Agent(name="alice", seed="alice recovery phrase")


# Provide your Agent with a job
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")


# This constructor simply ensure that only this script is running
if __name__ == "__main__":
    agent.run()
    