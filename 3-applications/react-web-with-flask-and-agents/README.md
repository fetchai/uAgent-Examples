# React Web News Sentiment Analyzer

![tech:react](https://img.shields.io/badge/react-61DAFB?style=flat&logo=react&logoColor=black)
![tech:python](https://img.shields.io/badge/python-3776AB?style=flat&logo=python&logoColor=white)
![tech:flask](https://img.shields.io/badge/flask-000000?style=flat&logo=flask&logoColor=white)
![tech:llm](https://img.shields.io/badge/llm-E85D2E?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik00LjUgMUM0LjUgMS4yMTg3NSA0LjQyMTg4IDEuNDIxODggNC4zMTI1IDEuNTc4MTJMNC43NjU2MiAyLjU2MjVDNC45MjE4OCAyLjUzMTI1IDUuMDc4MTIgMi41IDUuMjUgMi41QzUuODEyNSAyLjUgNi4zMjgxMiAyLjcxODc1IDYuNzE4NzUgMy4wNjI1TDggMi4xMDkzOEM4IDIuMDc4MTIgOCAyLjA0Njg4IDggMkM4IDEuNDUzMTIgOC40Mzc1IDEgOSAxQzkuNTQ2ODggMSAxMCAxLjQ1MzEyIDEwIDJDMTAgMi41NjI1IDkuNTQ2ODggMyA5IDNDOC44NDM3NSAzIDguNzE4NzUgMi45ODQzOCA4LjU5Mzc1IDIuOTIxODhMNy4zMTI1IDMuODU5MzhDNy40MjE4OCA0LjE0MDYyIDcuNSA0LjQzNzUgNy41IDQuNzVDNy41IDUgNy40NTMxMiA1LjIzNDM4IDcuMzc1IDUuNDUzMTJMOC41IDYuMTI1QzguNjU2MjUgNi4wNDY4OCA4LjgxMjUgNiA5IDZDOS41NDY4OCA2IDEwIDYuNDUzMTIgMTAgN0MxMCA3LjU2MjUgOS41NDY4OCA4IDkgOEM4LjQzNzUgOCA4IDcuNTYyNSA4IDdWNi45ODQzOEw2Ljg1OTM4IDYuMzEyNUM2LjQ1MzEyIDYuNzM0MzggNS44NzUgNyA1LjI1IDdDNC4xNzE4OCA3IDMuMjgxMjUgNi4yNjU2MiAzLjA0Njg4IDUuMjVIMS44NTkzOEMxLjY4NzUgNS41NjI1IDEuMzU5MzggNS43NSAxIDUuNzVDMC40Mzc1IDUuNzUgMCA1LjMxMjUgMCA0Ljc1QzAgNC4yMDMxMiAwLjQzNzUgMy43NSAxIDMuNzVDMS4zNTkzOCAzLjc1IDEuNjg3NSAzLjk1MzEyIDEuODU5MzggNC4yNUgzLjA0Njg4QzMuMTcxODggMy43MzQzOCAzLjQ1MzEyIDMuMjk2ODggMy44NTkzOCAyLjk4NDM4TDMuNDA2MjUgMkMyLjg5MDYyIDEuOTUzMTIgMi41IDEuNTMxMjUgMi41IDFDMi41IDAuNDUzMTI1IDIuOTM3NSAwIDMuNSAwQzQuMDQ2ODggMCA0LjUgMC40NTMxMjUgNC41IDFaTTUuMjUgNS41QzUuNTE1NjIgNS41IDUuNzUgNS4zNTkzOCA1Ljg5MDYyIDUuMTI1QzYuMDMxMjUgNC45MDYyNSA2LjAzMTI1IDQuNjA5MzggNS44OTA2MiA0LjM3NUM1Ljc1IDQuMTU2MjUgNS41MTU2MiA0IDUuMjUgNEM0Ljk2ODc1IDQgNC43MzQzOCA0LjE1NjI1IDQuNTkzNzUgNC4zNzVDNC40NTMxMiA0LjYwOTM4IDQuNDUzMTIgNC45MDYyNSA0LjU5Mzc1IDUuMTI1QzQuNzM0MzggNS4zNTkzOCA0Ljk2ODc1IDUuNSA1LjI1IDUuNVoiIGZpbGw9IndoaXRlIi8%2BCjwvc3ZnPgo%3D)

## Introduction

This example demonstrates how to build a React application integrated with a Flask backend, using various uAgents to perform tasks such as fetching news, scraping webpage data, and analyzing news sentiment using the Hugging Face FinBERT model.

## Project Structure

```
react-web/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── NewsFeed.jsx
│   │   │   ├── SearchComponent.jsx
│   │   │   └── SearchComponent.css
│   │   ├── App.css
│   │   └── App.js
│   └── package.json
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── agents/
│       ├── news_agent.py
│       ├── webscraper_agent.py
│       └── sentiment_agent.py
```

## Prerequisites

1. Node.js: Download from [Node.js official website](https://nodejs.org/)
2. Python 3.10+: Download from [Python official website](https://python.org/)
3. Flask: Install via pip:
```bash
pip install Flask flask-cors
```


## Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
# or
venv\Scripts\activate 
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
- ALPHA_VANTAGE_API_KEY (Get from [Alpha Vantage](https://www.alphavantage.co/))
- GNEWS_API_KEY (Get from [GNews](https://gnews.io/))
- HUGGING_FACE_API_KEY (Get from [Hugging Face](https://huggingface.co/))

4. Start the agents and Flask server:
```bash
python app.py
python agents/news_agent.py
python agents/webscraper_agent.py
python agents/sentiment_agent.py
```

## Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm start
```

## Usage

1. Open http://localhost:3000 in your browser
2. View the fetched news articles and their sentiment analysis


## Architecture

The application consists of three main components:

1. **News Agent**: Fetches news articles from various sources using Alpha Vantage and GNews APIs
2. **Web Scraper Agent**: Extracts content from news articles using BeautifulSoup
3. **Sentiment Analysis Agent**: Analyzes the sentiment of news content using FinBERT model

## Dependencies

### Backend
- Python 3.10+
- Flask
- uAgents
- aiohttp
- beautifulsoup4
- requests

### Frontend
- React
- Node.js
- npm
