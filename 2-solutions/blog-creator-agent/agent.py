import os
from enum import Enum

from models import (
    BlogRequest,
    BlogResponse,
    ContextPrompt,
    Response,
    TopicAnalysisRequest,
    TopicAnalysisResponse,
)
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit

AGENT_NAME = os.getenv("AGENT_NAME", "Blog Creator Agent")
AGENT_SEED = os.getenv("AGENT_SEED", "your-blog-agent-seed")
TOPIC_AGENT_ADDRESS = os.getenv("topic-agent-address")
AI_AGENT_ADDRESS = os.getenv("ai-agent-address")

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
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


@proto.on_message(BlogRequest, replies={TopicAnalysisRequest})
async def handle_request(ctx: Context, sender: str, msg: TopicAnalysisResponse):
    agent_requests = agent.storage.get("agent_requests") or {}
    agent_requests[str(ctx.session)] = {
        "sender": sender,
        "Main Topic": msg.topic,
    }
    await ctx.send(TOPIC_AGENT_ADDRESS, TopicAnalysisRequest(subreddit=msg.topic))
    agent.storage.set("agent_requests", agent_requests)


@proto.on_message(TopicAnalysisResponse, replies={ContextPrompt})
async def handle_response(ctx: Context, sender: str, msg: TopicAnalysisResponse):
    agent_requests = agent.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return
    mainTopic = agent_requests[session]["Main Topic"]

    prompt = ContextPrompt(
        context="Using the provided Main Topic and Sub Topic, write a well-structured, one-page blog post in Markdown format. Ensure the content is engaging, informative, and relevant to the topic.",
        text=f"Main Topic: {mainTopic}\nSub Topic: {msg.topic}",
    )
    await ctx.send(AI_AGENT_ADDRESS, prompt)
    agent.storage.set("agent_requests", agent_requests)


@proto.on_message(Response, replies={BlogResponse})
async def handle_response2(ctx: Context, _sender: str, msg: Response):
    agent_requests = agent.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return

    await ctx.send(agent_requests[session]["sender"], BlogResponse(blog=msg.text))

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
