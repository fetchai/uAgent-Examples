# Here we demonstrate how we can create a simple coin toss agent that is compatible with DeltaV.

# After running this agent, it can be registered to DeltaV on Agentverse My Agents tab. For registration you will have to use the agent's address.

import random
# third party modules used in this example
from uagents import Field
from ai_engine import UAgentResponse, UAgentResponseType

class CoinToss(Model):
    choice: str = Field(description="The choice. Must be heads or tails.")

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

agent.include(coin_toss_protocol, publish_manifest=True)