from langchain_community.document_loaders import PyPDFLoader
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from uagents import Agent, Context, Protocol, Model
from typing import List


class DocumentUnderstanding(Model):
    pdf_path: str
    question: str


class DocumentsResponse(Model):
    learnings: List


pdf_questioning_agent = Agent(
    name="pdf_questioning_agent",
    seed="",
    port=8003,
    endpoint=["http://127.0.0.1:8003/submit"],
)

print("uAgent address: ", pdf_questioning_agent.address)
pdf_loader_protocol = Protocol("Text Summariser")


@pdf_questioning_agent.on_message(model=DocumentUnderstanding, replies=DocumentsResponse)
async def document_load(ctx: Context, sender: str, msg: DocumentUnderstanding):
    loader = PyPDFLoader(msg.pdf_path)
    pages = loader.load_and_split()
    openai_api_key = os.environ['OPENAI_API_KEY']
    learnings = []

    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(openai_api_key=openai_api_key))

    docs = faiss_index.similarity_search(msg.question, k=2)

    for doc in docs:
        learnings.append(str(doc.metadata["page"]) + ":" + doc.page_content[:600])

    await ctx.send(sender, DocumentsResponse(learnings=learnings))


pdf_questioning_agent.include(pdf_loader_protocol, publish_manifest=True)
pdf_questioning_agent.run()
