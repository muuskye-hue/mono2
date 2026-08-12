# Quickstart: Agent Chat App

**Feature**: `001-agent-chat` | **Date**: 2026-08-12

Validate the feature end-to-end on a local machine. Contracts:
[agui-status.openapi.yaml](./contracts/agui-status.openapi.yaml),
[agui-run.openapi.yaml](./contracts/agui-run.openapi.yaml),
[health.openapi.yaml](./contracts/health.openapi.yaml). Data model:
[data-model.md](./data-model.md).

## Prerequisites

- Python 3.12+, Node.js 20+, `uv`, npm
- Model API key available to Agno (default: `OPENAI_API_KEY`)
- Ports **7777** (AgentOS / AG-UI) and **5173** (Vite) free

## Setup

```bash
# from repo root — use the same catalog CI will use
make install          # backend uv sync + frontend npm install

export OPENAI_API_KEY=...   # or provider key required by chosen model
# optional frontend override — FULL AG-UI endpoint including /agui:
export VITE_AGENT_URL=http://localhost:7777/agui
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

Stop backend and retry — **Expect**: connection failure / non-success.

### 2. Streaming chat (SC-001 / SC-002 / User Story 1)

1. Open the UI.
2. Send a Traditional Chinese message (e.g. `用繁體中文自我介紹`).
3. **Expect**: user message appears; assistant text grows in ≥2 visible updates
   before completion; send is disabled while streaming.
4. Send a follow-up — **Expect**: both turns remain in the same single thread.

### 3. Agent endpoint via env (SC-004 / User Story 3)

1. Start AgentOS on an alternate port (e.g. 7778).
2. Restart frontend with `VITE_AGENT_URL=http://localhost:7778/agui`.
3. Send a message — **Expect**: reply succeeds against the new backend.

### 4. Edge checks

| Case | Expect |
| --- | --- |
| Empty / whitespace send | Blocked in UI; no AgentOS run |
| Backend down mid-session | User-visible error; prior messages remain |
| Refresh page | Thread cleared (session-only) |

## Automated checks

```bash
make test             # backend pytest + frontend build (same as CI)
```

Contract tests assert `/status` and `/health`. Full AG-UI stream requires a
model API key (manual quickstart above).

## Done when

- [x] `make status` returns `status: available`
- [x] `make health` returns `status: ok`
- [ ] UI shows progressive streamed reply for Traditional Chinese input (needs API key)
- [x] Changing only `VITE_AGENT_URL` retargets the UI (config wired)
- [x] `make test` passes locally with the same commands CI runs
