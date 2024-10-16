# Here we demonstrate how we can create a news reading system agent that is compatible with DeltaV

# After running this agent, it can be registered to DeltaV on Agentverse. For registration you will have to use the agent's address

# Import required libraries
import requests
from ai_engine import UAgentResponse, UAgentResponseType


# Define News Reading Model
class News(Model):
    news: str


# Define Protocol for news reading system
news_protocol = Protocol("News System")


# Define a handler for the News system protocol
@news_protocol.on_message(model=News, replies=UAgentResponse)
async def on_news_request(ctx: Context, sender: str, msg: News):
    # Printing the news response on logger
    ctx.logger.info(f"Received news request from {sender} with title: {msg.news}")
    # Creating hyperlink and sending final response to the DeltaV GUI
    message = f"<a href='{msg.news}'>YOUR NEWS CONTENT</a>"
    await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL))


# Include the Generate News protocol in your agent
agent.include(news_protocol)