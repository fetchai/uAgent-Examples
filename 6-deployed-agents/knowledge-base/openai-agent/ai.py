import json
import os
from typing import Any
from openai import OpenAI, OpenAIError

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


client = OpenAI(api_key=OPENAI_API_KEY)


# Send a prompt and context to the AI model and return the content of the completion
def get_completion(
    context: str,
    prompt: str,
    response_schema: dict[str, Any] | None = None,
    max_tokens: int = MAX_TOKENS,
) -> str:
    if response_schema is not None:
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": response_schema["title"],
                "strict": False,
                "schema": response_schema,
            },
        }
    else:
        response_format = None

    try:
        response = client.chat.completions.create(
            model=MODEL_ENGINE,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
            ],
            response_format=response_format,
            max_tokens=max_tokens,
        )
    except OpenAIError as e:
        return f"An error occurred: {e}"

    return response.choices[0].message.content
