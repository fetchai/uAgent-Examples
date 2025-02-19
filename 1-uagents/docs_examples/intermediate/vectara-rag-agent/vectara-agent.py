import re

from ragfunctions import add_chat_turn, create_chat_session
from uagents import Agent, Bureau, Context, Field, Model


class QueryRequest(Model):
    user_query: str = Field(
        description="The user's initial query to start the chat session."
    )


class ResponseData(Model):
    response: str = Field(description="The response text returned by the Vectara API.")
    chat_id: str = Field(description="The unique identifier for the chat session.")


class FollowUpQuery(Model):
    chat_id: str = Field(
        description="The unique identifier for the ongoing chat session."
    )
    follow_up_query: str = Field(
        description="The user's follow-up question for the ongoing chat."
    )


class ExitHandlerMessage(Model):
    message: str = Field(
        description="The exit message sent to the user when the chat session ends."
    )


user_agent = Agent(name="user_agent", seed="user_agent_recovery")
vectara_agent = Agent(name="vectara_agent", seed="vectara_agent_recovery")

initial_query = input("Ask your question: ").strip()


@user_agent.on_event("startup")
async def initiate_query(ctx: Context):
    ctx.logger.info("[user_agent] : Sending initial query.")
    await ctx.send(vectara_agent.address, QueryRequest(user_query=initial_query))


@user_agent.on_message(model=ResponseData, replies={FollowUpQuery, ExitHandlerMessage})
async def handle_response(ctx: Context, sender: str, msg: ResponseData):
    ctx.logger.info(f"[user_agent] : Received response: {msg.response}")
    follow_up_query = input("Ask your question: ").strip()
    if follow_up_query.lower() in {"exit", "quit"}:
        await ctx.send(sender, ExitHandlerMessage(message="Exiting chat. Goodbye!"))
    else:
        await ctx.send(
            sender, FollowUpQuery(follow_up_query=follow_up_query, chat_id=msg.chat_id)
        )


@vectara_agent.on_message(model=QueryRequest, replies=ResponseData)
async def process_initial_query(ctx: Context, sender: str, msg: QueryRequest):
    ctx.logger.info(f"[vectara_agent] : Processing initial query: {msg.user_query}")
    chat_id, response = await create_chat_session(msg.user_query, ctx)
    if chat_id and response:
        await ctx.send(sender, ResponseData(response=response, chat_id=chat_id))
    else:
        ctx.logger.error("Failed to process initial query.")


@vectara_agent.on_message(
    model=FollowUpQuery, replies={ResponseData, ExitHandlerMessage}
)
async def process_follow_up_query(ctx: Context, sender: str, msg: FollowUpQuery):
    ctx.logger.info(
        f"[vectara_agent]: Processing follow-up query for chat_id {msg.chat_id}: {msg.follow_up_query}"
    )
    chat_id, response = await add_chat_turn(msg.chat_id, msg.follow_up_query, ctx)
    if chat_id and response:
        cleaned_response = re.sub(r"\[\d+\]", "", response)
        await ctx.send(sender, ResponseData(response=cleaned_response, chat_id=chat_id))
    else:
        await ctx.send(
            sender, ExitHandlerMessage(message="Failed to process follow-up query.")
        )


@vectara_agent.on_message(model=ExitHandlerMessage)
async def handle_exit_message(ctx: Context, sender: str, msg: ExitHandlerMessage):
    ctx.logger.info(f"[vectara_agent] : {msg.message}")


bureau = Bureau()
bureau.add(user_agent)
bureau.add(vectara_agent)

if __name__ == "__main__":
    bureau.run()
