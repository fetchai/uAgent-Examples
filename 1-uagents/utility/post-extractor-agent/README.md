# Post Extractor Agent

![Alt](https://img.shields.io/badge/integration-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNy43MzQyOSAyLjYwOTM4QzcuNzk2NzkgMi43NSA3Ljc0OTkyIDIuODkwNjIgNy42NDA1NCAzTDYuOTY4NjcgMy42MDkzOEM2Ljk4NDI5IDMuNzM0MzggNi45ODQyOSAzLjg3NSA2Ljk4NDI5IDRDNi45ODQyOSA0LjE0MDYyIDYuOTg0MjkgNC4yODEyNSA2Ljk2ODY3IDQuNDA2MjVMNy42NDA1NCA1LjAxNTYyQzcuNzQ5OTIgNS4xMDkzOCA3Ljc5Njc5IDUuMjY1NjIgNy43MzQyOSA1LjQwNjI1QzcuNjcxNzkgNS41OTM3NSA3LjU5MzY3IDUuNzY1NjIgNy40OTk5MiA1LjkzNzVMNy40MjE3OSA2LjA2MjVDNy4zMTI0MiA2LjIzNDM4IDcuMjAzMDQgNi40MDYyNSA3LjA3ODA0IDYuNTQ2ODhDNi45ODQyOSA2LjY3MTg4IDYuODI4MDQgNi43MDMxMiA2LjY4NzQyIDYuNjU2MjVMNS44MjgwNCA2LjM5MDYyQzUuNjA5MjkgNi41NDY4OCA1LjM3NDkyIDYuNjcxODggNS4xNDA1NCA2Ljc4MTI1TDQuOTM3NDIgNy42NzE4OEM0LjkwNjE3IDcuODEyNSA0Ljc5Njc5IDcuOTIxODggNC42NTYxNyA3Ljk1MzEyQzQuNDM3NDIgNy45ODQzOCA0LjIxODY3IDggMy45ODQyOSA4QzMuNzY1NTQgOCAzLjU0Njc5IDcuOTg0MzggMy4zMjgwNCA3Ljk1MzEyQzMuMTg3NDIgNy45MjE4OCAzLjA3ODA0IDcuODEyNSAzLjA0Njc5IDcuNjcxODhMMi44NDM2NyA2Ljc4MTI1QzIuNTkzNjcgNi42NzE4OCAyLjM3NDkyIDYuNTQ2ODggMi4xNTYxNyA2LjM5MDYyTDEuMjk2NzkgNi42NTYyNUMxLjE1NjE3IDYuNzAzMTIgMC45OTk5MTggNi42NzE4OCAwLjkwNjE2OCA2LjU2MjVDMC43ODExNjggNi40MDYyNSAwLjY3MTc5MyA2LjIzNDM4IDAuNTYyNDE4IDYuMDYyNUwwLjQ4NDI5MyA1LjkzNzVDMC4zOTA1NDMgNS43NjU2MiAwLjMxMjQxOCA1LjU5Mzc1IDAuMjQ5OTE4IDUuNDA2MjVDMC4xODc0MTggNS4yNjU2MiAwLjIzNDI5MyA1LjEyNSAwLjM0MzY2OCA1LjAxNTYyTDEuMDE1NTQgNC40MDYyNUMwLjk5OTkxOCA0LjI4MTI1IDAuOTk5OTE4IDQuMTQwNjIgMC45OTk5MTggNEMwLjk5OTkxOCAzLjg3NSAwLjk5OTkxOCAzLjczNDM4IDEuMDE1NTQgMy42MDkzOEwwLjM0MzY2OCAzQzAuMjM0MjkzIDIuODkwNjIgMC4xODc0MTggMi43NSAwLjI0OTkxOCAyLjYwOTM4QzAuMzEyNDE4IDIuNDIxODggMC4zOTA1NDMgMi4yNSAwLjQ4NDI5MyAyLjA3ODEyTDAuNTYyNDE4IDEuOTUzMTJDMC42NzE3OTMgMS43ODEyNSAwLjc4MTE2OCAxLjYwOTM4IDAuOTA2MTY4IDEuNDUzMTJDMC45OTk5MTggMS4zNDM3NSAxLjE1NjE3IDEuMzEyNSAxLjI5Njc5IDEuMzU5MzhMMi4xNTYxNyAxLjYyNUMyLjM3NDkyIDEuNDY4NzUgMi42MDkyOSAxLjMyODEyIDIuODQzNjcgMS4yMzQzOEwzLjA0Njc5IDAuMzQzNzVDMy4wNzgwNCAwLjIwMzEyNSAzLjE4NzQyIDAuMDkzNzUgMy4zMjgwNCAwLjA2MjVDMy41NDY3OSAwLjAzMTI1IDMuNzY1NTQgMCAzLjk5OTkyIDBDNC4yMTg2NyAwIDQuNDM3NDIgMC4wMzEyNSA0LjY1NjE3IDAuMDYyNUM0Ljc5Njc5IDAuMDc4MTI1IDQuOTA2MTcgMC4yMDMxMjUgNC45Mzc0MiAwLjM0Mzc1TDUuMTQwNTQgMS4yMzQzOEM1LjM5MDU0IDEuMzI4MTIgNS42MDkyOSAxLjQ2ODc1IDUuODI4MDQgMS42MjVMNi42ODc0MiAxLjM1OTM4QzYuODI4MDQgMS4zMTI1IDYuOTg0MjkgMS4zNDM3NSA3LjA3ODA0IDEuNDUzMTJDNy4yMDMwNCAxLjYwOTM4IDcuMzEyNDIgMS43ODEyNSA3LjQyMTc5IDEuOTUzMTJMNy40OTk5MiAyLjA3ODEyQzcuNTkzNjcgMi4yNSA3LjY3MTc5IDIuNDIxODggNy43NDk5MiAyLjYwOTM4SDcuNzM0MjlaTTMuOTk5OTIgNS4yNUM0LjQzNzQyIDUuMjUgNC44NDM2NyA1LjAxNTYyIDUuMDc4MDQgNC42MjVDNS4yOTY3OSA0LjI1IDUuMjk2NzkgMy43NjU2MiA1LjA3ODA0IDMuMzc1QzQuODQzNjcgMyA0LjQzNzQyIDIuNzUgMy45OTk5MiAyLjc1QzMuNTQ2NzkgMi43NSAzLjE0MDU0IDMgMi45MDYxNyAzLjM3NUMyLjY4NzQyIDMuNzY1NjIgMi42ODc0MiA0LjI1IDIuOTA2MTcgNC42MjVDMy4xNDA1NCA1LjAxNTYyIDMuNTQ2NzkgNS4yNSAzLjk5OTkyIDUuMjVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)
[![Alt](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgent-Examples/tree/main/1-uagents/utility/post-extractor-agent)
[![live](https://img.shields.io/badge/Live-8A2BE2?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik0yLjI1IDcuNUMxIDcuNSAwIDYuNSAwIDUuMjVDMCA0LjI4MTI1IDAuNjI1IDMuNDM3NSAxLjUgMy4xNDA2MkMxLjUgMy4wOTM3NSAxLjUgMy4wNDY4OCAxLjUgM0MxLjUgMS42MjUgMi42MDkzOCAwLjUgNCAwLjVDNC45MjE4OCAwLjUgNS43MzQzOCAxLjAxNTYyIDYuMTU2MjUgMS43NjU2MkM2LjM5MDYyIDEuNTkzNzUgNi42ODc1IDEuNSA3IDEuNUM3LjgyODEyIDEuNSA4LjUgMi4xNzE4OCA4LjUgM0M4LjUgMy4yMDMxMiA4LjQ1MzEyIDMuMzc1IDguMzkwNjIgMy41NDY4OEM5LjMxMjUgMy43MzQzOCAxMCA0LjU0Njg4IDEwIDUuNUMxMCA2LjYwOTM4IDkuMDkzNzUgNy41IDggNy41SDIuMjVaTTYuNzY1NjIgMy43NjU2MkM2LjkwNjI1IDMuNjI1IDYuOTA2MjUgMy4zOTA2MiA2Ljc2NTYyIDMuMjVDNi42MDkzOCAzLjA5Mzc1IDYuMzc1IDMuMDkzNzUgNi4yMzQzOCAzLjI1TDQuNSA0Ljk4NDM4TDMuNzY1NjIgNC4yNUMzLjYwOTM4IDQuMDkzNzUgMy4zNzUgNC4wOTM3NSAzLjIzNDM4IDQuMjVDMy4wNzgxMiA0LjM5MDYyIDMuMDc4MTIgNC42MjUgMy4yMzQzOCA0Ljc2NTYyTDQuMjM0MzggNS43NjU2MkM0LjM3NSA1LjkyMTg4IDQuNjA5MzggNS45MjE4OCA0Ljc2NTYyIDUuNzY1NjJMNi43NjU2MiAzLjc2NTYyWiIgZmlsbD0id2hpdGUiLz4KPC9zdmc%2BCg%3D%3D)](https://agentverse.ai/agents/details/agent1qdtd2stcr7jgvzljgmpsjp885cj9uqzwtl7tevk33wqk98faktd8suxptky/profile)

This agent retrieves the latest requested posts from Reddit. It uses the Reddit API to fetch posts

## Example input

```python
PostsRequest(
    limit=5
)
```

## Example output

```python
class PostsResponse(Model):
    posts=["Title: If you have work experience at a company like onlyfans or playboy do you think some companies people wouldn't want to hire you just because of that reason?\nAuthor: Ben5544477\nURL: https://www.reddit.com/r/NoStupidQuestions/comments/1gp0sdp/if_you_have_work_experience_at_a_company_like/\nCreated: 2024-11-11 13:29:28\nContent: Say I have 5 years of work experience at Playboy as a Software Developer. Do you think some companies would turn me down automatically because they don't like PlayBoy?\n", 'Title: DARK SOULS REMASTERED - Full Legendary INTRO\nAuthor: BarbosGaming\nURL: https://www.youtube.com/watch?v=Ga1g-6QmGec\nCreated: 2024-11-11 13:29:27\nContent: [No text content]\n', "Title: Do you think this is a faje\nAuthor: nec-gauss-blast\nURL: https://www.reddit.com/r/tagheuer/comments/1gp0sdl/do_you_think_this_is_a_faje/\nCreated: 2024-11-11 13:29:27\nContent: Just found this in eBay. It's cheep starting bid £100. But it doesn't look right to me the writing on tachymeter looks off. I'm not a massive watch enthusiast and looking for some deals to get started. Do you believe this is a genuine piece or has my eyes clicked on to a fake sale. TIA \n", 'Title: [WTS/WTT] Assembled Upper Receiver $460\nAuthor: bendyburner\nURL: https://www.reddit.com/r/GunAccessoriesForSale/comments/1gp0sdk/wtswtt_assembled_upper_receiver_460/\nCreated: 2024-11-11 13:29:27\nContent: [Timestamp](https://imgur.com/a/KXJD3JK)\n\nAssembled upper receiver. 11.5” Ballistic Advantage barrel, Keyhole forge upper, SLR pinned gas block, Dead Air Keymo (previously pinned), BCM KAG, and Magpul Pro front BUIS. $460 shipped\n\nOpen to trades for a salty Aimpoint Comp M4, Aimpoint PRO, Sig Romeo 4T/XT Pro, or a 30mm Geissele/Reptilia mount with a T2 or RMR top dot mount. Will take other trade offers as well.\n\nPP FF or Venmo only\n', 'Title: Shiny oily legs\nAuthor: miss_elektrashine\nURL: https://i.redd.it/gm8fvkhgqb0e1.jpeg\nCreated: 2024-11-11 13:29:27\nContent: [No text content]\n']
```

## Usage Example

Copy and paste the following code into a new [Blank agent](https://agentverse.ai/agents/create/getting-started/blank-agent) for an example of how to interact with this agent.

```python
from uagents import Agent, Context, Model


class PostsRequest(Model):
    limit: int


class PostsResponse(Model):
    posts: list[str] 


agent = Agent()


POST_AGENT_ADDRESS = = "{{ .Agent.Address }}"
LIMIT = 5

@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(POST_AGENT_ADDRESS, PostsRequest(limit=LIMIT))
    ctx.logger.info(f"Sent request for {LIMIT} latest posts")


@agent.on_message(PostsResponse)
async def handle_response(ctx: Context, sender: str, msg: PostsResponse):
    ctx.logger.info(f"Received response {len(msg.posts)} reddit posts from {sender[-10:]}:")
    print("\n".join(f"{p}\n{'-'*50}" for p in msg.posts))

if __name__ == "__main__":
    agent.run()
```

### Local Agent

1. Install the necessary packages:

   ```bash
   pip install uagents
   ```

2. To interact with this agent from a local agent instead, replace `agent = Agent()` in the above with:

   ```python
   agent = Agent(
       name="user",
       endpoint="http://localhost:8000/submit",
   )
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```
