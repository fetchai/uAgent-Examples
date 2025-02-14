# Slack Agent

![Alt](https://img.shields.io/badge/integration-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNy43MzQyOSAyLjYwOTM4QzcuNzk2NzkgMi43NSA3Ljc0OTkyIDIuODkwNjIgNy42NDA1NCAzTDYuOTY4NjcgMy42MDkzOEM2Ljk4NDI5IDMuNzM0MzggNi45ODQyOSAzLjg3NSA2Ljk4NDI5IDRDNi45ODQyOSA0LjE0MDYyIDYuOTg0MjkgNC4yODEyNSA2Ljk2ODY3IDQuNDA2MjVMNy42NDA1NCA1LjAxNTYyQzcuNzQ5OTIgNS4xMDkzOCA3Ljc5Njc5IDUuMjY1NjIgNy43MzQyOSA1LjQwNjI1QzcuNjcxNzkgNS41OTM3NSA3LjU5MzY3IDUuNzY1NjIgNy40OTk5MiA1LjkzNzVMNy40MjE3OSA2LjA2MjVDNy4zMTI0MiA2LjIzNDM4IDcuMjAzMDQgNi40MDYyNSA3LjA3ODA0IDYuNTQ2ODhDNi45ODQyOSA2LjY3MTg4IDYuODI4MDQgNi43MDMxMiA2LjY4NzQyIDYuNjU2MjVMNS44MjgwNCA2LjM5MDYyQzUuNjA5MjkgNi41NDY4OCA1LjM3NDkyIDYuNjcxODggNS4xNDA1NCA2Ljc4MTI1TDQuOTM3NDIgNy42NzE4OEM0LjkwNjE3IDcuODEyNSA0Ljc5Njc5IDcuOTIxODggNC42NTYxNyA3Ljk1MzEyQzQuNDM3NDIgNy45ODQzOCA0LjIxODY3IDggMy45ODQyOSA4QzMuNzY1NTQgOCAzLjU0Njc5IDcuOTg0MzggMy4zMjgwNCA3Ljk1MzEyQzMuMTg3NDIgNy45MjE4OCAzLjA3ODA0IDcuODEyNSAzLjA0Njc5IDcuNjcxODhMMi44NDM2NyA2Ljc4MTI1QzIuNTkzNjcgNi42NzE4OCAyLjM3NDkyIDYuNTQ2ODggMi4xNTYxNyA2LjM5MDYyTDEuMjk2NzkgNi42NTYyNUMxLjE1NjE3IDYuNzAzMTIgMC45OTk5MTggNi42NzE4OCAwLjkwNjE2OCA2LjU2MjVDMC43ODExNjggNi40MDYyNSAwLjY3MTc5MyA2LjIzNDM4IDAuNTYyNDE4IDYuMDYyNUwwLjQ4NDI5MyA1LjkzNzVDMC4zOTA1NDMgNS43NjU2MiAwLjMxMjQxOCA1LjU5Mzc1IDAuMjQ5OTE4IDUuNDA2MjVDMC4xODc0MTggNS4yNjU2MiAwLjIzNDI5MyA1LjEyNSAwLjM0MzY2OCA1LjAxNTYyTDEuMDE1NTQgNC40MDYyNUMwLjk5OTkxOCA0LjI4MTI1IDAuOTk5OTE4IDQuMTQwNjIgMC45OTk5MTggNEMwLjk5OTkxOCAzLjg3NSAwLjk5OTkxOCAzLjczNDM4IDEuMDE1NTQgMy42MDkzOEwwLjM0MzY2OCAzQzAuMjM0MjkzIDIuODkwNjIgMC4xODc0MTggMi43NSAwLjI0OTkxOCAyLjYwOTM4QzAuMzEyNDE4IDIuNDIxODggMC4zOTA1NDMgMi4yNSAwLjQ4NDI5MyAyLjA3ODEyTDAuNTYyNDE4IDEuOTUzMTJDMC42NzE3OTMgMS43ODEyNSAwLjc4MTE2OCAxLjYwOTM4IDAuOTA2MTY4IDEuNDUzMTJDMC45OTk5MTggMS4zNDM3NSAxLjE1NjE3IDEuMzEyNSAxLjI5Njc5IDEuMzU5MzhMMi4xNTYxNyAxLjYyNUMyLjM3NDkyIDEuNDY4NzUgMi42MDkyOSAxLjMyODEyIDIuODQzNjcgMS4yMzQzOEwzLjA0Njc5IDAuMzQzNzVDMy4wNzgwNCAwLjIwMzEyNSAzLjE4NzQyIDAuMDkzNzUgMy4zMjgwNCAwLjA2MjVDMy41NDY3OSAwLjAzMTI1IDMuNzY1NTQgMCAzLjk5OTkyIDBDNC4yMTg2NyAwIDQuNDM3NDIgMC4wMzEyNSA0LjY1NjE3IDAuMDYyNUM0Ljc5Njc5IDAuMDc4MTI1IDQuOTA2MTcgMC4yMDMxMjUgNC45Mzc0MiAwLjM0Mzc1TDUuMTQwNTQgMS4yMzQzOEM1LjM5MDU0IDEuMzI4MTIgNS42MDkyOSAxLjQ2ODc1IDUuODI4MDQgMS42MjVMNi42ODc0MiAxLjM1OTM4QzYuODI4MDQgMS4zMTI1IDYuOTg0MjkgMS4zNDM3NSA3LjA3ODA0IDEuNDUzMTJDNy4yMDMwNCAxLjYwOTM4IDcuMzEyNDIgMS43ODEyNSA3LjQyMTc5IDEuOTUzMTJMNy40OTk5MiAyLjA3ODEyQzcuNTkzNjcgMi4yNSA3LjY3MTc5IDIuNDIxODggNy43NDk5MiAyLjYwOTM4SDcuNzM0MjlaTTMuOTk5OTIgNS4yNUM0LjQzNzQyIDUuMjUgNC44NDM2NyA1LjAxNTYyIDUuMDc4MDQgNC42MjVDNS4yOTY3OSA0LjI1IDUuMjk2NzkgMy43NjU2MiA1LjA3ODA0IDMuMzc1QzQuODQzNjcgMyA0LjQzNzQyIDIuNzUgMy45OTk5MiAyLjc1QzMuNTQ2NzkgMi43NSAzLjE0MDU0IDMgMi45MDYxNyAzLjM3NUMyLjY4NzQyIDMuNzY1NjIgMi42ODc0MiA0LjI1IDIuOTA2MTcgNC42MjVDMy4xNDA1NCA1LjAxNTYyIDMuNTQ2NzkgNS4yNSAzLjk5OTkyIDUuMjVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)
[![Alt](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgents-official)

This agent is designed to send direct messages on Slack. Given a Slack user ID and a message, it delivers the message to the specified user. Note that recipients must belong to the workspace associated with the provided Slack token, follow these steps to set it up:

## Setup Slack Token

To configure a Slack token for sending messages within a workspace, follow these steps:

## 1. Create a Slack App

1. Go to the [Slack API Dashboard](https://api.slack.com/apps).
2. Click **Create an App**.
3. Choose "From scratch" and provide a name for your app.
4. Select the workspace where the app will be used.

## 2. Set up Bot Permissions

1. In your app dashboard, go to **OAuth & Permissions**.
2. Under **Scopes**, add the following **Bot Token Scopes** to allow the app to send messages:
   - `chat:write` – Required to send messages to channels.
   - `im:write` – Required to send direct messages to users.
3. Click **Save Changes**.

## 3. Install the App

1. Go to **Install App** in the sidebar.
2. Click **Install to Workspace**.
3. Authorize the app in your workspace.
4. Copy the **Bot User OAuth Token** (e.g., `xoxb-...`). This token is used to authenticate your bot.

## Deploy Slack Agent

To deploy Slack agent, copy and paste the code from `agent.py` into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) and run it, make sure to include your slack token

## Interact with Slack Agent

To interact with the Slack Agent, a user agent needs to send the target **Slack user ID** and a **message**, both on string format. To get the **Slack user ID** go to any of the profiles on your workspace, select **View full profile**, click on the 3 dots and select **Copy member ID**, you can start testing with your own ID!

Now copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent), replace the **Slack user ID** and the **Slack gent address** you deployed in the previous step

```python
from uagents import Agent, Context, Model

class SlackMessageRequest(Model):
    id: str
    text: str


class SlackMessageResponse(Model):
    text: str


agent = Agent()


SLACK_AGENT_ADDRESS = "<slack_agent_address>"
USERID = "target_user_id"
MSG = "Hello from slack Agent!"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(SLACK_AGENT_ADDRESS, SlackMessageRequest(id=USERID, text=MSG))
    ctx.logger.info(f"Sent request to Slack Agent")


@agent.on_message(SlackMessageResponse)
async def handle_response(ctx: Context, sender: str, msg: SlackMessageResponse):
    ctx.logger.info(f"Received response from {sender[-10:]}:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()
```

After running this user agent, the target user will see the message sent by a Slack bot.

### Local Agent

You can run all of this locally by following these steps for both Slack agent and User agent

1. Install the necessary packages:

   ```bash
   pip install uagents
   ```

2. To perform this interaction from local agents, replace `agent = Agent()` in both user and slack agent with:

   ```python
   agent = Agent(
       name="user", # or SlackAgent
       endpoint="http://localhost:8001/submit", # http://localhost:8000/submit for SlackAgent
   )
   ```

3. Run both agents:
   ```bash
   python agent.py
   python user.py
   ```
