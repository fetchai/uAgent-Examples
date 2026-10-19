import difflib
import os
from datetime import datetime
from uuid import UUID, uuid4

from ai import generate_image, get_completion
from uagents import Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    MetadataContent,
    Resource,
    ResourceContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from uagents_core.storage import ExternalStorage

STORAGE_URL = os.getenv("AGENTVERSE_URL", "https://agentverse.ai") + "/v1/storage"
API_TOKEN = os.getenv("API_TOKEN")
external_storage = (
    ExternalStorage(api_token=API_TOKEN, storage_url=STORAGE_URL)
    if API_TOKEN
    else None
)


def create_text_chat(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )


def create_metadata(metadata: dict[str, str]) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[MetadataContent(type="metadata", metadata=metadata)],
    )


def create_resource_chat(
    asset_id: str,
    uri: str,
    mime_type: str = "image/png",
) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[
            ResourceContent(
                type="resource",
                resource_id=UUID(asset_id),
                resource=Resource(
                    uri=uri,
                    metadata={"mime_type": mime_type, "role": "generated-image"},
                ),
            ),
            EndSessionContent(type="end-session"),
        ],
    )


def image_prompt(text: str) -> str | None:
    stripped = text.strip()
    lowered = stripped.lower()
    prefixes = (
        "/image ",
        "generate an image of ",
        "generate an image ",
        "create an image of ",
        "create an image ",
    )
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return stripped[len(prefix):].strip()

    words = lowered.split()
    if words and difflib.SequenceMatcher(None, words[0], "generate").ratio() >= 0.75:
        for noun in ("image", "picture", "photo", "illustration"):
            marker = f"{noun} "
            position = lowered.find(marker)
            if position >= 0:
                prompt = stripped[position + len(marker):].strip()
                if prompt.lower().startswith("of "):
                    prompt = prompt[3:].strip()
                return prompt
    return None


def image_mime_type(image: bytes) -> str:
    if image.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if image.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if image.startswith(b"RIFF") and image[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("ASI:One returned an unsupported image format.")


def store_image(ctx: Context, sender: str, image: bytes) -> tuple[str, str, str]:
    if external_storage is None:
        raise RuntimeError(
            "Agentverse API_TOKEN is required to publish generated images."
        )

    mime_type = image_mime_type(image)
    asset_id = external_storage.create_asset(
        name=f"asi1_{ctx.session}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        content=image,
        mime_type=mime_type,
    )
    external_storage.set_permissions(
        asset_id=asset_id,
        agent_address=sender,
    )
    uri = f"agent-storage://{external_storage.storage_url}/{asset_id}"
    return asset_id, uri, mime_type


chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Got a message from {sender}")
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id)
    )

    prompt_content = []
    text_parts: list[str] = []
    has_resource = False

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            await ctx.send(sender, create_metadata({"attachments": "true"}))

        elif isinstance(item, TextContent):
            prompt_content.append({"type": "text", "text": item.text})
            text_parts.append(item.text)

        elif isinstance(item, ResourceContent):
            has_resource = True
            try:
                external_storage = ExternalStorage(
                    identity=ctx.agent.identity,
                    storage_url=STORAGE_URL,
                )
                data = external_storage.download(str(item.resource_id))
                prompt_content.append({
                    "type": "resource",
                    "mime_type": data["mime_type"],
                    "contents": data["contents"],
                })

            except Exception as e:
                ctx.logger.error(f"Failed to download resource: {e}")
                await ctx.send(sender, create_text_chat("Failed to download resource."))
                return

        else:
            ctx.logger.warning(f"Unexpected content type from {sender}")

    if prompt_content:
        requested_image = image_prompt(" ".join(text_parts))
        if requested_image is not None:
            if has_resource:
                await ctx.send(
                    sender,
                    create_text_chat(
                        "ASI:One image-to-image editing is not currently supported."
                    ),
                )
                return
            if not requested_image:
                await ctx.send(
                    sender,
                    create_text_chat("Please add a prompt after /image."),
                )
                return

            try:
                image = generate_image(requested_image)
                asset_id, uri, mime_type = store_image(ctx, sender, image)
                await ctx.send(
                    sender,
                    create_resource_chat(asset_id, uri, mime_type),
                )
            except Exception as error:
                ctx.logger.error(f"Image generation failed: {error}")
                await ctx.send(
                    sender,
                    create_text_chat(f"Image generation failed: {error}"),
                )
            return

        response = get_completion(prompt_content)
        await ctx.send(sender, create_text_chat(response or "No response generated."))


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")
