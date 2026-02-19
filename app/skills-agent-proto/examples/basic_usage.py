"""
基本使用示例 - 展示 LangChain Skills Agent 的核心功能

这个示例展示了：
1. 如何创建 LangChainSkillsAgent 实例
2. 同步调用 vs 流式调用
3. Extended Thinking 功能
4. 事件流式输出

运行方式:
    uv run python examples/basic_usage.py

确保已配置认证（.env 文件或环境变量）:
    export ANTHROPIC_API_KEY=your-api-key
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text

from langchain_skills import LangChainSkillsAgent

console = Console()


def demo_streaming_with_thinking():
    """演示流式输出和 thinking 功能"""

    console.print(Panel(
        "[bold cyan]LangChain Skills Agent 流式输出演示[/bold cyan]\n\n"
        "这个示例演示：\n"
        "- 🧠 Extended Thinking: 显示模型思考过程\n"
        "- 💬 流式响应: 逐字显示输出\n"
        "- 🔧 工具调用: 实时显示调用过程",
        title="示例"
    ))
    console.print()

    # 创建 Agent 实例（启用 thinking）
    agent = LangChainSkillsAgent(enable_thinking=True)

    # 显示发现的 Skills
    skills = agent.get_discovered_skills()
    console.print(f"[dim]发现 {len(skills)} 个 Skills[/dim]")
    for skill in skills:
        console.print(f"  - {skill['name']}: {skill['description'][:50]}...")
    console.print()

    # 发送请求
    prompt = "请简要说明你能做什么，以及如何使用 Skills。"

    console.print(f"[bold green]请求:[/bold green] {prompt}")
    console.print()

    try:
        # 使用事件流式输出
        thinking_text = ""
        response_text = ""
        tool_calls = []

        console.print("[dim]使用 stream_events() 进行流式输出...[/dim]\n")

        with Live(console=console, refresh_per_second=10, transient=True) as live:
            for event in agent.stream_events(prompt):
                event_type = event.get("type")

                if event_type == "thinking":
                    thinking_text += event.get("content", "")
                    # 显示进度
                    display = []
                    if thinking_text:
                        display_thinking = thinking_text[-500:] if len(thinking_text) > 500 else thinking_text
                        display.append(Panel(
                            Text(display_thinking, style="dim"),
                            title="🧠 Thinking ...",
                            border_style="blue",
                        ))
                    live.update(Group(*display) if display else Text("⏳ Thinking...", style="dim"))

                elif event_type == "text":
                    response_text += event.get("content", "")
                    display = []
                    if thinking_text:
                        display_thinking = thinking_text[-300:] if len(thinking_text) > 300 else thinking_text
                        display.append(Panel(
                            Text(display_thinking, style="dim"),
                            title="🧠 Thinking",
                            border_style="blue",
                        ))
                    if response_text:
                        display.append(Panel(
                            Markdown(response_text),
                            title="💬 Response ...",
                            border_style="green",
                        ))
                    live.update(Group(*display) if display else Text("⏳ Responding...", style="dim"))

                elif event_type == "tool_call":
                    tool_calls.append(event)
                    console.print(f"[yellow]🔧 Tool: {event.get('name')}[/yellow]")

                elif event_type == "done":
                    if not response_text:
                        response_text = event.get("response", "")

        # 显示最终结果
        console.print()

        if thinking_text:
            display_thinking = thinking_text
            if len(display_thinking) > 1000:
                display_thinking = display_thinking[:500] + "\n\n... (truncated) ...\n\n" + display_thinking[-500:]
            console.print(Panel(
                Text(display_thinking, style="dim"),
                title="🧠 Thinking (完整)",
                border_style="blue",
            ))

        if tool_calls:
            console.print("[bold yellow]工具调用:[/bold yellow]")
            for tc in tool_calls:
                console.print(f"  - {tc.get('name')}")
            console.print()

        if response_text:
            console.print(Panel(
                Markdown(response_text),
                title="💬 Response (完整)",
                border_style="green",
            ))

        console.print()
        console.print(Panel(
            "[green]完成![/green]\n\n"
            f"Thinking tokens (估算): ~{len(thinking_text) // 4}\n"
            f"Response tokens (估算): ~{len(response_text) // 4}\n"
            f"Tool calls: {len(tool_calls)}",
            title="执行结果"
        ))

    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        console.print("[yellow]提示: 请确保已正确配置 ANTHROPIC_API_KEY[/yellow]")
        raise


def demo_without_thinking():
    """演示不启用 thinking 的情况"""

    console.print("\n")
    console.print(Panel(
        "[bold cyan]不启用 Thinking 的对比演示[/bold cyan]",
        title="对比"
    ))
    console.print()

    # 创建 Agent（不启用 thinking）
    agent = LangChainSkillsAgent(enable_thinking=False)

    prompt = "1 + 1 等于几？"
    console.print(f"[bold green]请求:[/bold green] {prompt}")
    console.print()

    try:
        response_text = ""

        for event in agent.stream_events(prompt):
            event_type = event.get("type")

            if event_type == "text":
                response_text += event.get("content", "")
                # 实时打印
                console.print(event.get("content", ""), end="")

            elif event_type == "done":
                if not response_text:
                    response_text = event.get("response", "")

        console.print("\n")
        console.print("[dim]（无 thinking 输出）[/dim]")

    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")


def main():
    """主入口"""
    demo_streaming_with_thinking()
    # 可选：运行不启用 thinking 的对比演示
    # demo_without_thinking()


if __name__ == "__main__":
    main()
