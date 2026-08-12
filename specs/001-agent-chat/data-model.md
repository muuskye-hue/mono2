# Data Model: Agent Chat App

**Feature**: `001-agent-chat` | **Date**: 2026-08-12

In-memory / session-scoped only. No durable persistence.

## Entities

### ChatThread

The single conversation container for one browser page session.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Stable for the page lifetime (UUID). Used as AgentOS `session_id`. |
| `messages` | Message[] | Ordered oldest→newest |
| `status` | enum | `idle` \| `streaming` \| `error` |

**Rules**:
- Exactly one thread per page load (no list/switch/create).
- Refresh creates a new empty thread (prior thread discarded).

### Message

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Client-generated id |
| `role` | enum | `user` \| `assistant` |
| `content` | string | Plain text (Traditional Chinese supported) |
| `state` | enum | `complete` \| `streaming` \| `error` |
| `createdAt` | datetime | Client timestamp |

**Validation**:
- User `content` MUST be non-empty after trim; max length **4000** characters.
- Assistant messages start as `streaming` with empty/partial `content`, then
  `complete` or `error`.

### AgentReplyStream

Ephemeral run of one assistant response.

| Field | Type | Notes |
| --- | --- | --- |
| `runId` | string \| null | From AgentOS SSE when available |
| `sessionId` | string | Same as ChatThread.id |
| `agentId` | string | From `VITE_AGENT_ID` / backend agent id |
| `chunks` | string[] | Incremental text pieces (optional to retain) |
| `status` | enum | `active` \| `completed` \| `failed` |

**Transitions**:
```text
(none) → active → completed
              ↘ failed
```

Only one `active` stream per thread. While `active`, user send is disabled.

### BackendHealth

| Field | Type | Notes |
| --- | --- | --- |
| `status` | string | Expect `ok` when healthy |
| `instantiatedAt` | string | Unix timestamp string from AgentOS |

Not stored in the UI model long-term; fetched on demand for verification.

## Relationships

```text
ChatThread 1──* Message
ChatThread 1──0..1 AgentReplyStream (active)
AgentReplyStream updates the latest assistant Message.content
```

## Mapping to AgentOS

| App concept | AgentOS field |
| --- | --- |
| ChatThread.id | `session_id` on run create |
| Message (user) text | `message` form field (may include short transcript prefix) |
| Agent id | path `/agents/{agent_id}/runs` |
| Stream deltas | SSE `RunContent` (content fields) |
| Stream end | SSE `RunCompleted` / error |
