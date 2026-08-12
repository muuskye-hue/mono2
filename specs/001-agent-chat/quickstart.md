# Quickstart: Agent Chat App

**Feature**: `001-agent-chat` | **Date**: 2026-08-12

Validate the feature end-to-end on a local machine. Contracts:
[agui-status.openapi.yaml](./contracts/agui-status.openapi.yaml),
[agui-run.openapi.yaml](./contracts/agui-run.openapi.yaml),
[health.openapi.yaml](./contracts/health.openapi.yaml). Data model:
[data-model.md](./data-model.md).

## Prerequisites

- Python 3.12+, Node.js 20+, `uv`, npm
- **Vercel AI Gateway** API key (`AI_GATEWAY_API_KEY`)
- Ports **7777** (AgentOS / AG-UI) and **5173** (Vite) free

## Setup

```bash
# from repo root — use the same catalog CI will use
make install

export AI_GATEWAY_API_KEY=...   # Vercel AI Gateway dashboard
# defaults (override if needed):
# export AI_GATEWAY_BASE_URL=https://ai-gateway.vercel.sh/v1
# export AGENT_MODEL_ID=google/gemini-3.5-flash-lite
# export VITE_AGENT_URL=http://localhost:7777/agui
```

## Run

```bash
# terminal A
make backend          # AgentOS + AGUI on :7777  (POST /agui, GET /status)

# terminal B
make frontend         # Vite UI on :5173
```

Open `http://localhost:5173`.

## Validation scenarios

### 1. Status / Health (SC-003 / User Story 2)

```bash
make status
# {"status":"available"}

make health
# {"status":"ok","instantiated_at":"..."}
```

### 2. Streaming chat (SC-001 / SC-002 / User Story 1)

1. Open the UI.
2. Send a Traditional Chinese message (e.g. `用繁體中文自我介紹`).
3. **Expect**: progressive streamed assistant reply via Gateway → Gemini.

### 3. Agent endpoint via env (SC-004 / User Story 3)

Restart frontend with a different full AG-UI URL, e.g.
`VITE_AGENT_URL=http://localhost:7778/agui`.

## Automated checks

```bash
make test             # backend pytest + frontend build (same as CI)
```

## Done when

- [x] `make status` returns `status: available`
- [x] `make health` returns `status: ok`
- [ ] UI shows progressive streamed reply (needs `AI_GATEWAY_API_KEY`)
- [x] `VITE_AGENT_URL` wires the full `/agui` endpoint
- [x] Model defaults to `google/gemini-3.5-flash-lite` via Vercel AI Gateway
- [x] `make test` passes
