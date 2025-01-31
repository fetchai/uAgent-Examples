import os

from crewai import Agent, Crew, Task
from dotenv import load_dotenv
from stripe_agent_toolkit.crewai.toolkit import StripeAgentToolkit

load_dotenv()


class PaymentProcess:
    def __init__(self):
        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")

        self.stripe_toolkit = StripeAgentToolkit(
            secret_key=self.stripe_secret_key,
            configuration={
                "actions": {
                    "customers": {"create": True, "read": True},
                    "payment_links": {"create": True},
                    "products": {"create": True},
                    "prices": {"create": True},
                }
            },
        )

        self.payment_agent = Agent(
            role="Payment Processor",
            goal="Handles secure Stripe payment processing.",
            backstory="You have been using Stripe forever.",
            tools=[*self.stripe_toolkit.get_tools()],
            verbose=True,
        )

        self.crew = Crew(
            agents=[self.payment_agent],
            verbose=True,
            planning=True,
        )

    def create_payment_link(
        self, amount, currency, product_name, quantity, customer_email
    ):
        description = (
            f"Create a payment link for a new product '{product_name}' "
            f"with a price of {amount} {currency} and quantity {quantity} "
            f"for customer {customer_email}."
        )

        task = Task(
            name="Create Payment Link",
            description=description,
            expected_output="url",
            agent=self.payment_agent,
        )

        self.crew.tasks = [task]
        self.crew.kickoff()

        return task.output.raw
