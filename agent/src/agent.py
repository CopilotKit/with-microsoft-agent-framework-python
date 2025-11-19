from typing import Annotated, Dict

from agent_framework import ChatAgent, ChatClientProtocol, ai_function
from agent_framework_ag_ui import AgentFrameworkAgent
from pydantic import BaseModel, Field


class SearchItem(BaseModel):
    query: str
    done: bool


# Define the state schema for AG-UI to validate and forward to the frontend
STATE_SCHEMA: Dict[str, object] = {
    "searches": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "done": {"type": "boolean"},
            },
            "required": ["query", "done"],
            "additionalProperties": False,
        },
        "description": "List of searches and whether each is done.",
    }
}

# Configure how the agent updates state. The agent will call the `update_searches`
# tool with the FULL list of searches to set the current state.
PREDICT_STATE_CONFIG: Dict[str, Dict[str, str]] = {
    "searches": {
        "tool": "update_searches",
        "tool_argument": "searches",
    }
}


@ai_function(
    name="update_searches",
    description=(
        "Replace the entire list of searches with the provided values. "
        "Always include the full list you want to keep. "
        "Each search should include: { query: string, done: boolean }."
    ),
)
def update_searches(
    searches: Annotated[list[SearchItem], Field(description=("The complete source of truth for the user's searches. Maintain ordering and include the full list on each call."))],
) -> str:
    return f"Searches updated. Tracking {len(searches)} item(s)."


def create_agent(chat_client: ChatClientProtocol) -> AgentFrameworkAgent:
    """
    Agent that maintains and streams a list of searches to the UI.
    The LLM is instructed to call `update_searches` whenever it adds or completes searches.
    """
    base_agent = ChatAgent(
        name="search_agent",
        instructions=(
            "You help users create and run searches.\n\n"
            "State sync rules:\n"
            "- Maintain a list of searches: each item has { query, done }.\n"
            "- When adding a new search, call `update_searches` with the FULL list, including the new item with done=false.\n"
            "- When running searches, update the list with done=true for completed items and call `update_searches` with the FULL list.\n"
            "- Never send partial updates—always include the full list on each call.\n"
        ),
        chat_client=chat_client,
        tools=[update_searches],
    )

    return AgentFrameworkAgent(
        agent=base_agent,
        name="CopilotKitMicrosoftAgentFrameworkAgent",
        description="Maintains a list of searches and streams state to the UI.",
        state_schema=STATE_SCHEMA,
        predict_state_config=PREDICT_STATE_CONFIG,
        require_confirmation=False,
    )


