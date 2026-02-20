# Weather Agent

![domain:utility](https://img.shields.io/badge/utility-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iNiIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgNiA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMS41MDk3NyAwQzEuNzc1MzkgMCAyLjAwOTc3IDAuMjM0Mzc1IDIuMDA5NzcgMC41VjJIMS4wMDk3N1YwLjVDMS4wMDk3NyAwLjIzNDM3NSAxLjIyODUyIDAgMS41MDk3NyAwWk00LjUwOTc3IDBDNC43NzUzOSAwIDUuMDA5NzcgMC4yMzQzNzUgNS4wMDk3NyAwLjVWMkg0LjAwOTc3VjAuNUM0LjAwOTc3IDAuMjM0Mzc1IDQuMjI4NTIgMCA0LjUwOTc3IDBaTTAuNTA5NzY2IDIuNUg1LjUwOTc3QzUuNzc1MzkgMi41IDYuMDA5NzcgMi43MzQzOCA2LjAwOTc3IDNDNi4wMDk3NyAzLjI4MTI1IDUuNzc1MzkgMy41IDUuNTA5NzcgMy41VjRDNS41MDk3NyA1LjIxODc1IDQuNjUwMzkgNi4yMTg3NSAzLjUwOTc3IDYuNDUzMTJWNy41QzMuNTA5NzcgNy43ODEyNSAzLjI3NTM5IDggMy4wMDk3NyA4QzIuNzI4NTIgOCAyLjUwOTc3IDcuNzgxMjUgMi41MDk3NyA3LjVWNi40NTMxMkMxLjM2OTE0IDYuMjE4NzUgMC41MDk3NjYgNS4yMTg3NSAwLjUwOTc2NiA0VjMuNUMwLjIyODUxNiAzLjUgMC4wMDk3NjU2MiAzLjI4MTI1IDAuMDA5NzY1NjIgM0MwLjAwOTc2NTYyIDIuNzM0MzggMC4yMjg1MTYgMi41IDAuNTA5NzY2IDIuNVoiIGZpbGw9IndoaXRlIi8%2BCjwvc3ZnPgo%3D)
[![Alt](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgents-official/tree/main/agents/weather-agent)

This agent is a simple agent that returns the information about the current temperature, weather conditions, humidity, and wind speed for a specified location. It uses the Weather API to get the weather forecast of a given location.

## Example input

```python
WeatherForecastRequest(
    location="London"
)
```

## Example output

```python
WeatherForecastResponse(
    location="London",
    temp=" 19.3°C",
    condition="Partly cloudy",
    humidity="46%",
    wind_speed="13.0 kph",
)
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.

```python
from uagents import Agent, Context, Model


class WeatherForecastRequest(Model):
    location: str = Field(
        description="Location", 
    )


class WeatherForecastResponse(Model):
    location: str
    temp: float
    condition: str
    humidity: float
    wind_speed: float


agent = Agent()

AI_AGENT_ADDRESS = "<deployed_agent_address>"

location = "London"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, WeatherForecastRequest(location=location))
    ctx.logger.info(f"Sent request to weather agent: {location}")


@agent.on_message(WeatherForecastResponse)
async def handle_response(ctx: Context, sender: str, msg: WeatherForecastResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.text)


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
