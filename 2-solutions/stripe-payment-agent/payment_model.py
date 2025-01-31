from uagents import Field, Model


class PaymentRequest(Model):
    amount: float = Field(description="Amount to be charged.")
    currency: str = Field(description="Currency (e.g., USD, EUR).")
    product_name: str = Field(description="Name of the product.")
    quantity: int = Field(description="Quantity of the product.")
    customer_email: str = Field(description="Email of the customer.")


class PaymentResponse(Model):
    status: str = Field(
        description="Status of the payment.", choices=["success", "pending"]
    )
    details: str = Field(
        description="Details of the payment (e.g., confirmation or processing details)."
    )
    payment_link: str = Field(description="URL of the payment link.")
    generate_time: int = Field(
        description="Timestamp when the payment link was generated."
    )
    payment_status: str = Field(description="Current status of the payment.")
    confirmation_time: int = Field(
        description="Timestamp when the payment was confirmed."
    )
    amount: float = Field(description="Amount charged.")
