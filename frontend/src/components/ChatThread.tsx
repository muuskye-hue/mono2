import {
  AuiIf,
  ComposerPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
} from "@assistant-ui/react";

export function ChatThread() {
  return (
    <ThreadPrimitive.Root className="thread-root">
      <ThreadPrimitive.Viewport className="thread-viewport">
        <AuiIf condition={(s) => s.thread.isEmpty}>
          <div className="welcome">
            <h2>Agent Chat</h2>
            <p>輸入繁體中文訊息，助理會串流回覆。</p>
          </div>
        </AuiIf>

        <ThreadPrimitive.Messages>
          {({ message }) =>
            message.role === "user" ? <UserMessage /> : <AssistantMessage />
          }
        </ThreadPrimitive.Messages>

        <ThreadPrimitive.ViewportFooter className="thread-footer">
          <Composer />
        </ThreadPrimitive.ViewportFooter>
      </ThreadPrimitive.Viewport>
    </ThreadPrimitive.Root>
  );
}

function UserMessage() {
  return (
    <MessagePrimitive.Root className="message user">
      <div className="bubble">
        <MessagePrimitive.Parts />
      </div>
    </MessagePrimitive.Root>
  );
}

function AssistantMessage() {
  return (
    <MessagePrimitive.Root className="message assistant">
      <div className="bubble">
        <MessagePrimitive.Parts />
      </div>
    </MessagePrimitive.Root>
  );
}

function Composer() {
  return (
    <ComposerPrimitive.Root className="composer">
      <ComposerPrimitive.Input
        className="composer-input"
        placeholder="輸入訊息體中文訊息…"
        rows={1}
      />
      <AuiIf condition={(s) => !s.thread.isRunning}>
        <ComposerPrimitive.Send className="composer-send">
          送出
        </ComposerPrimitive.Send>
      </AuiIf>
      <AuiIf condition={(s) => s.thread.isRunning}>
        <ComposerPrimitive.Cancel className="composer-cancel">
          停止
        </ComposerPrimitive.Cancel>
      </AuiIf>
    </ComposerPrimitive.Root>
  );
}
