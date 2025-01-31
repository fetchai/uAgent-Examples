import random

from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Field, Model, Protocol


class CoinToss(Model):
    choice: str = Field(description="The choice. Must be heads or tails.")


# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now go to https://agentverse.ai, register your agent in the Mailroom by providing the address you just copied.
# Then, copy the agent's mailbox key and insert it here below inline
AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"

# Now your agent is ready to join the agentverse!
coin_toss_agent = Agent(
    name="coin_toss_agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)


# Copy the address shown below
print(f"Your agent's address is: {coin_toss_agent.address}")

coin_toss_protocol = Protocol("CoinToss")


@coin_toss_protocol.on_message(model=CoinToss, replies={UAgentResponse})
async def toss_coin(ctx: Context, sender: str, msg: CoinToss):
    random_number = random.randint(0, 1)
    if random_number == 0:
        coin_tossed = "heads"
    else:
        coin_tossed = "tails"
    if coin_tossed == msg.choice:
        message = "You won!"
    else:
        message = "You lost!"
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
    )


coin_toss_agent.include(coin_toss_protocol, publish_manifest=True)

if __name__ == "__main__":
    coin_toss_agent.run()
