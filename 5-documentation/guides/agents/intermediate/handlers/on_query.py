import json

from fastapi import FastAPI, Request
from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope

AGENT_ADDRESS = "agent1qt6ehs6kqdgtrsduuzslqnrzwkrcn3z0cfvwsdj22s27kvatrxu8sy3vag0"

class TestRequest(Model):
    message: str

async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["text"]
    return response


app = FastAPI()

@app.get("/")
def read_root():
    return "Hello from the Agent controller"

@app.post("/endpoint")
async def make_agent_call(req: Request):
    model = TestRequest.parse_obj(await req.json())
    try:
        res = await agent_query(model)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"