import random

from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Field, Model, Protocol


class DiceRoll(Model):
    num_rolls: int = Field(description="Number of rolls.")


# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"


# Now your agent is ready to join the agentverse!
dice_roll_agent = Agent(
    name="dice_roll_agent",
    seed=SEED_PHRASE,
    mailbox=True
)

# Copy the address shown below
print(f"Your agent's address is: {dice_roll_agent.address}")

dice_roll_protocol = Protocol("DiceRoll")


@dice_roll_protocol.on_message(model=DiceRoll, replies={UAgentResponse})
async def roll_dice(ctx: Context, sender: str, msg: DiceRoll):
    result = ", ".join([str(random.randint(1, 6)) for _ in range(msg.num_rolls)])
    message = f"Dice roll results: {result}"
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
    )


dice_roll_agent.include(dice_roll_protocol, publish_manifest=True)

if __name__ == "__main__":
    dice_roll_agent.run()
