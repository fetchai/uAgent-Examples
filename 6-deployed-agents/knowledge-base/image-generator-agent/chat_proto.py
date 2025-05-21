import base64
import os
import requests
from uuid import uuid4
from datetime import datetime
from pydantic.v1 import UUID4

from uagents import Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
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

external_storage = ExternalStorage(api_token=API_TOKEN, storage_url=STORAGE_URL)


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

def create_resource_chat(asset_id: str, uri: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[
            ResourceContent(
                type="resource",
                resource_id=UUID4(asset_id),
                resource=Resource(
                    uri=uri,
                    metadata={
                        "mime_type": "image/png",
                        "role": "generated-image"
                    }
                )
            )
        ]
    )


chat_proto = Protocol(spec=chat_protocol_spec)


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")

            prompt = msg.content[0].text
            try:
                image_url = generate_image(prompt)

                response = requests.get(image_url)
                if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "")
                    image_data = response.content 
                    
                    try:
                        asset_id = external_storage.create_asset(
                            name=str(ctx.session),
                            content=image_data,
                            mime_type=content_type
                        )
                        ctx.logger.info(f"Asset created with ID: {asset_id}")

                    except RuntimeError as err:
                        ctx.logger.error(f"Asset creation failed: {err}")

                    external_storage.set_permissions(asset_id=asset_id, agent_address=sender)
                    ctx.logger.info(f"Asset permissions set to: {sender}")

                    asset_uri = f"agent-storage://{external_storage.storage_url}/{asset_id}"
                    await ctx.send(sender, create_resource_chat(asset_id, asset_uri))

                else:
                    ctx.logger.error("Failed to download image")
                    await ctx.send(
                        sender,
                        create_text_chat(
                            "Sorry, I couldn't process your request. Please try again later."
                        ),
                    )
                    return

            except Exception as err:
                ctx.logger.error(err)
                await ctx.send(
                    sender,
                    create_text_chat(
                        "Sorry, I couldn't process your request. Please try again later."
                    ),
                )
                return

            await ctx.send(sender, create_end_session_chat())

        else:
            ctx.logger.info(f"Got unexpected content from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")
