"use client";

import { useFrontendTool } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

export default function CopilotKitPage() {
  useFrontendTool({
    name: "sayHello",
    description: "Say hello to the user",
    parameters: [
      {
        name: "name",
        type: "string",
        description: "The name of the user to say hello to",
        required: true,
      },
    ],
    handler: ({ name }: { name: string }): { currentURLPath: string; userName: string } => {
      return { currentURLPath: window.location.href, userName: name };
    },
    render: ({ args }: { args: { name?: string } }) => {
      return (
        <div>
          <h1>Hello, {args.name}!</h1>
          <h1>You&apos;re currently on {window.location.href}</h1>
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