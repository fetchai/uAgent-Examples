from uagents import Model


class ShoppingRequest(Model):
    question: str


class ShoppingAssistResponse(Model):
    answer: str
