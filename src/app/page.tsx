"use client";

import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  type AgentState = {
    observed_steps: string[];
  };

  // Access both predicted and final states
  const { state } = useCoAgent<AgentState>({ name: "sample_agent" });

  // Observe predictions (render inside the chat)
  useCoAgentStateRender<AgentState>({
    name: "sample_agent",
    render: ({ state }) => {
      if (!state.observed_steps?.length) return null;
      return (
        <div>
          <h3>Current Progress:</h3>
          <ul>
            {state.observed_steps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ul>
        </div>
      );
    },
  });

  return (
    <main className="p-6">
      <h1 className="text-xl mb-4">Predictive State Updates</h1>
      <CopilotSidebar
        instructions={
          "You are assisting the user as best as you can. Answer in the best way possible given the data you have."
        }
        labels={{
          title: "Your Assistant",
          initial: "Hi! 👋 How can I assist you today?",
        }}
      />
      {/* Render final state as well */}
      {state.observed_steps?.length > 0 && (
        <div className="mt-4">
          <h3>Final Steps:</h3>
          <ul>
            {state.observed_steps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}