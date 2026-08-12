.PHONY: help install backend frontend test health status lint build

help:
	@echo "Commands (local == CI):"
	@echo "  make install   Install backend + frontend deps"
	@echo "  make backend   Run Agno AgentOS (AG-UI on :7777)"
	@echo "  make frontend  Run Vite UI on :5173"
	@echo "  make status    GET /status (AG-UI interface)"
	@echo "  make health    GET /health (AgentOS)"
	@echo "  make test      Run backend + frontend checks"
	@echo "  make lint      Lint frontend"
	@echo "  make build     Build frontend"

install:
	cd backend && uv sync --group dev
	cd frontend && npm install

backend:
	cd backend && uv run agent-chat-backend

frontend:
	cd frontend && npm run dev

status:
	curl -sS "$${AGENT_STATUS_URL:-http://localhost:7777/status}"

health:
	curl -sS "$${AGENT_HEALTH_URL:-http://localhost:7777/health}"

test:
	cd backend && uv run pytest -q
	cd frontend && npm run build

lint:
	cd frontend && npm run lint

build:
	cd frontend && npm run build
