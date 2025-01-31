import os
import re
import time

import httpx
from crew_ai import PaymentProcess
from payment_model import PaymentRequest, PaymentResponse
from uagents import Agent, Context, Model
from user_agent import user_agent as User

SEED_PHRASE = "STRIPE_PAYMENT_AGENT_SEED_PHRASE"
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
PAYMENT_CONFIRMATION_URL = "http://localhost:8000/payment_confirmation"

stripe_agent = Agent(
    name="Stripe Payment Agent",
    seed=SEED_PHRASE,
)

payment_processor = PaymentProcess()


@stripe_agent.on_rest_post("/generate_payment_link", PaymentRequest, PaymentResponse)
async def handle_payment(ctx: Context, req: PaymentRequest) -> PaymentResponse:
    ctx.logger.info(f"Received payment request. Details: {req}")
    try:
        result = payment_processor.create_payment_link(
            amount=req.amount,
            currency=req.currency,
            product_name=req.product_name,
            quantity=req.quantity,
            customer_email=req.customer_email,
        )

        payment_link_pattern = re.compile(r"https?://\S+")
        match = payment_link_pattern.search(result)
        if match:
            payment_link = match.group(0)
        else:
            raise ValueError("Failed to find a valid payment link in the result")

        generate_time = int(time.time())
        payment_status = "pending"
        confirmation_time = 0
        amount = req.amount
        payee_agent = User.address

        payment_details = {
            "payment_link": payment_link,
            "generate_time": generate_time,
            "payment_status": payment_status,
            "confirmation_time": confirmation_time,
            "amount": amount,
            "payee_agent": payee_agent,
        }
        ctx.storage.set("payment_details", payment_details)

        response = PaymentResponse(
            status="success",
            details="Payment link generated successfully",
            payment_link=payment_link,
            generate_time=generate_time,
            payment_status=payment_status,
            confirmation_time=confirmation_time,
            amount=amount,
        )
        return response
    except Exception as e:
        return PaymentResponse(status="error", details=str(e))


class StripeWebhookEvent(Model):
    type: str
    data: dict


@stripe_agent.on_rest_post("/stripe_webhook", StripeWebhookEvent, PaymentResponse)
async def handle_stripe_webhook(
    ctx: Context, event: StripeWebhookEvent
) -> PaymentResponse:
    ctx.logger.info(
        f"Received Stripe webhook event. Type: {event.type}, Data: {event.data}"
    )

    payload = event.data

    if event.type == "payment_intent.succeeded":
        payment_intent = payload
        # customer_email = payment_intent.get("receipt_email")
        amount_received = payment_intent.get("amount_received")
        currency = payment_intent.get("currency")
        description = payment_intent.get("description")
        confirmation_time = int(time.time())

        payment_details = ctx.storage.get("payment_details")
        if payment_details:
            payment_details["payment_status"] = "succeeded"
            payment_details["confirmation_time"] = confirmation_time
            ctx.storage.set("payment_details", payment_details)

        response = PaymentResponse(
            status="success",
            details=f"Payment of {amount_received} {currency} for {description} confirmed.",
            payment_link=payment_details.get("payment_link"),
            generate_time=payment_intent.get("created"),
            payment_status="succeeded",
            confirmation_time=confirmation_time,
            amount=amount_received / 100.0,
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            await client.post(PAYMENT_CONFIRMATION_URL, json=response.dict())
        return response

    return PaymentResponse(status="error", details="Unhandled event type")


if __name__ == "__main__":
    stripe_agent.run()
