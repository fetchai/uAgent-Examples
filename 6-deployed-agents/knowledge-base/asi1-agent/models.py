from uagents import Model


class ImageRequest(Model):
    prompt: str


class ImageResponse(Model):
    image_url: str
