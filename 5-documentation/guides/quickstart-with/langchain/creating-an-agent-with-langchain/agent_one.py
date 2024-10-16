from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType
from typing import List


class DocumentUnderstanding(Model):
    pdf_path: str
    question: str


class DocumentsResponse(Model):
    learnings: List


agent = Agent(
    name="find_in_pdf",
    seed="",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"]
)

print("uAgent address: ", agent.address)
summary_protocol = Protocol("Text Summarizer")

RECIPIENT_PDF_AGENT = ""


@agent.on_event("startup")
async def on_startup(ctx: Context):
    await ctx.send(RECIPIENT_PDF_AGENT,
                   DocumentUnderstanding(pdf_path="../a-little-story.pdf", question="What's the synopsis?"))


@agent.on_message(model=DocumentsResponse)
async def document_load(ctx: Context, sender: str, msg: DocumentsResponse):
    ctx.logger.info(msg.learnings)


agent.include(summary_protocol, publish_manifest=True)
agent.run()
