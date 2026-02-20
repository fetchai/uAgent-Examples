import os
from langchain_core.load import dumps, loads
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END, MessagesState
from uagents import Context

from tools import (
    search_agents,
    select_agents,
    next_page,
    prev_page,
    SearchResponse,
    reset_env,
)
# The following is needed in order to properly read the global var curr_search_result
import tools as tools_module


MODEL_ENGINE = os.getenv("MODEL_ENGINE", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

if OPENAI_API_KEY is None or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
    raise ValueError(
        "You need to provide an OpenAI API key: https://platform.openai.com/api-keys"
    )


class AgentState(MessagesState):
    """
    The state of the agent.
    Inherits the 'messages' key from MessagesState, which is a list of chat messages.
    In addition, it adds a key for the final, structured response.
    """
    # The final, structured response
    response: SearchResponse


model = ChatOpenAI(model=MODEL_ENGINE, temperature=0)

# Note: we add the structured output schema SearchResponse to the list of tools
tools = [search_agents, select_agents, next_page, prev_page, SearchResponse]
model = model.bind_tools(
    tools=tools,
    # "any" means that we're forcing the model to always use tools (i.e. no non-tool answer)
    tool_choice="any",
    # Ideally we'd set this to True, but we can't because the OpenAI API fails.
    # This is because strict is also applied to the tools (not just the SearchResponse structured output),
    # so to enforce strictness for just the structured output we'd need to change approach and use 2 LLM instances
    strict=False,
    # for this use case we don't want to call tools in parallel (we'll just need one tool at a time)
    parallel_tool_calls=False,
)

# We'll just use ToolNode as the node that calls the tools,
# so we don't need to define a custom one here
tool_node = ToolNode(tools=tools)


# Define the node that calls the model
def call_model(
    state: AgentState,
    config: RunnableConfig,
):
    # The custom system prompt
    system_prompt = SystemMessage(
        """# Purpose and Role
You are an AI assistant designed to help users find the most relevant agents based on their queries. You must interact exclusively through tool calls: plain text responses are not permitted.
The agents you will be able to search are part of the Agentverse (AV): a platform to explore, develop, test, and deploy agents, built by fetch.ai.

# Guidelines for Tool Usage

1. **Handling User Queries**
   - If the query relates to finding agents, follow the structured search and selection process.
   - User queries will often be about searching for agents, but they might not always be explicitly phrased as such.
     - For example, instead of saying, "Search for agents to do X" or "Find me an agent for Y", the user might simply say something like "finance agent" or "weather forecasts".
     - In such cases, infer the intent and search for agents that relate to that intent.
   - However, in some cases the query might be unrelated to your purpose of finding agents, in these cases just respond directly using `SearchResponse`, made of a single `SelectedAgent` with index -1 and an explanation in its `rationale` field, clearly stating your purpose, and that you can only assist with finding agents (e.g., "I am an AI assistant designed to help you search for agents on Agentverse based on your needs. I can only assist with finding agents.").

2. **Searching for Agents**
   - Always begin with `search_agents` to retrieve an initial list of agents.
   - Ensure that you use the arguments of `search_agents` appropriately based on the user's query. For example, if from the user query it's clear that results should be restricted to a particular geographical location, apply the corresponding filters to narrow down the search accordingly.
   - Analyse the results before deciding on the next step.

3. **Selecting Agents**
   - Use `select_agents` to mark one or more agents as selected.
   - Select only agents that are highly relevant and matching exactly (or very closely) what the user is asking for, and don't include unnecessary selections. Do not select agents just for the sake of returning results: if no relevant agents are found, return an appropriate response instead.
   - Avoid selecting near-duplicate agents; if multiple similar agents appear relevant, pick only the best one.
   - If the user specifies a number (e.g., "Find me 5 agents for X"), aim to meet that request without selecting unnecessary agents.
   - Once agents are selected, call `SearchResponse` to return the structured output.

4. **Navigating Through Pages**
   - Use `next_page` only if the initial results are unsatisfactory.
   - Use `prev_page` only if already past the first page and needing to revisit previous results.
   - Minimise unnecessary page navigation: prioritise finding relevant agents from the first page.
   - This should be rare, but if you can't find what you're looking for in the first search, you can perform another search (with a different, perhaps more general query and/or different filters). But do this sparingly, and only as a last resort.

5. **Handling No Results**
   - If no relevant agents are found, respond using `SearchResponse`, made of a single `SelectedAgent` with index -1 and an explanation in its `rationale` field, stating that you didn't find any result, and suggesting alternative possibilities if applicable.

6. **Finalising the Response**
   - The `SearchResponse` tool must always be the last tool used in the process.
   - Ensure the response is concise, relevant, and structured according to the available tools.

7. **Handling Follow-up Queries**
   - Users may ask follow-up questions or request modifications to their search (e.g., refining criteria, or looking for different types of agents).
   - When this happens, continue the process accordingly: perform a new search if needed, adjust filters, or navigate pages as appropriate, ensuring that each step aligns with these tool usage guidelines.
   - If the user is just asking a follow-up question related to the search results that doesn't need an additional search, you can reply to the question directly using `SearchResponse`.

"""
    )
    response = model.invoke([system_prompt] + state["messages"], config)
    # We return a list, because this will get added to the existing list of messages
    return {"messages": [response]}


# Define the conditional edge that determines whether to continue or not
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    # If there is only one tool call and it is the response tool call we go into the response node
    if (
        len(last_message.tool_calls) == 1
        and last_message.tool_calls[0]["name"] == "SearchResponse"
    ):
        return "respond"
    # Otherwise we will go into the tool node
    else:
        return "continue"


# Define the node that returns the final response
def respond(state: AgentState):
    # Construct the final answer from the arguments of the last tool call
    # (which should be the structured output response)
    result_tool_call = state["messages"][-1].tool_calls[0]
    response = SearchResponse(**result_tool_call["args"])
    # Since we're using tool calling to return structured output,
    # we need to add a tool message corresponding to the SearchResponse tool call,
    # This is due to LLM providers' requirement that AI messages with tool calls
    # need to be followed by a tool message for each tool call
    tool_message = {
        "type": "tool",
        "content": "Here is your structured response",
        "tool_call_id": result_tool_call["id"],
    }
    return {"response": response, "messages": [tool_message]}


# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("llm", call_model)
workflow.add_node("tools", tool_node)

# Define the final node
workflow.add_node("respond", respond)

# Set the entrypoint as `llm`
# This means that this node is the first one called
workflow.set_entry_point("llm")

# We now add a conditional edge
workflow.add_conditional_edges(
    # The conditional edge starts from the llm node
    source="llm",
    # This function is used to determine which node to go next
    path=should_continue,
    # The keys are strings, and the values are other nodes.
    # `should_continue` will return a string, which will be matched against these keys
    path_map={
        "continue": "tools",
        "respond": "respond",
    },
)

# We now add a normal edge from `tools` to `llm`
workflow.add_edge("tools", "llm")
# And an edge from `respond` to END
workflow.add_edge("respond", END)

# Now we can compile and visualize our graph
graph = workflow.compile()


def pretty_response(response: SearchResponse) -> str:
    curr_search_result = tools_module.curr_search_result
    if len(response.selected_agents) == 0:
        # The llm didn't find any suitable agents
        return "Sorry, I couldn't find any agents to satisfy your request :("
    elif (
        not curr_search_result
        or "agents" not in curr_search_result
        or not curr_search_result["agents"]
    ):
        # The llm didn't actually perform a search, or it did perform a search but the latest list of search results is empty.
        # In these cases it might justify the choices in the rationale
        return response.selected_agents[0].rationale
    else:
        output_str = ""
        n_selected = len(response.selected_agents)
        if n_selected == 1:
            output_str += "I found this agent for your request:\n"
        else:
            output_str += f"I found these {n_selected} agents for your request:\n"
        # We'll print the agents selected in a nice bullet points list
        rows = []
        for agent in response.selected_agents:
            # Make sure that the index is valid
            if agent.index < 0 or agent.index >= len(curr_search_result["agents"]):
                output_str += f"Oops, I've selected an index out of range. Let's ignore this one. And sorry about that.\n"
                continue
            # We have a valid index: let's print the corresponding agent
            name = curr_search_result["agents"][agent.index]["name"]
            address = curr_search_result["agents"][agent.index]["address"]
            rows.append([name, address, agent.rationale])
        if not rows:
            # All the selected indices were invalid
            output_str += "Apologies, I messed up. All the indices I selected are invalid. Please try again with a different query."
        else:
            for row in rows:
                output_str += f"- {row[0]} ({row[1]}): {row[2]}\n"
        return output_str


# Send a query to the agent and return the Agentverse search results selected
def search(
    ctx: Context,
    user_query: str,
    message_history: str | None = None,
) -> tuple[str, str]:
    messages = []
    if message_history:
        # De-serialise the given message history
        messages = loads(message_history)
    else:
        # No message history, so this is the beginning of the chat: reset the env
        reset_env()
    # Add the user query to the current message history
    messages.append({"role": "user", "content": user_query})
    # Execute the graph
    output = graph.invoke(input={"messages": messages})
    # Log the agent's sequence of internal messages, for debugging purposes
    messages = output["messages"]
    for message in messages:
        if message.type != "tool":
            ctx.logger.debug(f"{message.type}: {message}")
        else:
            ctx.logger.debug(f"{message.type}: {repr(message.content)}")
        ctx.logger.debug("-" * 50)
    # Serialise the new message history
    messages_serialised = dumps(messages)
    if "response" in output:
        # Return the response as a string, pretty-formatted
        return pretty_response(output["response"]), messages_serialised
    else:
        # Something went wrong with this request
        return "Sorry, something went wrong with this request :(", messages_serialised
