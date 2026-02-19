export type ThinkingEvent = {
  type: "thinking";
  content: string;
  id?: number;
};

export type TextEvent = {
  type: "text";
  content: string;
};

export type ToolCallEvent = {
  type: "tool_call";
  name: string;
  args: Record<string, unknown>;
  id?: string;
};

export type ToolResultEvent = {
  type: "tool_result";
  name: string;
  content: string;
  success?: boolean;
};

export type DoneEvent = {
  type: "done";
  response?: string;
};

export type ErrorEvent = {
  type: "error";
  message: string;
};

export type AgentStreamEvent =
  | ThinkingEvent
  | TextEvent
  | ToolCallEvent
  | ToolResultEvent
  | DoneEvent
  | ErrorEvent;
