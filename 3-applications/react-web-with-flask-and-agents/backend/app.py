import json

from flask import Flask
from flask_cors import CORS
from uagents import Model
from uagents.query import query


# Define Request Data Model classes for interacting with different agents
class NewsRequest(Model):
    company_name: str


class UrlRequest(Model):
    company_name: str


class wrapRequest(Model):
    url: str


class SentimentRequest(Model):
    news: str


# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enables CORS for all domains on all routes

# Define agent addresses
news_agent_address = "agent1q2e9kfdrxfa5dxn6zeyw47287ca36cdur9xevhmdzzfmf4cwlmahv73mpev"
news_content_agent_address = (
    "agent1qvumqq9xju7musr82l6ulqsvgka7d7z77jvvdrkyyr7n5s0u0lfdvse6k4t"
)
sentiment_agent_address = (
    "agent1q2pm392d2uux3wjsydatd4zhagrtq0lrwfgw4s8pv4x0090sfzk9qpgztaz"
)


@app.route("/")
def home():
    return "Welcome to the Company Analyzer API!"


# Define an asynchronous endpoint to get news for a given company
@app.route("/api/news/<string:company_name>", methods=["GET"])
async def get_news(company_name):
    response = await query(
        destination=news_agent_address,
        message=NewsRequest(company_name=company_name),
        timeout=15.0,
    )
    data = json.loads(response.decode_payload())
    print(data)
    return data["news_list"]


# Define an asynchronous endpoint to analyse sentiment for a given company
@app.route("/api/sentiment/<string:company_name>", methods=["GET"])
async def get_sentiment(company_name):
    urls = await query(
        destination=news_agent_address,
        message=UrlRequest(company_name=company_name),
        timeout=15.0,
    )
    data = json.loads(urls.decode_payload())
    sentiments = []
    content_list = []
    sentiment_scores = {}
    url_list = data.get("url_list", [])

    # For each URL, query for content and perform sentiment analysis
    for url in url_list:
        content = await query(
            destination=news_content_agent_address,
            message=wrapRequest(url=url),
            timeout=15.0,
        )
        news_summary = json.loads(content.decode_payload())
        summary_text = news_summary.get("summary", "")
        cleaned_text = summary_text.replace("\u00a0", " ")
        if len(cleaned_text) > 100:
            content_list.append(cleaned_text)
    for content in content_list:
        sentiment = await query(
            destination=sentiment_agent_address,
            message=SentimentRequest(news=content),
            timeout=15.0,
        )
        data = json.loads(sentiment.decode_payload())
        sentiment = data.get("sentiment", [])
        sentiments.append(sentiment)
    for sentiment in sentiments:
        label, score = sentiment.split(",")
        score = float(score)
        if label in sentiment_scores:
            sentiment_scores[label].append(score)
        else:
            sentiment_scores[label] = [score]
        sentiment_means = {
            label: sum(scores) / len(scores)
            for label, scores in sentiment_scores.items()
            if scores
        }

    # Calculate average sentiment scores and determine the predominant sentiment
    if sentiment_means:
        max_sentiment = max(sentiment_means, key=sentiment_means.get)
        final_sentiment = (
            str(max_sentiment) + " : " + str(round(sentiment_means[max_sentiment], 2))
        )
        return final_sentiment
    else:
        return None, None


# Start the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
