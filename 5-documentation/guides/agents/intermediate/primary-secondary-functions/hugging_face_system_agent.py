# Here we demonstrate how we can create a hugging face system agent that is compatible with DeltaV.

# After running this agent, it can be registered to DeltaV on Agentverse. For registration you will have to use the agent's address.

# Importing required libraries
import requests
from ai_engine import UAgentResponse, UAgentResponseType


# Define a model class for the Hugging Face agent's expected message format
class HF(Model):
    response: str  # This class has a single attribute 'response' that holds the string response from the subtask.


# Create a protocol for the Hugging Face (HF) agent, specifying its interactions_and_interval_task protocol
hf_protocol = Protocol("Hugging Face")


# Define a handler for the Hugging face protocol
@hf_protocol.on_message(model=HF, replies=UAgentResponse)
async def on_hf_request(ctx: Context, sender: str, msg: HF):
    # Log the receipt of a response, including the sender and the message prompt
    ctx.logger.info(f"Received hugging face request from {sender} with prompt: {msg.response}")

    # Format a response message incorporating the received message
    message = f'Response to your query from model is \n {msg.response}'
    # Asynchronously send a response back to the sender with the processed message
    await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL))


# Include the Hugging Face protocol in your agent
agent.include(hf_protocol)