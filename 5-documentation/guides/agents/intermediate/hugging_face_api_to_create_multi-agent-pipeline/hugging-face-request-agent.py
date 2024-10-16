# Here we demonstrate how we can create a hugging face request agent that is compatible with DeltaV.

# After running this agent, it can be registered to DeltaV on Agentverse Services tab. For registration you will have to use the agent's address.

# Importing required libraries.
import requests
import json
from ai_engine import UAgentResponse, UAgentResponseType


# Define a model class for the Hugging Face Request agent's expected message format.
class Search(Model):
    model_id: str
    query: str


# Define a function to handle query from user using model_id and query provided by user.
async def handle_query(model_id, query):
    Model_ID = model_id
    API_URL = f'https://api-inference.huggingface.co/models/{Model_ID}'  # hugging face url
    API_TOKEN = 'YOUR TOKEN HERE'  # hugging face API token

    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # Make request to hugging face API with model_id and query.
    response = requests.post(API_URL, headers=headers, json=query).json()
    return response


# Create a protocol for the Hugging Face Request(HF) agent, specifying its interactions_and_interval_task protocol.
hfprotocol = Protocol(name='Hugging Face protocol')


# Define a handler for the Hugging face request protocol.
@hfprotocol.on_message(model=Search, replies=UAgentResponse)
async def handle_message(ctx: Context, sender: str, msg: Search):
    # Log the model_id and query provided by user.
    ctx.logger.info(f'Message sent from {sender} : {msg.model_id}')
    ctx.logger.info(f'Message sent from subtask : {msg.query}')

    # Calling handle_query function to get response from API.
    response = await handle_query(msg.model_id, msg.query)
    # sending response to hugging face agent
    await ctx.send(sender, UAgentResponse(message=str(response), type=UAgentResponseType.FINAL))


# Include the Hugging Face protocol in your agent.
agent.include(hfprotocol, publish_manifest=True)