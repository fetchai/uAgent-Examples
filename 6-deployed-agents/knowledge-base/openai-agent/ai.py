import os
from typing import Any
from openai import OpenAI, OpenAIError

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

def get_text_completion(context: str, prompt: str, response_schema: dict[str, Any] | None = None):
    content = [{"type": "text", "text": prompt}]
    return get_completion(content, context, response_schema)

# Send a prompt and context to the AI model and return the content of the completion
def get_completion(
    content: list[dict[str, Any]],
    context: str = "",
    response_schema: dict[str, Any] | None = None,
    max_tokens: int = MAX_TOKENS,
) -> str:

    processed_content = []

    for item in content:
        if item.get("type") == "text":
            processed_content.append({"type": "text", "text": item["text"]})
        elif item.get("type") == "resource":
            mime_type = item["mime_type"]
            if mime_type.startswith("image/"):
                processed_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{item['contents']}",
                    },
                })
            else:
                return f"Unsupported mime type: {mime_type}"

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
                {"role": "user", "content": processed_content},
            ],
            response_format=response_format,
            max_tokens=max_tokens,
        )
    except OpenAIError as e:
        return f"An error occurred: {e}"

    return response.choices[0].message.content
