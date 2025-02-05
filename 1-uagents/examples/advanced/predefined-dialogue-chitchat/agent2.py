"""Chit chat dialogue example"""

from asyncio import sleep

from dialogues.hardcoded_chitchat import (
    ChitChatDialogue,
    ChitChatDialogueMessage,
    InitiateChitChatDialogue,
)
from uagents import Agent, Context

CHIT_AGENT_ADDRESS = "<your_agent_1_address>"

agent = Agent(
    name="chat_agent",
    seed="<random_string_of_choice>",
    port=8002,
    endpoint="http://127.0.0.1:8002/submit",
)

# Instantiate the dialogues
chitchat_dialogue = ChitChatDialogue(
    version="0.1",
)


@chitchat_dialogue.on_continue_dialogue()
async def continue_chitchat(
    ctx: Context,
    sender: str,
    msg: ChitChatDialogueMessage,
):
    ctx.logger.info(f"Returning: {msg.text}")
    await ctx.send(sender, ChitChatDialogueMessage(text=msg.text))


# Initiate dialogue after 5 seconds
@agent.on_event("startup")
async def start_cycle(ctx: Context):
    await sleep(5)
    await chitchat_dialogue.start_dialogue(
        ctx, CHIT_AGENT_ADDRESS, InitiateChitChatDialogue()
    )


agent.include(chitchat_dialogue)

if __name__ == "__main__":
    print(f"Agent address: {agent.address}")
    agent.run()
