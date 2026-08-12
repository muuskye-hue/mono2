# mono2

Spec-driven monorepo for a simple Traditional Chinese **agent chat** app.

| Layer | Stack | Default |
| --- | --- | --- |
| Frontend | Vite + React + **assistant-ui** (`@assistant-ui/react-ag-ui`) | `http://localhost:5173` |
| Backend | **Agno AgentOS** + **AG-UI** interface | `http://localhost:7777` |

## Commands

All repeatable actions live in the root `Makefile` (local == CI):

```bash
make install    # backend uv sync + frontend npm install
make backend    # AgentOS with POST /agui + GET /status
make frontend   # Vite UI
make status     # curl GET /status
make health     # curl GET /health
make test       # pytest + frontend build
make build      # frontend production build
```

## Environment

Copy `.env.example`. Important variables:

| Variable | Where | Default | Purpose |
| --- | --- | --- | --- |
| `VITE_AGENT_URL` | frontend | `http://localhost:7777/agui` | **Full** AG-UI agent endpoint |
| `OPENAI_API_KEY` | backend | — | Model provider key |
| `AGENT_OS_PORT` | backend | `7777` | AgentOS listen port |
| `AGENT_OS_HOST` | backend | `0.0.0.0` | Bind host |
| `AGENT_MODEL_ID` | backend | `gpt-4o-mini` | Chat model id |
| `AGENT_CORS_ORIGINS` | backend | Vite origins | Browser CORS allowlist |

## Quick start

```bash
make install
export OPENAI_API_KEY=sk-...
make backend    # terminal A
make frontend   # terminal B
```

Open `http://localhost:5173`, send a Traditional Chinese message, and watch the streamed reply.

Verify the AG-UI interface:

```bash
make status   # {"status":"available"}
```

## Layout

```text
backend/     Agno AgentOS + AGUI
frontend/    assistant-ui + HttpAgent
specs/       Spec Kit artifacts (spec/plan/contracts/tasks)
.specify/    Spec Kit project config + constitution
Makefile     Single command catalog
```

## Spec Kit

Feature docs: `specs/001-agent-chat/`. Constitution: `.specify/memory/constitution.md`.
