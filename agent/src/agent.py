from __future__ import annotations

from typing import Annotated

from agent_framework import ChatAgent, ChatClientProtocol, ai_function
from agent_framework_ag_ui import AgentFrameworkAgent
from pydantic import Field


@ai_function(
    name="get_weather",
    description="Get the weather for a given location.",
)
def get_weather(
    location: Annotated[str, Field(description="The location to get weather for")],
) -> str:
    normalized = location.strip() or "the requested location"
    return f"The weather for {normalized} is 70 degrees."


def create_agent(chat_client: ChatClientProtocol) -> AgentFrameworkAgent:
    """
    Minimal agent exposing a backend tool that can be rendered in the UI.
    """
    base_agent = ChatAgent(
        name="sample_agent",
        instructions="You are a helpful assistant.",
        chat_client=chat_client,
        tools=[get_weather],
    )

    return AgentFrameworkAgent(
        agent=base_agent,
        name="CopilotKitMicrosoftAgentFrameworkAgent",
        description="Assistant with a get_weather backend tool.",
        require_confirmation=False,
    )