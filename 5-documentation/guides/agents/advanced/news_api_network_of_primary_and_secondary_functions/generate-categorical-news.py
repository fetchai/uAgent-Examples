# Here we demonstrate how we can create a categorical news generating agent that is compatible with DeltaV.
# After running this agent, it can be registered to DeltaV on Agentverse. For registration you will have to use the agent's address.

# Importing libraries
import requests
import json
from ai_engine import UAgentResponse, UAgentResponseType


# Define the Generate News model
class GenerateNews(Model):
    category: str


# Define protocol for categorical news generation
generate_cat_news_protocol = Protocol("Generate Categorical News")


# Define function to generate news according to category in great britain - GB
async def generate_news(category):
    api_key = 'YOUR_NEWS_API_KEY'
    main_url = f"https://newsapi.org/v2/top-headlines?country=gb&category={category}&apiKey={api_key}"
    news = requests.get(main_url).json()
    # strip the source, get top 10 news and join the list with ' nnn ' to return the news as string and not list (DeltaV compatible type)
    titles = [article['title'].split(' - ')[0].strip() for article in news['articles']]
    titles = titles[:10]
    return titles


# Define a handler for the Categorical News generation protocol
@generate_cat_news_protocol.on_message(model=GenerateNews, replies=UAgentResponse)
async def on_generate_cat_news_request(ctx: Context, sender: str, msg: GenerateNews):
    # Logging category of news user wants to read
    ctx.logger.info(f"Received ticket request from {sender} with prompt: {msg.category}")
    try:
        # Generate news based on the requested category
        news_titles = generate_news(msg.category)
        # logging news
        ctx.logger.info(news_titles)
        # Send a successful response with the generated news
        await ctx.send(sender, UAgentResponse(message=str(news_titles), type=UAgentResponseType.FINAL))

    # Handle any exceptions that occur during news generation
    except Exception as exc:
        ctx.logger.error(f"Error in generating News: {exc}")
        # Send an error response with details of the encountered error.
        await ctx.send(
            sender,
            UAgentResponse(
                message=f"Error in generating News: {exc}",
                type=UAgentResponseType.ERROR
            )
        )


# Include the Generate News protocol in your agent
agent.include(generate_cat_news_protocol)