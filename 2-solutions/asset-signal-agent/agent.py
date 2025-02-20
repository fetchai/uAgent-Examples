import os
from enum import Enum

from models import (
    AssetSignalRequest,
    AssetSignalResponse,
    FinancialNewsSentimentRequest,
    FinancialNewsSentimentResponse,
    FinancialSentimentRequest,
    FinancialSentimentResponse,
    NewsSentiment,
    StockPriceRequest,
    StockPriceResponse,
    TickerRequest,
    TickerResponse,
)
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

COMPANY_TICKER_RESOLVER_AGENT = os.getenv("company-ticker-resolver-agent")
FINANCIAL_NEWS_SENTIMENT_AGENT = os.getenv("financial-news-sentiment-agent")
FINBERT_FINANCIAL_SENTIMENT_AGENT = os.getenv("finbert-financial-sentiment-agent")
STOCK_PRICE_AGENT = os.getenv("stock-price-agent")

AGENT_SEED = os.getenv("AGENT_SEED", "<your-agent-seed>")
AGENT_NAME = os.getenv("AGENT_NAME", "Asset Signal Agent")


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Company-Asset-Signal",
    version="0.1.0",
)


@proto.on_message(
    AssetSignalRequest,
    replies={TickerRequest},
    rate_limit=RateLimit(window_size_minutes=60, max_requests=3),
)
async def handle_request(ctx: Context, sender: str, msg: AssetSignalRequest):
    agent_requests = ctx.storage.get("agent_requests") or {}
    agent_requests[str(ctx.session)] = {
        "sender": sender,
        "company": msg.company_name,
    }
    await ctx.send(
        COMPANY_TICKER_RESOLVER_AGENT, TickerRequest(company=msg.company_name)
    )
    ctx.storage.set("agent_requests", agent_requests)


@proto.on_message(TickerResponse, replies={FinancialNewsSentimentRequest, ErrorMessage})
async def handle_ticker_response(ctx: Context, sender: str, msg: TickerResponse):
    agent_requests = ctx.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return
    await ctx.send(
        FINANCIAL_NEWS_SENTIMENT_AGENT,
        FinancialNewsSentimentRequest(ticker=msg.ticker),
    )
    agent_requests[session]["ticker"] = msg.ticker
    ctx.storage.set("agent_requests", agent_requests)


def generate_sentiment_overview(summary: list[NewsSentiment]) -> dict[str, int]:
    sentiments = [news.model_dump()["overall_sentiment_label"] for news in summary]
    count = len(sentiments)
    output = {
        "Bearish": 0,
        "Somewhat-Bearish": 0,
        "Neutral": 0,
        "Somewhat-Bullish": 0,
        "Bullish": 0,
    }
    for s in sentiments:
        output[s] += 1
    for key in output:
        output[key] = output[key] / count
    converted_output = {
        "positive": output["Somewhat-Bullish"] / 2 + output["Bullish"],
        "neutral": output["Neutral"]
        + output["Somewhat-Bullish"] / 2
        + output["Somewhat-Bearish"] / 2,
        "negative": output["Somewhat-Bearish"] / 2 + output["Bearish"],
    }
    return converted_output


@proto.on_message(FinancialNewsSentimentResponse, replies={FinancialSentimentRequest})
async def handle_sentiment_response(
    ctx: Context, sender: str, msg: FinancialNewsSentimentResponse
):
    agent_requests = ctx.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return

    await ctx.send(
        FINBERT_FINANCIAL_SENTIMENT_AGENT,
        FinancialSentimentRequest(
            text="\n".join([article.title for article in msg.summary[:10]])
        ),  # finbert can only handle 512 tokens
    )
    agent_requests[session]["news_sentiment"] = [
        news.model_dump() for news in msg.summary
    ]
    agent_requests[session]["sentiment_summary"] = generate_sentiment_overview(
        msg.summary
    )
    ctx.storage.set("agent_requests", agent_requests)


@proto.on_message(FinancialSentimentResponse, replies={StockPriceRequest})
async def handle_finbert_sentiment_response(
    ctx: Context, sender: str, msg: FinancialSentimentResponse
):
    agent_requests = ctx.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return

    await ctx.send(
        STOCK_PRICE_AGENT, StockPriceRequest(ticker=agent_requests[session]["ticker"])
    )
    s1 = agent_requests[session]["sentiment_summary"]
    s2 = msg.model_dump()
    agent_requests[session]["finbert_sentiment"] = s2
    agent_requests[session]["combined_sentiment"] = {
        "BUY": s1["positive"] + s2["positive"],
        "WAIT": s1["neutral"] + s2["neutral"],
        "SELL": s1["negative"] + s2["negative"],
    }
    ctx.storage.set("agent_requests", agent_requests)


@proto.on_message(StockPriceResponse, replies={AssetSignalResponse, ErrorMessage})
async def handle_stock_price_response(
    ctx: Context, sender: str, msg: StockPriceResponse
):
    agent_requests = ctx.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return

    await ctx.send(
        agent_requests[session]["sender"],
        AssetSignalResponse(
            signal=[
                k
                for k, _ in sorted(
                    agent_requests[session]["combined_sentiment"].items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ][0],
            price=float(msg.text),
            sources={news["url"] for news in agent_requests[session]["news_sentiment"]},
        ),
    )

    agent_requests.pop(session)
    ctx.storage.set("agent_requests", agent_requests)
    ctx.logger.info("Asset Signal Response sent")


agent.include(proto, publish_manifest=True)


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
