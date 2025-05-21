import os
from uagents import Model
from openai import OpenAI, OpenAIError


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("You need to provide an OpenAI API Key.")


client = OpenAI(api_key=OPENAI_API_KEY)


class ImageRequest(Model):
    image_description: str

class ImageResponse(Model):
    image_url: str

def generate_image(prompt: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
        )
    except OpenAIError as e:
        return f"An error occurred: {e}"
    return response.data[0].url