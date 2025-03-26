# Tavily Search Agent

![Search](https://img.shields.io/badge/search-3D8BD3?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI5IiB2aWV3Qm94PSIwIDAgOCA5IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNi41MDk3NyAzLjI1QzYuNTA5NzcgMy45Njg3NSA2LjI3NTM5IDQuNjQwNjIgNS44ODQ3NyA1LjE3MTg4TDcuODUzNTIgNy4xNTYyNUM4LjA1NjY0IDcuMzQzNzUgOC4wNTY2NCA3LjY3MTg4IDcuODUzNTIgNy44NTkzOEM3LjY2NjAyIDguMDYyNSA3LjMzNzg5IDguMDYyNSA3LjE1MDM5IDcuODU5MzhMNS4xNjYwMiA1Ljg3NUM0LjYzNDc3IDYuMjgxMjUgMy45NjI4OSA2LjUgMy4yNTk3NyA2LjVDMS40NjI4OSA2LjUgMC4wMDk3NjU2MiA1LjA0Njg4IDAuMDA5NzY1NjIgMy4yNUMwLjAwOTc2NTYyIDEuNDY4NzUgMS40NjI4OSAwIDMuMjU5NzcgMEM1LjA0MTAyIDAgNi41MDk3NyAxLjQ2ODc1IDYuNTA5NzcgMy4yNVpNMy4yNTk3NyA1LjVDNC4wNTY2NCA1LjUgNC43OTEwMiA1LjA3ODEyIDUuMTk3MjcgNC4zNzVDNS42MDM1MiAzLjY4NzUgNS42MDM1MiAyLjgyODEyIDUuMTk3MjcgMi4xMjVDNC43OTEwMiAxLjQzNzUgNC4wNTY2NCAxIDMuMjU5NzcgMUMyLjQ0NzI3IDEgMS43MTI4OSAxLjQzNzUgMS4zMDY2NCAyLjEyNUMwLjkwMDM5MSAyLjgyODEyIDAuOTAwMzkxIDMuNjg3NSAxLjMwNjY0IDQuMzc1QzEuNzEyODkgNS4wNzgxMiAyLjQ0NzI3IDUuNSAzLjI1OTc3IDUuNVoiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo=)
![LLM](https://img.shields.io/badge/llm-E85D2E?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik00LjUgMUM0LjUgMS4yMTg3NSA0LjQyMTg4IDEuNDIxODggNC4zMTI1IDEuNTc4MTJMNC43NjU2MiAyLjU2MjVDNC45MjE4OCAyLjUzMTI1IDUuMDc4MTIgMi41IDUuMjUgMi41QzUuODEyNSAyLjUgNi4zMjgxMiAyLjcxODc1IDYuNzE4NzUgMy4wNjI1TDggMi4xMDkzOEM4IDIuMDc4MTIgOCAyLjA0Njg4IDggMkM4IDEuNDUzMTIgOC40Mzc1IDEgOSAxQzkuNTQ2ODggMSAxMCAxLjQ1MzEyIDEwIDJDMTAgMi41NjI1IDkuNTQ2ODggMyA5IDNDOC44NDM3NSAzIDguNzE4NzUgMi45ODQzOCA4LjU5Mzc1IDIuOTIxODhMNy4zMTI1IDMuODU5MzhDNy40MjE4OCA0LjE0MDYyIDcuNSA0LjQzNzUgNy41IDQuNzVDNy41IDUgNy40NTMxMiA1LjIzNDM4IDcuMzc1IDUuNDUzMTJMOC41IDYuMTI1QzguNjU2MjUgNi4wNDY4OCA4LjgxMjUgNiA5IDZDOS41NDY4OCA2IDEwIDYuNDUzMTIgMTAgN0MxMCA3LjU2MjUgOS41NDY4OCA4IDkgOEM4LjQzNzUgOCA4IDcuNTYyNSA4IDdWNi45ODQzOEw2Ljg1OTM4IDYuMzEyNUM2LjQ1MzEyIDYuNzM0MzggNS44NzUgNyA1LjI1IDdDNC4xNzE4OCA3IDMuMjgxMjUgNi4yNjU2MiAzLjA0Njg4IDUuMjVIMS44NTkzOEMxLjY4NzUgNS41NjI1IDEuMzU5MzggNS43NSAxIDUuNzVDMC40Mzc1IDUuNzUgMCA1LjMxMjUgMCA0Ljc1QzAgNC4yMDMxMiAwLjQzNzUgMy43NSAxIDMuNzVDMS4zNTkzOCAzLjc1IDEuNjg3NSAzLjk1MzEyIDEuODU5MzggNC4yNUgzLjA0Njg4QzMuMTcxODggMy43MzQzOCAzLjQ1MzEyIDMuMjk2ODggMy44NTkzOCAyLjk4NDM4TDMuNDA2MjUgMkMyLjg5MDYyIDEuOTUzMTIgMi41IDEuNTMxMjUgMi41IDFDMi41IDAuNDUzMTI1IDIuOTM3NSAwIDMuNSAwQzQuMDQ2ODggMCA0LjUgMC40NTMxMjUgNC41IDFaTTUuMjUgNS41QzUuNTE1NjIgNS41IDUuNzUgNS4zNTkzOCA1Ljg5MDYyIDUuMTI1QzYuMDMxMjUgNC45MDYyNSA2LjAzMTI1IDQuNjA5MzggNS44OTA2MiA0LjM3NUM1Ljc1IDQuMTU2MjUgNS41MTU2MiA0IDUuMjUgNEM0Ljk2ODc1IDQgNC43MzQzOCA0LjE1NjI1IDQuNTkzNzUgNC4zNzVDNC40NTMxMiA0LjYwOTM4IDQuNDUzMTIgNC45MDYyNSA0LjU5Mzc1IDUuMTI1QzQuNzM0MzggNS4zNTkzOCA0Ljk2ODc1IDUuNSA1LjI1IDUuNVoiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo=)
[![link to source code](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgent-Examples/tree/main/1-uagents/search/tavily-search-agent)
[![live](https://img.shields.io/badge/Live-8A2BE2?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik0yLjI1IDcuNUMxIDcuNSAwIDYuNSAwIDUuMjVDMCA0LjI4MTI1IDAuNjI1IDMuNDM3NSAxLjUgMy4xNDA2MkMxLjUgMy4wOTM3NSAxLjUgMy4wNDY4OCAxLjUgM0MxLjUgMS42MjUgMi42MDkzOCAwLjUgNCAwLjVDNC45MjE4OCAwLjUgNS43MzQzOCAxLjAxNTYyIDYuMTU2MjUgMS43NjU2MkM2LjM5MDYyIDEuNTkzNzUgNi42ODc1IDEuNSA3IDEuNUM3LjgyODEyIDEuNSA4LjUgMi4xNzE4OCA4LjUgM0M4LjUgMy4yMDMxMiA4LjQ1MzEyIDMuMzc1IDguMzkwNjIgMy41NDY4OEM5LjMxMjUgMy43MzQzOCAxMCA0LjU0Njg4IDEwIDUuNUMxMCA2LjYwOTM4IDkuMDkzNzUgNy41IDggNy41SDIuMjVaTTYuNzY1NjIgMy43NjU2MkM2LjkwNjI1IDMuNjI1IDYuOTA2MjUgMy4zOTA2MiA2Ljc2NTYyIDMuMjVDNi42MDkzOCAzLjA5Mzc1IDYuMzc1IDMuMDkzNzUgNi4yMzQzOCAzLjI1TDQuNSA0Ljk4NDM4TDMuNzY1NjIgNC4yNUMzLjYwOTM4IDQuMDkzNzUgMy4zNzUgNC4wOTM3NSAzLjIzNDM4IDQuMjVDMy4wNzgxMiA0LjM5MDYyIDMuMDc4MTIgNC42MjUgMy4yMzQzOCA0Ljc2NTYyTDQuMjM0MzggNS43NjU2MkM0LjM3NSA1LjkyMTg4IDQuNjA5MzggNS45MjE4OCA0Ljc2NTYyIDUuNzY1NjJMNi43NjU2MiAzLjc2NTYyWiIgZmlsbD0id2hpdGUiLz4KPC9zdmc%2BCg%3D%3D)](https://agentverse.ai/agents/details/agent1qt5uffgp0l3h9mqed8zh8vy5vs374jl2f8y0mjjvqm44axqseejqzmzx9v8/profile)

This agent uses the Tavily Search API to give you a list of results from a prompt with a focus on efficient, quick and persistent search results.

## Example input

```python
input = "What is a Fetch.ai agent?"
```

## Example output

```python
WebSearchResponse(
   query = "What is a Fetch.ai agent?"
   results = [
      WebSearchResult(
         title="Fetch.AI - Wikipedia",
         url="https://en.wikipedia.org/wiki/Fetch.AI",
         content="Fetch.AI is an open-source decentralized machine-learning platform for creating autonomous economic agents. Using blockchain datasets, these agents operate on behalf of their owners, learning what preferences they seek in any given decision or transaction and making those decisions on their behalf. [4][11][12][13][1][14][9]",
      ),
      WebSearchResult(
         title="Fetch.ai Explained: The Google of AI Agents - YouTube",
         url="https://www.youtube.com/watch?v=XFEKsYFIH_k",
         content="What is Fetch.ai? Fetch.ai is a Cambridge-based AI company redefining the possibilities of an intelligent and connected world through its AI agent-based tech...",
      ),
      WebSearchResult(
         title="What Is Fetch.ai (FET)? Features and Tokenomics - CoinMarketCap",
         url="https://coinmarketcap.com/academy/article/what-is-fetch-ai-fet-features-tokenomics-and-price-prediction",
         content="Fetch.Ai Tokenomics. Fetch.ai (FET) aims to create a decentralized network of autonomous agents that can communicate, collaborate and learn from each other using artificial intelligence (AI) and machine learning (ML). It was founded in 2017 by a team of experts in AI, blockchain and software engineering. The FET token was launched in an initial ...",
      ),
      WebSearchResult(
         title="A Beginner's Journey into AI with Fetch.ai: Exploring the AI Agents ...",
         url="https://medium.com/fetch-ai/a-beginners-journey-into-ai-with-fetch-ai-exploring-the-ai-agents-part-1-f14dca532c92",
         content="Fetch.ai harnesses the power of intelligent agents to craft a vibrant and dynamic ecosystem, pushing the boundaries of what AI can achieve. Fetch.ai defines AI agents as autonomous programs ...",
      ),
      WebSearchResult(
         title="Agent Anatomy. IBM defines autonomous agents as… | by Fetch.ai - Medium",
         url="https://medium.com/fetch-ai/agent-anatomy-419048a5399b",
         content="What makes Fetch.ai's Autonomous Economic Agents unique? Structurally, agents are composed of three core components: Runtime — for an agent to deliver value, the Runtime fetches packages from ...",
      ),
   ]
)
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.

```python
import os
from typing import List

from uagents import Agent, Context, Model


class WebSearchRequest(Model):
    query: str


class WebSearchResult(Model):
    title: str
    url: str
    content: str


class WebSearchResponse(Model):
    query: str
    results: List[WebSearchResult]


agent = Agent()

AI_AGENT_ADDRESS = "{{ .Agent.Address }}"

prompt = "What is a Fetch.ai agent?"


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    """Send the prompt to the AI agent on startup."""
    await ctx.send(AI_AGENT_ADDRESS, WebSearchRequest(query=prompt))
    ctx.logger.info(f"Sent prompt to AI agent: {prompt}")


@agent.on_message(WebSearchResponse)
async def handle_response(ctx: Context, sender: str, msg: WebSearchResponse):
    """Do something with the response."""
    ctx.logger.info(f"Received response from: {sender}")
    ctx.logger.info(msg.results)


if __name__ == "__main__":
    agent.run()
```

### Local Agent

1. Install the necessary packages:

   ```bash
   pip install uagents
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
