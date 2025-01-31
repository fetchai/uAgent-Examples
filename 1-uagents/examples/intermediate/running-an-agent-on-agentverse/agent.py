from uagents import Agent, Model, Protocol


class Message(Model):
    message: str


agent = Agent(
    name="TestAgent",
    port=6145,
    seed="RANDOM STRINGS",
    endpoint=["http://YOUR_IP:6145/submit"],
)

test_protocol = Protocol("TestProtocol")

# Define your agent protocols
# Include the protocols within your agent
agent.include(test_protocol, publish_manifest=True)

agent.run()
