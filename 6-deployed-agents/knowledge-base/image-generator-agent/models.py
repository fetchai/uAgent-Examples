import base64
import io
import os
from uagents import Model
from openai import OpenAI, OpenAIError


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1.5")

if OPENAI_API_KEY is None:
    raise ValueError("You need to provide an OpenAI API Key.")


client = OpenAI(api_key=OPENAI_API_KEY)


class ImageRequest(Model):
    image_description: str

class ImageResponse(Model):
    image_url: str


def _decode_b64_image(resp) -> bytes:
    item = resp.data[0]
    b64 = getattr(item, "b64_json", None) or (item.get("b64_json") if isinstance(item, dict) else None)
    if not b64:
        raise RuntimeError(f"Missing b64_json in image response. item={item!r}")
    return base64.b64decode(b64)


def generate_image(prompt: str, input_image: bytes | None = None) -> bytes:
    try:
        if input_image is None:
            result = client.images.generate(
                model=OPENAI_IMAGE_MODEL,
                prompt=prompt,
            )
            return _decode_b64_image(result)

        buf = io.BytesIO(input_image)
        buf.name = "input.png"
        buf.seek(0)

        result = client.images.edit(
            model=OPENAI_IMAGE_MODEL,
            prompt=prompt,
            image=buf,
        )
        return _decode_b64_image(result)

    except OpenAIError as e:
        raise RuntimeError(f"OpenAI image error: {e}") from e
