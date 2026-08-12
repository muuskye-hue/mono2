from agent_chat.config import load_config


def test_load_config_defaults(monkeypatch):
    monkeypatch.delenv("AGENT_OS_PORT", raising=False)
    monkeypatch.delenv("AGENT_CORS_ORIGINS", raising=False)
    monkeypatch.delenv("AGENT_MODEL_ID", raising=False)
    cfg = load_config()
    assert cfg.port == 7777
    assert "http://localhost:5173" in cfg.cors_origins
    assert cfg.model_id == "gpt-4o-mini"
