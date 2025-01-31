import json

import requests
from models import ShoppingAssistResponse, ShoppingRequest
from uagents import Agent, Context

agent = Agent(
    name="Shopping Assistant",
    seed="shopping_assistant_seed_phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

YOUR_OPEN_AI_API_KEY = "PASTE_YOUR_OPEN_AI_API_KEY"


def get_chat_response(messages):
    """
    Sends a request to the OpenAI GPT-4 API to generate a chat response.

    Accepts:
        - messages: A list of dictionaries representing the conversation history,
                    where each dictionary contains a 'role' (e.g., 'system' or 'user')
                    and 'content' (the message text).

    What it does:
        - Sends a POST request to the OpenAI API with the conversation history.
        - Handles the API response, returning the generated response from the model
          or an error message if the request fails.

    Returns:
        - A string containing the model's response if the request is successful.
        - An error message string if the request fails.
    """
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {YOUR_OPEN_AI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7,
    }

    response = requests.post(
        api_url, headers=headers, data=json.dumps(data), timeout=10
    )

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"


@agent.on_query(model=ShoppingRequest, replies=ShoppingAssistResponse)
async def handler(ctx: Context, sender: str, msg: ShoppingRequest):
    """
    Handles incoming queries from other agents, specifically ShoppingRequest messages.

    Accepts:
        - ctx: The context object, used for logging and communication.
        - sender: A string representing the address of the agent that sent the message.
        - msg: A ShoppingRequest object containing the question from the user.

    What it does:
        - Logs the received question.
        - Prepares a conversation history for the chat model with the role of the assistant and user.
        - Sends the conversation history to the get_chat_response function to generate a response.
        - Logs the generated response.
        - Sends the response back to the sender as a ShoppingAssistResponse.

    Returns:
        - None (asynchronous function).
    """
    ctx.logger.info(f"Received message from {sender} with question: {msg.question}")
    messages = [{"role": "system", "content": "You are a helpful shopping assistant."}]
    messages.append({"role": "user", "content": msg.question})
    response = get_chat_response(messages)
    ctx.logger.info(f"Question: {msg.question}\nAnswer: {response}")
    await ctx.send(sender, ShoppingAssistResponse(answer=response))


if __name__ == "__main__":
    agent.run()
