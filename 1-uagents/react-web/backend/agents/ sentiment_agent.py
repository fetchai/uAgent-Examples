# Import Required libraries
import requests
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import time
import asyncio
import aiohttp
import json
 
# Define Request and Response Data Models
class SentimentRequest(Model):
    news : str
 
class SentimentResponse(Model):
    sentiment : str
 
class ErrorResponse(Model):
    error : str
 
# Define Sentiment analysis Agent
SentimentAgent = Agent(
    name="Sentiment Agent",
    port=8002,
    seed="Sentiment Agent secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)
 
# Registering agent on Almanac and funding it.
fund_agent_if_low(SentimentAgent.wallet.address())
 
# Define function to provide sentiment for given content
async def sentiment_analysis(news):
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": "Bearer <Hugging face API>"}
 
    payload = {"inputs": news}
 
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as response:
            if response.status == 200:
                sentiments = await response.json()
                await asyncio.sleep(5)  # Proper async sleep
                # Flatten the list of dicts to a single list
                flattened_sentiments = [item for sublist in sentiments for item in sublist]
                max_sentiment = max(flattened_sentiments, key=lambda s: s['score'])
                max_label = str(max_sentiment['label'])
                max_score = str(round(max_sentiment['score'], 3))
                return f"{max_label},{max_score}"
            else:
                return "Error: Failed to fetch data from API"
 
# On agent startup printing address
@SentimentAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Search Agent Address is {SentimentAgent.address}')
 
# On_query handler for processing sentiment request
@SentimentAgent.on_query(model=SentimentRequest, replies={SentimentResponse})
async def query_handler(ctx: Context, sender: str, msg: SentimentRequest):
    try:
        sentiment = await sentiment_analysis(msg.news)
        if sentiment == "Error: Failed to fetch data from API":
            sentiment = await sentiment_analysis(msg.news[:500]) # if model is not ale to perform sentiment request we will just take string with 500 characters
            ctx.logger.info(msg.news[:300])
        ctx.logger.info(sentiment)
        await ctx.send(sender, SentimentResponse(sentiment = sentiment))
    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(error=str(error_message)))
 
if __name__ == "__main__":
    SentimentAgent.run()