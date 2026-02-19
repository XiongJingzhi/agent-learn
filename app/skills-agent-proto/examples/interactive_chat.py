"""
交互式对话示例 - 与 LangChain Skills Agent 进行多轮对话

这个示例展示了如何进行交互式对话，支持：
- 流式输出（逐字显示响应）
- Extended Thinking 显示（模型思考过程）
- 多轮对话记忆

运行方式:
    uv run python examples/interactive_chat.py

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
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text

from langchain_skills import LangChainSkillsAgent

console = Console()


def print_banner():
    """打印欢迎横幅"""
    console.print(Panel(
        "[bold cyan]LangChain Skills Agent 交互式对话[/bold cyan]\n\n"
        "你可以与 Agent 进行多轮对话，Agent 能够：\n"
        "- 自动发现和使用 ~/.claude/skills/ 中的 Skills\n"
        "- 读取、编辑文件\n"
        "- 执行命令\n\n"
        "[bold green]流式输出功能：[/bold green]\n"
        "- 🧠 实时显示模型思考过程（蓝色）\n"
        "- 🔧 显示工具调用（黄色）\n"
        "- 💬 逐字显示响应（绿色）\n\n"
        "[dim]输入 /exit 退出，/skills 查看可用 Skills[/dim]",
        title="欢迎"
    ))
    console.print()


def create_streaming_display(
    thinking_text: str = "",
    response_text: str = "",
    tool_calls: list = None,
    is_thinking: bool = False,
    is_responding: bool = False,
) -> Group:
    """创建流式显示的布局"""
    elements = []

    # Thinking 面板
    if thinking_text:
        thinking_title = "🧠 Thinking"
        if is_thinking:
            thinking_title += " ..."
        display_thinking = thinking_text
        if len(display_thinking) > 800:
            display_thinking = "..." + display_thinking[-800:]
        elements.append(Panel(
            Text(display_thinking, style="dim"),
            title=thinking_title,
            border_style="blue",
            padding=(0, 1),
        ))

    # Tool Calls 显示
    if tool_calls:
        for tc in tool_calls:
            tool_text = f"🔧 {tc['name']}"
            elements.append(Text(tool_text, style="yellow"))

    # Response 面板
    if response_text:
        response_title = "💬 Response"
        if is_responding:
            response_title += " ..."
        elements.append(Panel(
            Markdown(response_text),
            title=response_title,
            border_style="green",
            padding=(0, 1),
        ))
    elif is_responding and not thinking_text:
        elements.append(Text("⏳ Generating response...", style="dim"))

    return Group(*elements) if elements else Text("⏳ Processing...", style="dim")


def chat():
    """交互式对话（流式输出版本）"""

    print_banner()

    # 创建 Agent（启用 thinking）
    agent = LangChainSkillsAgent(enable_thinking=True)

    # 显示发现的 Skills
    skills = agent.get_discovered_skills()
    console.print(f"[dim]已加载 {len(skills)} 个 Skills，Extended Thinking: [green]enabled[/green][/dim]")
    console.print()

    thread_id = "interactive_demo"

    while True:
        try:
            # 获取用户输入
            user_input = Prompt.ask("[bold green]你[/bold green]")

            # 处理特殊命令
            if user_input.lower() in ("/exit", "/quit", "/q"):
                console.print("[yellow]再见！[/yellow]")
                break

            if user_input.lower() == "/skills":
                console.print("\n[bold]可用 Skills:[/bold]")
                for skill in skills:
                    console.print(f"  - [green]{skill['name']}[/green]: {skill['description'][:60]}...")
                console.print()
                continue

            if not user_input.strip():
                continue

            # 运行 Agent（流式输出）
            console.print()

            thinking_text = ""
            response_text = ""
            tool_calls = []

            with Live(console=console, refresh_per_second=10, transient=True) as live:
                for event in agent.stream_events(user_input, thread_id=thread_id):
                    event_type = event.get("type")

                    if event_type == "thinking":
                        thinking_text += event.get("content", "")
                        live.update(create_streaming_display(
                            thinking_text=thinking_text,
                            response_text=response_text,
                            tool_calls=tool_calls,
                            is_thinking=True,
                            is_responding=False,
                        ))

                    elif event_type == "text":
                        response_text += event.get("content", "")
                        live.update(create_streaming_display(
                            thinking_text=thinking_text,
                            response_text=response_text,
                            tool_calls=tool_calls,
                            is_thinking=False,
                            is_responding=True,
                        ))

                    elif event_type == "tool_call":
                        tool_calls.append({
                            "name": event.get("name", "unknown"),
                            "args": event.get("args", {}),
                        })
                        live.update(create_streaming_display(
                            thinking_text=thinking_text,
                            response_text=response_text,
                            tool_calls=tool_calls,
                            is_thinking=False,
                            is_responding=False,
                        ))

                    elif event_type == "done":
                        if not response_text:
                            response_text = event.get("response", "")

            # 显示最终结果
            if thinking_text:
                display_thinking = thinking_text
                if len(display_thinking) > 500:
                    display_thinking = display_thinking[:250] + "\n...\n" + display_thinking[-250:]
                console.print(Panel(
                    Text(display_thinking, style="dim"),
                    title="🧠 Thinking",
                    border_style="blue",
                ))

            for tc in tool_calls:
                console.print(f"[yellow]🔧 {tc['name']}[/yellow]")

            if response_text:
                console.print("[bold blue]Agent:[/bold blue]")
                console.print(Markdown(response_text))
            console.print()

        except KeyboardInterrupt:
            console.print("\n[yellow]中断，退出...[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]错误: {e}[/red]")


def main():
    """主入口"""
    chat()


if __name__ == "__main__":
    main()
