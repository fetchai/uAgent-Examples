import requests
from ai_engine import UAgentResponse, UAgentResponseType


# Define a news content structure using the Model class to represent a news content
class NewsRequest(Model):
    company_name: str


# Create a protocol for the Hugging Face finbert agent
news_protocol = Protocol("Institute News")


async def fetch_symbol(company_name):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Typically, the best match will be the first item in the bestMatches list
        if data.get('bestMatches') and len(data['bestMatches']) > 0:
            # Return the symbol of the best match
            symbol = data['bestMatches'][0]['1. symbol']
            return symbol
    return 'No Symbol found'


async def analyze_news(company_name):
    """Analyze news sentiment for the company using GNews."""
    url = f"https://gnews.io/api/v4/search?q={company_name}&token={GNEWS_API_KEY}&lang=en"
    response = requests.get(url)
    articles = response.json().get('articles', [])

    # Extract URLs and convert them to hyperlinks with titles
    button_list = []
    for article in articles:
        title = article.get("title", "No Title")
        url = article.get("url", "No Url")
        if url != "No Url":
            # Create a clickable button with the title as text
            button_list.append(f'<a href="{url}">{title}</a>')

    # Combine buttons into a single string with line breaks
    buttons_combined = '\n'.join(button_list)

    return buttons_combined


@news_protocol.on_message(model=NewsRequest, replies=UAgentResponse)
async def on_institute_news_request(ctx: Context, sender: str, msg: NewsRequest):
    ctx.logger.info(msg.company_name)
    symbol = await fetch_symbol(msg.company_name)
    ctx.logger.info(symbol)
    news_content = await analyze_news(symbol)
    ctx.logger.info(news_content)
    await ctx.send(sender, UAgentResponse(message=news_content, type=UAgentResponseType.FINAL))


agent.include(news_protocol)
