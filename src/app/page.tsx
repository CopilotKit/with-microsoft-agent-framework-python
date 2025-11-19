"use client";

import { useCopilotAction } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  useCopilotAction({
    name: "get_weather",
    available: "disabled", // Render-only; don't allow invoking from UI
    parameters: [
      {
        name: "location",
        type: "string",
        description: "The location to get weather for",
        required: false,
      },
    ],
    render: ({ status, args }) => {
      const location =
        typeof args.location === "string" && args.location.length > 0
          ? args.location
          : "the requested location";
      return (
        <p className="text-gray-500 mt-2">
          {status !== "complete" ? "Calling weather API..." : `Called the weather API for ${location}.`}
        </p>
      );
    },
  });

  return (
    <CopilotChat
      instructions={
        "You are assisting the user as best as you can. Answer in the best way possible given the data you have."
      }
      labels={{
        title: "Your Assistant",
        initial: "Hi! 👋 How can I assist you today?",
      }}
    />
  );
}