# Import libraries
import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Model, Protocol


# Define the Generate News model
class GenerateNews(Model):
    keyword: str


# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now go to https://agentverse.ai, register your agent in the Mailroom by providing the address you just copied.
# Then, copy the agent's mailbox key and insert it here below inline
AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"

# Now your agent is ready to join the agentverse!
generate_news_keyw_agent = Agent(
    name="generate_news_keyw_agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

# Copy the address shown below
print(f"Your agent's address is: {generate_news_keyw_agent.address}")

# Define protocol for keyword news generation
generate_news_keyw_protocol = Protocol("Generate Keyword News")


# Define function to generate news according to keyword
async def get_keyword_news(keyword):
    api_key = "YOUR_API_KEY"
    main_url = f"https://newsapi.org/v2/top-headlines?q={keyword}&apiKey={api_key}"
    news = requests.get(main_url).json()
    # Strip the source, get top 10 news and join the list with nnn to return the news as string and not list - DeltaV compatible type
    titles = [article["title"].split(" - ")[0].strip() for article in news["articles"]]
    titles = titles[:10]
    _ = " nnn ".join([f"{title}" for title in titles])


# Define a handler for the Keyword News generation protocol
@generate_news_keyw_protocol.on_message(model=GenerateNews, replies=UAgentResponse)
async def on_generate_news_request(ctx: Context, sender: str, msg: GenerateNews):
    ctx.logger.info(f"Received news request from {sender} with prompt: {msg.keyword}")
    # Generate news based on the requested keyword
    try:
        news = get_keyword_news(msg.keyword)
        # Send a successful response with the generated news
        await ctx.send(
            sender, UAgentResponse(message=news, type=UAgentResponseType.FINAL)
        )

    # Handle any exceptions that occur during news generation
    except Exception as exc:
        ctx.logger.error(f"Error in generating News: {exc}")
        # Send an error response with details of the encountered error
        await ctx.send(
            sender,
            UAgentResponse(
                message=f"Error in generating News: {exc}",
                type=UAgentResponseType.ERROR,
            ),
        )


# Include the Generate Keyword News protocol in your agent
generate_news_keyw_agent.include(generate_news_keyw_protocol)

generate_news_keyw_agent.run()
