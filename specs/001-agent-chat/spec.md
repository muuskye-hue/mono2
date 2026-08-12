# Feature Specification: Agent Chat App

**Feature Branch**: `001-agent-chat`

**Created**: 2026-08-12

**Status**: Draft

**Input**: User description: "建立一個簡單的 agent chat app。使用者可在 web 介面輸入繁體中文訊息，並收到由 backend agent 串流回傳的回覆。v1 只需要單一聊天 thread；不包含登入、資料庫、RAG、tools、上傳附件或 production deployment。Acceptance criteria：1. web 介面可送出訊息並顯示串流回覆。2. backend 有可檢查的 health/status endpoint。3. 前端 endpoint 可透過 environment variable 設定。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Send message and see streaming reply (Priority: P1)

A visitor opens the chat web page, types a Traditional Chinese message into the
input, and sends it. The page shows their message, then progressively displays
the agent’s reply as it arrives (streaming), rather than waiting for the full
answer before showing anything.

**Why this priority**: This is the core value of the product — without
send + streamed reply, there is no usable chat experience.

**Independent Test**: Open the web UI, send one Traditional Chinese message,
and confirm the reply appears in chunks over time in the same conversation
view.

**Acceptance Scenarios**:

1. **Given** the chat page is open and the backend is available, **When** the
   user submits a non-empty Traditional Chinese message, **Then** the message
   appears in the conversation and a streamed agent reply appears
   progressively in the same thread.
2. **Given** the user has already exchanged messages in this visit, **When**
   they send another message, **Then** the new exchange appends to the same
   single thread (prior messages remain visible).
3. **Given** a reply is currently streaming, **When** the stream completes,
   **Then** the full reply is visible as a finished agent message and the
   user can send another message.

---

### User Story 2 - Verify backend health (Priority: P2)

An operator (or the developer running the app locally) checks a dedicated
health/status URL on the backend and receives a clear indication that the
service is up and ready to accept chat traffic.

**Why this priority**: Required for local verification and for confirming the
backend is reachable before diagnosing chat failures; secondary to the chat
flow itself.

**Independent Test**: Call the health/status endpoint while the backend is
running and confirm a successful healthy response; stop the backend and
confirm the check fails.

**Acceptance Scenarios**:

1. **Given** the backend is running, **When** someone requests the
   health/status endpoint, **Then** they receive a successful response that
   indicates the service is healthy.
2. **Given** the backend is not running, **When** someone requests the
   health/status endpoint, **Then** the request fails (connection error or
   non-success), making unavailability observable.

---

### User Story 3 - Point the web UI at a configured backend (Priority: P2)

A developer configures where the web UI sends chat requests using an
environment variable, so the same frontend build can talk to different
backend locations without code edits.

**Why this priority**: Explicit acceptance criterion for local flexibility;
needed once the chat UI exists, but not the primary user-facing journey.

**Independent Test**: Set the backend location via environment variable,
start the web UI, send a message, and confirm traffic goes to that location;
change the value and confirm the UI targets the new location.

**Acceptance Scenarios**:

1. **Given** a backend location is set via the documented environment
   variable, **When** the web UI starts, **Then** chat requests are sent to
   that location.
2. **Given** the environment variable is unset, **When** the web UI starts,
   **Then** it uses a documented default local backend location suitable for
   development.

---

### Edge Cases

- Empty or whitespace-only message: system MUST reject send and MUST NOT
  call the agent; the UI shows a clear validation message.
- Backend unreachable or stream interrupted mid-reply: the UI shows an
  actionable error and leaves prior messages intact; the user can retry.
- Very long Traditional Chinese input: system accepts within a documented
  reasonable length limit; above the limit, send is rejected with a clear
  message.
- Concurrent send while a reply is still streaming: the UI MUST prevent a
  second send until the current stream finishes or fails (single in-flight
  reply per thread).
- Page refresh: v1 has no durable storage; the in-progress thread MAY be
  lost — this is acceptable and MUST be documented to the user as session-
  only conversation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a web chat interface where a user can
  compose and send Traditional Chinese text messages.
- **FR-002**: System MUST display the user’s sent messages in a single
  conversation thread on the page.
- **FR-003**: System MUST return agent replies as a stream of incremental
  text so the UI can show the reply progressing before it is complete.
- **FR-004**: System MUST render streamed reply content in the same thread,
  clearly distinguished as agent messages versus user messages.
- **FR-005**: System MUST support exactly one chat thread per browser
  session in v1 (no thread list, no thread switching, no thread creation).
- **FR-006**: Backend MUST expose a health/status endpoint that returns a
  successful healthy indication when the service is running.
- **FR-007**: Web UI MUST obtain the full agent endpoint URL (including the
  AG-UI path) from an environment variable (with a documented development
  default when unset).
- **FR-008**: System MUST reject empty or whitespace-only messages without
  invoking the agent.
- **FR-009**: System MUST surface a user-visible error when the backend is
  unavailable or the stream fails, without corrupting already-displayed
  messages.
- **FR-010**: System MUST allow the user to send another message only after
  the current agent stream completes or fails.
- **FR-011**: Conversation state in v1 MUST be session-scoped only (no
  login, no durable database persistence across restarts or devices).

### Out of Scope (v1)

- User authentication / login / accounts
- Durable database or cross-session history
- RAG / document retrieval
- Agent tools / function calling
- File or attachment upload
- Production deployment, scaling, or multi-region hosting
- Multiple concurrent threads or thread management UI
- Non-web clients (native mobile, CLI) as primary experience

### Key Entities

- **Chat Thread**: The single conversation container for one browser
  session; holds an ordered sequence of messages for the current visit.
- **Message**: A unit of conversation content with role (user or agent),
  text body, and completion state (pending stream vs complete vs error).
- **Agent Reply Stream**: A progressive delivery of agent text for one user
  message, ending in completion or failure.
- **Backend Health Status**: A simple readiness signal indicating whether
  the backend can accept chat requests.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can open the chat page, send a Traditional Chinese
  message, and see the first visible chunk of the agent reply within 3
  seconds under normal local conditions (backend up, typical network).
- **SC-002**: During a successful reply, the user sees at least two
  distinct UI updates of growing reply text before the reply is marked
  complete (streaming is observable, not a single dump).
- **SC-003**: 100% of successful local verification runs can confirm
  backend health via the health/status endpoint returning healthy while the
  service is up.
- **SC-004**: Changing only the documented frontend environment variable
  (no code edits) is sufficient to point the UI at a different backend
  location, verified by a successful send against that backend.
- **SC-005**: Empty-message send attempts never produce an agent reply
  (0 false agent invocations) and always show validation feedback.
- **SC-006**: After a backend failure mid-stream, the user can still read
  prior messages and retry a new send without reloading for unrelated UI
  breakage.

## Assumptions

- Target users are developers or demo visitors using a desktop browser;
  responsive polish for mobile is nice-to-have, not required for v1.
- “Agent” means a backend-driven conversational responder that produces
  natural-language replies to the user’s messages. v1 model access is via
  **Vercel AI Gateway** with default model `google/gemini-3.5-flash-lite`
  (planning/runtime concern documented in plan.md).
- Replies SHOULD be intelligible for Traditional Chinese input; exact
  bilingual policy is left to planning (default: reply in the user’s
  language when practical).
- Streaming means progressive text appearance in the UI; transport details
  are deferred to planning, provided the user-visible behavior matches
  SC-002.
- Single deployable / minimal process count is preferred per project
  constitution unless planning documents a justified exception.
- No authentication: anyone who can open the web UI may use the chat for
  v1 (local/demo trust model).
- Default backend location for unset environment variable is a localhost
  URL documented in the project command/README surface.
- Message length limit defaults to 4,000 characters unless planning sets a
  different explicit cap.
- Page refresh may clear the thread; no recovery UX beyond a clear empty
  state is required in v1.
