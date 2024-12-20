import os

from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Field, Model, Protocol
from uagents.setup import fund_agent_if_low

from crew_ai import MarketResearchProcess

SEED_PHRASE = "YOUR_SEED_PHRASE"

agent = Agent(
    name="startup idea analyzer",
    seed=SEED_PHRASE,
    mailbox=True
)

protocol = Protocol("Startup idea Analyzer version", version="0.1.2")
researcher = MarketResearchProcess()

print(agent.address, "agent_address")

fund_agent_if_low(agent.wallet.address())


class StartUpIdeaAnalyzer(Model):
    description: str = Field(
        description="describes the field which will be the description of the startup idea and it is provided by the user in context"
    )


@protocol.on_message(model=StartUpIdeaAnalyzer, replies={UAgentResponse})
async def on_message(ctx: Context, sender: str, msg: StartUpIdeaAnalyzer):
    ctx.logger.info(f"Received message from {sender}, message {msg.description}")
    result = researcher.run_process(msg.description)
    await ctx.send(
        sender, UAgentResponse(message=result, type=UAgentResponseType.FINAL)
    )


agent.include(protocol, publish_manifest=True)

agent.run()
