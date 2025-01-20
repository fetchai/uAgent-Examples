import os

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

SLACK_URL = "https://slack.com/api"

class SlackMessageRequest(Model):
    id: str
    text: str


class SlackMessageResponse(Model):
    text: str


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)

proto = Protocol(name="Slack-Protocol", version="0.1.0")

def open_dm_channel(user_id):
    try:
        response = requests.post(
            f"{SLACK_URL}/conversations.open",
            headers={
                "Authorization": f"Bearer {SLACK_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"users": user_id}
        )

        if response.status_code == 200 and response.json().get("ok", False):
            channel_id = response.json()["channel"]["id"]
            return channel_id
        else:
            return (
                f"Failed to open DM channel: {response.json().get('error', 'Unknown error')}"
            )
    except Exception as e:
        return "Error encountered: " + str(e)

def send_message(channel, message):
    try:
        response = requests.post(
            f"{SLACK_URL}/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "channel": channel,
                "text": message
            }
        )

        if response.status_code == 200 and response.json().get("ok", False):
            return (f"Message sent successfully: {response.json()['ts']}")
        else:
            return (
                f"Failed to send message: {response.json().get('error', 'Unknown error')}"
            )
    except Exception as e:
        return "Error encountered: " + str(e)

rate_limiter = RateLimiter(agent.storage)

@proto.on_message(SlackMessageRequest, replies={SlackMessageResponse, ErrorMessage})
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: SlackMessageRequest):
    try:
        dm_channel_id = open_dm_channel(msg.id)
        if not dm_channel_id:
            error_message = f"Failed to open DM channel for user ID {msg.id}"
            ctx.logger.error(error_message)
            await ctx.send(sender, ErrorMessage(error=error_message))
        else:
            status = send_message(dm_channel_id, msg.text)
            await ctx.send(sender, SlackMessageResponse(text=status))
    except Exception as err:
        ctx.logger.error(f"Unexpected error occurred: {err}")
        await ctx.send(sender, ErrorMessage(error=f"An error occurred: {str(err)}"))


agent.include(proto, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
