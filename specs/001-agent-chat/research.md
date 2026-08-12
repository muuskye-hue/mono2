# Research: Agent Chat App

**Feature**: `001-agent-chat` | **Date**: 2026-08-12

## 1. Frontend chat UI library

**Decision**: Use **assistant-ui** (`@assistant-ui/react`) with a **custom
LocalRuntime `ChatModelAdapter`** that calls Agno AgentOS SSE.

**Rationale**: User mandated assistant-ui. It provides Thread/Composer/streaming
UX primitives. AgentOS does **not** speak the Vercel AI SDK data-stream /
UI-message-stream protocols, so `@assistant-ui/react-ai-sdk` and
`useDataStreamRuntime` are a poor fit without a protocol-translating BFF.

**Alternatives considered**:
- `useChatRuntime` + AI SDK route — requires a Node/Next BFF (extra process;
  rejected under constitution I).
- `useDataStreamRuntime` against AgentOS — wire format mismatch (AgentOS uses
  `event: RunContent` SSE, not AI SDK stream headers).
- Hand-rolled chat UI — rejected; user chose assistant-ui.

## 2. Backend agent runtime

**Decision**: Use **Agno AgentOS** (`pip/uv`: `agno[os]`). Register one agent
`id="chat-agent"`. Serve with `agent_os.serve(...)` (default port **7777**).
Enable CORS for the Vite origin. Do **not** enable authorization for v1.

**Rationale**: User mandated Agno SDK with AgentOS enabled. AgentOS exposes
`GET /health` and streaming `POST /agents/{agent_id}/runs` with `stream=true`
(SSE), matching acceptance criteria.

**Alternatives considered**:
- Bare Agno `Agent.arun` behind custom FastAPI — reinvented AgentOS routes;
  rejected.
- LangGraph / other agent frameworks — out of scope; user chose Agno.

## 3. Browser ↔ AgentOS integration pattern

**Decision**: Browser → AgentOS directly. Adapter issues:

`POST {VITE_BACKEND_URL}/agents/{VITE_AGENT_ID}/runs` as `multipart/form-data`
with `message`, `stream=true`, and a page-scoped `session_id`.

Parse SSE (`event` + `data` JSON). Append `content` deltas from `RunContent`
(and equivalent content-bearing events) into the assistant-ui message stream;
finish on `RunCompleted` / error events.

**Rationale**: Keeps process count at two (UI + AgentOS). Avoids a translation
BFF. Contracts live at the AgentOS boundary (constitution IV).

**Alternatives considered**:
- Next.js API route translating to AI SDK streams — third runtime; rejected.
- AgentOSClient from Python only — not usable in the browser.

## 4. Storage / multi-turn context (no product database)

**Decision**: No durable database. UI thread state is in-memory in the browser
(assistant-ui LocalRuntime). For agent multi-turn awareness without a DB, the
adapter MAY prepend a short rolling transcript (last N turns, capped) into the
`message` field sent to AgentOS. Restart/refresh clears the thread (spec).

**Rationale**: Spec excludes 資料庫. AgentOS session DB features are unused in
v1. Transcript-in-message is an explicit, deletable adapter concern.

**Alternatives considered**:
- SqliteDb / Postgres for AgentOS sessions — product “database”; rejected for v1.
- Stateless single-turn only — weaker UX vs user story of continuing a thread.

## 5. Model provider

**Decision**: Configure the Agno Agent with an env-driven model (default
OpenAI-compatible chat model via `OPENAI_API_KEY`). Exact model id is an
implementation default documented in quickstart; swappable via env without code
edits where Agno supports it.

**Rationale**: AgentOS examples standardize on provider keys in env. Spec does
not pin a vendor beyond “backend agent.”

**Alternatives considered**: Local-only mock agent — useful for CI smoke without
keys; keep as optional test double, not the primary runtime.

## 6. Health / status

**Decision**: Use AgentOS built-in **`GET /health`** → `{ "status": "ok",
"instantiated_at": "<unix>" }` (schema versioned in contracts).

**Rationale**: Satisfies FR-006 / SC-003 without custom routes.

## 7. Frontend backend URL configuration

**Decision**: Vite env var **`VITE_BACKEND_URL`** (default
`http://localhost:7777`). Optional **`VITE_AGENT_ID`** (default `chat-agent`).
Read only in `frontend/src/config.ts`.

**Rationale**: Matches FR-007 / SC-004. Vite exposes only `VITE_*` to the
browser bundle.

## 8. Commands (constitution X)

**Decision**: Root `Makefile` (or equivalent single catalog) listing:
`backend`, `frontend`, `test`, `health`, `install`. CI invokes the same targets.

**Rationale**: Discoverable one-place interface; local == CI.

## 9. Observability (constitution VI)

**Decision**: Backend request-path structured events (JSON) including
`request_id`, `session_id`, `agent_id`, and feature-flag placeholders when
applicable. No unstructured `print`/string logs in new code. Frontend may log
errors to console for local DX only; no production telemetry stack in v1.

## Resolved clarifications

All Technical Context items resolved — no remaining NEEDS CLARIFICATION.
