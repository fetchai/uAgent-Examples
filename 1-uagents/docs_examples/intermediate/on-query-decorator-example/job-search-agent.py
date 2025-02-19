# import required libraries
import json

import aiohttp
from uagents import Agent, Context, Model


# Define Request and Response Data Models
class Request(Model):
    query: str


class Response(Model):
    response: str


# Define asynchronous function to handle job search queries using a serpapi url
async def get_job_summary(query: str, location: str, api_key: str):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query + " careers",
        "location": location,
        "engine": "google_jobs",
        "api_key": api_key,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                jobs = data.get("jobs_results", [])
                if jobs:
                    job = jobs[0] if jobs else None  # Ensuring there is a job to report
                    if not job:
                        return "No job details available."
                    res_str = json.dumps(
                        {
                            "Title": job.get("title", "N/A"),
                            "Company": job.get("company_name", "N/A"),
                            "Location": job.get("location", "N/A"),
                            "Link": job.get("link", "N/A"),
                            "Posted": job.get("detected_extensions", {}).get(
                                "posted_at", "N/A"
                            ),
                            "Type": job.get("detected_extensions", {}).get(
                                "schedule_type", "N/A"
                            ),
                            "Description": job.get("description", "N/A"),
                        },
                        indent=2,
                    )
                    return res_str
                else:
                    return "No job results found."
            else:
                return f"Failed to fetch data: {response.status}"


# Define Search Agent
SearchAgent = Agent(
    name="SearchAgent",
    port=8000,
    seed="<YOUR_AGENT_SECRET_PHRASE>",
    endpoint=["http://127.0.0.1:8000/submit"],
)  # Update your agent's secret phrase


# On agent startup printing address
@SearchAgent.on_event("startup")
async def agent_details(ctx: Context):
    ctx.logger.info(f"Search Agent Address is {SearchAgent.address}")


# On_query decorator to handle jobs request
@SearchAgent.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, msg: Request):
    ctx.logger.info("Query received")
    try:
        ctx.logger.info(f"Fetching job details for query: {msg.query}")
        response = await get_job_summary(
            msg.query,
            "United Kingdom",
            "<YOUR_SERPAPI_API_KEY_HERE>",  # Update your serpapi API key
        )  # Replace your serpAPI key.
        ctx.logger.info(f"Response: {response}")
        await ctx.send(sender, Response(response=response))
    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, Response(response=str(error_message)))


if __name__ == "__main__":
    SearchAgent.run()
