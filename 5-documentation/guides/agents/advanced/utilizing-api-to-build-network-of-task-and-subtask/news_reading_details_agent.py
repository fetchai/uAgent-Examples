# Here we demonstrate how we can create a news details agent that is compatible with DeltaV.
# After running this agent, it can be registered to DeltaV on Agentverse. For registration you will have to use the agent's address.

# Import required libraries
import requests
import json
from ai_engine import UAgentResponse, UAgentResponseType


# Define News Generating Model.
class GetNewsDetails(Model):
    news_type: str
    news_subtype: str
    news_url_content: str


# Define Generate news protocol.
generate_news_protocol = Protocol("Get News Details")


# Define a handler for the News generation protocol
@generate_news_protocol.on_message(model=GetNewsDetails, replies=UAgentResponse)
async def news_details_agent(ctx: Context, sender: str, msg: GetNewsDetails):
    # Logging user request
    ctx.logger.info(
        f"Received ticket request from {sender} with prompt: {msg.news_type} and {msg.news_subtype}")  # and {msg.news_subtype}
    # Defining dictionary for country codes
    country_codes = {
        "argentina": "ar", "australia": "au", "austria": "at", "belgium": "be",
        "bulgaria": "bg", "brazil": "br", "canada": "ca", "china": "cn",
        "colombia": "co", "cuba": "cu", "czech republic": "cz", "germany": "de",
        "egypt": "eg", "france": "fr", "united kingdom": "gb", "greece": "gr",
        "hong kong": "hk", "hungary": "hu", "indonesia": "id", "ireland": "ie",
        "israel": "il", "india": "in", "italy": "it", "japan": "jp",
        "south korea": "kr", "lithuania": "lt", "latvia": "lv", "morocco": "ma",
        "mexico": "mx", "malaysia": "my", "nigeria": "ng", "netherlands": "nl",
        "norway": "no", "new zealand": "nz", "philippines": "ph", "poland": "pl",
        "portugal": "pt", "romania": "ro", "serbia": "rs", "russia": "ru",
        "saudi arabia": "sa", "sweden": "se", "singapore": "sg", "slovenia": "si",
        "slovakia": "sk", "thailand": "th", "turkey": "tr", "taiwan": "tw",
        "ukraine": "ua", "united states": "us", "venezuela": "ve", "south africa": "za"
    }

    try:
        # Generate news based on the requested category.
        ctx.logger.info('Getting News URL')
        ctx.logger.info(f'User have selected {msg.news_type} type and {msg.news_subtype} subtype')

        # Checking news type and getting news url
        if msg.news_type.lower() == 'categorical':  # For categorical news type
            main_url = f"https://newsapi.org/v2/top-headlines?country=gb&category={msg.news_subtype}&apiKey={api_key}"
            response = requests.get(main_url).json()
            ctx.logger.info(response)
            # Iterate through the news articles to find a title containing the msg.news
            for article in response['articles']:
                if msg.news_url_content.lower() in article['title'].lower():
                    # If found, send the URL back as a clickable link
                    news_url = article['url']
                    ctx.logger.info(f'Categorical news {news_url}')
                    await ctx.send(sender, UAgentResponse(message=str(news_url), type=UAgentResponseType.FINAL))
        elif msg.news_type.lower() == 'regional':  # For regional news type
            main_url = f"https://newsapi.org/v2/top-headlines?country={country_codes.get(msg.news_subtype.lower())}&apiKey={api_key}"
            response = requests.get(main_url).json()
            ctx.logger.info(response)
            # Iterate through the news articles to find a title containing the msg.news
            for article in response['articles']:
                if msg.news_url_content.lower() in article['title'].lower():
                    # If found, send the URL back as a clickable link
                    news_url = article['url']
                    ctx.logger.info(f'Regional news {news_url}')
                    await ctx.send(sender, UAgentResponse(message=str(news_url), type=UAgentResponseType.FINAL))

        elif msg.news_type.lower() == 'keyword':  # For Keyword news type
            main_url = f"https://newsapi.org/v2/top-headlines?q={msg.news_subtype}&apiKey={api_key}"
            response = requests.get(main_url).json()
            ctx.logger.info(response)
            # Iterate through the news articles to find a title containing the msg.news
            for article in response['articles']:
                if msg.news_url_content.lower() in article['title'].lower():
                    # If found, send the URL back as a clickable link
                    news_url = article['url']
                    ctx.logger.info(f'Keyword news {news_url}')
                    await ctx.send(sender, UAgentResponse(message=str(news_url), type=UAgentResponseType.FINAL))
        else:  # If news type is not valid
            await ctx.send(sender, UAgentResponse(message="You have not provided valid news type",
                                                  type=UAgentResponseType.FINAL))

    # Handle any exceptions that occur during news generation.
    except Exception as exc:
        ctx.logger.error(f"Error in generating  news: {exc}")

        # Send an error response with details of the encountered error.
        await ctx.send(
            sender,
            UAgentResponse(
                message=f"Error in generating news: {exc}",
                type=UAgentResponseType.ERROR
            )
        )


# Include the Generate News protocol in your agent.
agent.include(generate_news_protocol)