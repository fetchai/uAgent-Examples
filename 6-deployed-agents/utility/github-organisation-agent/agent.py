import os
from enum import Enum

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "github-organisation-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Github Organisation Agent")


class GitHubOrganisationRequest(Model):
    organisation_name: str


class GitHubOrganisationResponse(Model):
    name: str
    description: str
    created_at: str
    blog: str
    location: str
    public_repos: int
    followers: int
    twitter_username: str
    is_verified: bool


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

github_organisation_protocol = QuotaProtocol(
    storage_reference=agent.storage,
    name="Github Organisation",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def get_details(org_name):
    """
    Retrieves details about an organisation from Github.

    Args:
        org_name (str): Organisation Name for which data needs to be retrieved.

    Returns:
        dict: A dictionary containing the details of the organization.
    """
    try:
        response = requests.get(
            url=f"https://api.github.com/orgs/{org_name}",
            timeout=10,
        )

        if response.status_code == 200:
            org_info = response.json()
            # Create a dictionary with individual fields
            org_details = {
                "name": org_info.get("name") or "N/A",
                "description": org_info.get("description") or "N/A",
                "created_at": org_info.get("created_at") or "N/A",
                "blog": org_info.get("blog") or "N/A",
                "location": org_info.get("location") or "N/A",
                "public_repos": org_info.get("public_repos", 0),
                "followers": org_info.get("followers", 0),
                "twitter_username": org_info.get("twitter_username") or "N/A",
                "is_verified": org_info.get("is_verified", False),
            }
            return org_details
        return {"error": f"Error fetching organisation details: {response.reason}"}

    except requests.Timeout:
        return {
            "error": "Request timed out. Check your internet connection or try again later."
        }
    except requests.RequestException as e:
        return {"error": f"An error occurred during the request: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@github_organisation_protocol.on_message(
    model=GitHubOrganisationRequest, replies=GitHubOrganisationResponse
)
async def on_message(ctx: Context, sender: str, msg: GitHubOrganisationRequest):
    ctx.logger.info(f"Received organisation name: {msg.organisation_name}")
    try:
        org_details = get_details(msg.organisation_name)

        if "error" in org_details:
            await ctx.send(sender, ErrorMessage(error=org_details["error"]))
            return

        # Unpack the JSON and send it as a response
        await ctx.send(
            sender,
            GitHubOrganisationResponse(
                name=org_details["name"],
                description=org_details["description"],
                created_at=org_details["created_at"],
                blog=org_details["blog"],
                location=org_details["location"],
                public_repos=org_details["public_repos"],
                followers=org_details["followers"],
                twitter_username=org_details["twitter_username"],
                is_verified=org_details["is_verified"],
            ),
        )

    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))
        return


agent.include(github_organisation_protocol, publish_manifest=True)


### Health check related code
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
