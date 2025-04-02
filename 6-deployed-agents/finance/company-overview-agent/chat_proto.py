from datetime import datetime
import os
import time
from typing import Any
from uagents import Context, Model, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from uuid import uuid4

from functions import CompanyOverviewRequest, fetch_overview_json


AI_AGENT_ADDRESS = os.getenv("AI_AGENT_ADDRESS")


def create_text_chat(text: str, end_session: bool = True) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )


chat_proto = Protocol(spec=chat_protocol_spec)

struct_output_client_proto = Protocol(
    name="StructuredOutputClientProtocol", version="0.1.0"
)


class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    output: dict[str, Any]


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id
        ),
    )
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")
            ctx.storage.set(str(ctx.session), sender)
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=item.text, output_schema=CompanyOverviewRequest.schema()
                ),
            )
        else:
            ctx.logger.info(f"Got unexpected content from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )


@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    prompt = CompanyOverviewRequest.parse_obj(msg.output)
    session_sender = ctx.storage.get(str(ctx.session))
    if session_sender is None:
        ctx.logger.error(
            "Discarding message because no session sender found in storage"
        )
        return

    cache = ctx.storage.get(prompt.ticker) or None
    if cache:
        if int(time.time()) - cache["timestamp"] < 86400:
            cache.pop("timestamp")
            chat_message = create_text_chat(
                f"Company: {cache['Name']} ({cache['Symbol']})\n"
                f"Exchange: {cache['Exchange']} | Currency: {cache['Currency']}\n"
                f"Industry: {cache['Industry']} | Sector: {cache['Sector']}\n"
                f"Market Cap: {cache['Currency']} {cache['MarketCapitalization']}\n"
                f"PE Ratio: {cache['PERatio']} | EPS: {cache['EPS']}\n"
                f"Website: {cache['OfficialSite']}\n\n"
                f"Description: {cache['Description']}"
            )
            await ctx.send(session_sender, chat_message)
            return

    try:
        output_json = fetch_overview_json(prompt.ticker)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your request. Please try again later."
            ),
        )
        return

    if "error" in output_json:
        await ctx.send(session_sender, create_text_chat(str(output_json["error"])))
        return

    chat_message = create_text_chat(
        f"Company: {output_json['Name']} ({output_json['Symbol']})\n"
        f"Exchange: {output_json['Exchange']} | Currency: {output_json['Currency']}\n"
        f"Industry: {output_json['Industry']} | Sector: {output_json['Sector']}\n"
        f"Market Cap: {output_json['Currency']} {output_json['MarketCapitalization']}\n"
        f"PE Ratio: {output_json['PERatio']} | EPS: {output_json['EPS']}\n"
        f"Website: {output_json['OfficialSite']}\n\n"
        f"Description: {output_json['Description']}"
    )

    output_json["timestamp"] = int(time.time())
    ctx.storage.set(prompt.ticker, output_json)
    await ctx.send(session_sender, chat_message)
