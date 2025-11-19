from __future__ import annotations

from agent_framework import ChatAgent, ChatClientProtocol
from agent_framework_ag_ui import AgentFrameworkAgent


def create_agent(chat_client: ChatClientProtocol) -> AgentFrameworkAgent:
    """
    Minimal agent for agent app context demo (frontend context is forwarded automatically).
    """
    base_agent = ChatAgent(
        name="sample_agent",
        instructions="You are a helpful assistant.",
        chat_client=chat_client,
    )

    return AgentFrameworkAgent(
        agent=base_agent,
        name="CopilotKitMicrosoftAgentFrameworkAgent",
        description="Assistant using app context forwarded from the frontend.",
        require_confirmation=False,
    )