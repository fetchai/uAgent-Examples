import os
from datetime import datetime
from uuid import uuid4
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

from helpers import FlightsSearchRequest, NotDirectFlightException, create_direct_flight_from_sky_scrapper_response, search_flights
from schemas import Flight


AI_AGENT_ADDRESS = os.getenv("AI_AGENT_ADDRESS")


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
                    prompt=item.text, output_schema=FlightsSearchRequest.schema()
                ),
            )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )


@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    prompt = FlightsSearchRequest.parse_obj(msg.output)
    session_sender = ctx.storage.get(str(ctx.session))

    try:
        flights_raw = search_flights(
            logger=ctx.logger, request=prompt, storage=ctx.storage
        )
        if flights_raw is None:
            await ctx.send(
                session_sender,
                create_text_chat("Error while connecting to the external API."),
            )
            return

        flights: list[Flight] = []
        discarded_flights: int = 0
        for flight in flights_raw["itineraries"]:
            try:
                flights.append(
                    create_direct_flight_from_sky_scrapper_response(itinerary=flight)
                )
            except NotDirectFlightException:
                discarded_flights += 1

        ctx.logger.info(
            f"{len(flights_raw['itineraries'])} total flights retrieved, "
            f"{discarded_flights} discarded, sending {len(flights)} direct flights."
        )
        if not flights:
            flight_messages = ["Sorry, no flights found."]
        else:
            flight_messages = [
                f"✈️ {flight.airline} | {flight.origin} ({flight.departure_time}) ➡️ {flight.destination} ({flight.arrival_time})"
                f" | Price: {flight.price_formatted}"
                for flight in flights
            ]

        chat_message = create_text_chat("\n\n".join(flight_messages))

        ctx.logger.debug(f"Sending response: {chat_message}")
        await ctx.send(session_sender, chat_message)
        await ctx.send(session_sender, create_end_session_chat())
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your request. Please try again later."
            ),
        )
        return
