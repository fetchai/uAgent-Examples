# Import Required libraries
import aiohttp
from bs4 import BeautifulSoup
from uagents import Agent, Context, Model


# Define data Models to handle request
class wrapRequest(Model):
    url: str


class Message(Model):
    message: str


class wrapResponse(Model):
    summary: str


class ErrorResponse(Model):
    error: str


# Define webscraper Agent
webScraperAgent = Agent(
    name="Web Scraper Agent",
    port=8001,
    seed="Web Scraper Agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)


# Define function to scrap webpage and get paragraph content.
async def get_webpage_content(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, "html.parser")

                    for script_or_style in soup(
                        ["script", "style", "header", "footer", "nav", "aside"]
                    ):
                        script_or_style.decompose()

                    text_blocks = soup.find_all("p")
                    text_content = " ".join(
                        block.get_text(strip=True)
                        for block in text_blocks
                        if block.get_text(strip=True)
                    )

                    words = text_content.split()
                    limited_text = " ".join(
                        words[:500]
                    )  # Limit to first 500 words for faster response of sentiment agent.
                    return limited_text
                else:
                    return "Error: Unable to fetch content."
    except Exception as e:
        return f"Error encountered: {str(e)}"


# On agent startup printing address
@webScraperAgent.on_event("startup")
async def agent_details(ctx: Context):
    ctx.logger.info(f"Search Agent Address is {webScraperAgent.address}")


# On_query handler to handle webpage wrapping
@webScraperAgent.on_query(model=wrapRequest, replies={wrapResponse})
async def query_handler(ctx: Context, sender: str, msg: wrapRequest):
    try:
        ctx.logger.info(f"URL wrapper for request : {msg.url}")
        news_content = await get_webpage_content(msg.url)
        ctx.logger.info(news_content)
        if "Error" not in news_content:
            await ctx.send(sender, wrapResponse(summary=news_content))
        else:
            await ctx.send(sender, ErrorResponse(error="ERROR" + news_content))
    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(error=str(error_message)))


if __name__ == "__main__":
    webScraperAgent.run()
