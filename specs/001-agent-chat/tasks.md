# Tasks: 001-agent-chat

**Date**: 2026-08-12

## Setup
- [x] T001 建立 monorepo root 與 shared conventions（Makefile、.gitignore、.env.example、README）

## Foundational
- [x] T002 確定 AG-UI contract、ports、environment variables
  - Ports: backend `7777`, frontend `5173`
  - Env: `VITE_AGENT_URL`（完整 `/agui` URL）、`OPENAI_API_KEY`、`AGENT_OS_*`、`AGENT_CORS_ORIGINS`
  - Contracts: `contracts/agui-run.openapi.yaml`, `contracts/agui-status.openapi.yaml`, `contracts/health.openapi.yaml`

## Parallel implementation
- [x] T003 Frontend — 初始化 assistant-ui，以 `VITE_AGENT_URL` 讀取完整 agent endpoint（`HttpAgent` + `useAgUiRuntime`）
- [x] T004 Backend — 初始化 Agno AgentOS + `AGUI`，提供 `POST /agui` 與 `GET /status`

## Polish
- [x] T005 End-to-end check、README、PR review
  - Verified `make status` → `available`, `make health` → `ok`
  - `make test` passes (pytest + frontend build)
  - Streaming chat requires `OPENAI_API_KEY` (manual)
