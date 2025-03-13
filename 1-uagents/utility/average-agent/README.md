# Average Agent

![domain:utility](https://img.shields.io/badge/utility-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iNiIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgNiA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMS41MDk3NyAwQzEuNzc1MzkgMCAyLjAwOTc3IDAuMjM0Mzc1IDIuMDA5NzcgMC41VjJIMS4wMDk3N1YwLjVDMS4wMDk3NyAwLjIzNDM3NSAxLjIyODUyIDAgMS41MDk3NyAwWk00LjUwOTc3IDBDNC43NzUzOSAwIDUuMDA5NzcgMC4yMzQzNzUgNS4wMDk3NyAwLjVWMkg0LjAwOTc3VjAuNUM0LjAwOTc3IDAuMjM0Mzc1IDQuMjI4NTIgMCA0LjUwOTc3IDBaTTAuNTA5NzY2IDIuNUg1LjUwOTc3QzUuNzc1MzkgMi41IDYuMDA5NzcgMi43MzQzOCA2LjAwOTc3IDNDNi4wMDk3NyAzLjI4MTI1IDUuNzc1MzkgMy41IDUuNTA5NzcgMy41VjRDNS41MDk3NyA1LjIxODc1IDQuNjUwMzkgNi4yMTg3NSAzLjUwOTc3IDYuNDUzMTJWNy41QzMuNTA5NzcgNy43ODEyNSAzLjI3NTM5IDggMy4wMDk3NyA4QzIuNzI4NTIgOCAyLjUwOTc3IDcuNzgxMjUgMi41MDk3NyA3LjVWNi40NTMxMkMxLjM2OTE0IDYuMjE4NzUgMC41MDk3NjYgNS4yMTg3NSAwLjUwOTc2NiA0VjMuNUMwLjIyODUxNiAzLjUgMC4wMDk3NjU2MiAzLjI4MTI1IDAuMDA5NzY1NjIgM0MwLjAwOTc2NTYyIDIuNzM0MzggMC4yMjg1MTYgMi41IDAuNTA5NzY2IDIuNVoiIGZpbGw9IndoaXRlIi8%2BCjwvc3ZnPgo%3D)
[![link to source code](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgent-Examples/tree/main/1-uagents/utility/average-agent)
[![live](https://img.shields.io/badge/Live-8A2BE2?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik0yLjI1IDcuNUMxIDcuNSAwIDYuNSAwIDUuMjVDMCA0LjI4MTI1IDAuNjI1IDMuNDM3NSAxLjUgMy4xNDA2MkMxLjUgMy4wOTM3NSAxLjUgMy4wNDY4OCAxLjUgM0MxLjUgMS42MjUgMi42MDkzOCAwLjUgNCAwLjVDNC45MjE4OCAwLjUgNS43MzQzOCAxLjAxNTYyIDYuMTU2MjUgMS43NjU2MkM2LjM5MDYyIDEuNTkzNzUgNi42ODc1IDEuNSA3IDEuNUM3LjgyODEyIDEuNSA4LjUgMi4xNzE4OCA4LjUgM0M4LjUgMy4yMDMxMiA4LjQ1MzEyIDMuMzc1IDguMzkwNjIgMy41NDY4OEM5LjMxMjUgMy43MzQzOCAxMCA0LjU0Njg4IDEwIDUuNUMxMCA2LjYwOTM4IDkuMDkzNzUgNy41IDggNy41SDIuMjVaTTYuNzY1NjIgMy43NjU2MkM2LjkwNjI1IDMuNjI1IDYuOTA2MjUgMy4zOTA2MiA2Ljc2NTYyIDMuMjVDNi42MDkzOCAzLjA5Mzc1IDYuMzc1IDMuMDkzNzUgNi4yMzQzOCAzLjI1TDQuNSA0Ljk4NDM4TDMuNzY1NjIgNC4yNUMzLjYwOTM4IDQuMDkzNzUgMy4zNzUgNC4wOTM3NSAzLjIzNDM4IDQuMjVDMy4wNzgxMiA0LjM5MDYyIDMuMDc4MTIgNC42MjUgMy4yMzQzOCA0Ljc2NTYyTDQuMjM0MzggNS43NjU2MkM0LjM3NSA1LjkyMTg4IDQuNjA5MzggNS45MjE4OCA0Ljc2NTYyIDUuNzY1NjJMNi43NjU2MiAzLjc2NTYyWiIgZmlsbD0id2hpdGUiLz4KPC9zdmc%2BCg%3D%3D)](https://agentverse.ai/agents/details/agent1qvtnt9s6uhua3c3jundxrpgqjsy9quc2h4s83anjg6r2m95g90dn2ruw8zm/profile)

This agent accepts a list type object (e.g. tuple, list, set) of integer and/or float values, and calculates different mathematical averages and deviations from them.

## Example input

```python
Prompt(
    data=(-3, 5, 8, -2, 4, 6, 8, 3, 5, 12)
)
```

## Example output

```python
Response(
    mean=4.6,
    median=5.0,
    median_low=5.0,
    median_high=5.0,
    mode=5.0,
    multi_mode=[5, 8],
    population_variance=18.44,
    sample_variance=20.488888888888887,
    population_standard_deviation=4.294182110716778,
    sample_standard_deviation=4.526465385804788,
)
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.


```python
from uagents import Agent, Context, Model
from typing import Union, List, Set, Tuple


class Prompt(Model):
    data: Union[Tuple[Union[int, float]], List[Union[int, float]], Set[Union[int, float]]]


class Response(Model):
    mean: float
    median: float
    median_low: float
    median_high: float
    mode: float
    multi_mode: List[Union[int, float]]
    population_variance: float
    sample_variance: float
    population_standard_deviation: float
    sample_standard_deviation: float


agent = Agent()


AVERAGE_AGENT_ADDRESS = "{{ .Agent.Address }}"

prompts = [
    (1, 6, 3, 7, 2, 5, 8, 3, 5, 12),  # tuple
    [-3, 5, 8, -2, 4, 6, 8, 3, 5, 12],  # list
    set([1.5, 6.3, 3.7, -7.2, 2.9, 5.8, 8.3, -5.5, 12.1]),  # set
]


@agent.on_event("startup")
async def send_message(ctx: Context):
    m = ctx.storage.get("matrix") or {}
    for prompt in prompts:
        await ctx.send(AVERAGE_AGENT_ADDRESS, Prompt(data=prompt))
        ctx.logger.info(f"Sent prompt to AI agent: {prompt}")
        m[str(ctx.session)] = {"prompt": list(prompt)}
    ctx.storage.set("matrix", m)


@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    m = ctx.storage.get("matrix") or {}
    ctx.logger.info(f"Received response: {msg}")
    if str(ctx.session) not in m:  # this should never happen
        ctx.logger.error("Session not found in storage.")
        return
    m[str(ctx.session)]["response"] = msg.dict()
    ctx.storage.set("matrix", m)


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

