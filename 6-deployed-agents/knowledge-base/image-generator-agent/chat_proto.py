import base64
import os
from uuid import uuid4
from datetime import datetime
from pydantic.v1 import UUID4

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
from models import generate_image

API_TOKEN = os.getenv("API_TOKEN")
STORAGE_URL = os.getenv("AGENTVERSE_URL", "https://agentverse.ai") + "/v1/storage"
if API_TOKEN is None:
    raise ValueError("You need to provide an API_TOKEN.")

external_storage = ExternalStorage(
    api_token=API_TOKEN,
    storage_url=STORAGE_URL
)

chat_proto = Protocol(spec=chat_protocol_spec)


def create_text_chat(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )

def create_end_session_chat() -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[EndSessionContent(type="end-session")],
    )

def create_metadata(metadata: dict[str, str]) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[MetadataContent(type="metadata", metadata=metadata)],
    )

def create_resource_chat(asset_id: str, uri: str, mime_type: str = "image/png") -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[
            ResourceContent(
                type="resource",
                resource_id=UUID4(asset_id),
                resource=Resource(
                    uri=uri,
                    metadata={"mime_type": mime_type, "role": "generated-image"},
                ),
            )
        ],
    )

def _decode_downloaded_asset(data) -> tuple[str, bytes]:
    if isinstance(data, dict):
        mime_type = data.get("mime_type") or "application/octet-stream"
        contents = data.get("contents")
        if isinstance(contents, str):
            return mime_type, base64.b64decode(contents)
        return mime_type, bytes(contents)
    return "application/octet-stream", bytes(data)


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    prompt_parts: list[str] = []
    input_image: bytes | None = None

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            await ctx.send(sender, create_metadata({"attachments": "true"}))

        if isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")
            prompt_parts.append(item.text)

        if isinstance(item, ResourceContent):
            ctx.logger.info(f"Got an image resource from {sender}: {item.resource_id}")
            try:
                external_storage_att = ExternalStorage(identity=ctx.agent.identity, storage_url=STORAGE_URL)
                data = external_storage_att.download(str(item.resource_id))
                mime_type, blob = _decode_downloaded_asset(data)

                if not mime_type.startswith("image/"):
                    await ctx.send(sender, create_text_chat("Attachment must be an image."))
                    return

                input_image = blob
            except Exception as ex:
                ctx.logger.error(f"Failed to download resource: {ex}")
                await ctx.send(sender, create_text_chat("Failed to download image attachment."))
                return

            continue

        ctx.logger.info(f"Got unexpected content from {sender}")

    prompt = " ".join(prompt_parts).strip()
    if not prompt:
        prompt = "Edit the image." if input_image else "Generate an image."

    try:
        out_png = generate_image(prompt, input_image=input_image)

        asset_id = external_storage.create_asset(
            name=str(ctx.session),
            content=out_png,
            mime_type="image/png",
        )
        ctx.logger.info(f"Asset created with ID: {asset_id}")

        external_storage.set_permissions(asset_id=asset_id, agent_address=sender)
        ctx.logger.info(f"Asset permissions set to: {sender}")

        asset_uri = f"agent-storage://{external_storage.storage_url}/{asset_id}"
        await ctx.send(sender, create_resource_chat(asset_id, asset_uri, mime_type="image/png"))

    except Exception as err:
        await ctx.send(sender, create_text_chat(f"Error processing image generation request: {err}"))
        ctx.logger.error(f"Error processing image generation request: {err}")
        return

    await ctx.send(sender, create_end_session_chat())



@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")
