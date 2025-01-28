from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
 
class Message(Model):
    message: str
 
# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now your agent is ready to join the agentverse!
agent = Agent(
    name="alice",
    seed=SEED_PHRASE,
    mailbox=True,
)
 
fund_agent_if_low(agent.wallet.address())
 
# Copy the address shown below
print(f"Your agent's address is: {agent.address}")
 
@agent.on_message(model=Message, replies={Message})
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    ctx.logger.info("Sending message to bob")
    await ctx.send(sender, Message(message="hello there bob"))
 
if __name__ == "__main__":
    agent.run()
