import os
import statistics
from typing import Any, Literal, TypedDict
from datetime import datetime
from pydantic.v1 import UUID4
from uagents import Model, Protocol, Context
from uuid import uuid4

from helpers import (
    NotDirectFlightException,
    create_direct_flight_from_sky_scrapper_response,
    search_flights,
)
from schemas import Flight, FlightsSearchRequest, FlightsSearchResponse


AI_AGENT_ADDRESS = os.getenv("AI_AGENT_ADDRESS")


class Metadata(TypedDict):

    # primarily used with hte `Resource` model. This field specifies the mime_type of
    # resource that is being referenced. A full list can be found at `docs/mime_types.md`
    mime_type: str

    # the role of the resource
    role: str


class TextContent(Model):
    type: Literal["text"]

    # The text of the content. The format of this field is UTF-8 encoded strings. Additionally,
    # markdown based formatting can be used and will be supported by most clients
    text: str


class Resource(Model):

    # the uri of the resource
    uri: str

    # the set of metadata for this resource, for more detailed description of the set of
    # fields see `docs/metadata.md`
    metadata: dict[str, str]


class ResourceContent(Model):
    type: Literal["resource"]

    # The resource id
    resource_id: UUID4

    # The resource or list of resource for this content. typically only a single
    # resource will be sent, however, if there are accompanying resources like
    # thumbnails and audo tracks these can be additionally referenced
    #
    # In the case of the a list of resources, the first element of the list is always
    # considered the primary resource
    resource: Resource | list[Resource]


class MetadataContent(Model):
    type: Literal["metadata"]

    # the set of metadata for this content, for more detailed description of the set of
    # fields see `docs/metadata.md`
    metadata: dict[str, str]


class StartSessionContent(Model):
    type: Literal["start-session"]


class EndSessionContent(Model):
    type: Literal["end-session"]


class StartStreamContent(Model):
    type: Literal["start-stream"]

    stream_id: UUID4


class EndStreamContent(Model):
    type: Literal["start-stream"]

    stream_id: UUID4


# The combined agent content types
AgentContent = (
    TextContent
    | ResourceContent
    | MetadataContent
    | StartSessionContent
    | EndSessionContent
    | StartStreamContent
    | EndStreamContent
)


class ChatMessage(Model):

    # the timestamp for the message, should be in UTC
    timestamp: datetime

    # a unique message id that is generated from the message instigator
    msg_id: UUID4

    # the list of content elements in the chat
    content: list[AgentContent]


class ChatAcknowledgement(Model):

    # the timestamp for the message, should be in UTC
    timestamp: datetime

    # the msg id that is being acknowledged
    acknowledged_msg_id: UUID4

    # optional acknowledgement metadata
    metadata: dict[str, str] | None = None


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


chat_proto = Protocol(name="AgentChatProtcol", version="0.2.1")

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
    ctx.logger.info(f"Got a message from {sender}: {msg.content[0].text}")
    ctx.storage.set(str(ctx.session), sender)
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    await ctx.send(
        AI_AGENT_ADDRESS,
        StructuredOutputPrompt(
            prompt=msg.content[0].text, output_schema=FlightsSearchRequest.schema()
        ),
    )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")


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
            await ctx.send(session_sender, create_text_chat("Error while connecting to the external API."))
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
            flight_messages = "Sorry, no flights found."
        else:
            flight_messages = [
                f"✈️ {flight.airline} | {flight.origin} ({flight.departure_time}) ➡️ {flight.destination} ({flight.arrival_time})"
                f" | Price: {flight.price_formatted}"
                for flight in flights
            ]

        chat_message = create_text_chat("\n\n".join(flight_messages))

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