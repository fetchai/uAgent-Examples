import random

from ai_engine import UAgentResponse, UAgentResponseType

# third party modules used in this example
from uagents import Context, Field, Model, Protocol


class DiceRoll(Model):
    num_rolls: int = Field(description="Number of rolls.")


dice_roll_protocol = Protocol("DiceRoll")


@dice_roll_protocol.on_message(model=DiceRoll, replies={UAgentResponse})
async def roll_dice(ctx: Context, sender: str, msg: DiceRoll):
    result = ", ".join([str(random.randint(1, 6)) for _ in range(msg.num_rolls)])
    message = f"Dice roll results: {result}"
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
    )


agent.include(dice_roll_protocol, publish_manifest=True)
