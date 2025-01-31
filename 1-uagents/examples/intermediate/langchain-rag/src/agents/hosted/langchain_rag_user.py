from typing import Optional

from ai_engine import UAgentResponse
from uagents import Context, Field, Model, Protocol

QUESTION = "How to install uagents using pip"
URL = "https://fetch.ai/docs/guides/agents/installing-uagent"
DEEP_READ = "no"


class RagRequest(Model):
    question: str = Field(
        description="The question that the user wants to have an answer for."
    )
    url: str = Field(description="The url of the docs where the answer is.")
    deep_read: Optional[str] = Field(
        description="Specifies weather all nested pages referenced from the starting URL should be read or not. The value should be yes or no.",
        default="no",
    )


RAG_AGENT_ADDRESS = "YOUR_LANGCHAIN_RAG_AGENT_ADDRESS"

rag_user = Protocol("LangChain RAG user")


@agent.on_interval(60, messages=RagRequest)
async def ask_question(ctx: Context):
    ctx.logger.info(
        f"Asking RAG agent to answer {QUESTION} based on document located at {URL}, reading nested pages too: {DEEP_READ}"
    )
    await ctx.send(
        RAG_AGENT_ADDRESS, RagRequest(question=QUESTION, url=URL, deep_read=DEEP_READ)
    )


@agent.on_message(model=UAgentResponse)
async def handle_data(ctx: Context, sender: str, data: UAgentResponse):
    ctx.logger.info(f"Got response from RAG agent: {data.message}")


agent.include(rag_user)
