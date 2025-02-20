from uagents import Model


class TopicAnalysisRequest(Model):
    subreddit: str
    time_range: str = "week"


class TopicAnalysisResponse(Model):
    topic: str


class BlogRequest(Model):
    topic: str


class BlogResponse(Model):
    blog: str


class ContextPrompt(Model):
    context: str
    text: str


class Response(Model):
    text: str
