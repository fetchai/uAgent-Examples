from uagents import Agent, Context, Model

class Message(Model):
    message: str

# Initialize the agent
agent = Agent(
    name="alice",
    seed="your_agent_seed_phrase",
    proxy=True
)

# Display the agent's address
print(f"Your agent's address is: {agent.address}")

if __name__ == "__main__":
    agent.run()