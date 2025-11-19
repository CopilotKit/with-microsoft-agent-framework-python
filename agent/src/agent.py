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
            # Extract AG-UI forwarded context as [description, value] pairs
            additional = getattr(getattr(context, "chat_options", None), "additional_properties", {}) or {}
            agui_ctx: Any = additional.get("ag_ui_context")

            if isinstance(agui_ctx, list) and len(agui_ctx) > 0:
                try:
                    # Expect shape: [["The current user's colleagues", [{...}, {...}]], ...]
                    # Find colleagues item by description
                    colleagues_item = None
                    for pair in agui_ctx:
                        if isinstance(pair, (list, tuple)) and len(pair) == 2 and pair[0] == "The current user's colleagues":
                            colleagues_item = pair[1]
                            break

                    if isinstance(colleagues_item, list) and len(colleagues_item) > 0:
                        lines = ["The user's colleagues are:"]
                        for c in colleagues_item:
                            if isinstance(c, dict):
                                name = c.get("name")
                                role = c.get("role")
                                if name and role:
                                    lines.append(f"- {name} ({role})")
                        system_text = "\n".join(lines)
                    else:
                        # Fallback: serialize all context pairs
                        entries = [f"- {k}: {v}" for k, v in agui_ctx if isinstance(k, str)]
                        system_text = "The following context from the user's application is available:\n" + "\n".join(entries)

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