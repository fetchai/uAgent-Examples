# Website Validation Agent

![domain:utility](https://img.shields.io/badge/utility-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iNiIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgNiA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMS41MDk3NyAwQzEuNzc1MzkgMCAyLjAwOTc3IDAuMjM0Mzc1IDIuMDA5NzcgMC41VjJIMS4wMDk3N1YwLjVDMS4wMDk3NyAwLjIzNDM3NSAxLjIyODUyIDAgMS41MDk3NyAwWk00LjUwOTc3IDBDNC43NzUzOSAwIDUuMDA5NzcgMC4yMzQzNzUgNS4wMDk3NyAwLjVWMkg0LjAwOTc3VjAuNUM0LjAwOTc3IDAuMjM0Mzc1IDQuMjI4NTIgMCA0LjUwOTc3IDBaTTAuNTA5NzY2IDIuNUg1LjUwOTc3QzUuNzc1MzkgMi41IDYuMDA5NzcgMi43MzQzOCA2LjAwOTc3IDNDNi4wMDk3NyAzLjI4MTI1IDUuNzc1MzkgMy41IDUuNTA5NzcgMy41VjRDNS41MDk3NyA1LjIxODc1IDQuNjUwMzkgNi4yMTg3NSAzLjUwOTc3IDYuNDUzMTJWNy41QzMuNTA5NzcgNy43ODEyNSAzLjI3NTM5IDggMy4wMDk3NyA4QzIuNzI4NTIgOCAyLjUwOTc3IDcuNzgxMjUgMi41MDk3NyA3LjVWNi40NTMxMkMxLjM2OTE0IDYuMjE4NzUgMC41MDk3NjYgNS4yMTg3NSAwLjUwOTc2NiA0VjMuNUMwLjIyODUxNiAzLjUgMC4wMDk3NjU2MiAzLjI4MTI1IDAuMDA5NzY1NjIgM0MwLjAwOTc2NTYyIDIuNzM0MzggMC4yMjg1MTYgMi41IDAuNTA5NzY2IDIuNVoiIGZpbGw9IndoaXRlIi8%2BCjwvc3ZnPgo%3D)
![tech:crew](https://img.shields.io/badge/crew-E85D2E?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTYuMDY3NDUgMC45NjE0MDNDNi42NzU1MSAxLjY3MjM1IDYuNjMxNTEgMi43NzY5NSA2LjE2OTkxIDMuNTc2NzdDNy4yNTUxIDMuNjQ1MTUgNy4zMDM0MiA1LjA1NDEgNi44NDAzMSA1Ljc3ODY0QzYuMzc2OTggNi41MDI5NiA1LjgzMzQyIDcuMDMxMjEgNS4wNjQ4OCA3LjQ1NDQyQzQuMjk2MzQgNy44Nzc2MiAzLjEzNTY1IDguMTI0ODEgMi4yNDI2NSA3LjkzNTQzQzEuMzQ5NDQgNy43NDYyNiAwLjY5MjQxNCA3LjI3MDY0IDAuMjgzMDE0IDYuNDQzODZDLTAuMTI2NjAxIDUuNjE3MyAtMC4wNTg2NTUxIDQuNDAwMzEgMC4yNzY1NDMgMy41NzIwMkMwLjYxMTUyNiAyLjc0MzUyIDAuOTYwOTYxIDIuMDc2NTcgMS41NzAxIDEuNDE0MzdDMi4xNzk0NSAwLjc1MjM4OSAyLjc2MTYzIDAuMjg5OTI3IDMuNjQ3NzMgMC4wNjIzNjMyQzQuNTMzODIgLTAuMTY0OTg1IDUuNDU5MzkgMC4yNTA2NyA2LjA2NzQ1IDAuOTYxNDAzWk0zLjM1OTM1IDAuOTAyMDgyQzMuMzc1ODkgMC44OTQ5MTEgMy4zOTI1OCAwLjg4Nzg1NyAzLjQwOTQ0IDAuODgwOTE5QzMuNjc5MDYgMC43NzAyNjUgNC4wNDAzNiAwLjY0MTA2IDQuMzU4MDkgMC42ODYzNTdDNC42MzQxOCAwLjcyNTgzIDQuODk1NCAwLjg3MjI5MSA1LjEyOTIyIDEuMDM2ODdDNS4zNjMwNCAxLjIwMTQ1IDUuNTI2NzUgMS4zNzI3MiA1LjY5MDQ3IDEuNjE4ODNDNS44NTQxOSAxLjg2NDk0IDUuODg3ODQgMi4yNjc4NyA1LjgwMzUgMi41NjMxN0M1LjcyMjUgMi44NDY1NiA1LjYyMyAzLjA2MzkgNS41MDAwMiAzLjMzMjVDNS40OTQ5NSAzLjM0MzU4IDUuNDg5ODQgMy4zNTQ3NCA1LjQ4NDY5IDMuMzY2QzUuNDQ1ODQgMy40NTA5MyA1LjQwNzczIDMuNTI3NjIgNS4zNzA4MiAzLjYwMTkxQzUuMjg0MTcgMy43NzYyOSA1LjIwNDEgMy45Mzc0NCA1LjEzNjMzIDQuMTYwODZDNS4xMDM5OCA0LjI2NzIgNS4wMzkxMiA0LjMzNTMxIDQuOTU4NzYgNC4zNzA4NUM0Ljc5ODU0IDQuNDQxNzQgNC41NzY2OCA0LjM4MzE0IDQuNDI4MTMgNC4yNDAwNUM0LjQyMjc2IDQuMjM0ODkgNC40MTc0MyA0LjIyOTc2IDQuNDEyMTQgNC4yMjQ2N0M0LjE5NzM2IDQuMDE4MTYgNC4wNDE4NyAzLjg2ODY0IDMuOTkxNzcgMy41NTQ3N0MzLjk1MjY3IDMuMzA5NjcgNC4wMjU5MiAzLjA4NjcxIDQuMTAxOTUgMi44NTUzMkM0LjEyNTc1IDIuNzgyODggNC4xNDk4MiAyLjcwOTYyIDQuMTcwOCAyLjYzNDU5QzQuMjEzMDkgMi40ODMzNCA0LjI3NjAyIDIuMzc1MTQgNC4zMzk5MyAyLjI2NTIzQzQuNDA5IDIuMTQ2NDUgNC40NzkyMyAyLjAyNTY4IDQuNTI1ODQgMS44NDY0MkM0LjU4MDE3IDEuNjM3MzQgNC40MjI5MiAxLjYyNTYxIDQuMjU2NDMgMS42OTkzMUM0LjE0Nzk1IDEuNzQ3MzQgNC4wMzU1NSAxLjgzMTY0IDMuOTc1MjIgMS45MjEyNEMzLjkwMjI2IDIuMDI5MzQgMy44MTE3OCAyLjExNTUxIDMuNzIxMzUgMi4yMDE2M0MzLjYyMTk3IDIuMjk2MjggMy41MjI2NSAyLjM5MDg2IDMuNDQ2NzUgMi41MTQ0MkMzLjM4MDc5IDIuNjIxOTEgMy4zMDgyMSAyLjcyMDczIDMuMjM1MzIgMi44MTk5N0MzLjE0ODA1IDIuOTM4OCAzLjA2MDM0IDMuMDU4MjQgMi45ODMgMy4xOTM4N0MyLjg4MjEyIDMuMzcwMzggMi43OTY0NSAzLjU0MDAzIDIuNzA1OTQgMy43MTkyN0MyLjY2ODkyIDMuNzkyNTkgMi42MzEwOCAzLjg2NzUxIDIuNTkxMDcgMy45NDUxNkMyLjQ1MzI0IDQuMjEyNDEgMi4zOTUgNC41MzMxNiAyLjM3MzY0IDQuODQ5MzdDMi4zNTIyOSA1LjE2NTU5IDIuMzQ0MzEgNS41MTMwOCAyLjU0MDgxIDUuNzgyMjhDMi43Mzc1MyA2LjA1MTI2IDMuMDc2MTggNi4wNTQ5MiAzLjM4NzQ0IDYuMDM1NzNDMy42OTg2OSA2LjAxNjUzIDQuMDIwNTIgNS45Mjc0NSA0LjI5ODEyIDUuODI0NzdDNC4zMDc2NSA1LjgyMTI2IDQuMzE3MTIgNS44MTc2OCA0LjMyNjUxIDUuODE0MDVDNC4zNzc4IDUuNzk0MTggNC40MjcwNiA1Ljc3MjUzIDQuNDc0OCA1Ljc0OTQ1QzQuNjQ0MzEgNS42Njc0NyA0Ljc5NDczIDUuNTY3MzUgNC45NDkyMiA1LjQ2NDUyQzQuOTc1NDcgNS40NDcwNSA1LjAwMTgzIDUuNDI5NSA1LjAyODQyIDUuNDExOTVDNS4xNjMwMSA1LjMyMzI1IDUuMjY5NTkgNS4yMDY5IDUuMzczNzggNS4wOTMxNUM1LjQ1MTc3IDUuMDA4MDEgNS41Mjg0MiA0LjkyNDMyIDUuNjE0NDggNC44NTQ3OUM1LjY4OTg2IDQuNzkzODMgNS43NDM3OCA0LjY5NDQxIDUuNzk3OTUgNC41OTQ1NUM1Ljg2NjYxIDQuNDY3OTYgNS45MzU2NiA0LjM0MDY2IDYuMDQ5MyA0LjI5MDA1QzYuMDg0ODUgNC4yNzQyMSA2LjEyNDc3IDQuMjY1ODcgNi4xNzA0IDQuMjY3NDJDNi40NzcxMyA0LjI3Nzk4IDYuNDY2NTYgNC44NTYyOCA2LjM4NTg5IDUuMDg2ODZDNi4zMDUyMiA1LjMxNzQ0IDYuMTUyNSA1LjYxOTY0IDUuOTc3NTcgNS44MjE3NUM1LjgwMjYzIDYuMDIzODYgNS42MTg0MyA2LjIxMjgyIDUuMzk5OTIgNi4zODczMkM1LjE4MTYzIDYuNTYxODIgNC45ODkwMSA2LjcwNzIgNC43MzEyNSA2Ljg0MDI5QzQuNzI5MTQgNi44NDEzOCA0LjcyNzAzIDYuODQyNDYgNC43MjQ5MiA2Ljg0MzU1QzQuNTY2MDEgNi45MjU0NCA0LjQwNTc4IDYuOTk5MjggNC4yMzc5MSA3LjA2NDYxQzQuMTM1ODcgNy4xMDQzMiA0LjAzMSA3LjE0MDkgMy45MjE4OCA3LjE3NDIyQzMuNjMwNjggNy4yNjMwOSAzLjIzNTA5IDcuMzEwOTggMi45MTI4MyA3LjMwODM5QzIuNTkwNTggNy4zMDU4IDIuMjQ1MDMgNy4yNTE2NiAxLjk2MjI0IDcuMTM3MzRDMS42Nzk0NiA3LjAyMzIzIDEuNDg1NzYgNi44ODgyIDEuMjc4NDcgNi42Nzc4OUMxLjA3MTE4IDYuNDY3NTkgMC45NDU4NjIgNi4yNjIyNCAwLjgzNTIwOCA1Ljk3Nzk1QzAuNzI0NTUzIDUuNjkzODcgMC42NzczMTUgNS4yOTk1NyAwLjY5MTEyIDQuOTc4ODJDMC43MDQ5MjQgNC42NTgwOCAwLjc1NzEyNCA0LjMwNDMzIDAuODQ5MjI4IDQuMDE1MjlDMC45NDExMTYgMy43MjYyNSAxLjA1MDY5IDMuNDY2OTggMS4xODU1IDMuMjA4MzVDMS4zMjA1MyAyLjk0OTk0IDEuNDQ4MjMgMi43MTgwNyAxLjYwMzUzIDIuNDgzMTdDMS43NTkwNSAyLjI0ODQ5IDEuOTA4MSAyLjA2NTM2IDIuMDk4NTYgMS44NTY1NkMyLjI4ODgxIDEuNjQ3NTUgMi40NzA2NSAxLjQ4MDU5IDIuNjkxNzQgMS4zMDY1MkMyLjg2OTg3IDEuMTY2MTEgMy4wNTE5MSAxLjA0NzY3IDMuMjU2ODMgMC45NDg5NjZDMy4yOTAzNiAwLjkzMjgxMyAzLjMyNDUxIDAuOTE3MTg4IDMuMzU5MzUgMC45MDIwODJaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)
[![link to source code](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgent-Examples/tree/main/1-uagents/utility/website-validation-agent)
[![live](https://img.shields.io/badge/Live-8A2BE2?logo=elixir
)](https://agentverse.ai)

This agent ensure that your website is error-free and fully functional. This system checks for typos and identifies invalid links, providing a detailed report to help you maintain a high-quality website.

## Features

- **Typo Detection**: The agent scans your website content to identify and suggest corrections for any typos.
- **Invalid Link Detection**: The agent checks for invalid links throughout your website, ensuring all links are valid.
- **Comprehensive Reporting**: Receive detailed reports highlighting typos and invalid links, allowing you to address issues promptly.

## Example input

```python
WebsiteValidationInput(
   website_url="https://fetch.ai"
)
```

## Example output

```python
WebsiteValidationResponse(
    invalid_links=[],
    grammar_mistakes=[
        GrammarMistake(
            error="Fetch AI: Open platform to build AI Apps & Services",
            solution="Fetch.ai: An open platform to build AI apps and services.",
        ),
        GrammarMistake(
            error="A tech stack for devs with capabilities to",
            solution="A tech stack for developers with capabilities to",
        ),
        GrammarMistake(
            error="Creating AI platforms and services that let anyone build and deploy AI services at scale, anytime and anywhere.",
            solution="Creating AI platforms and services that allow anyone to build and deploy AI services at scale, anytime and anywhere.",
        ),
        GrammarMistake(
            error="Updates from the company and what’s happening within the community.",
            solution="Updates from the company and what is happening within the community.",
        ),
        GrammarMistake(
            error="Introducing the new Guest Lectures Series: Exploring AI Agents with Fetch.ai in collaboration with Fetch.ai Foundation partners",
            solution="Introducing the new Guest Lectures Series: Exploring AI agents with Fetch.ai in collaboration with Fetch.ai Foundation partners.",
        ),
    ],
)
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.

```python
from uagents import Agent, Context, Model

agent = Agent()

AI_AGENT_ADDRESS = "<deployed_agent_address>"


class WebsiteValidationInput(Model):
    website_url: str


class GrammarMistake(Model):
    error: str
    solution: str


class WebsiteValidationResponse(Model):
    invalid_links: list[str]
    grammar_mistakes: list[GrammarMistake]


website = "https://fetch.ai"


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    """Send the prompt to the AI agent on startup."""
    await ctx.send(AI_AGENT_ADDRESS, WebsiteValidationInput(website_url=website))
    ctx.logger.info(f"Sent prompt to AI agent: {website}")


@agent.on_message(WebsiteValidationResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteValidationResponse):
    """Do something with the response."""
    ctx.logger.info(f"Received response from: {sender}:")
    ctx.logger.info(msg)


if __name__ == "__main__":
    agent.run()
```

### Local Agent

1. Install the necessary packages:

   ```bash
   pip install uagents openai langchain crewai validators
   ```

2. To interact with this agent from a local agent instead, replace `agent = Agent()` in the above with:

   ```python
   agent = Agent(
       name="user",
       endpoint="http://localhost:8000/submit",
   )
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```

## Usage Allowance

Each agent is allowed to make up to 6 requests per hour from this agent.
