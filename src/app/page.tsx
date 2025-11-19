"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  type AgentState = {
    language: "english" | "spanish";
  };

  const { state, setState } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState: { language: "spanish" },
  });

  return (
    <main className="p-6">
      <div className="mb-2 text-lg">Language: {state.language}</div>
      <button
        type="button"
        onClick={toggleLanguage}
        className="px-3 py-2 mb-4 rounded bg-blue-600 text-white"
      >
        Toggle Language
      </button>
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