import os
import requests
from enum import Enum
from datetime import datetime
from uagents import Agent, Context, Model, Protocol
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit

class RedditPostsRequest(Model):
    limit: int
    subreddit: str
    time_range: str = "week"

class RedditPost(Model):
    title: str
    author: str
    url: str
    content: str

class RedditPostsResponse(Model):
    posts: list[RedditPost]


AGENT_SEED = os.getenv("AGENT_SEED", "your-post-agent-seed")
AGENT_NAME = os.getenv("AGENT_NAME", "Post Extractor Agent")
REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER = os.getenv("REDDIT_USER")


PORT = 8000
agent = ChatAgent(
    name="Post Extractor Agent",
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = Protocol(name="Post-Extractor", version="0.1.0")


auth = requests.auth.HTTPBasicAuth(REDDIT_ID, REDDIT_SECRET)
data = {
    "grant_type": "client_credentials"
}
headers = {
    "User-Agent": REDDIT_USER
}

response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
response.raise_for_status()
access_token = response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}",
    "User-Agent": REDDIT_USER
}

@proto.on_message(RedditPostsRequest, replies={RedditPostsResponse})
async def handle_request(ctx: Context, sender: str, msg: RedditPostsRequest):
    url = f"https://oauth.reddit.com/r/{msg.subreddit}/top"
    params = {"limit": 100, "t": msg.time_range} 

    posts = []
    remaining_posts = msg.limit
    after = None

    while remaining_posts > 0:
        if after:
            params["after"] = after

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        posts_data = response.json()["data"]["children"]

        for post in posts_data:
            post_data = post["data"]
            reddit_post = RedditPost(
                title=post_data["title"],
                author=post_data["author"],
                url=post_data["url"],
                content=post_data["selftext"] if post_data["selftext"] else "[No text content]",
            )

            posts.append(reddit_post)

            remaining_posts -= 1
            if remaining_posts == 0:
                break

        after = response.json()["data"].get("after")
        if not after:
            break

    await ctx.send(sender, RedditPostsResponse(posts=posts))

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