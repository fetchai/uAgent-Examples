import os
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Literal

from agentverse_client.search import (
    SearchApi,
    ApiClient,
    Configuration,
    AgentSearchRequest,
    AgentGeoSearchRequest,
    AgentFilters,
    AgentGeoFilter,
    SearchFeedbackRequest,
)
from agentverse_client.search.rest import ApiException


AGENTVERSE_URL = os.getenv("AGENTVERSE_URL", "https://agentverse.ai")
configuration = Configuration(host=AGENTVERSE_URL)
api_client = ApiClient(configuration=configuration)
api_instance = SearchApi(api_client)
AGENTS_PER_PAGE = 10
curr_search_id = None
curr_search_request = None
curr_page = 0
curr_search_result = None


def reset_env():
    global api_instance, curr_search_id, curr_search_request, curr_page, curr_search_result
    configuration = Configuration(host=AGENTVERSE_URL)
    api_client = ApiClient(configuration=configuration)
    api_instance = SearchApi(api_client)
    curr_search_id = None
    curr_search_request = None
    curr_page = 0
    curr_search_result = None


class SearchAgentsInput(BaseModel):
    search_text: str = Field(description="The search terms", default="")
    n_interactions: Literal["1k", "10k", "100k", "1m", "10m", "100m"] | None = Field(description="The minimum number of interactions that the agent should have", default=None)
    latitude: float | None = Field(description="The latitude of the agent's location. If providing this, also the longitute and the radius must be provided", default=None)
    longitude: float | None = Field(description="The longitude of the agent's location. If providing this, also the latitude and the radius must be provided", default=None)
    radius: float | None = Field(description="The radius for searching the agent's location, in metres. If providing this, also the latitude and the longitute must be provided", default=None)
    sort_by: Literal["relevancy", "interactions", "created-at", "last-modified"] = Field(description="The type of sorting that should be applied to the search results", default="relevancy")
    order: Literal["desc", "asc"] = Field(description="The sort order", default="desc")


class SelectAgentsInput(BaseModel):
    indices: list[int] = Field(description="The indices in the current page of search results of the agent(s) to be selected")


def _search_agents(search_request: AgentSearchRequest | AgentGeoSearchRequest) -> str:
    # Declare which global variables we're going to write
    global curr_search_id, curr_search_result

    # When navigating pages, we're effectively going to perform searches with different offsets,
    # but we need to make sure to re-use the same search_id
    if curr_search_id:
        search_request.search_id = curr_search_id

    is_geo_request = isinstance(search_request, AgentGeoSearchRequest)

    # Call the API with the given search request
    try:
        if not is_geo_request:
            search_response = api_instance.search_agents(search_request)
        else:
            search_response = api_instance.search_agent_by_geolocation(search_request)
    except ApiException as e:
        return f"An exception occurred:\n{e}"

    # Unpack and return the list of results
    search_result = search_response.model_dump()
    curr_search_result = search_result
    curr_search_id = search_result["search_id"]
    n_results = search_result["total"]
    results = search_result["agents"]
    # Build the str to return
    if not results:
        return "The search returned no results"
    output = f"Total number of agents found: {n_results}\n"
    output += f"Page: {curr_page}"
    for index, result in enumerate(results):
        output += f"""
Index: {index}
Name: '{result["name"]}'
Readme: '{result["readme"]}'
Number of recent interactions: {result["recent_interactions"]}
Number of total interactions: {result["total_interactions"]}
"""
        if is_geo_request and result["geo_location"]:
            output += f"Location: {result['geo_location']}"
        output += """
----------------
"""
    return output


@tool("search_agents", args_schema=SearchAgentsInput)
def search_agents(
    search_text: str = "",
    n_interactions: Literal["1k", "10k", "100k", "1m", "10m", "100m"] | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    radius: float | None = None,
    sort_by: Literal["relevancy", "interactions", "created-at", "last-modified"] = "relevancy",
    order: Literal["desc", "asc"] = "desc",
) -> str:
    """Perform a search based on the provided criteria, and return an ordered list of agents"""
    # Declare which global variables we're going to write
    global curr_search_request, curr_search_id

    # To know whether this is going to be a geo search or not
    geo_query = False

    # Filters and sorting
    filters = AgentFilters()
    if n_interactions:
        filters.n_interactions = n_interactions
    if latitude is not None and longitude is not None and radius is not None:
        geo_filter = AgentGeoFilter(latitude=latitude, longitude=longitude, radius=radius)
        geo_query = True
    if sort_by != "relevancy":
        sort_order = order
    else:
        sort_order = "desc" if order == "asc" else "asc"

    # Create the base search request
    if not geo_query:
        # Normal search
        search_request = AgentSearchRequest()
    else:
        # Geo search
        search_request = AgentGeoSearchRequest(geo_filter=geo_filter)

    # Set the properties of the request
    search_request.search_text = search_text
    search_request.filters = filters
    search_request.sort = sort_by
    search_request.direction = sort_order
    search_request.limit = AGENTS_PER_PAGE
    search_request.source = ""  # TODO: change to this agent's address once it's known

    # Save the request (this is needed if next_page() or prev_page() are going to be called later)
    curr_search_request = search_request

    # Reset the current search id (if we're calling this method, it means we're performing a new search)
    curr_search_id = None

    # Do the actual search
    return _search_agents(search_request=search_request)


@tool("next_page")
def next_page() -> str:
    """Navigates to the next page of search results, and return an ordered list of agents"""
    # Declare which global variables we're going to write
    global curr_page

    # We can only go to the next page if search_agents() has been called before
    if not curr_search_request:
        return "Error: next_page() should only be called after search_agents()"

    search_request = curr_search_request
    # Update the current page index, and set the offset accordingly
    curr_page += 1
    search_request.offset = curr_page * AGENTS_PER_PAGE

    # Do the actual search
    return _search_agents(search_request=search_request)


@tool("prev_page")
def prev_page() -> str:
    """Navigates to the previous page of search results, and return an ordered list of agents"""
    # Declare which global variables we're going to write
    global curr_page

    # We can only go to the previous page if search_agents() and next_page() have been called before
    if not curr_search_request:
        return "Error: prev_page() should only be called after search_agents()"
    elif curr_page == 0:
        return "Error: cannot call prev_page() when on the first page"

    search_request = curr_search_request
    # Update the current page index, and set the offset accordingly
    curr_page -= 1
    search_request.offset = curr_page * AGENTS_PER_PAGE

    # Do the actual search
    return _search_agents(search_request=search_request)


@tool("select_agents", args_schema=SelectAgentsInput)
def select_agents(indices: list[int]) -> str:
    """Marks as selected the agents identified by the given indices in the current page of search results"""

    # We can select an agent only if search_agents() has been called before
    if not curr_search_id or not curr_search_result:
        return "Error: select_agents() should only be called after search_agents()"
    # Make sure that there is at least one result
    if "agents" not in curr_search_result or not curr_search_result["agents"]:
        return "Error: select_agents() should only be called when there is at least one search result in the current page"
    # Iterate over the given indices
    for index in indices:
        # Make sure that the index is valid
        if index < 0 or index >= len(curr_search_result["agents"]):
            return f"Error: index out of range. Allowed values: [0, {len(curr_search_result["agents"]) - 1}]"

        # Prepare the feedback request
        search_feedback_request = SearchFeedbackRequest(
            search_id=curr_search_id,
            page_index=curr_page,
            address=curr_search_result["agents"][index]["address"],
        )
        # Use the feedback API with the given agent address
        try:
            api_instance.feedback(search_feedback_request=search_feedback_request)
        except ApiException as e:
            return f"An exception occurred:\n{e}"
    return f"Agent(s) with indices {indices} on the current page successfully selected"


# Define the structured output desired as final response

class SelectedAgent(BaseModel):
    """One of the selected agents."""
    index: int = Field(description="The index of the agent (in the current page)")
    rationale: str = Field(description="A brief and concise explanation for choosing this agent")


class SearchResponse(BaseModel):
    """Response format to use."""
    selected_agents: list[SelectedAgent] = Field(description="The ordered list of agents to return (it can consist of a single agent if appropriate)", default=[])
