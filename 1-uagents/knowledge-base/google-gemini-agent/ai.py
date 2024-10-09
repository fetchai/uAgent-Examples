import os

import google.generativeai as genai

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
MODEL_ENGINE = os.getenv("MODEL_ENGINE", "gemini-1.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
if GEMINI_API_KEY is None or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
    raise ValueError(
        "You need to provide an API key: https://github.com/google-gemini/generative-ai-python?tab=readme-ov-file#get-started-with-the-gemini-api"
    )

genai.configure(api_key=GEMINI_API_KEY)


# Send a prompt to the AI model and return the content of the completion
def get_completion(prompt: str, code_generation: bool) -> str | None:
    tools = "code_execution" if code_generation else None

    model = genai.GenerativeModel(
        model_name=MODEL_ENGINE,
        tools=tools,
        generation_config=genai.GenerationConfig(max_output_tokens=MAX_TOKENS),
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None
