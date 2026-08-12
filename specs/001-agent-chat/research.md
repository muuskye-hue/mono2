# Research: Agent Chat App

**Feature**: `001-agent-chat` | **Date**: 2026-08-12

## 1. Frontend chat UI library

**Decision**: Use **assistant-ui** with `@assistant-ui/react-ag-ui` and
`HttpAgent` pointing at the full AG-UI URL (`VITE_AGENT_URL`, default
`http://localhost:7777/agui`).

**Rationale**: User mandated assistant-ui. Agno exposes AG-UI natively, so the
AG-UI runtime is the correct adapter (not AI SDK data-stream / custom SSE
parser).

**Alternatives considered**: Custom LocalRuntime against `/agents/.../runs`;
AI SDK BFF — rejected (extra process / wire mismatch).

## 2. Backend agent runtime

**Decision**: **Agno AgentOS** with `interfaces=[AGUI(agent=...)]`.
Endpoints: `POST /agui`, `GET /status` (also AgentOS `GET /health`).

**Rationale**: User mandated Agno + AgentOS and AG-UI status/run surface.

## 3. Model provider — Vercel AI Gateway + Gemini

**Decision**: Call models through **Vercel AI Gateway** OpenAI-compatible API:

- Base URL: `https://ai-gateway.vercel.sh/v1` (`AI_GATEWAY_BASE_URL`)
- Auth: `AI_GATEWAY_API_KEY`
- Default model: `google/gemini-3.5-flash-lite` (`AGENT_MODEL_ID`)
- Agno client: `OpenAILike(id=..., api_key=..., base_url=...)`

**Rationale**: Explicit product preference — not direct OpenAI. Gateway routes
to Google Gemini without Google Cloud credentials in-app.

**Alternatives considered**:
- Direct OpenAI / `OPENAI_API_KEY` — rejected by product direction.
- Direct Google Gemini SDK — bypasses preferred Gateway billing/routing.

## 4. Storage / multi-turn

**Decision**: No durable database. UI thread in browser; AG-UI protocol carries
messages for the run. Refresh clears the thread.

## 5. Health / status

**Decision**: Prefer AG-UI `GET /status` → `{ "status": "available" }` for the
interface check; keep AgentOS `GET /health` as secondary.

## 6. Commands

**Decision**: Root `Makefile`: `install`, `backend`, `frontend`, `status`,
`health`, `test`, `build`, `lint`.

## Resolved clarifications

No remaining NEEDS CLARIFICATION for v1 stack choices above.
