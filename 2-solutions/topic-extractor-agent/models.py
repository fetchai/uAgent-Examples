from uagents import Model


class TopicAnalysisRequest(Model):
    subreddit: str
    time_range: str = "week"


class TopicAnalysisResponse(Model):
    topic: str


class RedditPostsRequest(Model):
    limit: int
    subreddit: str
    time_range: str = "week"


class RedditPost(Model):
    title: str
    author: str
    url: str
    content: str


class RedditPostsResponse(Model):
    posts: list[RedditPost]


class ContextPrompt(Model):
    context: str
    text: str


class Response(Model):
    text: str
