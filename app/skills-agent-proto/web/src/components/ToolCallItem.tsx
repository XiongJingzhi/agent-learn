import { memo } from "react";

import type { ToolCallView } from "../state/chatReducer";

const MAX_VISIBLE_LINES = 12;

type ToolCallItemProps = {
  assistantId: string;
  tool: ToolCallView;
  onToggleExpand: (assistantId: string, toolId: string) => void;
};

function formatToolCompact(tool: ToolCallView): string {
  const args = tool.args ?? {};

  if (tool.name === "load_skill") {
    const skillName = args["skill_name"];
    return typeof skillName === "string"
      ? `Skill(${skillName})`
      : "Skill(load_skill)";
  }

  if (tool.name === "bash") {
    const command = args["command"];
    return typeof command === "string" ? `Bash(${command})` : "Bash()";
  }

  if (tool.name === "read_file") {
    const filePath = args["file_path"];
    return typeof filePath === "string" ? `Read(${filePath})` : "Read()";
  }

  if (tool.name === "grep") {
    const pattern = args["pattern"];
    const path = args["path"];
    if (typeof pattern === "string" && typeof path === "string") {
      return `Grep(${pattern}, ${path})`;
    }
  }

  const summarizedArgs = Object.entries(args)
    .map(([key, value]) => `${key}=${String(value)}`)
    .join(", ");

  return summarizedArgs ? `${tool.name}(${summarizedArgs})` : `${tool.name}()`;
}

function linesWithTreePrefix(content: string, expanded: boolean): {
  lines: string[];
  hiddenCount: number;
  totalLines: number;
} {
  const normalized = content.trimEnd();
  if (!normalized) {
    return { lines: ["└ (no output)"], hiddenCount: 0, totalLines: 1 };
  }

  const rawLines = normalized.split("\n");
  const hiddenCount = expanded
    ? 0
    : Math.max(0, rawLines.length - MAX_VISIBLE_LINES);
  const visibleLines = expanded ? rawLines : rawLines.slice(0, MAX_VISIBLE_LINES);

  const prefixed = visibleLines.map((line, index) =>
    index === 0 ? `└ ${line}` : `  ${line}`,
  );
  return { lines: prefixed, hiddenCount, totalLines: rawLines.length };
}

export const ToolCallItem = memo(function ToolCallItem({
  assistantId,
  tool,
  onToggleExpand,
}: ToolCallItemProps) {
  const statusClass =
    tool.status === "running"
      ? "tool-call__dot tool-call__dot--running"
      : tool.status === "success"
        ? "tool-call__dot tool-call__dot--success"
        : "tool-call__dot tool-call__dot--failed";

  const expanded = Boolean(tool.expanded);
  const { lines, hiddenCount, totalLines } = linesWithTreePrefix(
    tool.result ?? "",
    expanded,
  );

  return (
    <article className="tool-call">
      <header className="tool-call__header">
        <span className={statusClass}>
          ●
          {tool.status === "running" && <span className="inline-spinner" aria-hidden />}
        </span>
        <strong>{formatToolCompact(tool)}</strong>
      </header>

      {tool.skillName && (
        <div className="tool-call__skill-tag">Detected skill: {tool.skillName}</div>
      )}

      {tool.result && (
        <div className="tool-call__result">
          <pre>{lines.join("\n")}</pre>
          {hiddenCount > 0 && (
            <button
              type="button"
              className="link-button"
              onClick={() => onToggleExpand(assistantId, tool.id)}
            >
              Show {hiddenCount} more lines
            </button>
          )}
          {hiddenCount === 0 && expanded && totalLines > MAX_VISIBLE_LINES && (
            <button
              type="button"
              className="link-button"
              onClick={() => onToggleExpand(assistantId, tool.id)}
            >
              {expanded ? "Collapse output" : "Expand output"}
            </button>
          )}
        </div>
      )}
    </article>
  );
});
