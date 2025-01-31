# Here we demonstrate how we can create a categorical news generating agent that is compatible with DeltaV.

# Importing libraries
import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Model, Protocol


# Define the Generate News model.
class GenerateNews(Model):
    category: str


# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now go to https://agentverse.ai, register your agent in the Mailroom by providing the address you just copied.
# Then, copy the agent's mailbox key and insert it here below inline
AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"

# Now your agent is ready to join the agentverse!
generate_cat_news_agent = Agent(
    name="generate_cat_news_agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

# Copy the address shown below
print(f"Your agent's address is: {generate_cat_news_agent.address}")

# Define protocol for categorical news generation.
generate_cat_news_protocol = Protocol("Generate Categorical News")


# Define function to generate news according to category in great britain - GB.
async def generate_news(category):
    api_key = "YOUR_NEWS_API_KEY"
    main_url = f"https://newsapi.org/v2/top-headlines?country=gb&category={category}&apiKey={api_key}"
    news = requests.get(main_url).json()
    # strip the source, get top 10 news and join the list with ' nnn ' to return the news as string and not list (DeltaV compatible type)
    titles = [article["title"].split(" - ")[0].strip() for article in news["articles"]]
    titles = titles[:10]
    results = " nnn ".join([f"{title}" for title in titles])

    return results


# Define a handler for the Categorical News generation protocol.
@generate_cat_news_protocol.on_message(model=GenerateNews, replies=UAgentResponse)
async def on_generate_news_request(ctx: Context, sender: str, msg: GenerateNews):
    # Logging category of news user wants to read
    ctx.logger.info(
        f"Received ticket request from {sender} with prompt: {msg.category}"
    )
    try:
        # Generate news based on the requested category.
        news = generate_news(msg.category)
        # logging news
        ctx.logger.info(news)
        message = str(news)
        # Send a successful response with the generated news.
        await ctx.send(
            sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
        )

    # Handle any exceptions that occur during news generation.
    except Exception as exc:
        ctx.logger.error(f"Error in generating News: {exc}")
        # Send an error response with details of the encountered error.
        await ctx.send(
            sender,
            UAgentResponse(
                message=f"Error in generating News: {exc}",
                type=UAgentResponseType.ERROR,
            ),
        )


# Include the Generate News protocol in your agent.
generate_cat_news_agent.include(generate_cat_news_protocol)

generate_cat_news_agent.run()
