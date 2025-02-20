# Here we demonstrate how we can create a news reading system agent that is compatible with DeltaV

# Import required libraries
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Model, Protocol


# Define News Reading Model
class News(Model):
    news: str


# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now go to https://agentverse.ai, register your agent in the Mailroom by providing the address you just copied.
# Then, copy the agent's mailbox key and insert it here below inline
AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"

# Now your agent is ready to join the agentverse!
news_agent = Agent(
    name="news_agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

# Copy the address shown below
print(f"Your agent's address is: {news_agent.address}")

# Define Protocol for news reading system
news_protocol = Protocol("News System")


# Define a handler for the News system protocol
@news_protocol.on_message(model=News, replies=UAgentResponse)
async def on_news_request(ctx: Context, sender: str, msg: News):
    # splitting the news titles with nnn and enumerating them with line break for visually better results
    result_list = msg.news.split(" nnn ")
    final_news = "\n".join([f"{i + 1}. {title}" for i, title in enumerate(result_list)])
    # Printing the news response on logger
    ctx.logger.info(f"Received news request from {sender} with prompt: {final_news}")
    # sending final response to the DeltaV GUI
    await ctx.send(
        sender, UAgentResponse(message=final_news, type=UAgentResponseType.FINAL)
    )


# Include the Generate News protocol in your agent
news_agent.include(news_protocol)

news_agent.run()
