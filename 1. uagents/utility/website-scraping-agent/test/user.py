from uagents import Agent, Context, Model


class WebsiteScraperRequest(Model):
    url: str


class WebsiteScraperResponse(Model):
    text: str


agent = Agent()


AI_AGENT_ADDRESS = "agent1qfnfh7axy6lvau9537ce3n0dy86y7w37vshu94gwm6e5gmlxutkmg0el2yz"

website_url = "https://fetch.ai/"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, WebsiteScraperRequest(url=website_url))
    ctx.logger.info(f"Sent request for scraping the Website: {website_url}")


@agent.on_message(WebsiteScraperResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteScraperResponse):
    ctx.logger.info(f"Received response from {sender[-10:]}:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()
