# Quickstart: Agent Chat App

**Feature**: `001-agent-chat` | **Date**: 2026-08-12

Validate the feature end-to-end on a local machine. Contracts:
[health.openapi.yaml](./contracts/health.openapi.yaml),
[agent-run.openapi.yaml](./contracts/agent-run.openapi.yaml). Data model:
[data-model.md](./data-model.md).

## Prerequisites

- Python 3.12+, Node.js 20+, `uv`, npm/pnpm
- Model API key available to Agno (default: `OPENAI_API_KEY`)
- Ports **7777** (AgentOS) and **5173** (Vite) free

## Setup

```bash
# from repo root — use the same catalog CI will use
make install          # backend uv sync + frontend npm install

export OPENAI_API_KEY=...   # or provider key required by chosen model
# optional frontend overrides:
export VITE_BACKEND_URL=http://localhost:7777
export VITE_AGENT_ID=chat-agent
```

## Run

```bash
# terminal A
make backend          # AgentOS on :7777

# terminal B
make frontend         # Vite UI on :5173
```

Open `http://localhost:5173`.

## Validation scenarios

### 1. Health (SC-003 / User Story 2)

```bash
make health
# equivalent: curl -sS "$VITE_BACKEND_URL/health"
```

**Expect**: HTTP 200 JSON with `"status":"ok"` and `instantiated_at`.

Stop backend and retry — **Expect**: connection failure / non-success.

### 2. Streaming chat (SC-001 / SC-002 / User Story 1)

1. Open the UI.
2. Send a Traditional Chinese message (e.g. `用繁體中文自我介紹`).
3. **Expect**: user message appears; assistant text grows in ≥2 visible updates
   before completion; send is disabled while streaming.
4. Send a follow-up — **Expect**: both turns remain in the same single thread.

### 3. Backend URL via env (SC-004 / User Story 3)

1. Start AgentOS on an alternate port (e.g. 7778).
2. Restart frontend with `VITE_BACKEND_URL=http://localhost:7778`.
3. Send a message — **Expect**: reply succeeds against the new backend
   (confirm via backend logs / structured events).

### 4. Edge checks

| Case | Expect |
| --- | --- |
| Empty / whitespace send | Blocked in UI; no AgentOS run |
| Backend down mid-session | User-visible error; prior messages remain |
| Refresh page | Thread cleared (session-only) |

## Automated checks

```bash
make test             # backend pytest + frontend vitest (same as CI)
```

Contract tests SHOULD assert `/health` schema and that a streamed run emits
content-bearing SSE events (may use a mock model in CI if no API key).

## Done when

- [ ] `make health` returns `status: ok`
- [ ] UI shows progressive streamed reply for Traditional Chinese input
- [ ] Changing only `VITE_BACKEND_URL` retargets the UI
- [ ] `make test` passes locally with the same commands CI runs
