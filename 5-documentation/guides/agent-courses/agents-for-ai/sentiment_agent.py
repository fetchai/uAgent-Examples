from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType
import openai


class SentimentResponse(Model):
    text: str


SEED_PHRASE = ""
AGENT_MAILBOX_KEY = ""

sentimentagent = Agent(
    name="SentimentAgent",  # or any name
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

print(sentimentAgent.address)

content_protocol = Protocol("text sentiment analysis")


def get_sentiment(text):
    response = openai.chat.completions.create(

        messages=[{
            "role": "user",
            "content": f"Sentiment analysis of the following text:\n{text}\n",
        }], model=("gpt-3.5-turbo"))

    return response.choices[0].message.content


@content_protocol.on_message(model=SentimentResponse, replies={UAgentResponse})
async def sentiment(ctx: Context, sender: str, msg: SentimentResponse):
    sentiment = get_sentiment(msg.text)
    await ctx.send(
        sender, UAgentResponse(message=sentiment, type=UAgentResponseType.FINAL)
    )


sentimentAgent.include(content_protocol, publish_manifest=True)
sentimentAgent.run()