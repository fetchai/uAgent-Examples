from uagents import Agent, Context, Model

class Message(Model):
    message: str

AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"
SEED_PHRASE = "put_your_seed_phrase_here"

# Now your agent is ready to join the agentverse!
agent = Agent(
    name="alice",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

# Copy the address shown below
print(f"Your agent's address is: {agent.address}")

if __name__ == "__main__":
    agent.run()