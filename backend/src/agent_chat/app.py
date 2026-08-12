"""AgentOS composition root — AG-UI (/agui) + /status."""

from __future__ import annotations

from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI

from agent_chat.agent import create_chat_agent
from agent_chat.config import BackendConfig, load_config


def create_agent_os(config: BackendConfig) -> AgentOS:
    chat_agent = create_chat_agent(config)
    return AgentOS(
        id="mono2-agent-chat",
        description="mono2 Traditional Chinese agent chat (AG-UI)",
        agents=[chat_agent],
        interfaces=[AGUI(agent=chat_agent)],
        cors_allowed_origins=list(config.cors_origins),
    )


def build_app(config: BackendConfig | None = None):
    cfg = config or load_config()
    agent_os = create_agent_os(cfg)
    return agent_os.get_app(), agent_os, cfg


_config = load_config()
app, _agent_os, _ = build_app(_config)


def main() -> None:
    config = load_config()
    _, agent_os, _ = build_app(config)
    agent_os.serve(
        app="agent_chat.app:app",
        host=config.host,
        port=config.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
