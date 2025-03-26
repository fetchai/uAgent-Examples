import os
from enum import Enum
from typing import Optional

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "github-repository-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Github Repositories Agent")


class GitHubRepoRequest(Model):
    organisation_name: str


class GitHubRepo(Model):
    name: str
    url: str
    description: Optional[str]
    language: Optional[str]
    created_at: str
    stars: int
    forks: int
    open_issues: int


class GitHubRepoResponse(Model):
    repo_list: list[GitHubRepo]


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


github_repo_protocol = QuotaProtocol(
    storage_reference=agent.storage,
    name="Github Repositories",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def get_git_repos(org_name):
    """
    Fetches all GitHub repositories for a given organization and returns them as a JSON string.

    Args:
        org_name (str): The GitHub organization name.

    Returns:
        str: A JSON string with the repository information.
             Returns an error message if an error occurs.
    """
    repos = []
    page = 1
    per_page = 30  # Number of repositories per page
    try:
        while True:
            response = requests.get(
                url=f"https://api.github.com/orgs/{org_name}/repos?per_page={per_page}&page={page}",
                timeout=10,
            )

            if response.status_code == 200:
                current_repos = response.json()
                if not current_repos:
                    break  # Exit if there are no more repositories

                repos.extend(current_repos)
                page += 1  # Move to the next page
            else:
                return {"error": f"Error: {response.status_code} - {response.text}"}

        # Convert the repositories into a structured JSON format
        repo_list = []
        if repos:
            for repo in repos:
                repo_list.append(
                    GitHubRepo(
                        name=repo["name"],
                        url=repo["html_url"],
                        description=repo["description"],
                        language=repo["language"],
                        created_at=repo["created_at"],
                        stars=repo["stargazers_count"],
                        forks=repo["forks_count"],
                        open_issues=repo["open_issues_count"],
                    )
                )

        return {"repositories": repo_list}

    except requests.Timeout as e:
        return {"error": f"Request timed out: {str(e)}"}
    except requests.RequestException as e:
        return {"error": f"An error occurred during the request: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@github_repo_protocol.on_message(model=GitHubRepoRequest, replies=GitHubRepoResponse)
async def on_message(ctx: Context, sender: str, msg: GitHubRepoRequest):
    ctx.logger.info(f"Received organisation name: {msg.organisation_name}")
    try:
        repos = get_git_repos(msg.organisation_name)

        if "error" in repos:
            await ctx.send(sender, ErrorMessage(error=repos["error"]))
            return

    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))
        return

    await ctx.send(
        sender,
        GitHubRepoResponse(repo_list=repos["repositories"]),
    )


agent.include(github_repo_protocol)


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
