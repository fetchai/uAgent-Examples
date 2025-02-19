import json

from fastapi import FastAPI, Query
from models import ShoppingRequest
from uagents.query import query

app = FastAPI()

DESTINATION = "agent1qg9p5xppsdv6067lg570g8t3lzens32fg6d0fe88jawd2v0lsh8f6ru9ntc"


@app.get("/api/question-answer")
async def question_answering(
    message: str = Query(..., description="The message or question you want to ask"),
):
    """
    Handles GET requests to the /api/question-answer endpoint.

    Accepts:
        - message: A string query parameter representing the message or question that you want to ask.

    What it does:
        - Creates a ShoppingRequest object using the provided message.
        - Sends the ShoppingRequest object to the specified agent (DESTINATION) using the query function.
        - Decodes the response payload received from the agent and parses it as JSON.

    Returns:
        - A dictionary containing the "response" with the answer retrieved from the agent.
    """
    shopping_request = ShoppingRequest(question=message)
    answer = await query(destination=DESTINATION, message=shopping_request)
    response_data = json.loads(answer.decode_payload())
    return {"response": response_data.get("answer")}


@app.get("/")
async def root():
    """
    Handles GET requests to the root endpoint ("/").

    What it does:
        - Returns a simple "Hello World" message.

    Returns:
        - A dictionary containing a "message" key with the value "Hello World".
    """
    return {"message": "Hello World"}
