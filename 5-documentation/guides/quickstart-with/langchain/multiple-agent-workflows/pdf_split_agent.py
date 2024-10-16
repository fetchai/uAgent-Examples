from langchain_community.document_loaders import PyPDFLoader
from uagents import Agent, Context, Protocol, Model
from typing import List


class PDF_Request(Model):
    pdf_path: str


class PagesResponse(Model):
    pages: List


pdf_loader_agent = Agent(
    name="pdf_loader_agent",
    seed="",
    port=8003,
    endpoint=["http://127.0.0.1:8003/submit"],
)

print("uAgent address: ", pdf_loader_agent.address)
pdf_loader_protocol = Protocol("Text Summarizer")


@pdf_loader_agent.on_message(model=PDF_Request, replies=PagesResponse)
async def document_load(ctx: Context, sender: str, msg: PDF_Request):
    loader = PyPDFLoader(msg.pdf_path)
    pages = loader.load_and_split()
    await ctx.send(sender, PagesResponse(pages=pages))


pdf_loader_agent.include(pdf_loader_protocol, publish_manifest=True)
pdf_loader_agent.run()
