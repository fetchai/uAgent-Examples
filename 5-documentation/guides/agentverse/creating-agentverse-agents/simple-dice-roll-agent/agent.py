"""
This agent can create a simple dice roll, it is compatible with DeltaV.
"""

import random
from uagents import Agent, Context, Field, Model, Protocol
from ai_engine import UAgentResponse, UAgentResponseType

agent = Agent()


class DiceRoll(Model):
    num_rolls: int = Field(description="Number of rolls.")


dice_roll_protocol = Protocol("DiceRoll")


@dice_roll_protocol.on_message(model=DiceRoll, replies={UAgentResponse})
async def roll_dice(ctx: Context, sender: str, msg: DiceRoll):
    """Simulate a dice roll for the specified number of times and sends the results."""
    result = ", ".join([str(random.randint(1, 6)) for _ in range(msg.num_rolls)])
    message = f"Dice roll results: {result}"
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
    )


agent.include(dice_roll_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
