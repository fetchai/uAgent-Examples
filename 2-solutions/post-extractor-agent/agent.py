import os
import requests
from datetime import datetime
from enum import Enum
from uagents import Agent, Context, Model, Protocol
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


AGENT_NAME = "Post Extractor Agent"
AGENT_SEED = os.getenv("AGENT_SEED", "your-post-agent-seed")
REDDIT_ID = os.getenv("REDDIT_ID_KEY")
REDDIT_SECRET = os.getenv("REDDIT_SECRET_KEY")
REDDIT_USER = os.getenv("REDDIT_USER_KEY")


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Post-Extractor",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)

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
                created=datetime.fromtimestamp(post_data["created_utc"]).isoformat(),
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

### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.

    For example, check if the agent can connect to a third party API,
    check if the agent has enough resources, etc.
    """
    condition = True  # TODO: logic here
    return bool(condition)


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
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
