"""
THIS IS A REFERENCE IMPLEMENTATION.

The code of this agent is not the actual implementation of the Email Agent as
it requires sensitive information to be provided in order to send emails.

The deployed agent will send an email to the owner of the agent that sends
the request.
"""

import os
import smtplib
from email.mime.text import MIMEText
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_NAME = os.getenv("AGENT_NAME", "Email Agent")
AGENT_SEED = os.getenv("AGENT_SEED")

GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")
assert GOOGLE_APP_PASSWORD, "GOOGLE_APP_PASSWORD is required to send emails."

EMAIL_RECIPIENT = "<insert-email-address>"

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


class EmailSendRequest(Model):
    subject: str
    body: str


class EmailStatusResponse(Model):
    status_code: int
    errors: dict = {}


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Custom-Email-Sender-Forwarder",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def send_email(subject, body) -> dict:
    errs = {}
    sender = GOOGLE_EMAIL
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = EMAIL_RECIPIENT
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, GOOGLE_APP_PASSWORD)
        errs = smtp_server.sendmail(sender, EMAIL_RECIPIENT, msg.as_string())
    return errs


@proto.on_message(EmailSendRequest, replies={EmailStatusResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: EmailSendRequest):
    """
    This code differs from the actual implementation of the Email Agent.
    (see note at the top of the file)

    This agent will:
        - receive an email request,
        - invoke sending the email to the user.
    """
    response = EmailStatusResponse(status_code=200)

    errs = send_email(msg.subject, msg.body)
    if errs:
        response = EmailStatusResponse(status_code=500, errors=errs)

    await ctx.send(sender, response)


agent.include(proto)


# Health Check code
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
