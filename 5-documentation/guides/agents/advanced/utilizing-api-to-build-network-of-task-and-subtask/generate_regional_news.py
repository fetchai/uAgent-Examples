# Import libraries
import requests
import json
from ai_engine import UAgentResponse, UAgentResponseType

# Define dictionary with country codes
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


# Define the Generate News model
class GenerateNews(Model):
    country: str


# Define function to generate regional news according to country
async def get_regional_news(country):
    api_key = 'YOUR_API_KEY'
    main_url = f"https://newsapi.org/v2/top-headlines?country={country_codes.get(country.lower())}&apiKey={api_key}"
    news = requests.get(main_url).json()
    # Strip the source, get top 10 news and join the list with nnn to return the news as string and not list - DeltaV compatible type
    titles = [article['title'].split(' - ')[0].strip() for article in news['articles']]
    titles = titles[:10]
    return titles


# Define protocol for regional news generation Protocol
generate_news_reg_protocol = Protocol("Generate Regional News")


# Define a handler for the Regional News generation protocol
@generate_news_reg_protocol.on_message(model=GenerateNews, replies=UAgentResponse)
async def on_generate_news_request(ctx: Context, sender: str, msg: GenerateNews):
    ctx.logger.info(f"Received ticket request from {sender} with prompt: {msg.country}")
    try:
        # Get the country code from the country_code dictionary
        country_code = country_codes.get(msg.country.lower())
        # Generate news based on the requested country and log it on agentverse
        news_titles = await get_regional_news(msg.country)
        ctx.logger.info(f"Message from endpoint: {news_titles}")
        # Send a successful response with the generated news
        await ctx.send(sender, UAgentResponse(message=str(news_titles), type=UAgentResponseType.FINAL))
    # Handle any exceptions that occur during news generation
    except Exception as exc:
        ctx.logger.error(f"Error in generating News: {exc}")
        # Send an error response with details of the encountered error
        await ctx.send(
            sender,
            UAgentResponse(
                message=f"Error in generating News: {exc}",
                type=UAgentResponseType.ERROR
            )
        )


# Include the Generate Regional News protocol in your agent
agent.include(generate_news_reg_protocol)