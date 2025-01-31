import os
from enum import Enum

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "github-PR-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Github Pull Requests Agent")


class GitHubPRRequest(Model):
    organisation_name: str
    repo_name: str


class GitHubPR(Model):
    title: str
    url: str
    user: str
    created_at: str


class GitHubPRResponse(Model):
    pr_list: list[GitHubPR]


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


github_pr_protocol = QuotaProtocol(
    storage_reference=agent.storage,
    name="Github Pull Requests",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def get_open_prs(org_name, repo_name) -> dict:
    """
    Fetches all open pull requests for a given GitHub repository in an organization and returns them as a JSON string.

    Args:
        org_name (str): The GitHub organization name.
        repo_name (str): The GitHub repository name.

    Returns:
        str: A JSON string with the pull request information. Returns an error message if an error occurs.
    """
    prs = []
    page = 1
    per_page = 30  # Number of pull requests per page
    try:
        while True:
            response = requests.get(
                url=f"https://api.github.com/repos/{org_name}/{repo_name}/pulls?state=open&per_page={per_page}&page={page}",
                timeout=10,
            )

            if response.status_code == 200:
                current_prs = response.json()
                if not current_prs:
                    break  # Exit if there are no more pull requests

                prs.extend(current_prs)
                page += 1  # Move to the next page
            else:
                return {"error": f"Error: {response.status_code} - {response.text}"}

        # Convert the pull requests into a structured JSON format
        pr_list = []
        if prs:
            for pr in prs:
                pr_list.append(
                    GitHubPR(
                        title=pr["title"],
                        url=pr["html_url"],
                        user=pr["user"]["login"],
                        created_at=pr["created_at"],
                    )
                )

        return {"pull_requests": pr_list}

    except requests.Timeout as e:
        return {"error": f"Request timed out: {str(e)}"}
    except requests.RequestException as e:
        return {"error": f"An error occurred during the request: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@github_pr_protocol.on_message(model=GitHubPRRequest, replies=GitHubPRResponse)
async def on_message(ctx: Context, sender: str, msg: GitHubPRRequest):
    ctx.logger.info(
        f"Received organisation name: {msg.organisation_name}, repo name: {msg.repo_name}"
    )
    try:
        prs = get_open_prs(msg.organisation_name, msg.repo_name)
        if "error" in prs:
            await ctx.send(sender, ErrorMessage(error=prs["error"]))
            return

    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))
        return

    await ctx.send(sender, GitHubPRResponse(pr_list=prs["pull_requests"]))


agent.include(github_pr_protocol)


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
