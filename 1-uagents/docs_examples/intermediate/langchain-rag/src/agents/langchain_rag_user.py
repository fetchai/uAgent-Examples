from ai_engine import UAgentResponse
from messages.requests import RagRequest
from uagents import Agent, Context, Protocol

QUESTION = "How to install uagents using pip"
URL = "https://fetch.ai/docs/guides/agents/installing-uagent"
DEEP_READ = "no"

RAG_AGENT_ADDRESS = "YOUR_LANGCHAIN_RAG_AGENT_ADDRESS"

user = Agent(
    name="langchain_rag_user",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

rag_user = Protocol("LangChain RAG user")


@rag_user.on_interval(60, messages=RagRequest)
async def ask_question(ctx: Context):
    ctx.logger.info(
        f"Asking RAG agent to answer {QUESTION} based on document located at {URL}, reading nested pages too: {DEEP_READ}"
    )
    await ctx.send(
        RAG_AGENT_ADDRESS, RagRequest(question=QUESTION, url=URL, deep_read=DEEP_READ)
    )


@rag_user.on_message(model=UAgentResponse)
async def handle_data(ctx: Context, sender: str, data: UAgentResponse):
    ctx.logger.info(f"Got response from RAG agent: {data.message}")


user.include(rag_user)

if __name__ == "__main__":
    user.run()
