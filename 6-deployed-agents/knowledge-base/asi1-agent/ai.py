import os
from typing import Any, List
from openai import OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam


ASI1_URL = "https://api.asi1.ai/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "asi1-mini")
ASI1_API_KEY = os.getenv("ASI1_API_KEY", "")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))


if not ASI1_API_KEY:
    raise ValueError(
        "You need to provide an API key:https://docs.asi1.ai/docs/getting-api-key"
    )


client = OpenAI(api_key=ASI1_API_KEY, base_url=ASI1_URL)


# Send a prompt and context to the AI model and return the content of the completion
def get_completion(
    content: List[dict[str, Any]],
    max_tokens: int = MAX_TOKENS,
) -> str:
    message_parts = []

    for item in content:
        if item.get("type") == "text":
            message_parts.append({"type": "text", "text": item["text"]})
        elif item.get("type") == "resource":
            mime_type = item["mime_type"]
            if mime_type.startswith("image/"):
                message_parts.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{item['contents']}",
                    },
                })
            else:
                return f"Unsupported mime type: {mime_type}"


    if len(message_parts) == 1 and message_parts[0].get("type") == "text":
        user_content = message_parts[0]["text"]
    else:
        user_content = message_parts

    try:
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": "You are Fetch.ai agent, running on AgentVerse.ai platform."},
            {"role": "user", "content": user_content},
        ]
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content

        return str(content)

    except OpenAIError as e:
        return f"An error occurred: {e}"
