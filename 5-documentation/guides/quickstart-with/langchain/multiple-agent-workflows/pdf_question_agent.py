from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from uagents import Agent, Context, Protocol, Model
from langchain_core.documents import Document
from typing import List
import os
import uuid
import faiss


class PDF_Request(Model):
    pdf_path: str


class DocumentUnderstanding(Model):
    pdf_path: str
    question: str


class PagesResponse(Model):
    pages: List


class DocumentsResponse(Model):
    learnings: str


faiss_pdf_agent = Agent(
    name="faiss_pdf_agent",
    seed="",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)

print("uAgent address: ", faiss_pdf_agent.address)
faiss_protocol = Protocol("FAISS")

RequestAgent = ""
PDF_splitter_address = ""

openai_api_key = os.environ["OPENAI_API_KEY"]
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


@faiss_pdf_agent.on_message(model=DocumentUnderstanding, replies=PDF_Request)
async def document_load(ctx: Context, sender: str, msg: DocumentUnderstanding):
    ctx.logger.info(msg)
    ctx.storage.set(str(ctx.session), {"question": msg.question, "sender": sender})
    await ctx.send(
        PDF_splitter_address, PDF_Request(pdf_path=msg.pdf_path)
    )


@faiss_pdf_agent.on_message(model=PagesResponse, replies=DocumentsResponse)
async def document_understand(ctx: Context, sender: str, msg: PagesResponse):
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello")))

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    documents = []
    for page in msg.pages:
        documents.append(
            Document(page_content=page["page_content"], metadata=page["metadata"])
        )

    uuids = [str(uuid.uuid4()) for _ in range(len(documents))]

    vector_store.add_documents(documents=documents, ids=uuids)

    prev = ctx.storage.get(str(ctx.session))

    results = vector_store.similarity_search(
        prev["question"],
        k=2,
    )

    if len(results) > 0:
        await ctx.send(
            prev["sender"], DocumentsResponse(learnings=results[0].page_content)
        )


faiss_pdf_agent.include(faiss_protocol, publish_manifest=True)
faiss_pdf_agent.run()
