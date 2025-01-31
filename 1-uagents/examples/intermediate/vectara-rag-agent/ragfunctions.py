import os

import requests

CORPUS_KEY = os.getenv("CORPUS_KEY")
API_KEY = os.getenv("API_KEY")


async def create_chat_session(query, ctx):
    url = "https://api.vectara.io/v2/chats"
    payload = {
        "query": query,
        "search": {
            "corpora": [{"corpus_key": CORPUS_KEY, "semantics": "default"}],
            "offset": 0,
            "limit": 5,
        },
        "chat": {"store": True},
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": API_KEY,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            chat_data = response.json()
            return chat_data["chat_id"], chat_data["answer"]
        ctx.logger.error(
            f"Failed to create chat session: {response.status_code}, {response.text}"
        )
        return None, None
    except Exception as e:
        ctx.logger.error(f"Error creating chat session: {e}")
        return None, None


async def add_chat_turn(chat_id, query, ctx):
    url = f"https://api.vectara.io/v2/chats/{chat_id}/turns"
    payload = {
        "query": query,
        "search": {
            "corpora": [{"corpus_key": CORPUS_KEY, "semantics": "default"}],
            "offset": 0,
            "limit": 5,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": API_KEY,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            turn_data = response.json()
            return turn_data["chat_id"], turn_data.get("answer", "No answer returned")
        ctx.logger.error(
            f"Failed to add chat turn: {response.status_code}, {response.text}"
        )
        return None, "Error"
    except Exception as e:
        ctx.logger.error(f"Error adding chat turn: {e}")
        return None, "Error"
