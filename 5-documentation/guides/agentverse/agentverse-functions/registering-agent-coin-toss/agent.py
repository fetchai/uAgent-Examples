"""
This is a simple coin toss agent that is compatible with DeltaV.
"""

from uagents import Agent, Context, Field, Model, Protocol
from ai_engine import UAgentResponse, UAgentResponseType
import random

agent = Agent()


class CoinToss(Model):
    choice: str = Field(description="The choice. Must be heads or tails.")


coin_toss_protocol = Protocol("CoinToss")


@coin_toss_protocol.on_message(model=CoinToss, replies={UAgentResponse})
async def toss_coin(ctx: Context, sender: str, msg: CoinToss):
    """Simulates a coin toss, compares the result to the sender's choice and send back result"""
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


# Include protocol in agent
agent.include(coin_toss_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
