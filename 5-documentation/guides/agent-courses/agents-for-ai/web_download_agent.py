from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_openai import ChatOpenAI
from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType
import requests
import os


class SummaryRequest(Model):
    url: str


SEED_PHRASE = "<your_seed_phrase>"
AGENT_MAILBOX_KEY = "<your_mailbox_key>"
OPENAI_API_KEY = "<your_open_ai_key>"

summaryAgent = Agent(
    name="SummaryAgent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

summary_protocol = Protocol("Text Summariser")

print(summaryAgent.address)
print(OPENAI_API_KEY)


@summary_protocol.on_message(model=SummaryRequest, replies={UAgentResponse})
async def summarise(ctx: Context, sender: str, msg: SummaryRequest):


r = requests.get(msg.url)
with open("./temp.html", "w", encoding="utf-8") as f:
    f.write(r.text)

# Step 1: Initialize WebBaseLoader with the given URL
loader = UnstructuredHTMLLoader("./temp.html")

# Step 2: Load the document
docs = loader.load()

# Step 3: Load summarization chain
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo-1106")
chain = load_summarize_chain(llm, chain_type="stuff")

# Step 4: Run the summarization chain on the loaded document
summarized_content = chain.invoke(docs)
summarized = summarized_content["input_documents"][0].to_json()

# Step 5: Define the needed dependencies
dependencies = {
    "langchain": ">=1.0.0",
    "langchain_community": ">=1.0.0",
    "langchain_openai": ">=1.0.0"
}

result = chain.invoke(docs)

await ctx.send(
    sender,
    UAgentResponse(message=(result["output_text"]), type=UAgentResponseType.FINAL),
)

summaryAgent.include(summary_protocol, publish_manifest=True)
summaryAgent.run()