from __future__ import annotations

from typing import Any, Iterable

from agent_framework import ChatAgent, ChatClientProtocol, ChatMiddleware, ChatContext
from agent_framework_ag_ui import AgentFrameworkAgent


def create_agent(chat_client: ChatClientProtocol) -> AgentFrameworkAgent:
    """
    Agent that is explicitly aware of app context forwarded by AG-UI.
    We inject the frontend context as a system message via chat middleware.
    """
    class ContextInjectionMiddleware(ChatMiddleware):
        async def process(self, context: ChatContext, next) -> None:  # type: ignore[override]
            # Extract AG-UI forwarded state: we expect {"colleagues": [{id,name,role}, ...]}
            additional = getattr(getattr(context, "chat_options", None), "additional_properties", {}) or {}
            agui_state: Any = additional.get("ag_ui_state")

            if isinstance(agui_state, dict) and isinstance(agui_state.get("colleagues"), list):
                try:
                    colleagues = agui_state["colleagues"]
                    lines = ["The user's colleagues are:"]
                    for c in colleagues:
                        name = c.get("name")
                        role = c.get("role")
                        if name and role:
                            lines.append(f"- {name} ({role})")
                    system_text = "\n".join(lines)
                    context.messages = [{"role": "system", "content": system_text}, *context.messages]
                except Exception:
                    # If shape is unexpected, skip injection silently
                    pass

            await next(context)

    base_agent = ChatAgent(
        name="sample_agent",
        instructions="You are a helpful assistant. Use the provided application context to improve your answers.",
        chat_client=chat_client,
        middleware=[ContextInjectionMiddleware()],
    )

    return AgentFrameworkAgent(
        agent=base_agent,
        name="CopilotKitMicrosoftAgentFrameworkAgent",
        description="Assistant that consumes app context forwarded from the frontend.",
        require_confirmation=False,
    )