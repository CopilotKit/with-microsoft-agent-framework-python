"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  type Colleague = { id: number; name: string; role: string };
  type AgentState = {
    colleagues: Colleague[];
  };

  // Make the agent explicitly aware of app context by storing it in agent state.
  useCoAgent<AgentState>({
    name: "sample_agent",
    initialState: {
      colleagues: [
        { id: 1, name: "John Doe", role: "Developer" },
        { id: 2, name: "Jane Smith", role: "Designer" },
        { id: 3, name: "Bob Wilson", role: "Product Manager" },
      ],
    },
  });

  return (
    <main className="p-6">
      <h1 className="text-xl mb-4">Your main content</h1>
      <CopilotSidebar
        instructions={
          "You are assisting the user as best as you can. Answer in the best way possible given the data you have."
        }
        labels={{
          title: "Your Assistant",
          initial: "Hi! 👋 How can I assist you today?",
        }}
      />
    </main>
  );
}