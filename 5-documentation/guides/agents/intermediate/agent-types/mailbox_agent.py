from uagents import Agent, Context, Model


class Message(Model):
    message: str


SEED_PHRASE = "put_your_seed_phrase_here"

# Now your agent is ready to join the agentverse!
agent = Agent(
    name="alice",
    port=8000,
    mailbox=True
)

# Copy the address shown below
print(f"Your agent's address is: {agent.address}")

if __name__ == "__main__":
    agent.run()
