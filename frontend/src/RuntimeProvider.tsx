import { useMemo, type ReactNode } from "react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useAgUiRuntime } from "@assistant-ui/react-ag-ui";
import { HttpAgent } from "@ag-ui/client";
import { loadFrontendConfig } from "./config";

type Props = {
  children: ReactNode;
};

export function RuntimeProvider({ children }: Props) {
  const { agentUrl } = loadFrontendConfig();

  const agent = useMemo(
    () =>
      new HttpAgent({
        url: agentUrl,
        headers: {
          Accept: "text/event-stream",
        },
      }),
    [agentUrl],
  );

  const runtime = useAgUiRuntime({
    agent,
    showThinking: false,
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {children}
    </AssistantRuntimeProvider>
  );
}
