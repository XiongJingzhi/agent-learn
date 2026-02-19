import { useCallback, useEffect, useMemo, useReducer, useRef } from "react";

import { ChatTimeline } from "./components/ChatTimeline";
import { Composer } from "./components/Composer";
import { SkillPanel } from "./components/SkillPanel";
import { openChatStream } from "./lib/sse";
import {
  chatReducer,
  createInitialState,
  type SkillSummary,
} from "./state/chatReducer";
import type { AgentStreamEvent } from "./types/events";
import "./App.css";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.trim() || "http://localhost:8000";

function makeId(prefix: string): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return `${prefix}-${crypto.randomUUID()}`;
  }
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function skillsAsMarkdown(skills: SkillSummary[]): string {
  if (!skills.length) {
    return "No skills discovered.";
  }

  return [
    "## Available Skills",
    ...skills.map(
      (skill) =>
        `- **${skill.name}**: ${skill.description || "No description"}\n  - path: \`${skill.path}\``,
    ),
  ].join("\n");
}

function promptAsMarkdown(prompt: string): string {
  const escaped = prompt.replaceAll("```", "` ` `");
  return `## System Prompt\n\n\`\`\`text\n${escaped}\n\`\`\``;
}

export default function App() {
  const [state, dispatch] = useReducer(chatReducer, undefined, createInitialState);
  const streamCloserRef = useRef<(() => void) | null>(null);

  const activeThread = state.threads[state.activeThreadId];

  useEffect(() => {
    let cancelled = false;

    const loadSkills = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/skills`);
        if (!response.ok) {
          throw new Error(`Failed to load skills (${response.status})`);
        }
        const payload = (await response.json()) as { skills: SkillSummary[] };
        if (!cancelled) {
          dispatch({ type: "skills_loaded", skills: payload.skills || [] });
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        if (!cancelled) {
          dispatch({ type: "skills_failed", message });
        }
      }
    };

    loadSkills();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    return () => {
      streamCloserRef.current?.();
    };
  }, []);

  const threadOptions = useMemo(
    () =>
      state.threadOrder.map((threadId) => {
        const thread = state.threads[threadId];
        return {
          value: threadId,
          label: thread?.label || threadId,
        };
      }),
    [state.threadOrder, state.threads],
  );

  const appendSystemMessage = (content: string, markdown = true) => {
    dispatch({
      type: "append_system_message",
      threadId: state.activeThreadId,
      entryId: makeId("system"),
      message: content,
      markdown,
      createdAt: Date.now(),
    });
  };

  const handleSend = async (text: string) => {
    if (state.isStreaming) {
      return;
    }

    if (text === "/skills") {
      appendSystemMessage(skillsAsMarkdown(state.skills));
      return;
    }

    if (text === "/prompt") {
      try {
        const response = await fetch(`${API_BASE_URL}/api/prompt`);
        if (!response.ok) {
          throw new Error(`Failed to load system prompt (${response.status})`);
        }
        const payload = (await response.json()) as { prompt: string };
        dispatch({ type: "prompt_loaded", prompt: payload.prompt || "" });
        appendSystemMessage(promptAsMarkdown(payload.prompt || ""));
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        appendSystemMessage(`Error: ${message}`, false);
      }
      return;
    }

    const threadId = state.activeThreadId;
    const userEntryId = makeId("user");
    const assistantEntryId = makeId("assistant");

    dispatch({
      type: "submit_user_message",
      threadId,
      message: text,
      userEntryId,
      assistantEntryId,
      createdAt: Date.now(),
    });

    streamCloserRef.current?.();
    streamCloserRef.current = openChatStream({
      apiBaseUrl: API_BASE_URL,
      message: text,
      threadId,
      onEvent: (event: AgentStreamEvent) => {
        dispatch({
          type: "stream_event",
          threadId,
          assistantEntryId,
          event,
        });

        if (event.type === "done" || event.type === "error") {
          streamCloserRef.current = null;
        }
      },
      onError: (message) => {
        dispatch({
          type: "stream_failed",
          threadId,
          assistantEntryId,
          message,
        });
        streamCloserRef.current = null;
      },
    });
  };

  const handleToggleToolExpand = useCallback(
    (assistantId: string, toolId: string) => {
      dispatch({
        type: "toggle_tool_expand",
        threadId: state.activeThreadId,
        assistantEntryId: assistantId,
        toolId,
      });
    },
    [state.activeThreadId],
  );

  const createThread = () => {
    if (state.isStreaming) {
      return;
    }
    const threadNumber = state.threadOrder.length + 1;
    const threadId = `thread-${threadNumber}`;
    dispatch({
      type: "create_thread",
      threadId,
      label: `Thread ${threadNumber}`,
    });
  };

  return (
    <div className="app-shell">
      <header className="top-bar">
        <div className="brand">
          <p className="eyebrow">Skills Agent</p>
          <h1>Streaming Web Console</h1>
        </div>

        <div className="thread-controls">
          <label htmlFor="thread-select">Thread</label>
          <select
            id="thread-select"
            value={state.activeThreadId}
            disabled={state.isStreaming}
            onChange={(event) =>
              dispatch({
                type: "switch_thread",
                threadId: event.target.value,
              })
            }
          >
            {threadOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <button type="button" disabled={state.isStreaming} onClick={createThread}>
            New Thread
          </button>
        </div>
      </header>

      <div className="workspace">
        <SkillPanel
          skills={state.skills}
          activeSkillName={activeThread?.activeSkillName}
          loading={!state.skillsLoaded && !state.skillsError}
          error={state.skillsError}
        />

        <main className="chat-panel">
          <ChatTimeline
            entries={activeThread?.timeline || []}
            onToggleToolExpand={handleToggleToolExpand}
          />

          {state.streamError && <p className="global-error">{state.streamError}</p>}

          <Composer disabled={state.isStreaming} onSubmit={handleSend} />
        </main>
      </div>
    </div>
  );
}
