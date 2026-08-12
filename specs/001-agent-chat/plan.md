# Implementation Plan: Agent Chat App

**Branch**: `001-agent-chat` | **Date**: 2026-08-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-agent-chat/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Build a minimal Traditional Chinese agent chat app: a **Vite + React** web UI using
**assistant-ui** for the chat thread/composer UX, talking to an **Agno AgentOS**
backend that streams replies over SSE via `POST /agents/{agent_id}/runs`. The
frontend obtains the backend base URL from `VITE_BACKEND_URL`. v1 is a single
in-browser thread, no auth, no durable database, no RAG/tools/uploads/production
deploy.

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript 5.x + React 19 (frontend)

**Primary Dependencies**:
- Backend: `agno[os]` (AgentOS/FastAPI), model provider SDK as required by Agno
  (default OpenAI-compatible via env key)
- Frontend: `@assistant-ui/react`, Vite, React; custom LocalRuntime
  `ChatModelAdapter` that consumes AgentOS SSE (not AI SDK data-stream)

**Storage**: N/A for product data — no durable database. Conversation lives in
the browser session. Agent turns are request-scoped; optional short transcript
prefix may be sent in the run `message` for multi-turn context (see research.md).

**Testing**: pytest (backend unit/contract/integration), Vitest + Testing Library
(frontend unit), manual quickstart stream check

**Target Platform**: Local developer machines (Linux/macOS); desktop browser

**Project Type**: Web application (frontend + backend)

**Performance Goals**: First streamed token visible within 3s under normal local
conditions; progressive UI updates during reply (spec SC-001/SC-002)

**Constraints**: Single chat thread; Traditional Chinese input; no login; no
durable DB; no RAG/tools/uploads; no production deployment; backend health via
`GET /health`; frontend backend URL via env var

**Scale/Scope**: Single demo agent, single user session, one conversation thread
per page load

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
| --- | --- | --- |
| I. Do Not Distribute by Default | Prefer one deployable; justify extra processes | **PASS WITH JUSTIFICATION** — see Complexity Tracking (local DX: Vite + AgentOS) |
| II. Optimize for Deletion | Modules rewritable in a day; no speculative frameworks | **PASS** — thin adapter + one AgentOS entry module + one Thread page |
| III. Make Dependencies Explicit | No hidden globals; deps in signatures/file tops; DI over singletons | **PASS** — config from env at composition root; adapter receives base URL/agent id |
| IV. Contract at the Boundary | Versioned schemas at HTTP boundaries | **PASS** — contracts for `/health` and `/agents/{agent_id}/runs` (+ SSE events) |
| V. Test the Transformation | Unit pure logic; integration at boundaries; no mock-owned code | **PASS** — unit-test SSE→UI text mapping; contract/integration for health + run stream |
| VI. Emit Structured Events | Structured events with high-cardinality fields on request path | **PASS** — request-path logging as structured events (`request_id`, `session_id`, `agent_id`); no free-form logs in new code |
| VII. Recovery Over Prevention | Revertible without code change; expand-then-contract N/A | **PASS** — no migrations; stop processes / refresh page to reset session state |
| VIII. Attention Is Finite | No decorative alerts | **PASS** — v1 has no paging alerts; health is on-demand only |
| IX. Value at the User | Done = runnable, observable, revertible locally | **PASS** — quickstart proves chat + health; local stop is the rollback |
| X. Commands Discoverable | One command catalog; local == CI | **PASS** — root command list for `backend`, `frontend`, `test`, `health` |

**Post-design re-check**: Unchanged — design keeps two local processes only as
justified, contracts versioned, no durable DB, no extra queues/services.

## Project Structure

### Documentation (this feature)

```text
specs/001-agent-chat/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── health.openapi.yaml
│   └── agent-run.openapi.yaml
└── tasks.md                 # /speckit-tasks (not created here)
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml
├── src/
│   └── agent_chat/
│       ├── __init__.py
│       ├── app.py              # AgentOS composition + serve entry
│       ├── agent.py            # Agent factory (id, instructions, model)
│       └── config.py           # explicit env config
└── tests/
    ├── unit/
    ├── contract/
    └── integration/

frontend/
├── package.json
├── vite.config.ts
├── index.html
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── config.ts               # VITE_BACKEND_URL, VITE_AGENT_ID
│   ├── runtime/
│   │   └── agnoChatAdapter.ts  # LocalRuntime ChatModelAdapter → AgentOS SSE
│   ├── lib/
│   │   └── sse.ts              # SSE parse helpers (pure)
│   └── components/
│       └── ChatThread.tsx      # assistant-ui Thread composition
└── tests/

Makefile                        # single command catalog (local == CI targets)
```

**Structure Decision**: Split `backend/` (Agno AgentOS) and `frontend/`
(assistant-ui + Vite) because the stacks are different languages/toolchains.
No monorepo packages beyond this. No BFF process — the browser talks to AgentOS
directly through the adapter.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| Two local processes (Vite UI + AgentOS) | React/assistant-ui and Python/AgentOS have separate runtimes and hot-reload needs (**organizational independence** of UI vs agent toolchain). Production packaging is out of scope for v1. | Serving a static UI from AgentOS alone removes Vite HMR and slows UI iteration; embedding React inside Python is not supported. A third BFF process was rejected as extra distribution. |
