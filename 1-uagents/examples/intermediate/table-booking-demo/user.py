from protocols.book import BookTableRequest, BookTableResponse
from protocols.query import (
    QueryTableRequest,
    QueryTableResponse,
)
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
 
RESTAURANT_ADDRESS = "agent1qw50wcs4nd723ya9j8mwxglnhs2kzzhh0et0yl34vr75hualsyqvqdzl990"
 
user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
fund_agent_if_low(user.wallet.address())
 
table_query = QueryTableRequest(
    guests=3,
    time_start=19,
    duration=2,
)
 
# This on_interval agent function performs a request on a defined period
@user.on_interval(period=3.0, messages=QueryTableRequest)
async def interval(ctx: Context):
    completed = ctx.storage.get("completed")
 
    if not completed:
        await ctx.send(RESTAURANT_ADDRESS, table_query)
 
@user.on_message(QueryTableResponse, replies={BookTableRequest})
async def handle_query_response(ctx: Context, sender: str, msg: QueryTableResponse):
    if len(msg.tables) > 0:
        ctx.logger.info("There is a free table, attempting to book one now")
 
        table_number = msg.tables[0]
 
        request = BookTableRequest(
            table_number=table_number,
            time_start=table_query.time_start,
            duration=table_query.duration,
        )
 
        await ctx.send(sender, request)
 
    else:
 
        ctx.logger.info("No free tables - nothing more to do")
        ctx.storage.set("completed", True)
 
@user.on_message(BookTableResponse, replies=set())
async def handle_book_response(ctx: Context, _sender: str, msg: BookTableResponse):
    if msg.success:
        ctx.logger.info("Table reservation was successful")
 
    else:
        ctx.logger.info("Table reservation was UNSUCCESSFUL")
 
    ctx.storage.set("completed", True)
 
if __name__ == "__main__":
    user.run()