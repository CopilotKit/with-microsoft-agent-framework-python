"use client";

import { useHumanInTheLoop } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  useHumanInTheLoop({
    name: "humanApprovedCommand",
    description: "Ask human for approval to run a command.",
    parameters: [
      {
        name: "command",
        type: "string",
        description: "The command to run",
        required: true,
      },
    ],
    render: ({
      args,
      respond,
    }: {
      args: { command?: string };
      respond?: (decision: string) => void;
    }) => {
      if (!respond) return <></>;
      return (
        <div>
          <pre>{args.command}</pre>
          <button onClick={() => respond("Command is APPROVED")}>Approve</button>
          <button onClick={() => respond("Command is DENIED")}>Deny</button>
        </div>
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