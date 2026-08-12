"""Agent factory — one Traditional Chinese-friendly chat agent."""

from __future__ import annotations

from agno.agent.agent import Agent
from agno.models.openai import OpenAILike

from agent_chat.config import BackendConfig


def create_chat_agent(config: BackendConfig) -> Agent:
    model = OpenAILike(
        id=config.model_id,
        name="VercelAIGateway",
        provider="Vercel AI Gateway",
        api_key=config.ai_gateway_api_key,
        base_url=config.ai_gateway_base_url,
    )
    return Agent(
        id="chat-agent",
        name=config.agent_name,
        model=model,
        instructions=[
            "你是一個有幫助的助理。",
            "請使用繁體中文回覆使用者。",
            "回覆清楚、簡潔，避免不必要的冗長。",
        ],
        markdown=True,
    )
