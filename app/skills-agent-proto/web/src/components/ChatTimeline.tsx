import { memo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { AssistantEntry, SystemEntry, TimelineEntry, UserEntry } from "../state/chatReducer";
import { ToolCallItem } from "./ToolCallItem";

type ChatTimelineProps = {
  entries: TimelineEntry[];
  onToggleToolExpand: (assistantId: string, toolId: string) => void;
};

function phaseLabel(phase: string): string {
  switch (phase) {
    case "waiting":
      return "AI 正在思考中...";
    case "thinking":
      return "Thinking";
    case "analyzing":
      return "AI 正在分析结果...";
    case "responding":
      return "Generating Response";
    case "done":
      return "Completed";
    case "error":
      return "Error";
    default:
      return phase;
  }
}

function showSpinner(phase: string): boolean {
  return (
    phase === "waiting" ||
    phase === "thinking" ||
    phase === "analyzing" ||
    phase === "responding"
  );
}

const UserMessage = memo(function UserMessage({ entry }: { entry: UserEntry }) {
  return (
    <article className="message message--user">
      <header>User</header>
      <p>{entry.text}</p>
    </article>
  );
});

const SystemMessage = memo(function SystemMessage({ entry }: { entry: SystemEntry }) {
  return (
    <article className="message message--system">
      <header>Command</header>
      {entry.markdown ? (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {entry.text}
        </ReactMarkdown>
      ) : (
        <p>{entry.text}</p>
      )}
    </article>
  );
});

const AssistantMessage = memo(function AssistantMessage({
  entry,
  onToggleToolExpand,
}: {
  entry: AssistantEntry;
  onToggleToolExpand: (assistantId: string, toolId: string) => void;
}) {
  return (
    <article className="message message--assistant">
      <header className="assistant-header">
        <span>Assistant</span>
        <span className="phase-pill">
          {showSpinner(entry.phase) && <span className="inline-spinner" aria-hidden />}
          {phaseLabel(entry.phase)}
        </span>
      </header>

      {entry.thinking && (
        <section className="panel panel--thinking">
          <h4>Thinking</h4>
          <pre>{entry.thinking}</pre>
        </section>
      )}

      {entry.tools.length > 0 && (
        <section className="panel panel--tools">
          <h4>Tool Calls</h4>
          <div className="tools-list">
            {entry.tools.map((tool) => (
              <ToolCallItem
                key={tool.id}
                assistantId={entry.id}
                tool={tool}
                onToggleExpand={onToggleToolExpand}
              />
            ))}
          </div>
        </section>
      )}

      {entry.response && (
        <section className="panel panel--response">
          <h4>Response</h4>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {entry.response}
          </ReactMarkdown>
        </section>
      )}

      {entry.error && <p className="error-text">{entry.error}</p>}
    </article>
  );
});

export const ChatTimeline = memo(function ChatTimeline({ entries, onToggleToolExpand }: ChatTimelineProps) {
  return (
    <section className="chat-timeline" aria-live="polite">
      {entries.length === 0 && (
        <div className="empty-state">
          <h3>Start a conversation</h3>
          <p>Paste a task, URL, or command objective. The full execution chain will stream here.</p>
        </div>
      )}

      {entries.map((entry) => {
        if (entry.kind === "user") {
          return <UserMessage key={entry.id} entry={entry} />;
        }

        if (entry.kind === "system") {
          return <SystemMessage key={entry.id} entry={entry} />;
        }

        return (
          <AssistantMessage
            key={entry.id}
            entry={entry}
            onToggleToolExpand={onToggleToolExpand}
          />
        );
      })}
    </section>
  );
});
