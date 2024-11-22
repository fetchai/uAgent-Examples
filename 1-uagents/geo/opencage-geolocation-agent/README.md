# Opencage Geolocation Agent

![domain:geo](https://img.shields.io/badge/geo-3D8BD3?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNiIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgNiA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMy4zNjkxNCA3LjgxMjVDMy4xODE2NCA4LjA0Njg4IDIuODIyMjcgOC4wNDY4OCAyLjYzNDc3IDcuODEyNUMxLjgzNzg5IDYuNzk2ODggMC4wMDk3NjU2MiA0LjM3NSAwLjAwOTc2NTYyIDNDMC4wMDk3NjU2MiAxLjM0Mzc1IDEuMzUzNTIgMCAzLjAwOTc3IDBDNC42NjYwMiAwIDYuMDA5NzcgMS4zNDM3NSA2LjAwOTc3IDNDNi4wMDk3NyA0LjM3NSA0LjE4MTY0IDYuNzk2ODggMy4zNjkxNCA3LjgxMjVaTTMuMDA5NzcgMkMyLjY1MDM5IDIgMi4zMjIyNyAyLjIwMzEyIDIuMTM0NzcgMi41QzEuOTYyODkgMi44MTI1IDEuOTYyODkgMy4yMDMxMiAyLjEzNDc3IDMuNUMyLjMyMjI3IDMuODEyNSAyLjY1MDM5IDQgMy4wMDk3NyA0QzMuMzUzNTIgNCAzLjY4MTY0IDMuODEyNSAzLjg2OTE0IDMuNUM0LjA0MTAyIDMuMjAzMTIgNC4wNDEwMiAyLjgxMjUgMy44NjkxNCAyLjVDMy42ODE2NCAyLjIwMzEyIDMuMzUzNTIgMiAzLjAwOTc3IDJaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)
[![link to source code](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgent-Examples/tree/main/1-uagents/geo/opencage-geolocation-agent)
[![live](https://img.shields.io/badge/Live-8A2BE2?logo=elixir
)](https://agentverse.ai/agents/details/agent1qgtaj7emyccjrhce8xh0dmxltu6akurkddhttr58krafq55vpf9vjwtcdqn/profile)

This agent is a simple agent that returns the geocode of a given address.
It uses the Opencage API to get the latitude and longitude of a given address.

## Example input

```python
GeolocationRequest(
    address="Kings Cross Station, London",
)
```

## Example output

```python
GeolocationResponse(
    latitude=51.5317606,
    longitude=-0.1246769,
)
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.

```python
from uagents import Agent, Context, Model


class GeolocationRequest(Model):
    address: str


class GeolocationResponse(Model):
    latitude: float
    longitude: float


agent = Agent()


AI_AGENT_ADDRESS = "<deployed_agent_address>"


address = "Kings Cross Station, London"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, GeolocationRequest(address=address))
    ctx.logger.info(f"Sent address to Geolocation agent: {address}")


@agent.on_message(GeolocationResponse)
async def handle_response(ctx: Context, sender: str, msg: GeolocationResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")


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

3. You need to load the environment variable manually using `os.getenv("OPENCAGE_API_KEY")`
   To get API key please visit [OPENCAGE](https://opencagedata.com/).

4. Run the agent:
   ```bash
   python agent.py
   ```
