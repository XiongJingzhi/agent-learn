import { describe, expect, it } from "vitest";

import { chatReducer, createInitialState } from "./chatReducer";

describe("chatReducer", () => {
  it("creates waiting assistant turn when user submits message", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "submit_user_message",
      threadId: "thread-1",
      message: "extract this url",
      userEntryId: "user-1",
      assistantEntryId: "assistant-1",
      createdAt: 1,
    });

    const timeline = next.threads["thread-1"].timeline;
    expect(next.isStreaming).toBe(true);
    expect(timeline).toHaveLength(2);
    expect(timeline[0]).toMatchObject({ kind: "user", text: "extract this url" });
    expect(timeline[1]).toMatchObject({ kind: "assistant", phase: "waiting" });
  });

  it("applies thinking and text stream events incrementally", () => {
    const start = chatReducer(createInitialState(), {
      type: "submit_user_message",
      threadId: "thread-1",
      message: "hello",
      userEntryId: "user-1",
      assistantEntryId: "assistant-1",
      createdAt: 1,
    });

    const withThinking = chatReducer(start, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: { type: "thinking", content: "plan " },
    });

    const withText = chatReducer(withThinking, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: { type: "text", content: "answer" },
    });

    const assistant = withText.threads["thread-1"].timeline[1];
    expect(assistant).toMatchObject({
      kind: "assistant",
      phase: "responding",
      thinking: "plan ",
      response: "answer",
    });
  });

  it("deduplicates tool_call by tool id and tracks detected skill", () => {
    const start = chatReducer(createInitialState(), {
      type: "submit_user_message",
      threadId: "thread-1",
      message: "use skill",
      userEntryId: "user-1",
      assistantEntryId: "assistant-1",
      createdAt: 1,
    });

    const firstCall = chatReducer(start, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: {
        type: "tool_call",
        name: "load_skill",
        id: "tool-1",
        args: {},
      },
    });

    const secondCall = chatReducer(firstCall, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: {
        type: "tool_call",
        name: "load_skill",
        id: "tool-1",
        args: { skill_name: "news-extractor" },
      },
    });

    const assistant = secondCall.threads["thread-1"].timeline[1];
    expect(assistant.kind).toBe("assistant");
    if (assistant.kind !== "assistant") return;

    expect(assistant.tools).toHaveLength(1);
    expect(assistant.tools[0].id).toBe("tool-1");
    expect(assistant.tools[0].args).toMatchObject({ skill_name: "news-extractor" });
    expect(secondCall.threads["thread-1"].activeSkillName).toBe("news-extractor");
  });

  it("marks tool result status and transitions to done on done event", () => {
    const submitted = chatReducer(createInitialState(), {
      type: "submit_user_message",
      threadId: "thread-1",
      message: "run tool",
      userEntryId: "user-1",
      assistantEntryId: "assistant-1",
      createdAt: 1,
    });

    const withToolCall = chatReducer(submitted, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: {
        type: "tool_call",
        id: "tool-1",
        name: "bash",
        args: { command: "echo ok" },
      },
    });

    const withResult = chatReducer(withToolCall, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: {
        type: "tool_result",
        name: "bash",
        content: "[OK]\n\nok",
        success: true,
      },
    });

    const done = chatReducer(withResult, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: {
        type: "done",
        response: "final answer",
      },
    });

    const assistant = done.threads["thread-1"].timeline[1];
    expect(assistant.kind).toBe("assistant");
    if (assistant.kind !== "assistant") return;

    expect(assistant.tools[0].status).toBe("success");
    expect(assistant.phase).toBe("done");
    expect(assistant.response).toBe("final answer");
    expect(done.isStreaming).toBe(false);
  });

  it("stores skills on skills_loaded", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "skills_loaded",
      skills: [
        { name: "news-extractor", description: "Extract news", path: "/skills/news" },
      ],
    });

    expect(next.skillsLoaded).toBe(true);
    expect(next.skillsError).toBeUndefined();
    expect(next.skills).toHaveLength(1);
    expect(next.skills[0].name).toBe("news-extractor");
  });

  it("records error on skills_failed", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "skills_failed",
      message: "network error",
    });

    expect(next.skillsLoaded).toBe(true);
    expect(next.skillsError).toBe("network error");
    expect(next.skills).toHaveLength(0);
  });

  it("caches prompt on prompt_loaded", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "prompt_loaded",
      prompt: "You are a test agent.",
    });

    expect(next.promptCache).toBe("You are a test agent.");
  });

  it("creates a new thread and switches to it", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "create_thread",
      threadId: "thread-2",
      label: "Thread 2",
    });

    expect(next.activeThreadId).toBe("thread-2");
    expect(next.threadOrder).toContain("thread-2");
    expect(next.threads["thread-2"]).toMatchObject({
      id: "thread-2",
      label: "Thread 2",
      timeline: [],
    });
  });

  it("switches to existing thread on duplicate create_thread", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "create_thread",
      threadId: "thread-1",
      label: "Thread 1 dup",
    });

    expect(next.activeThreadId).toBe("thread-1");
    expect(next.threadOrder).toHaveLength(1);
  });

  it("switches thread on switch_thread", () => {
    let state = createInitialState();
    state = chatReducer(state, {
      type: "create_thread",
      threadId: "thread-2",
      label: "Thread 2",
    });

    const next = chatReducer(state, {
      type: "switch_thread",
      threadId: "thread-1",
    });

    expect(next.activeThreadId).toBe("thread-1");
  });

  it("ignores switch_thread for non-existing thread", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "switch_thread",
      threadId: "non-existing",
    });

    expect(next.activeThreadId).toBe("thread-1");
    expect(next).toBe(state);
  });

  it("appends system message to thread", () => {
    const state = createInitialState();
    const next = chatReducer(state, {
      type: "append_system_message",
      threadId: "thread-1",
      entryId: "sys-1",
      message: "## Skills List",
      markdown: true,
      createdAt: 100,
    });

    const timeline = next.threads["thread-1"].timeline;
    expect(timeline).toHaveLength(1);
    expect(timeline[0]).toMatchObject({
      kind: "system",
      id: "sys-1",
      text: "## Skills List",
      markdown: true,
    });
  });

  it("toggles tool expanded state", () => {
    let state = createInitialState();
    state = chatReducer(state, {
      type: "submit_user_message",
      threadId: "thread-1",
      message: "test",
      userEntryId: "user-1",
      assistantEntryId: "assistant-1",
      createdAt: 1,
    });
    state = chatReducer(state, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: { type: "tool_call", id: "tool-1", name: "bash", args: { command: "ls" } },
    });

    const toggled = chatReducer(state, {
      type: "toggle_tool_expand",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      toolId: "tool-1",
    });

    const assistant = toggled.threads["thread-1"].timeline[1];
    expect(assistant.kind).toBe("assistant");
    if (assistant.kind !== "assistant") return;
    expect(assistant.tools[0].expanded).toBe(true);

    const toggledBack = chatReducer(toggled, {
      type: "toggle_tool_expand",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      toolId: "tool-1",
    });

    const assistant2 = toggledBack.threads["thread-1"].timeline[1];
    if (assistant2.kind !== "assistant") return;
    expect(assistant2.tools[0].expanded).toBe(false);
  });

  it("handles error stream event", () => {
    const submitted = chatReducer(createInitialState(), {
      type: "submit_user_message",
      threadId: "thread-1",
      message: "hello",
      userEntryId: "user-1",
      assistantEntryId: "assistant-1",
      createdAt: 1,
    });

    const errored = chatReducer(submitted, {
      type: "stream_event",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      event: { type: "error", message: "agent crashed" },
    });

    const assistant = errored.threads["thread-1"].timeline[1];
    expect(assistant.kind).toBe("assistant");
    if (assistant.kind !== "assistant") return;

    expect(assistant.phase).toBe("error");
    expect(assistant.error).toBe("agent crashed");
    expect(errored.isStreaming).toBe(false);
    expect(errored.streamError).toBe("agent crashed");
  });

  it("records stream failure on connection errors", () => {
    const submitted = chatReducer(createInitialState(), {
      type: "submit_user_message",
      threadId: "thread-1",
      message: "hello",
      userEntryId: "user-1",
      assistantEntryId: "assistant-1",
      createdAt: 1,
    });

    const failed = chatReducer(submitted, {
      type: "stream_failed",
      threadId: "thread-1",
      assistantEntryId: "assistant-1",
      message: "SSE closed unexpectedly",
    });

    const assistant = failed.threads["thread-1"].timeline[1];
    expect(assistant.kind).toBe("assistant");
    if (assistant.kind !== "assistant") return;

    expect(assistant.phase).toBe("error");
    expect(assistant.error).toContain("SSE closed unexpectedly");
    expect(failed.isStreaming).toBe(false);
  });
});
