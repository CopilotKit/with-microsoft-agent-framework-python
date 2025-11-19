"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  type AgentState = {
    language: "english" | "spanish";
  };

  const { state } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState: { language: "spanish" },
  });

  return (
    <main className="p-6">
      <div className="mb-4 text-lg">Language: {state.language}</div>
      <CopilotChat
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