# mono2

Spec-driven monorepo for a simple Traditional Chinese **agent chat** app.

| Layer | Stack | Default |
| --- | --- | --- |
| Frontend | Vite + React + **assistant-ui** (`@assistant-ui/react-ag-ui`) | `http://localhost:5173` |
| Backend | **Agno AgentOS** + **AG-UI** interface | `http://localhost:7777` |
| Model | **Vercel AI Gateway** → `google/gemini-3.5-flash-lite` | `AI_GATEWAY_API_KEY` |

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
| `AI_GATEWAY_API_KEY` | backend | — | Vercel AI Gateway API key |
| `AI_GATEWAY_BASE_URL` | backend | `https://ai-gateway.vercel.sh/v1` | Gateway OpenAI-compatible base URL |
| `AGENT_MODEL_ID` | backend | `google/gemini-3.5-flash-lite` | Gateway model id |
| `AGENT_OS_PORT` | backend | `7777` | AgentOS listen port |
| `AGENT_OS_HOST` | backend | `0.0.0.0` | Bind host |
| `AGENT_CORS_ORIGINS` | backend | Vite origins | Browser CORS allowlist |

## Quick start

```bash
make install
export AI_GATEWAY_API_KEY=...   # from Vercel AI Gateway dashboard
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
backend/     Agno AgentOS + AGUI (Vercel AI Gateway / Gemini)
frontend/    assistant-ui + HttpAgent
specs/       Spec Kit artifacts (spec/plan/contracts/tasks)
.specify/    Spec Kit project config + constitution
Makefile     Single command catalog
```

## Spec Kit

Feature docs: `specs/001-agent-chat/`. Constitution: `.specify/memory/constitution.md`.
