# Import Required libraries
import os

import requests
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low


# Define Request and Response Models
class NewsRequest(Model):
    company_name: str


class UrlRequest(Model):
    company_name: str


class NewsResponse(Model):
    news_list: list


class UrlResponse(Model):
    url_list: list


class ErrorResponse(Model):
    error: str


ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


# Define function to get ticker symbol for given company name
async def fetch_symbol(company_name):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Typically, the best match will be the first item in the bestMatches list
        if data.get("bestMatches") and len(data["bestMatches"]) > 0:
            Symbol = data["bestMatches"][0][
                "1. symbol"
            ]  # Return the symbol of the best match
            return Symbol
        else:
            return "No Symbol found"
    else:
        return "No Symbol found"


async def fetch_news(
    company_name,
):  # get news urls and description for the given news company or ticker
    url = (
        f"https://gnews.io/api/v4/search?q={company_name}&token={GNEWS_API_KEY}&lang=en"
    )
    response = requests.get(url)
    articles = response.json().get("articles", [])
    # Return a list of titles and descriptions with hyperlinks
    news_list = []
    for article in articles:
        article_url = article.get("url", "No url")
        description = article.get("description", "No Description")
        # Create a hyperlink using HTML anchor tag
        hyperlink = {"url": article_url, "title": description}
        news_list.append(hyperlink)
    return news_list


async def fetch_url(
    company_name,
):  # Get the news url's for given company name or symbol
    url = (
        f"https://gnews.io/api/v4/search?q={company_name}&token={GNEWS_API_KEY}&lang=en"
    )
    response = requests.get(url)
    articles = response.json().get("articles", [])
    # Return a list of titles and descriptions with hyperlinks
    url_list = []
    for article in articles:
        article_url = article.get("url", "No url")
        url_list.append(article_url)
    return url_list


# Define News Agent
NewsAgent = Agent(
    name="NewsAgent",
    port=8000,
    seed="News Agent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# Registering agent on Almanac and funding it.
fund_agent_if_low(NewsAgent.wallet.address())


# On agent startup printing address
@NewsAgent.on_event("startup")
async def agent_details(ctx: Context):
    ctx.logger.info(f"Search Agent Address is {NewsAgent.address}")


# On_query handler for news request
@NewsAgent.on_query(model=NewsRequest, replies={NewsResponse})
async def query_handler(ctx: Context, sender: str, msg: NewsRequest):
    try:
        ctx.logger.info(f"Fetching news details for company_name: {msg.company_name}")
        symbol = await fetch_symbol(msg.company_name)
        ctx.logger.info(f" Symbol for company provided is {symbol}")
        if (
            symbol is not None
        ):  # if company symbol fetch successfully getting news using ticker symbol else using the company name itself.
            news_list = await fetch_news(symbol)
        else:
            news_list = await fetch_news(msg.company_name)
            ctx.logger.info(str(news_list))
        await ctx.send(sender, NewsResponse(news_list=news_list))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(error=str(error_message)))


# On_query handler for news_url request
@NewsAgent.on_query(model=UrlRequest, replies={UrlResponse})
async def query_handler2(ctx: Context, sender: str, msg: UrlRequest):
    try:
        ctx.logger.info(
            f"Fetching news url details for company_name: {msg.company_name}"
        )
        symbol = await fetch_symbol(msg.company_name)
        ctx.logger.info(f" Symbol for company provided is {symbol}")
        if symbol is not None:
            url_list = await fetch_url(symbol)
        else:
            url_list = await fetch_url(msg.company_name)
        ctx.logger.info(str(url_list))
        await ctx.send(sender, UrlResponse(url_list=url_list))
    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(error=str(error_message)))


if __name__ == "__main__":
    NewsAgent.run()
