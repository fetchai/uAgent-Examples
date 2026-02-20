from datetime import datetime
from uuid import uuid4

from ai import search
from uagents import Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)


def create_text_chat(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )


chat_proto = Protocol(spec=chat_protocol_spec)


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id
        ),
    )
    if not msg.content:
        ctx.logger.warning("Empty message content.")
        await ctx.send(sender, create_text_chat("You've sent a ChatMessage with empty content."))
        return
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):

            if item.type != "text":
                msg = f"Unsupported message type: {item.type}."
                ctx.logger.warning(msg)
                await ctx.send(sender, create_text_chat(f"{msg} I only support TextContent."))
                return

            # Retrieve the serialised message history for this session, if any
            messages_key = f"messages-{str(ctx.session)}"
            messages_serialised: str = ctx.storage.get(messages_key) or None
            # Perform the search
            response, messages_serialised = search(
                ctx=ctx,
                user_query=item.text,
                message_history=messages_serialised,
            )
            # Save the serialised message history for this session
            ctx.storage.set(messages_key, messages_serialised)
            # Send the final response
            await ctx.send(sender, create_text_chat(response))


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")
