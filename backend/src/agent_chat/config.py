"""Explicit environment configuration for the AgentOS backend."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_GATEWAY_BASE_URL = "https://ai-gateway.vercel.sh/v1"
DEFAULT_MODEL_ID = "google/gemini-3.5-flash-lite"


@dataclass(frozen=True)
class BackendConfig:
    host: str
    port: int
    model_id: str
    agent_name: str
    cors_origins: tuple[str, ...]
    ai_gateway_api_key: str | None
    ai_gateway_base_url: str


def load_config() -> BackendConfig:
    cors_raw = os.environ.get(
        "AGENT_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    origins = tuple(o.strip() for o in cors_raw.split(",") if o.strip())
    return BackendConfig(
        host=os.environ.get("AGENT_OS_HOST", "0.0.0.0"),
        port=int(os.environ.get("AGENT_OS_PORT", "7777")),
        model_id=os.environ.get("AGENT_MODEL_ID", DEFAULT_MODEL_ID),
        agent_name=os.environ.get("AGENT_NAME", "chat-agent"),
        cors_origins=origins,
        ai_gateway_api_key=os.environ.get("AI_GATEWAY_API_KEY"),
        ai_gateway_base_url=os.environ.get(
            "AI_GATEWAY_BASE_URL",
            DEFAULT_GATEWAY_BASE_URL,
        ).rstrip("/"),
    )
