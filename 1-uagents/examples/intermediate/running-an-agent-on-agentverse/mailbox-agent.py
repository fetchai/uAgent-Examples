from uagents import Agent, Context, Model, Protocol
 
class Message(Model):
    message: str
 
SEED_PHRASE = "put_your_seed_phrase_here"

agent = Agent(
    name="MailboxTestAgent",
    seed=SEED_PHRASE,
    mailbox=True
)
 
print(f"Your agent's address is: {agent.address}")
 
test_protocol = Protocol("TestProtocol")
 
# Define your agent protocols and behaviour
# Include the protocols within your agent
 
if __name__ == "__main__":
    agent.run()