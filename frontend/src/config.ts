/** Explicit frontend config — agent endpoint from env. */

export type FrontendConfig = {
  /** Full AG-UI agent endpoint, including `/agui`. */
  agentUrl: string;
};

export function loadFrontendConfig(
  env: ImportMetaEnv = import.meta.env,
): FrontendConfig {
  const agentUrl =
    (env.VITE_AGENT_URL as string | undefined)?.trim() ||
    "http://localhost:7777/agui";

  if (!agentUrl.endsWith("/agui")) {
    console.warn(
      `[config] VITE_AGENT_URL should be the full AG-UI endpoint ending in /agui (got: ${agentUrl})`,
    );
  }

  return { agentUrl };
}
