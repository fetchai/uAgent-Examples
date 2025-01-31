import os
from enum import Enum

from models import (
    ContextPrompt,
    RedditPostsRequest,
    RedditPostsResponse,
    Response,
    TopicAnalysisRequest,
    TopicAnalysisResponse,
)
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit

AGENT_NAME = os.getenv("AGENT_NAME", "Topic Extractor Agent")
AGENT_SEED = os.getenv("AGENT_SEED", "your-topic-agent-seed")
POSTS_AGENT_ADDRESS = os.getenv("posts-agent-address")
OPEN_AI_AGENT_ADDRESS = os.getenv("openai-agent-address")


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
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


@proto.on_message(TopicAnalysisRequest, replies={RedditPostsRequest})
async def handle_request(ctx: Context, sender: str, msg: TopicAnalysisRequest):
    agent_requests = agent.storage.get("agent_requests") or {}
    agent_requests[str(ctx.session)] = {
        "sender": sender,
    }
    await ctx.send(
        POSTS_AGENT_ADDRESS, RedditPostsRequest(limit=LIMIT, subreddit=msg.subreddit)
    )
    agent.storage.set("agent_requests", agent_requests)


@proto.on_message(RedditPostsResponse, replies={ContextPrompt})
async def handle_posts_response(ctx: Context, sender: str, msg: RedditPostsResponse):
    combined_text = "\n\n".join(
        f"Title: {post.title}\nAuthor: {post.author}\nContent: {post.content}"
        for post in msg.posts
    )

    prompt = ContextPrompt(
        context="Analyze the following Reddit posts and determine the single most common overarching topic that best represents their general theme. The topic should be concise, descriptive, and phrased as a clear, engaging title (no more than 5 words). Focus on summarizing the dominant idea or trend, avoiding generic terms, unnecessary details, or excessive specificity.",
        text=combined_text,
    )

    await ctx.send(OPEN_AI_AGENT_ADDRESS, prompt)


@agent.on_message(Response, replies={TopicAnalysisResponse})
async def handle_response(ctx: Context, sender: str, msg: Response):
    agent_requests = agent.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return
    await ctx.send(
        agent_requests[session]["sender"], TopicAnalysisResponse(topic=msg.text)
    )
    agent_requests.pop(session)
    agent.storage.set("agent_requests", agent_requests)


agent.include(proto)


# Health Check code
class HealthCheck(Model):
    pass


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class AgentHealth(Model):
    agent_name: str
    status: HealthStatus


health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)


@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    await ctx.send(
        sender, AgentHealth(agent_name=AGENT_NAME, status=HealthStatus.HEALTHY)
    )


agent.include(health_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
