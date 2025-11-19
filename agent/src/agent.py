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
            # Attempt to extract AG-UI forwarded context from additional chat options
            additional = getattr(getattr(context, "chat_options", None), "additional_properties", {}) or {}
            agui_ctx: Any = additional.get("ag_ui_context")

            # Format context into a readable system instruction
            if agui_ctx:
                lines: list[str] = ["The following context from the user's application is available:"]

                def _iter_items(obj: Any) -> Iterable[tuple[str, Any]]:
                    # Supports: dict-like, list of tuples, list of dicts with description/value
                    if isinstance(obj, dict):
                        return obj.items()
                    if isinstance(obj, list):
                        out: list[tuple[str, Any]] = []
                        for item in obj:
                            if isinstance(item, tuple) and len(item) == 2:
                                out.append((str(item[0]), item[1]))
                            elif isinstance(item, dict):
                                # Heuristic mapping of common shapes
                                if "description" in item and "value" in item:
                                    out.append((str(item["description"]), item["value"]))
                                elif "key" in item and "value" in item:
                                    out.append((str(item["key"]), item["value"]))
                        return out
                    return []

                for key, value in _iter_items(agui_ctx):
                    lines.append(f"- {key}: {value}")

                system_text = "\n".join(lines)
                # Prepend a minimal system message; most chat clients accept dict shape
                context.messages = [{"role": "system", "content": system_text}, *context.messages]

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