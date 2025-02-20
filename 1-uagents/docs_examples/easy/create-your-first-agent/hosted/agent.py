# Import necessary classes from the uAgents library
from uagents import Context


# Function to be called when the agent is started
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    # Print a greeting message with the agent's name and its address
    print(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")
