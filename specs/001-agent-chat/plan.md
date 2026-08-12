# Implementation Plan: Agent Chat App

**Branch**: `001-agent-chat` | **Date**: 2026-08-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-agent-chat/spec.md`

**Note**: Updated for AG-UI transport and Vercel AI Gateway + Gemini.

## Summary

Build a minimal Traditional Chinese agent chat app: a **Vite + React** web UI
using **assistant-ui** (`@assistant-ui/react-ag-ui` + `HttpAgent`) talking to an
**Agno AgentOS** backend with the **AG-UI** interface (`POST /agui`,
`GET /status`). The LLM is reached through **Vercel AI Gateway** using model
`google/gemini-3.5-flash-lite` (OpenAI-compatible client via Agno `OpenAILike`).
The frontend obtains the full agent endpoint from `VITE_AGENT_URL`. v1 is a
single in-browser thread, no auth, no durable database, no RAG/tools/uploads/
production deploy.

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript 5.x + React 19 (frontend)

**Primary Dependencies**:
- Backend: `agno[os,agui]` (AgentOS + AGUI), `openai` client library pointed at
  Vercel AI Gateway (`AI_GATEWAY_API_KEY`, `AI_GATEWAY_BASE_URL`)
- Frontend: `@assistant-ui/react`, `@assistant-ui/react-ag-ui`, `@ag-ui/client`,
  Vite, React

**Storage**: N/A for product data — no durable database. Conversation lives in
the browser session.

**Testing**: pytest (backend unit/contract), frontend production build check,
manual AG-UI stream check with gateway key

**Target Platform**: Local developer machines (Linux/macOS); desktop browser

**Project Type**: Web application (frontend + backend)

**Performance Goals**: First streamed token visible within 3s under normal local
conditions; progressive UI updates during reply (spec SC-001/SC-002)

**Constraints**: Single chat thread; Traditional Chinese input; no login; no
durable DB; no RAG/tools/uploads; no production deployment; AG-UI `/status`
(+ AgentOS `/health`); frontend full agent URL via `VITE_AGENT_URL`; model via
Vercel AI Gateway (not direct OpenAI)

**Scale/Scope**: Single demo agent, single user session, one conversation thread
per page load

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
| --- | --- | --- |
| I. Do Not Distribute by Default | Prefer one deployable; justify extra processes | **PASS WITH JUSTIFICATION** — Vite UI + AgentOS (organizational independence of toolchains); no BFF |
| II. Optimize for Deletion | Modules rewritable in a day | **PASS** — thin RuntimeProvider + AgentOS entry + agent factory |
| III. Make Dependencies Explicit | No hidden globals; env at composition root | **PASS** — `VITE_AGENT_URL`, `AI_GATEWAY_*`, `AGENT_*` loaded explicitly |
| IV. Contract at the Boundary | Versioned schemas at HTTP boundaries | **PASS** — AG-UI `/agui` + `/status` (+ `/health`) contracts |
| V. Test the Transformation | Unit/integration at boundaries | **PASS** — status/health/config tests; stream needs gateway key |
| VI. Emit Structured Events | Structured events on request path | **PASS** — prefer structured logging; no free-form new logs |
| VII. Recovery Over Prevention | Revertible without code change | **PASS** — stop processes / refresh page |
| VIII. Attention Is Finite | No decorative alerts | **PASS** — on-demand status/health only |
| IX. Value at the User | Runnable, observable, revertible locally | **PASS** — Makefile quickstart |
| X. Commands Discoverable | One command catalog; local == CI | **PASS** — root Makefile |

## Project Structure

### Documentation (this feature)

```text
specs/001-agent-chat/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── agui-run.openapi.yaml
│   ├── agui-status.openapi.yaml
│   ├── health.openapi.yaml
│   └── agent-run.openapi.yaml   # legacy AgentOS runs (superseded for UI path)
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml
├── src/agent_chat/
│   ├── app.py
│   ├── agent.py          # OpenAILike → Vercel AI Gateway / Gemini
│   └── config.py
└── tests/

frontend/
├── package.json
├── src/
│   ├── config.ts         # VITE_AGENT_URL
│   ├── RuntimeProvider.tsx
│   └── components/ChatThread.tsx
└── ...

Makefile
```

**Structure Decision**: Split `backend/` (Agno AgentOS + AGUI) and `frontend/`
(assistant-ui). Browser talks to AgentOS AG-UI directly — no BFF.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| Two local processes (Vite UI + AgentOS) | React/assistant-ui and Python/AgentOS have separate runtimes (**organizational independence**). Production packaging out of scope. | Static-only UI from AgentOS removes HMR; a third BFF adds distribution. |
