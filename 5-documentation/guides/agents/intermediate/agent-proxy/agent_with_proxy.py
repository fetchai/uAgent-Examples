from uagents import Agent, Context, Model


class Message(Model):
    message: str


# Now your agent is ready to join the agentverse!
agent = Agent(
    name="alice",
    seed="your_agent_seed_phrase",
    proxy=True,
)

# Copy the address shown below
print(f"Your agent's address is: {agent.address}")

if __name__ == "__main__":
    agent.run()