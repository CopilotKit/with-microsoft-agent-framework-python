from __future__ import annotations

from typing import Any

from agent_framework import ChatAgent, ChatClientProtocol, ChatMiddleware, ChatContext
from agent_framework_ag_ui import AgentFrameworkAgent


def create_agent(chat_client: ChatClientProtocol) -> AgentFrameworkAgent:
    """
    Agent that consumes app context forwarded by AG-UI.
    A tiny middleware injects a single system message with the colleagues list.
    """
    class ContextInjectionMiddleware(ChatMiddleware):
        async def process(self, context: ChatContext, next) -> None:  # type: ignore[override]
            # Extract AG-UI forwarded context as [description, value] pairs
            additional = getattr(getattr(context, "chat_options", None), "additional_properties", {}) or {}
            agui_ctx: Any = additional.get("ag_ui_context")

            if isinstance(agui_ctx, list) and len(agui_ctx) > 0:
                try:
                    # Expect shape like: [["The current user's colleagues", [{...}, {...}]], ...]
                    colleagues_item = next(
                        (pair[1] for pair in agui_ctx
                         if isinstance(pair, (list, tuple)) and len(pair) == 2 and pair[0] == "The current user's colleagues"),
                        None
                    )

                    if isinstance(colleagues_item, list) and len(colleagues_item) > 0:
                        entries = [
                            f"- {c.get('name')} ({c.get('role')})"
                            for c in colleagues_item
                            if isinstance(c, dict) and c.get("name") and c.get("role")
                        ]
                        if entries:
                            system_text = "The user's colleagues are:\n" + "\n".join(entries)
                            context.messages = [{"role": "system", "content": system_text}, *context.messages]

                except Exception:
                    # If shape is unexpected, skip injection silently
                    pass

            await next(context)

    base_agent = ChatAgent(
        name="sample_agent",
        instructions="You are a helpful assistant.",
        chat_client=chat_client,
        middleware=[ContextInjectionMiddleware()],
    )

    return AgentFrameworkAgent(
        agent=base_agent,
        name="CopilotKitMicrosoftAgentFrameworkAgent",
        description="Assistant that consumes app context forwarded from the frontend.",
        require_confirmation=False,
    )