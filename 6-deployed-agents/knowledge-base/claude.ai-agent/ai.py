import json
import os

import requests

CLAUDE_URL = "https://api.anthropic.com/v1/messages"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY")
if ANTHROPIC_API_KEY is None or ANTHROPIC_API_KEY == "YOUR_ANTHROPIC_API_KEY":
    raise ValueError(
        "You need to provide an API key: https://platform.openai.com/api-keys"
    )
MODEL_ENGINE = os.getenv("MODEL_ENGINE", "claude-3-haiku-20240307")
HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

# "claude-3-5-sonnet-20240620",  # Most intelligent model
# "claude-3-opus-20240229",  # Excels at writing and complex tasks
# "claude-3-sonnet-20240229",  # Balance of speed and intelligence
# "claude-3-haiku-20240307",  # Fast & cost-effective


# Send a prompt to the AI model and return the content of the completion
def get_completion(prompt: str) -> str | None:
    data = {
        "model": MODEL_ENGINE,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(
            CLAUDE_URL, headers=HEADERS, data=json.dumps(data), timeout=120
        )
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

    messages = response.json()["content"]
    message = messages[0]["text"]

    return message
