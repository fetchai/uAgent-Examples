# Claude.ai Agent

![domain:integration](https://img.shields.io/badge/integration-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNy43MzQyOSAyLjYwOTM4QzcuNzk2NzkgMi43NSA3Ljc0OTkyIDIuODkwNjIgNy42NDA1NCAzTDYuOTY4NjcgMy42MDkzOEM2Ljk4NDI5IDMuNzM0MzggNi45ODQyOSAzLjg3NSA2Ljk4NDI5IDRDNi45ODQyOSA0LjE0MDYyIDYuOTg0MjkgNC4yODEyNSA2Ljk2ODY3IDQuNDA2MjVMNy42NDA1NCA1LjAxNTYyQzcuNzQ5OTIgNS4xMDkzOCA3Ljc5Njc5IDUuMjY1NjIgNy43MzQyOSA1LjQwNjI1QzcuNjcxNzkgNS41OTM3NSA3LjU5MzY3IDUuNzY1NjIgNy40OTk5MiA1LjkzNzVMNy40MjE3OSA2LjA2MjVDNy4zMTI0MiA2LjIzNDM4IDcuMjAzMDQgNi40MDYyNSA3LjA3ODA0IDYuNTQ2ODhDNi45ODQyOSA2LjY3MTg4IDYuODI4MDQgNi43MDMxMiA2LjY4NzQyIDYuNjU2MjVMNS44MjgwNCA2LjM5MDYyQzUuNjA5MjkgNi41NDY4OCA1LjM3NDkyIDYuNjcxODggNS4xNDA1NCA2Ljc4MTI1TDQuOTM3NDIgNy42NzE4OEM0LjkwNjE3IDcuODEyNSA0Ljc5Njc5IDcuOTIxODggNC42NTYxNyA3Ljk1MzEyQzQuNDM3NDIgNy45ODQzOCA0LjIxODY3IDggMy45ODQyOSA4QzMuNzY1NTQgOCAzLjU0Njc5IDcuOTg0MzggMy4zMjgwNCA3Ljk1MzEyQzMuMTg3NDIgNy45MjE4OCAzLjA3ODA0IDcuODEyNSAzLjA0Njc5IDcuNjcxODhMMi44NDM2NyA2Ljc4MTI1QzIuNTkzNjcgNi42NzE4OCAyLjM3NDkyIDYuNTQ2ODggMi4xNTYxNyA2LjM5MDYyTDEuMjk2NzkgNi42NTYyNUMxLjE1NjE3IDYuNzAzMTIgMC45OTk5MTggNi42NzE4OCAwLjkwNjE2OCA2LjU2MjVDMC43ODExNjggNi40MDYyNSAwLjY3MTc5MyA2LjIzNDM4IDAuNTYyNDE4IDYuMDYyNUwwLjQ4NDI5MyA1LjkzNzVDMC4zOTA1NDMgNS43NjU2MiAwLjMxMjQxOCA1LjU5Mzc1IDAuMjQ5OTE4IDUuNDA2MjVDMC4xODc0MTggNS4yNjU2MiAwLjIzNDI5MyA1LjEyNSAwLjM0MzY2OCA1LjAxNTYyTDEuMDE1NTQgNC40MDYyNUMwLjk5OTkxOCA0LjI4MTI1IDAuOTk5OTE4IDQuMTQwNjIgMC45OTk5MTggNEMwLjk5OTkxOCAzLjg3NSAwLjk5OTkxOCAzLjczNDM4IDEuMDE1NTQgMy42MDkzOEwwLjM0MzY2OCAzQzAuMjM0MjkzIDIuODkwNjIgMC4xODc0MTggMi43NSAwLjI0OTkxOCAyLjYwOTM4QzAuMzEyNDE4IDIuNDIxODggMC4zOTA1NDMgMi4yNSAwLjQ4NDI5MyAyLjA3ODEyTDAuNTYyNDE4IDEuOTUzMTJDMC42NzE3OTMgMS43ODEyNSAwLjc4MTE2OCAxLjYwOTM4IDAuOTA2MTY4IDEuNDUzMTJDMC45OTk5MTggMS4zNDM3NSAxLjE1NjE3IDEuMzEyNSAxLjI5Njc5IDEuMzU5MzhMMi4xNTYxNyAxLjYyNUMyLjM3NDkyIDEuNDY4NzUgMi42MDkyOSAxLjMyODEyIDIuODQzNjcgMS4yMzQzOEwzLjA0Njc5IDAuMzQzNzVDMy4wNzgwNCAwLjIwMzEyNSAzLjE4NzQyIDAuMDkzNzUgMy4zMjgwNCAwLjA2MjVDMy41NDY3OSAwLjAzMTI1IDMuNzY1NTQgMCAzLjk5OTkyIDBDNC4yMTg2NyAwIDQuNDM3NDIgMC4wMzEyNSA0LjY1NjE3IDAuMDYyNUM0Ljc5Njc5IDAuMDc4MTI1IDQuOTA2MTcgMC4yMDMxMjUgNC45Mzc0MiAwLjM0Mzc1TDUuMTQwNTQgMS4yMzQzOEM1LjM5MDU0IDEuMzI4MTIgNS42MDkyOSAxLjQ2ODc1IDUuODI4MDQgMS42MjVMNi42ODc0MiAxLjM1OTM4QzYuODI4MDQgMS4zMTI1IDYuOTg0MjkgMS4zNDM3NSA3LjA3ODA0IDEuNDUzMTJDNy4yMDMwNCAxLjYwOTM4IDcuMzEyNDIgMS43ODEyNSA3LjQyMTc5IDEuOTUzMTJMNy40OTk5MiAyLjA3ODEyQzcuNTkzNjcgMi4yNSA3LjY3MTc5IDIuNDIxODggNy43NDk5MiAyLjYwOTM4SDcuNzM0MjlaTTMuOTk5OTIgNS4yNUM0LjQzNzQyIDUuMjUgNC44NDM2NyA1LjAxNTYyIDUuMDc4MDQgNC42MjVDNS4yOTY3OSA0LjI1IDUuMjk2NzkgMy43NjU2MiA1LjA3ODA0IDMuMzc1QzQuODQzNjcgMyA0LjQzNzQyIDIuNzUgMy45OTk5MiAyLjc1QzMuNTQ2NzkgMi43NSAzLjE0MDU0IDMgMi45MDYxNyAzLjM3NUMyLjY4NzQyIDMuNzY1NjIgMi42ODc0MiA0LjI1IDIuOTA2MTcgNC42MjVDMy4xNDA1NCA1LjAxNTYyIDMuNTQ2NzkgNS4yNSAzLjk5OTkyIDUuMjVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)
![tech:llm](https://img.shields.io/badge/llm-E85D2E?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik00LjUgMUM0LjUgMS4yMTg3NSA0LjQyMTg4IDEuNDIxODggNC4zMTI1IDEuNTc4MTJMNC43NjU2MiAyLjU2MjVDNC45MjE4OCAyLjUzMTI1IDUuMDc4MTIgMi41IDUuMjUgMi41QzUuODEyNSAyLjUgNi4zMjgxMiAyLjcxODc1IDYuNzE4NzUgMy4wNjI1TDggMi4xMDkzOEM4IDIuMDc4MTIgOCAyLjA0Njg4IDggMkM4IDEuNDUzMTIgOC40Mzc1IDEgOSAxQzkuNTQ2ODggMSAxMCAxLjQ1MzEyIDEwIDJDMTAgMi41NjI1IDkuNTQ2ODggMyA5IDNDOC44NDM3NSAzIDguNzE4NzUgMi45ODQzOCA4LjU5Mzc1IDIuOTIxODhMNy4zMTI1IDMuODU5MzhDNy40MjE4OCA0LjE0MDYyIDcuNSA0LjQzNzUgNy41IDQuNzVDNy41IDUgNy40NTMxMiA1LjIzNDM4IDcuMzc1IDUuNDUzMTJMOC41IDYuMTI1QzguNjU2MjUgNi4wNDY4OCA4LjgxMjUgNiA5IDZDOS41NDY4OCA2IDEwIDYuNDUzMTIgMTAgN0MxMCA3LjU2MjUgOS41NDY4OCA4IDkgOEM4LjQzNzUgOCA4IDcuNTYyNSA4IDdWNi45ODQzOEw2Ljg1OTM4IDYuMzEyNUM2LjQ1MzEyIDYuNzM0MzggNS44NzUgNyA1LjI1IDdDNC4xNzE4OCA3IDMuMjgxMjUgNi4yNjU2MiAzLjA0Njg4IDUuMjVIMS44NTkzOEMxLjY4NzUgNS41NjI1IDEuMzU5MzggNS43NSAxIDUuNzVDMC40Mzc1IDUuNzUgMCA1LjMxMjUgMCA0Ljc1QzAgNC4yMDMxMiAwLjQzNzUgMy43NSAxIDMuNzVDMS4zNTkzOCAzLjc1IDEuNjg3NSAzLjk1MzEyIDEuODU5MzggNC4yNUgzLjA0Njg4QzMuMTcxODggMy43MzQzOCAzLjQ1MzEyIDMuMjk2ODggMy44NTkzOCAyLjk4NDM4TDMuNDA2MjUgMkMyLjg5MDYyIDEuOTUzMTIgMi41IDEuNTMxMjUgMi41IDFDMi41IDAuNDUzMTI1IDIuOTM3NSAwIDMuNSAwQzQuMDQ2ODggMCA0LjUgMC40NTMxMjUgNC41IDFaTTUuMjUgNS41QzUuNTE1NjIgNS41IDUuNzUgNS4zNTkzOCA1Ljg5MDYyIDUuMTI1QzYuMDMxMjUgNC45MDYyNSA2LjAzMTI1IDQuNjA5MzggNS44OTA2MiA0LjM3NUM1Ljc1IDQuMTU2MjUgNS41MTU2MiA0IDUuMjUgNEM0Ljk2ODc1IDQgNC43MzQzOCA0LjE1NjI1IDQuNTkzNzUgNC4zNzVDNC40NTMxMiA0LjYwOTM4IDQuNDUzMTIgNC45MDYyNSA0LjU5Mzc1IDUuMTI1QzQuNzM0MzggNS4zNTkzOCA0Ljk2ODc1IDUuNSA1LjI1IDUuNVoiIGZpbGw9IndoaXRlIi8%2BCjwvc3ZnPgo%3D)
[![link to source code](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgents-official/tree/main/agents/claude-agent)

Claude is a personal assistant AI which excels at personal usage through repeated interaction by gathering context about the user.

In this case, the Claude.ai interface is wrapped through an agent making it accessible but without the possibility of personalisation.

## Example input

```python
TextPrompt(
    text="Compare the inflation rates of the past years in various European countries."
)
```

## Example output

```python
TextResponse(
    text="Certainly! Here's a comparison of the inflation rates in various European countries over the past few years: Inflation Rates (Annual Percentage Change): Country 2020 2021 2022 ----------------------------------------- Germany 0.4% 3.1% 7.9% France 0.5% 2.1% 5.9% Italy -0.1% 1.9% 8.0% Spain -0.3% 3.1% 8.5% United Kingdom0.9% 2.6% 9.1% Poland 3.4% 5.2% 13.9% Sweden 0.5% 2.7% 8.8% Netherlands 1.1% 2.8% 11.7% Belgium 0.4% 3.2% 9.9% Austria 1.4% 2.8% 8.6% Some key observations: - Inflation rates have generally been rising across Europe in recent years, with a significant spike in 2022. - The highest inflation rates in 2022 were seen in Poland (13.9%), the Netherlands (11.7%), and the United Kingdom (9.1%). - The lowest inflation rates in 2022 were in Germany (7.9%) and France (5.9%), though these are still relatively high historical figures. - The trend of rising inflation is widespread, with most countries seeing a substantial increase from 2020 to 2022. This data highlights the broad inflationary pressures being experienced across the European continent in the past couple of years. The specific drivers and policy responses may vary by country, but the general pattern of elevated inflation is common."
)
```

## Usage Example

The input is comparable to other agent based LLM wrappers you see on the platform. If you provide a text as input, you'll receive a text response.

```python
from uagents import Agent, Context, Model


class TextPrompt(Model):
    text: str


class TextResponse(Model):
    text: str


agent = Agent()


AI_AGENT_ADDRESS = "{{ .Agent.Address }}"

prompts = [
    "How is the weather in London today?",
    "Compare the inflation rates of the past years in various European countries.",
]


@agent.on_event("startup")
async def send_message(ctx: Context):
    for prompt in prompts:
        await ctx.send(AI_AGENT_ADDRESS, TextPrompt(text=prompt))
        ctx.logger.info(f"[Sent prompt to AI agent]: {prompt}")


@agent.on_message(TextResponse)
async def handle_response(ctx: Context, sender: str, msg: TextResponse):
    ctx.logger.info(f"[Received response from ...{sender[-8:]}]:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()
```

### Local Agent

1. Install the necessary packages:

   ```bash
   pip install requests uagents
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
