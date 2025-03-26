import json
import os

import requests

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MODEL_ENGINE = os.getenv("MODEL_ENGINE", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}


if OPENAI_API_KEY is None or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
    raise ValueError(
        "You need to provide an API key: https://platform.openai.com/api-keys"
    )


# Send a prompt and context to the AI model and return the content of the completion
def get_completion(prompt: str, max_tokens: int = MAX_TOKENS) -> str:
    data = {
        "model": MODEL_ENGINE,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert in finance and are answering questions about finance.",
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(
            OPENAI_URL, headers=HEADERS, data=json.dumps(data), timeout=120
        )
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

    messages = response.json()["choices"]
    message = messages[0]["message"]["content"]

    return message
