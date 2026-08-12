from agent_chat.config import DEFAULT_MODEL_ID, load_config


def test_load_config_defaults(monkeypatch):
    monkeypatch.delenv("AGENT_OS_PORT", raising=False)
    monkeypatch.delenv("AGENT_CORS_ORIGINS", raising=False)
    monkeypatch.delenv("AGENT_MODEL_ID", raising=False)
    monkeypatch.delenv("AI_GATEWAY_BASE_URL", raising=False)
    monkeypatch.delenv("AI_GATEWAY_API_KEY", raising=False)
    cfg = load_config()
    assert cfg.port == 7777
    assert "http://localhost:5173" in cfg.cors_origins
    assert cfg.model_id == DEFAULT_MODEL_ID
    assert cfg.ai_gateway_base_url == "https://ai-gateway.vercel.sh/v1"
    assert cfg.ai_gateway_api_key is None


def test_load_config_gateway_overrides(monkeypatch):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "test-key")
    monkeypatch.setenv("AGENT_MODEL_ID", "google/gemini-3.5-flash-lite")
    monkeypatch.setenv("AI_GATEWAY_BASE_URL", "https://ai-gateway.vercel.sh/v1/")
    cfg = load_config()
    assert cfg.ai_gateway_api_key == "test-key"
    assert cfg.model_id == "google/gemini-3.5-flash-lite"
    assert cfg.ai_gateway_base_url == "https://ai-gateway.vercel.sh/v1"
