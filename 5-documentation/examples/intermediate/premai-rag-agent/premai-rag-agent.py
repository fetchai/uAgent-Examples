import re
import os
from uagents import Field, Model, Context, Agent, Bureau
from premai import Prem

REPO_ID = os.getenv("REPO_ID")
PROJECT_ID = os.getenv("PROJECT_ID")
API_KEY = os.getenv("API_KEY")

prem_client = Prem(api_key=API_KEY)

def query_prem_ai(user_query):
    """
    Handles both initial and follow-up queries by calling Prem.ai API.
    """
    try:
        messages = [{"role": "user", "content": user_query}]
        repositories = dict(ids=[REPO_ID], similarity_threshold=0.25, limit=5)
        response = prem_client.chat.completions.create(
            project_id=PROJECT_ID,
            messages=messages,
            repositories=repositories,
            stream=False,
            model="gpt-4o",
        )
        final_response = response.choices[0].message.content
        cleaned_response = re.sub(r'\[\d+\]', '', final_response)
        return cleaned_response
    except Exception as e:
        raise RuntimeError(f"Error querying Prem.ai: {e}")


class HealthQuery(Model):
    user_query: str = Field(description="The user's initial or follow-up query about health and wellness.")

class HealthResponse(Model):
    response: str = Field(description="The response text returned by the Prem.ai API.")

class ExitMessage(Model):
    message: str = Field(description="The exit message sent to the user when the chat session ends.")

user_agent = Agent(name="health_user_agent", seed="health_user_recovery")
prem_agent = Agent(name="health_prem_agent", seed="health_prem_recovery")

initial_query = input("Ask your health and wellness question: ").strip()

@user_agent.on_event("startup")
async def send_health_query(ctx: Context):
    ctx.logger.info("[health_user_agent]: Sending initial query.")
    await ctx.send(prem_agent.address, HealthQuery(user_query=initial_query))

@user_agent.on_message(model=HealthResponse, replies={HealthQuery, ExitMessage})
async def handle_health_response(ctx: Context, sender: str, msg: HealthResponse):
    ctx.logger.info(f"[health_user_agent]: Received response: {msg.response}")
    follow_up_query = input("Ask your next question (or type 'exit' to quit): ").strip()
    if follow_up_query.lower() in {"exit", "quit"}:
        await ctx.send(sender, ExitMessage(message="Exiting chat. Goodbye!"))
    else:
        await ctx.send(sender, HealthQuery(user_query=follow_up_query))


@prem_agent.on_message(model=HealthQuery, replies={HealthResponse, ExitMessage})
async def process_health_query(ctx: Context, sender: str, msg: HealthQuery):
    ctx.logger.info(f"[health_prem_agent]: Processing query: {msg.user_query}")
    try:
        response = query_prem_ai(msg.user_query)
        await ctx.send(sender, HealthResponse(response=response))
    except RuntimeError as e:
        await ctx.send(sender, ExitMessage(message="Failed to process query."))

@prem_agent.on_message(model=ExitMessage)
async def handle_exit_message(ctx: Context, sender: str, msg: ExitMessage):
    ctx.logger.info(f"[health_prem_agent]: {msg.message}")

bureau = Bureau(port=8000, endpoint="http://localhost:8000/submit")
bureau.add(user_agent)
bureau.add(prem_agent)

if __name__ == "__main__":
    bureau.run()
