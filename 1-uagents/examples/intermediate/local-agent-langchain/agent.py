from ai_engine import UAgentResponse, UAgentResponseType
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from uagents import Agent, Context, Field, Model, Protocol


# Extend your protocol with Wikipedia data fetching
class WikiReq(Model):
    search_keyword: str = Field(
        description="This describes the keyword you want to search on wiki"
    )


SEED_PHRASE = "<Secret Phrase for your agent>"

# Copy the address shown below
print(f"Your agent's address is: {Agent(seed=SEED_PHRASE).address}")

AGENT_MAILBOX_KEY = "Your_mailbox_address"

# Now your agent is ready to join the agentverse!
WikiAgent = Agent(
    name="Wiki Agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

wiki_protocol = Protocol("Wiki Protocol")


@wiki_protocol.on_message(model=WikiReq, replies={UAgentResponse})
async def load_dalle(ctx: Context, sender: str, msg: WikiReq):
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    ctx.logger.info(msg.search_keyword)
    try:
        result = wikipedia.run(msg.search_keyword)
    except Exception as e:
        ctx.logger.info(f"Error generating response: {e}")
    # Send an error response back to the user
    await ctx.send(
        sender, UAgentResponse(message=str(result), type=UAgentResponseType.FINAL)
    )


WikiAgent.include(wiki_protocol, publish_manifest=True)
WikiAgent.run()
