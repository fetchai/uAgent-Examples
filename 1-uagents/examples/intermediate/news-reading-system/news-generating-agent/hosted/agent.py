# Here we demonstrate how we can create a news generating agent that is compatible with DeltaV.
# After running this agent, it can be registered to DeltaV on Agentverse My Agents tab. For registration you will have to use the agent's address.

# Import required libraries
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Context, Model, Protocol


# Define News Generating Model.
class GenerateNews(Model):
    news_type: str
    news: str


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
agent.include(generate_news_protocol)
