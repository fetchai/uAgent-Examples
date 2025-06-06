import os
from typing import Any
from openai import OpenAI, OpenAIError


MODEL_ENGINE = os.getenv("MODEL_ENGINE", "MODEL_NAME")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENAI_API_KEY")
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
}


if OPENROUTER_API_KEY is None or OPENROUTER_API_KEY == "YOUR_OPENAI_API_KEY":
    raise ValueError(
        "You need to provide an API key: https://platform.openai.com/api-keys"
    )


client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)


# Send a prompt and context to the AI model and return the content of the completion
def get_completion(
    context: str,
    prompt: str,
    response_schema: dict[str, Any] | None = None,
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
        )
    except OpenAIError as e:
        return f"An error occurred: {e}"

    return response.choices[0].message.content
