from uagents import Agent, Model, Protocol


class Message(Model):
    message: str


SEED_PHRASE = "put_your_seed_phrase_here"

AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"

agent = Agent(
    name="MailboxTestAgent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

print(f"Your agent's address is: {agent.address}")

test_protocol = Protocol("TestProtocol")

# Define your agent protocols and behaviour
# Include the protocols within your agent

if __name__ == "__main__":
    agent.run()
