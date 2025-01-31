# Email Agent

![domain:utility](https://img.shields.io/badge/utility-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iNiIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgNiA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMS41MDk3NyAwQzEuNzc1MzkgMCAyLjAwOTc3IDAuMjM0Mzc1IDIuMDA5NzcgMC41VjJIMS4wMDk3N1YwLjVDMS4wMDk3NyAwLjIzNDM3NSAxLjIyODUyIDAgMS41MDk3NyAwWk00LjUwOTc3IDBDNC43NzUzOSAwIDUuMDA5NzcgMC4yMzQzNzUgNS4wMDk3NyAwLjVWMkg0LjAwOTc3VjAuNUM0LjAwOTc3IDAuMjM0Mzc1IDQuMjI4NTIgMCA0LjUwOTc3IDBaTTAuNTA5NzY2IDIuNUg1LjUwOTc3QzUuNzc1MzkgMi41IDYuMDA5NzcgMi43MzQzOCA2LjAwOTc3IDNDNi4wMDk3NyAzLjI4MTI1IDUuNzc1MzkgMy41IDUuNTA5NzcgMy41VjRDNS41MDk3NyA1LjIxODc1IDQuNjUwMzkgNi4yMTg3NSAzLjUwOTc3IDYuNDUzMTJWNy41QzMuNTA5NzcgNy43ODEyNSAzLjI3NTM5IDggMy4wMDk3NyA4QzIuNzI4NTIgOCAyLjUwOTc3IDcuNzgxMjUgMi41MDk3NyA3LjVWNi40NTMxMkMxLjM2OTE0IDYuMjE4NzUgMC41MDk3NjYgNS4yMTg3NSAwLjUwOTc2NiA0VjMuNUMwLjIyODUxNiAzLjUgMC4wMDk3NjU2MiAzLjI4MTI1IDAuMDA5NzY1NjIgM0MwLjAwOTc2NTYyIDIuNzM0MzggMC4yMjg1MTYgMi41IDAuNTA5NzY2IDIuNVoiIGZpbGw9IndoaXRlIi8%2BCjwvc3ZnPgo%3D)

The deployed version of this agent allows you to send text messages comprising of a text body and subject to your registered email address. The owner of the agent sending the request will receive the email if agentverse.ai has been logged into at least once.

## Example input

```python
EmailSendRequest(
   subject="automated email response",
   body="content to be sent via mail",
)
```

## Example output

```python
EmailStatusResponse(
   status_code=200
) # in case everything works as intended
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.

```python
from uagents import Agent, Context, Model


class EmailSendRequest(Model):
    subject: str
    body: str


class EmailStatusResponse(Model):
    status_code: int
    errors: dict = {}


agent = Agent()


EMAIL_AGENT_ADDRESS = "agent1qvw8gy6c7uc6xn5tvhwqmzelugyqal0fvhe73tahcg5q7638qqn2z8h33t9"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(
        EMAIL_AGENT_ADDRESS,
        EmailSendRequest(
            subject="automated email response",
            body="content to be sent via mail",
        ),
    )
    ctx.logger.info("Sent email request to agent.")


@agent.on_message(EmailStatusResponse)
async def handle_response(ctx: Context, sender: str, msg: EmailStatusResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg)


if __name__ == "__main__":
    agent.run()
```

### Local Agent

1. Install the necessary packages:

   ```bash
   pip install uagents
   ```

2. To interact with this agent from a local agent instead, replace `agent = Agent()` in the above with the following and make sure that your agent is reachable:

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
