from __future__ import annotations

from typing import Annotated, Dict

from agent_framework import ChatAgent, ChatClientProtocol, ai_function
from agent_framework_ag_ui import AgentFrameworkAgent
from pydantic import Field


def create_agent(chat_client: ChatClientProtocol) -> AgentFrameworkAgent:
    """
    Agent with predictive state updates for observed steps.
    """
    # 1) Define state schema for AG-UI
    STATE_SCHEMA: Dict[str, object] = {
        "observed_steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Array of completed steps",
        }
    }

    # 2) Predictive state mapping: observed_steps <- step_progress.steps
    PREDICT_STATE_CONFIG: Dict[str, Dict[str, str]] = {
        "observed_steps": {
            "tool": "step_progress",
            "tool_argument": "steps",
        }
    }

    # 3) Tool that the LLM will call with step updates
    @ai_function(
        name="step_progress",
        description="Report current step progress.",
    )
    def step_progress(
        steps: Annotated[list[str], Field(description="Steps completed so far")],
    ) -> str:
        return "Progress received."

    base = ChatAgent(
        name="sample_agent",
        instructions="You are a task performer. Report progress using step_progress.",
        chat_client=chat_client,
        tools=[step_progress],
    )

    return AgentFrameworkAgent(
        agent=base,
        name="CopilotKitMicrosoftAgentFrameworkAgent",
        description="Agent with predictive state updates for observed steps.",
        state_schema=STATE_SCHEMA,
        predict_state_config=PREDICT_STATE_CONFIG,
        require_confirmation=False,
    )