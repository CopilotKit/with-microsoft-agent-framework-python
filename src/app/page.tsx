"use client";

import { AgentState } from "@/lib/types";
import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  return (
    <main>
      <CopilotSidebar
        disableSystemMessage={true}
        clickOutsideToClose={false}
        labels={{
          title: "Popup Assistant",
          initial: "👋 Hi, there! You're chatting with an agent."
        }}
      >
        <YourMainContent />
      </CopilotSidebar>
    </main>
  );
}

function YourMainContent() {
  // 🪁 Shared State: https://docs.copilotkit.ai/pydantic-ai/shared-state
  
  useCoAgentStateRender<AgentState>({
    name: "sample_agent", // the name the agent is served as
    render: ({ state }) => (
      <div>
        {state.searches?.map((search, index) => (
          <div key={index}>
            {search.done ? "✅" : "❌"} {search.query}{search.done ? "" : "..."}
          </div>
        ))}
      </div>
    ),
  });

  const { state } = useCoAgent<AgentState>({
    name: "sample_agent", // the name the agent is served as
  })

  return (
    <div>
      {/* ... */}
      <div className="flex flex-col gap-2 mt-4">
        {state.searches?.map((search, index) => (
          <div key={index} className="flex flex-row">
            {search.done ? "✅" : "❌"} {search.query}
          </div>
        ))}
      </div>
    </div>
  );
}