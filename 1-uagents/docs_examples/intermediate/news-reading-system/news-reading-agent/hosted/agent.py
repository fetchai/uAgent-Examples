# Here we demonstrate how we can create a news reading system agent that is compatible with DeltaV

# After running this agent, it can be registered to DeltaV on Agentverse My Agents tab. For registration you will have to use the agent's address

# Import required libraries
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Context, Model, Protocol


# Define News Reading Model
class News(Model):
    news: str


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
agent.include(news_protocol)
