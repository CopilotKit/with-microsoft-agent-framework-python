from __future__ import annotations

from typing import Annotated, Dict

from agent_framework import ChatAgent, ChatClientProtocol, ai_function
from agent_framework_ag_ui import AgentFrameworkAgent
from pydantic import Field


def create_agent(chat_client: ChatClientProtocol) -> AgentFrameworkAgent:
    """
    Agent with language state support. Frontend tools are forwarded automatically, and
    language can be tracked as part of agent state.
    """
    # State schema describing the agent state (mirrors UI type).
    STATE_SCHEMA: Dict[str, object] = {
        "language": {
            "type": "string",
            "enum": ["english", "spanish"],
            "description": "Preferred language.",
        }
    }

    # Predictive state configuration - when the model decides to update language, it
    # should call the update_language tool with the 'language' argument.
    PREDICT_STATE_CONFIG: Dict[str, Dict[str, str]] = {
        "language": {
            "tool": "update_language",
            "tool_argument": "language",
        }
    }

    @ai_function(
        name="update_language",
        description="Update the preferred language (english or spanish).",
    )
    def update_language(
        language: Annotated[str, Field(description="Preferred language: 'english' or 'spanish'")],
    ) -> str:
        normalized = (language or "").strip().lower()
        if normalized not in ("english", "spanish"):
            return "Language unchanged. Use 'english' or 'spanish'."
        return f"Language updated to {normalized}."

    base_agent = ChatAgent(
        name="sample_agent",
        instructions="You are a helpful assistant.",
        chat_client=chat_client,
        tools=[update_language],
    )

    return AgentFrameworkAgent(
        agent=base_agent,
        name="CopilotKitMicrosoftAgentFrameworkAgent",
        description="Assistant that tracks a simple language state.",
        state_schema=STATE_SCHEMA,
        predict_state_config=PREDICT_STATE_CONFIG,
        require_confirmation=False,
    )