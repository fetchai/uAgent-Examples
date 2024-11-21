from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Protocol, Model
 
class Message(Model):
    message: str
 
agent = Agent(
    name="TestAgent",
    port=6145,
    seed="RANDOM STRINGS",
    endpoint=["http://YOUR_IP:6145/submit"],
)
 
fund_agent_if_low(agent.wallet.address())
 
@agent.on_event("startup")
async def hi(ctx: Context):
    ctx.logger.info(agent.address)
 
test_protocol = Protocol("TestProtocol")
 
# Define your agent protocols
# Include the protocols within your agent
agent.include(test_protocol, publish_manifest=True)
 
agent.run()