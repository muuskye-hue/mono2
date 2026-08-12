from fastapi.testclient import TestClient

from agent_chat.app import build_app
from agent_chat.config import BackendConfig


def _client() -> TestClient:
    config = BackendConfig(
        host="127.0.0.1",
        port=7777,
        model_id="gpt-4o-mini",
        agent_name="chat-agent",
        cors_origins=("http://localhost:5173",),
        openai_api_key=None,
    )
    app, _, _ = build_app(config)
    return TestClient(app)


def test_status_endpoint_available():
    response = _client().get("/status")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "available"


def test_health_endpoint_ok():
    response = _client().get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "instantiated_at" in body
