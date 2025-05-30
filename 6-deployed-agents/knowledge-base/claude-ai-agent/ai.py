import json
import os
from typing import Any

import requests

CLAUDE_URL = "https://api.anthropic.com/v1/messages"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY")
if ANTHROPIC_API_KEY is None or ANTHROPIC_API_KEY == "YOUR_ANTHROPIC_API_KEY":
    raise ValueError(
        "You need to provide an API key: https://platform.openai.com/api-keys"
    )
MODEL_ENGINE = os.getenv("MODEL_ENGINE", "claude-3-5-haiku-latest")
HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

# "claude-3-5-sonnet-20240620",  # Most intelligent model
# "claude-3-opus-20240229",  # Excels at writing and complex tasks
# "claude-3-sonnet-20240229",  # Balance of speed and intelligence
# "claude-3-haiku-20240307",  # Fast & cost-effective


def create_structured_response_tool(
    response_model_schema: dict[str, Any],
) -> dict[str, Any]:

    # Exclude the title from the schema (not allowed in the API)
    for data in response_model_schema["properties"].values():
        if "title" in data:
            data.pop("title")

    return {
        "name": response_model_schema["title"],
        "description": response_model_schema.get("description", ""),
        "input_schema": response_model_schema,
    }


def get_text_completion(prompt: str, tool: dict[str, Any] | None = None) -> str | None:
    content = [{"type": "text", "text": prompt}]
    return get_completion(content, tool)


# Send a prompt to the AI model and return the content of the completion
def get_completion(
    content: list[dict[str, Any]], tool: dict[str, Any] | None = None
) -> str | None:

    processed_content = []

    for item in content:
        if item.get("type") == "text":
            processed_content.append({"type": "text", "text": item["text"]})
        elif item.get("type") == "resource":
            mime_type = item["mime_type"]
            if mime_type.startswith("image/"):
                processed_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime_type,
                        "data": item["contents"],
                    }
                })
            else:
                return f"Unsupported mime type: {mime_type}"

    data = {
        "model": MODEL_ENGINE,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {
                "role": "user",
                "content": processed_content,
            }
        ],
    }

    if tool:
        data["tools"] = [tool]
        data["tool_choice"] = {"type": "tool", "name": tool["name"]}

    try:
        response = requests.post(
            CLAUDE_URL, headers=HEADERS, data=json.dumps(data), timeout=120
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

    # Check if the response was successful
    response_data = response.json()

    # Handle error responses
    if "error" in response_data:
        return f"API Error: {response_data['error'].get('message', 'Unknown error')}"

    if tool:
        for item in response_data["content"]:
            if item["type"] == "tool_use":
                return item["input"]
            
    messages = response_data["content"]

    if messages:
        return messages[0]["text"]
    else:
        return None


def get_structured_response(
    prompt: str, response_model_schema: dict[str, Any]
) -> dict[str, Any] | None:
    tool = create_structured_response_tool(response_model_schema)
    return get_text_completion(prompt, tool)
