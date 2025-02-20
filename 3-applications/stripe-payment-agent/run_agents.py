from agent import stripe_agent as Stripe
from uagents import Bureau
from user_agent import user_agent as User

bureau = Bureau(
    port=8000, agents=[User, Stripe], endpoint="http://localhost:8000/submit"
)


bureau.add(User)
bureau.add(Stripe)

if __name__ == "__main__":
    bureau.run()
