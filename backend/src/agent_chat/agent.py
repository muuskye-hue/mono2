"""Agent factory — one Traditional Chinese-friendly chat agent."""

from __future__ import annotations

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat

from agent_chat.config import BackendConfig


def create_chat_agent(config: BackendConfig) -> Agent:
    return Agent(
        id="chat-agent",
        name=config.agent_name,
        model=OpenAIChat(id=config.model_id),
        instructions=[
            "你是一個有幫助的助理。",
            "請使用繁體中文回覆使用者。",
            "回覆清楚、簡潔，避免不必要的冗長。",
        ],
        markdown=True,
    )
