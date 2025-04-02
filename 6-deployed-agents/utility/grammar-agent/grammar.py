import os

import requests

SAPLING_API_KEY = os.getenv("SAPLING_API_KEY")

if SAPLING_API_KEY is None:
    raise ValueError("You need to provide an API key for Sapling.")


def apply_corrections(text, edits) -> str:
    """
    Apply corrections to the original text based on the edit suggestions from
    Sapling API using the official Sapling edit logic.
    """
    # Ensure text is a string
    text = str(text)

    # Sort edits by the position they need to be applied at
    edits = sorted(
        edits, key=lambda e: (e["sentence_start"] + e["start"]), reverse=True
    )

    # Apply each edit to the text
    for edit in edits:
        start = edit["sentence_start"] + edit["start"]
        end = edit["sentence_start"] + edit["end"]

        # Check bounds to avoid errors
        if start > len(text) or end > len(text):
            continue

        # Apply the replacement
        text = text[:start] + edit["replacement"] + text[end:]

    return text


def check_grammar(text) -> dict:
    """
    Sends a request to the Sapling API to check the grammar of the provided text and returns the corrected text.

    Args:
        text (str): The input text to check.
    Returns:
        corrected_text (str): The corrected text.
    """
    try:
        response = requests.post(
            url="https://api.sapling.ai/api/v1/edits",
            headers={"Content-Type": "application/json"},
            json={
                "key": SAPLING_API_KEY,
                "text": text,
                "session_id": "test-session",
            },
            timeout=10,
        )

        if response.status_code == 200:
            results = response.json()
            edits = results.get("edits", [])
            return {"text": apply_corrections(text, edits)}

        return {"error": f"Error: {response.status_code} - {response.text}"}

    except requests.Timeout as e:
        return {"error": f"The request timed out: {str(e)}"}
    except requests.RequestException as e:
        return {"error": f"An error occurred during the request: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
