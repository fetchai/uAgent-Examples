from typing import Optional
from uagents import Model

class RagRequest(Model):
    question: str
    url: str
    deep_read: Optional[str]