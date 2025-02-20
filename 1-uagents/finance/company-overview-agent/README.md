# Company Overview Agent

![domain:finance](https://img.shields.io/badge/finance-3D8BD3?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI2IiB2aWV3Qm94PSIwIDAgOCA2IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCA0LjVDMS43ODEyNSA0LjUgMCAzLjUgMCAyLjI1QzAgMS4wMTU2MiAxLjc4MTI1IDAgNCAwQzYuMjAzMTIgMCA4IDEuMDE1NjIgOCAyLjI1QzggMy41IDYuMjAzMTIgNC41IDQgNC41Wk0xLjM0Mzc1IDIuODkwNjJDMS41MzEyNSAzLjA2MjUgMS43ODEyNSAzLjIwMzEyIDIuMDQ2ODggMy4yOTY4OEMyLjU2MjUgMy41MTU2MiAzLjI1IDMuNjI1IDQgMy42MjVDNC43MzQzOCAzLjYyNSA1LjQyMTg4IDMuNTE1NjIgNS45NTMxMiAzLjI5Njg4QzYuMjAzMTIgMy4yMDMxMiA2LjQ1MzEyIDMuMDYyNSA2LjY0MDYyIDIuODkwNjJDNi44MjgxMiAyLjcwMzEyIDcgMi40NTMxMiA3IDIuMTI1QzcgMS44MTI1IDYuODI4MTIgMS41NjI1IDYuNjQwNjIgMS4zNzVDNi40NTMxMiAxLjIwMzEyIDYuMjAzMTIgMS4wNjI1IDUuOTUzMTIgMC45NTMxMjVDNS40MjE4OCAwLjc1IDQuNzM0MzggMC42MjUgNCAwLjYyNUMzLjI1IDAuNjI1IDIuNTYyNSAwLjc1IDIuMDQ2ODggMC45NTMxMjVDMS43ODEyNSAxLjA2MjUgMS41MzEyNSAxLjIwMzEyIDEuMzQzNzUgMS4zNzVDMS4xNTYyNSAxLjU2MjUgMSAxLjgxMjUgMSAyLjEyNUMxIDIuNDUzMTIgMS4xNTYyNSAyLjcwMzEyIDEuMzQzNzUgMi44OTA2MlpNMS41IDIuMTI1QzEuNSAxLjU3ODEyIDIuNjA5MzggMS4xMjUgNCAxLjEyNUM1LjM3NSAxLjEyNSA2LjUgMS41NzgxMiA2LjUgMi4xMjVDNi41IDIuNjg3NSA1LjM3NSAzLjEyNSA0IDMuMTI1QzIuNjA5MzggMy4xMjUgMS41IDIuNjg3NSAxLjUgMi4xMjVaTTAgMy41NDY4OEMwLjIwMzEyNSAzLjc4MTI1IDAuNDUzMTI1IDQgMC43NSA0LjE3MTg4VjUuMTcxODhDMC4yNjU2MjUgNC44NDM3NSAwIDQuNDM3NSAwIDRWMy41NDY4OFpNMS4yNSA1LjQ1MzEyVjQuNDUzMTJDMS42ODc1IDQuNjU2MjUgMi4xODc1IDQuODEyNSAyLjc1IDQuOTA2MjVWNS45MDYyNUMyLjE3MTg4IDUuODEyNSAxLjY3MTg4IDUuNjU2MjUgMS4yNSA1LjQ1MzEyWk0zLjI1IDUuOTY4NzVWNC45Njg3NUMzLjQ4NDM4IDUgMy43MzQzOCA1LjAxNTYyIDQgNS4wMTU2MkM0LjI1IDUuMDE1NjIgNC41IDUgNC43NSA0Ljk2ODc1VjUuOTY4NzVDNC41IDYgNC4yNSA2IDQgNkMzLjczNDM4IDYgMy40ODQzOCA2IDMuMjUgNS45Njg3NVpNNS4yNSA1LjkwNjI1VjQuOTA2MjVDNS43OTY4OCA0LjgxMjUgNi4yOTY4OCA0LjY1NjI1IDYuNzUgNC40NTMxMlY1LjQ2ODc1QzYuMzEyNSA1LjY1NjI1IDUuODEyNSA1LjgxMjUgNS4yNSA1LjkwNjI1Wk03LjI1IDUuMTcxODhWNC4xNzE4OEM3LjUzMTI1IDQgNy43ODEyNSAzLjc4MTI1IDggMy41NDY4OFY0QzggNC40Mzc1IDcuNzE4NzUgNC44NDM3NSA3LjI1IDUuMTcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)
[![link to source code](https://img.shields.io/badge/source%20code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgent-Examples/tree/main/1-uagents/finance/company-overview-agent)
[![live](https://img.shields.io/badge/Live-8A2BE2?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik0yLjI1IDcuNUMxIDcuNSAwIDYuNSAwIDUuMjVDMCA0LjI4MTI1IDAuNjI1IDMuNDM3NSAxLjUgMy4xNDA2MkMxLjUgMy4wOTM3NSAxLjUgMy4wNDY4OCAxLjUgM0MxLjUgMS42MjUgMi42MDkzOCAwLjUgNCAwLjVDNC45MjE4OCAwLjUgNS43MzQzOCAxLjAxNTYyIDYuMTU2MjUgMS43NjU2MkM2LjM5MDYyIDEuNTkzNzUgNi42ODc1IDEuNSA3IDEuNUM3LjgyODEyIDEuNSA4LjUgMi4xNzE4OCA4LjUgM0M4LjUgMy4yMDMxMiA4LjQ1MzEyIDMuMzc1IDguMzkwNjIgMy41NDY4OEM5LjMxMjUgMy43MzQzOCAxMCA0LjU0Njg4IDEwIDUuNUMxMCA2LjYwOTM4IDkuMDkzNzUgNy41IDggNy41SDIuMjVaTTYuNzY1NjIgMy43NjU2MkM2LjkwNjI1IDMuNjI1IDYuOTA2MjUgMy4zOTA2MiA2Ljc2NTYyIDMuMjVDNi42MDkzOCAzLjA5Mzc1IDYuMzc1IDMuMDkzNzUgNi4yMzQzOCAzLjI1TDQuNSA0Ljk4NDM4TDMuNzY1NjIgNC4yNUMzLjYwOTM4IDQuMDkzNzUgMy4zNzUgNC4wOTM3NSAzLjIzNDM4IDQuMjVDMy4wNzgxMiA0LjM5MDYyIDMuMDc4MTIgNC42MjUgMy4yMzQzOCA0Ljc2NTYyTDQuMjM0MzggNS43NjU2MkM0LjM3NSA1LjkyMTg4IDQuNjA5MzggNS45MjE4OCA0Ljc2NTYyIDUuNzY1NjJMNi43NjU2MiAzLjc2NTYyWiIgZmlsbD0id2hpdGUiLz4KPC9zdmc%2BCg%3D%3D)](https://agentverse.ai/agents/details/agent1qggzwfa032ddngqkrsgn9d3qwp4a7dh34q9cnpy9np7vzzvp8ws5u0rq5d8/profile)

This agent uses the Alphavantage Finance API to provide company overview of a given company name.

## Example input

```python
CompanyOverviewRequest(
    ticker: "AMZN"
)
```

## Example output

```python
CompanyOverviewResponse(
    overview={
        "Symbol": "AMZN",
        "AssetType": "Common Stock",
        "Name": "Amazon.com Inc",
        "Description": "Amazon.com, Inc. is an American multinational technology company which focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence. It is one of the Big Five companies in the U.S. information technology industry, along with Google, Apple, Microsoft, and Facebook. The company has been referred to as one of the most influential economic and cultural forces in the world, as well as the world's most valuable brand.",
        "CIK": "1018724",
        "Exchange": "NASDAQ",
        "Currency": "USD",
        "Country": "USA",
        "Sector": "TRADE & SERVICES",
        "Industry": "RETAIL-CATALOG & MAIL-ORDER HOUSES",
        "Address": "410 TERRY AVENUE NORTH, SEATTLE, WA, US",
        "OfficialSite": "https://www.aboutamazon.com",
        "FiscalYearEnd": "December",
        "LatestQuarter": "2024-06-30",
        "MarketCapitalization": "1957324390000",
        "EBITDA": "104049000000",
        "PERatio": "44.51",
        "PEGRatio": "1.771",
        "BookValue": "22.54",
        "DividendPerShare": "None",
        "DividendYield": "None",
        "EPS": "4.19",
        "RevenuePerShareTTM": "58.22",
        "ProfitMargin": "0.0735",
        "OperatingMarginTTM": "0.0992",
        "ReturnOnAssetsTTM": "0.0658",
        "ReturnOnEquityTTM": "0.219",
        "RevenueTTM": "604333998000",
        "GrossProfitTTM": "225152000000",
        "DilutedEPSTTM": "4.19",
        "QuarterlyEarningsGrowthYOY": "0.938",
        "QuarterlyRevenueGrowthYOY": "0.101",
        "AnalystTargetPrice": "218.35",
        "AnalystRatingStrongBuy": "17",
        "AnalystRatingBuy": "44",
        "AnalystRatingHold": "2",
        "AnalystRatingSell": "0",
        "AnalystRatingStrongSell": "0",
        "TrailingPE": "44.51",
        "ForwardPE": "31.55",
        "PriceToSalesRatioTTM": "3.239",
        "PriceToBookRatio": "8.28",
        "EVToRevenue": "3.311",
        "EVToEBITDA": "18.79",
        "Beta": "1.146",
        "52WeekHigh": "201.2",
        "52WeekLow": "118.35",
        "50DayMovingAverage": "179.94",
        "200DayMovingAverage": "173.92",
        "SharesOutstanding": "10495600000",
        "DividendDate": "None",
        "ExDividendDate": "None"
    }
)
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.

```python
from typing import Dict
from uagents import Agent, Context, Model


class CompanyOverviewRequest(Model):
    ticker: str


class CompanyOverviewResponse(Model):
    overview: Dict[str, str]


agent = Agent()


AI_AGENT_ADDRESS = "{{ .Agent.Address }}"

ticker = "AMZN"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, CompanyOverviewRequest(ticker=ticker))
    ctx.logger.info(f"Sent prompt to AI agent: {ticker}")


@agent.on_message(CompanyOverviewResponse)
async def handle_response(ctx: Context, sender: str, msg: CompanyOverviewResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.overview)


if __name__ == "__main__":
    agent.run()
```

### Local Agent

1. Install the necessary packages:

   ```bash
   pip install uagents
   ```

2. To interact with this agent from a local agent instead, replace `agent = Agent()` in the above with:

   ```python
   agent = Agent(
       name="user",
       endpoint="http://localhost:8001/submit",
   )
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```
