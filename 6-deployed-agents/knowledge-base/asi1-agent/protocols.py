import os
from datetime import datetime
from uuid import uuid4

from ai import get_completion
from uagents import Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    MetadataContent,
    ResourceContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from uagents_core.storage import ExternalStorage

STORAGE_URL = os.getenv("AGENTVERSE_URL", "https://agentverse.ai") + "/v1/storage"


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

chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Got a message from {sender}")
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id)
    )

    prompt_content = []

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            await ctx.send(sender, create_metadata({"attachments": "true"}))

        elif isinstance(item, TextContent):
            prompt_content.append({"type": "text", "text": item.text})

        elif isinstance(item, ResourceContent):
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
        response = get_completion(prompt_content)
        await ctx.send(sender, create_text_chat(response or "No response generated."))


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")
