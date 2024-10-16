# Here we demonstrate how we can create a model list agent that is compatible with DeltaV

# After running this agent, it can be registered to DeltaV on Agentverse Services tab. For registration you will have to use the agent's address

# Importing required libraries
import requests
from ai_engine import UAgentResponse, UAgentResponseType
import json


# Define a model class for the Model List agent's expected message format
class Search(Model):
    search: str  # This is a keyword for which user wants to search model


# Create a protocol for the Model List agent, specifying its interactions_and_interval_task protocol
model_list_protocol = Protocol(name='Model List protocol')


# Define a function to handle query from user using search keyword provided by user
async def handle_query(search):
    url = "https://huggingface.co/api/models"

    params = {
        "search": search,
        "filter": "text-classification",
        "sort": "downloads",
        "direction": -1,
        "limit": 5
    }  # Search parameters.

    models = []  # List of models.

    # Make the GET request
    response = requests.get(url, params=params)

    # Append models in list
    for model in response.json():
        models.append(model['id'])

    return models


# Define a handler for the Model list protocol
@model_list_protocol.on_message(model=Search, replies=UAgentResponse)
async def handle_message(ctx: Context, sender: str, msg: Search):
    # Log search keyword provided by user.
    ctx.logger.info(f'Message sent from {sender} : {msg.search}')

    # Call handle_query to get list of models
    options = handle_query(msg.search)
    # Log model list responded by hugging face request
    ctx.logger.info(f'Message sent from {sender} : {options}')

    # Format options in dictionary format to provide options to user
    formatted_options = [{'key': i + 1, 'value': value} for i, value in enumerate(options)]

    # Send message to the user
    await ctx.send(sender, UAgentResponse(message=str(formatted_options), type=UAgentResponseType.FINAL))


# Include model_list protocol in agent
agent.include(model_list_protocol, publish_manifest=True)