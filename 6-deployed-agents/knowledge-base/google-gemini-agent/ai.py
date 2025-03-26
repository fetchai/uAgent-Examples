import os
from typing import Any

from google import genai
from google.genai import types

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
MODEL_ENGINE = os.getenv("MODEL_ENGINE", "gemini-2.0-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
if GEMINI_API_KEY is None or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
    raise ValueError(
        "You need to provide an API key: https://github.com/google-gemini/generative-ai-python?tab=readme-ov-file#get-started-with-the-gemini-api"
    )

client = genai.Client(api_key=GEMINI_API_KEY)


# Send a prompt to the AI model and return the content of the completion
def get_completion(
    prompt: str,
    code_generation: bool = False,
    response_schema: dict[str, Any] | None = None,
) -> str | None:
    if code_generation:
        config = types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        )
    elif response_schema is not None:
        config = {
            "response_mime_type": "application/json",
            "response_schema": response_schema,
        }
    else:
        config = None

    try:
        response = client.models.generate_content(
            model=MODEL_ENGINE,
            contents=prompt,
            config=config,
        )
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None
