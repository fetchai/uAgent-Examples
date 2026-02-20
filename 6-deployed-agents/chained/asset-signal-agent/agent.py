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
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

COMPANY_TICKER_RESOLVER_AGENT = os.getenv("company-ticker-resolver-agent")
FINANCIAL_NEWS_SENTIMENT_AGENT = os.getenv("financial-news-sentiment-agent")
FINBERT_FINANCIAL_SENTIMENT_AGENT = os.getenv("finbert-financial-sentiment-agent")
STOCK_PRICE_AGENT = os.getenv("stock-price-agent")

AGENT_SEED = os.getenv("AGENT_SEED", "<your-agent-seed>")
AGENT_NAME = os.getenv("AGENT_NAME", "Asset Signal Agent")


PORT = 8000
agent = ChatAgent(
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


@proto.on_message(
    AssetSignalRequest,
    replies={AssetSignalResponse, ErrorMessage},
    rate_limit=RateLimit(window_size_minutes=60, max_requests=3),
)
async def handle_request(ctx: Context, sender: str, msg: AssetSignalRequest):
    if not COMPANY_TICKER_RESOLVER_AGENT:
        ctx.logger.info("COMPANY_TICKER_RESOLVER_AGENT is not set")
        return
    if not FINANCIAL_NEWS_SENTIMENT_AGENT:
        ctx.logger.info("FINANCIAL_NEWS_SENTIMENT_AGENT is not set")
        return
    if not FINBERT_FINANCIAL_SENTIMENT_AGENT:
        ctx.logger.info("FINBERT_FINANCIAL_SENTIMENT_AGENT is not set")
        return
    if not STOCK_PRICE_AGENT:
        ctx.logger.info("STOCK_PRICE_AGENT is not set")
        return

    ticker_reply, ticker_status = await ctx.send_and_receive(
        COMPANY_TICKER_RESOLVER_AGENT,
        TickerRequest(company=msg.company_name),
        response_type=TickerResponse,
    )
    if not isinstance(ticker_reply, TickerResponse):
        await ctx.send(sender, ErrorMessage(error=f"Ticker resolver failed: {ticker_status}"))
        return
    ticker = ticker_reply.ticker

    news_reply, news_status = await ctx.send_and_receive(
        FINANCIAL_NEWS_SENTIMENT_AGENT,
        FinancialNewsSentimentRequest(ticker=ticker),
        response_type=FinancialNewsSentimentResponse,
    )
    if not isinstance(news_reply, FinancialNewsSentimentResponse):
        await ctx.send(sender, ErrorMessage(error=f"News sentiment failed: {news_status}"))
        return
    if not news_reply.summary:
        await ctx.send(sender, ErrorMessage(error="News sentiment returned empty summary"))
        return

    sentiment_summary = generate_sentiment_overview(news_reply.summary)

    finbert_reply, finbert_status = await ctx.send_and_receive(
        FINBERT_FINANCIAL_SENTIMENT_AGENT,
        FinancialSentimentRequest(text="\n".join([a.title for a in news_reply.summary[:10]])),
        response_type=FinancialSentimentResponse,
    )
    if not isinstance(finbert_reply, FinancialSentimentResponse):
        await ctx.send(sender, ErrorMessage(error=f"FinBERT failed: {finbert_status}"))
        return

    s2 = finbert_reply.model_dump()
    combined = {
        "BUY": sentiment_summary["positive"] + s2["positive"],
        "WAIT": sentiment_summary["neutral"] + s2["neutral"],
        "SELL": sentiment_summary["negative"] + s2["negative"],
    }

    price_reply, price_status = await ctx.send_and_receive(
        STOCK_PRICE_AGENT,
        StockPriceRequest(ticker=ticker),
        response_type=StockPriceResponse,
    )
    if not isinstance(price_reply, StockPriceResponse):
        await ctx.send(sender, ErrorMessage(error=f"Stock price failed: {price_status}"))
        return

    try:
        price = float(price_reply.text)
    except Exception:
        await ctx.send(sender, ErrorMessage(error=f"Invalid price payload: {getattr(price_reply, 'text', None)!r}"))
        return

    signal = max(combined, key=combined.get)

    sources = sorted({news.url for news in news_reply.summary if getattr(news, "url", None)})

    await ctx.send(
        sender,
        AssetSignalResponse(
            signal=signal,
            price=price,
            sources=sources,
        ),
    )


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
