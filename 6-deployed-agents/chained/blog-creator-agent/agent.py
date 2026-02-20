import os
from uagents import Agent, Context
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from models import (
    TopicAnalysisRequest,
    TopicAnalysisResponse,
    BlogRequest,
    BlogResponse,
    ContextPrompt,
    Response,
)

AGENT_SEED = os.getenv("AGENT_SEED", "your-blog-agent-seed")
TOPIC_AGENT_ADDRESS = os.getenv("topic-agent-address")
AI_AGENT_ADDRESS = os.getenv("ai-agent-address")

PORT = 8000
agent = ChatAgent(
    name="Blog Creator Agent",
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Blog-Creation",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=3),
)

BLOG_INSTRUCTION = (
    "Using the provided Main Topic and Sub Topic, write a well-structured, one-page blog post "
    "in Markdown format. Ensure the content is engaging, informative, and relevant to the topic."
)

@proto.on_message(BlogRequest, replies={BlogResponse})
async def handle_request(ctx: Context, sender: str, msg: BlogRequest):
    # Extract main topic from BlogRequest (supports common field names)
    main_topic = getattr(msg, "topic", None) or getattr(msg, "main_topic", None)
    if not main_topic:
        await ctx.send(sender, BlogResponse(blog="Missing main topic in BlogRequest."))
        return

    if not TOPIC_AGENT_ADDRESS:
        ctx.logger.info("TOPIC_AGENT_ADDRESS is not set")
        return
    if not AI_AGENT_ADDRESS:
        ctx.logger.info("AI_AGENT_ADDRESS is not set")
        return

    topic_reply, topic_status = await ctx.send_and_receive(
        TOPIC_AGENT_ADDRESS,
        TopicAnalysisRequest(subreddit=main_topic),
        response_type=TopicAnalysisResponse,
    )
    if not isinstance(topic_reply, TopicAnalysisResponse):
        await ctx.send(sender, BlogResponse(blog=f"Topic agent failed: {topic_status}"))
        return

    sub_topic = getattr(topic_reply, "topic", None)
    if not sub_topic:
        await ctx.send(sender, BlogResponse(blog="Topic agent response missing expected field 'topic'."))
        return

    prompt = ContextPrompt(
        context=BLOG_INSTRUCTION,
        text=f"Main Topic: {main_topic}\nSub Topic: {sub_topic}",
    )
    llm_reply, llm_status = await ctx.send_and_receive(
        AI_AGENT_ADDRESS,
        prompt,
        response_type=Response,
    )
    if not isinstance(llm_reply, Response):
        await ctx.send(sender, BlogResponse(blog=f"AI agent failed: {llm_status}"))
        return

    blog_text = getattr(llm_reply, "text", None)
    if not isinstance(blog_text, str) or not blog_text.strip():
        await ctx.send(sender, BlogResponse(blog="AI agent returned empty blog text."))
        return

    await ctx.send(sender, BlogResponse(blog=blog_text))


agent.include(proto)

if __name__ == "__main__":
    agent.run()