import httpx
from payment_model import PaymentRequest, PaymentResponse
from uagents import Agent, Context, Field, Model

USER_AGENT_SEED_PHRASE = "USER_AGENT_SEED_PHRASE"
GENERATE_PAYMENT_LINK_URL = "http://localhost:8000/generate_payment_link"

user_agent = Agent(
    name="User Agent",
    seed=USER_AGENT_SEED_PHRASE,
)


class UserRequest(Model):
    amount: float
    product_name: str
    quantity: int
    email: str


class UserResponse(Model):
    status: str = Field(
        description="Status of the user request.",
        choices=["success", "pending", "error"],
    )
    details: str = Field(description="Additional details about the request status.")
    payment_link: str = Field(description="URL of the payment link.")


@user_agent.on_rest_post("/create_payment", UserRequest, UserResponse)
async def handle_user_request(ctx: Context, req: UserRequest) -> UserResponse:
    ctx.logger.info(f"Received user request. Details: {req}")

    payment_request = PaymentRequest(
        amount=req.amount,
        currency="USD",
        product_name=req.product_name,
        quantity=req.quantity,
        customer_email=req.email,
    )
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                GENERATE_PAYMENT_LINK_URL, json=payment_request.dict()
            )
            response_data = response.json()

            return UserResponse(
                status=response_data["status"],
                details=response_data["details"],
                payment_link=response_data["payment_link"],
            )
    except Exception as e:
        return UserResponse(status="error", details=str(e))


@user_agent.on_rest_post("/payment_confirmation", PaymentResponse, UserResponse)
async def handle_payment_confirmation(
    ctx: Context, resp: PaymentResponse
) -> UserResponse:
    ctx.logger.info(f"Received payment confirmation. Details: {resp}")
    return UserResponse(
        status=resp.status, details=resp.details, payment_link=resp.payment_link
    )


if __name__ == "__main__":
    user_agent.run()
