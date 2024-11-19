from uagents import Agent, Context, Protocol, Model
import random
from uagents import Field
from ai_engine import UAgentResponse, UAgentResponseType
import sys

agent = Agent(
    name="dungeonsanddragonsdiceroll",
    port=6145,
    seed="RANDOM STRINGS",
    endpoint=["http://YOUR_IP:6145/submit"],
)


@agent.on_event("startup")
async def hi(ctx: Context):
    ctx.logger.info(agent.address)


class Request(Model):
    dice_sides: int = Field(description="How many sides does your dice need?")


dice_roll_protocol = Protocol("DungeonsAndDragonsDiceRoll")


@dice_roll_protocol.on_message(model=Request, replies={UAgentResponse})
async def roll_dice(ctx: Context, sender: str, msg: Request):
    result = str(random.randint(1, msg.dice_sides))
    message = f"Dice roll result: {result}"
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
    )


agent.include(dice_roll_protocol, publish_manifest=True)

agent.run()