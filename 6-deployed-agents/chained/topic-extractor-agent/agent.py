import os
from uagents import Agent, Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from models import (
    TopicAnalysisRequest,
    TopicAnalysisResponse,
    RedditPostsRequest,
    RedditPostsResponse,
    ContextPrompt,
    Response,
)

AGENT_SEED = os.getenv("AGENT_SEED", "your-topic-agent-seed")
POSTS_AGENT_ADDRESS = os.getenv("posts-agent-address")
OPEN_AI_AGENT_ADDRESS = os.getenv("openai-agent-address")


PORT = 8000
agent = ChatAgent(
    name="Topic Extractor Agent",
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Topic-Extractor",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=3),
)

LIMIT = 500


@proto.on_message(TopicAnalysisRequest, replies={TopicAnalysisResponse})
async def handle_request(ctx: Context, sender: str, msg: TopicAnalysisRequest):
    if not POSTS_AGENT_ADDRESS:
        ctx.logger.info("POSTS_AGENT_ADDRESS is not set")
        return
    if not OPEN_AI_AGENT_ADDRESS:
        ctx.logger.info("OPEN_AI_AGENT_ADDRESS is not set")
        return

    posts_reply, posts_status = await ctx.send_and_receive(
        POSTS_AGENT_ADDRESS,
        RedditPostsRequest(limit=LIMIT, subreddit=msg.subreddit),
        response_type=RedditPostsResponse,
    )
    if not isinstance(posts_reply, RedditPostsResponse):
        await ctx.send(sender, TopicAnalysisResponse(topic=f"Posts agent failed: {posts_status}"))
        return

    combined_text = "\n\n".join(
        f"Title: {post.title}\nAuthor: {post.author}\nContent: {post.content}"
        for post in posts_reply.posts
    )

    prompt = ContextPrompt(
        context=(
            "Analyze the following Reddit posts and determine the single most common overarching "
            "topic that best represents their general theme. The topic should be concise, descriptive, "
            "and phrased as a clear, engaging title (no more than 5 words). Focus on summarizing the "
            "dominant idea or trend, avoiding generic terms, unnecessary details, or excessive specificity."
        ),
        text=combined_text,
    )

    llm_reply, llm_status = await ctx.send_and_receive(
        OPEN_AI_AGENT_ADDRESS,
        prompt,
        response_type=Response,
    )
    if not isinstance(llm_reply, Response):
        await ctx.send(sender, TopicAnalysisResponse(topic=f"LLM agent failed: {llm_status}"))
        return

    await ctx.send(sender, TopicAnalysisResponse(topic=llm_reply.text))


agent.include(proto)

if __name__ == "__main__":
    agent.run()
