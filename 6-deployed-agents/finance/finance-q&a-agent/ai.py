import json
import os

import requests

ASI1_BASE_URL = os.getenv("ASI1_BASE_URL", "https://api.asi1.ai/v1")
ASI1_URL = f"{ASI1_BASE_URL.rstrip('/')}/chat/completions"
ASI1_MODEL = os.getenv("ASI1_MODEL", "asi1")
ASI1_API_KEY = os.getenv("ASI1_API_KEY", "")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ASI1_API_KEY}",
}


if not ASI1_API_KEY:
    raise ValueError("You need to provide an ASI:One API key.")


# Send a prompt and context to the AI model and return the content of the completion
def get_completion(prompt: str, max_tokens: int = MAX_TOKENS) -> str:
    data = {
        "model": ASI1_MODEL,
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
            ASI1_URL, headers=HEADERS, data=json.dumps(data), timeout=120
        )
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

    messages = response.json()["choices"]
    message = messages[0]["message"]["content"]

    return message
