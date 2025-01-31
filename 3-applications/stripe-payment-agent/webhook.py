import os

import httpx
import stripe
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
async def webhook():
    event = None
    payload = request.data
    sig_header = request.headers["STRIPE_SIGNATURE"]
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]

        request_data = {"type": event["type"], "data": payment_intent}
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:8000/stripe_webhook", json=request_data
            )
            # response_data = response.json()
    else:
        return jsonify(
            success=False, error="Unhandled event type {}".format(event["type"])
        )
    return jsonify(success=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(debug=True, port=port)
