# Here we demonstrate how we can create a news generating agent that is compatible with DeltaV.

# Import required libraries
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Model, Protocol


# Define News Generating Model.
class GenerateNews(Model):
    news_type: str
    news: str


# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now go to https://agentverse.ai, register your agent in the Mailroom by providing the address you just copied.
# Then, copy the agent's mailbox key and insert it here below inline
AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"

# Now your agent is ready to join the agentverse!
generate_news_agent = Agent(
    name="generate_news_agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

# Copy the address shown below
print(f"Your agent's address is: {generate_news_agent.address}")

# Define Generate news protocol.
generate_news_protocol = Protocol("Generate News")


# Define a handler for the News generation protocol
@generate_news_protocol.on_message(model=GenerateNews, replies=UAgentResponse)
async def on_generate_news_request(ctx: Context, sender: str, msg: GenerateNews):
    try:
        # Generate news based on the requested category.
        ctx.logger.info("Generating News")
        ctx.logger.info(f"User have selected {msg.news_type} category")

        ctx.logger.info(f"Generate News \n {msg.news}")
        message = msg.news

        # Send a successful response with the generated news.
        await ctx.send(
            sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
        )

    # Handle any exceptions that occur during news generation.
    except Exception as exc:
        ctx.logger.error(f"Error in generating  news: {exc}")

        # Send an error response with details of the encountered error.
        await ctx.send(
            sender,
            UAgentResponse(
                message=f"Error in generating news: {exc}",
                type=UAgentResponseType.ERROR,
            ),
        )


# Include the Generate News protocol in your agent.
generate_news_agent.include(generate_news_protocol)

generate_news_agent.run()
