# LangChain Skills Agent 架构与工作流程分析

## 目录
- [概述](#概述)
- [核心架构](#核心架构)
- [三层加载机制](#三层加载机制)
- [模块详解](#模块详解)
- [工作流程](#工作流程)
- [流式处理架构](#流式处理架构)
- [与 Claude Agent SDK 对比](#与-claude-agent-sdk-对比)

---

## 概述

**LangChain Skills Agent** 是使用 LangChain 1.0 实现的演示项目，用于展示 Anthropic Skills 的三层加载机制底层原理。

### 核心特点
- ✅ **透明性**: 显式展示 Skills 加载的每一步
- ✅ **教育性**: 清晰的三层机制演示
- ✅ **完整性**: 支持 Extended Thinking 和流式输出
- ✅ **可扩展**: 基于 LangChain 1.0 标准接口

### 设计理念
> 让大模型成为真正的"智能体"，自己阅读指令、发现脚本、决定执行。
> 代码层面不需要特殊处理脚本发现/执行逻辑。

---

## 核心架构

### 目录结构

```
src/langchain_skills/
├── __init__.py           # 包入口，导出公共 API
├── agent.py              # 核心 Agent 实现
├── skill_loader.py       # Skills 发现和加载器
├── tools.py              # LangChain 工具定义
├── cli.py                # 命令行界面
├── web_api.py            # Web API 接口
└── stream/               # 流式处理模块
    ├── __init__.py
    ├── emitter.py        # 事件发射器
    ├── tracker.py        # 工具调用追踪器
    ├── formatter.py      # 输出格式化器
    └── utils.py          # 工具函数
```

### 核心类图

```
┌─────────────────────────────────────────────────────────┐
│           LangChainSkillsAgent                         │
├─────────────────────────────────────────────────────────┤
│ - skill_loader: SkillLoader                             │
│ - system_prompt: str                                    │
│ - context: SkillAgentContext                            │
│ - agent: LangGraph Agent                                │
│ - enable_thinking: bool                                 │
├─────────────────────────────────────────────────────────┤
│ + __init__()                                            │
│ + invoke(message): dict                                 │
│ + stream(message): Iterator[dict]                       │
│ + stream_events(message): Iterator[dict]                │
│ + get_system_prompt(): str                              │
│ + get_discovered_skills(): list[dict]                   │
└─────────────────────────────────────────────────────────┘
                         │
                         │ 使用
                         ▼
┌─────────────────────────────────────────────────────────┐
│              SkillLoader                                │
├─────────────────────────────────────────────────────────┤
│ - skill_paths: list[Path]                               │
│ - _metadata_cache: dict                                 │
├─────────────────────────────────────────────────────────┤
│ + scan_skills(): list[SkillMetadata]     # Level 1      │
│ + load_skill(name): SkillContent          # Level 2      │
│ + build_system_prompt(): str                          │
└─────────────────────────────────────────────────────────┘
                         │
                         │ 提供
                         ▼
┌─────────────────────────────────────────────────────────┐
│          ALL_TOOLS (LangChain Tools)                   │
├─────────────────────────────────────────────────────────┤
│ - load_skill: Tool     # Level 2 入口                   │
│ - bash: Tool          # Level 3 执行                    │
│ - read_file: Tool                                     │
│ - write_file: Tool                                    │
│ - glob: Tool                                           │
│ - grep: Tool                                           │
│ - edit: Tool                                           │
│ - list_dir: Tool                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 三层加载机制

### Level 1: 启动时 - Skills 元数据注入

**时机**: Agent 初始化时（`__init__`）

**实现位置**: `agent.py:123-152` → `skill_loader.py:108-148`

**工作流程**:
```python
# agent.py
def __init__(self, ...):
    self.skill_loader = SkillLoader(skill_paths)
    self.system_prompt = self._build_system_prompt()  # Level 1

def _build_system_prompt(self) -> str:
    base_prompt = "You are a helpful coding assistant..."
    return self.skill_loader.build_system_prompt(base_prompt)
```

**输出示例**:
```
## Available Skills

You have access to the following specialized skills:

- **news-extractor**: 新闻站点内容提取。支持微信公众号、今日头条、网易新闻、搜狐新闻、腾讯新闻
- **humanizer**: Remove signs of AI-generated writing from text...

### How to Use Skills
1. **Discover**: Review the skills list above
2. **Load**: When a user request matches a skill's description, use `load_skill(skill_name)`
3. **Execute**: Follow the skill's instructions, which may include running scripts via `bash`
```

**Token 消耗**: 每个 skill 约 100 tokens

---

### Level 2: 请求匹配时 - 加载详细指令

**时机**: 用户请求匹配 skill 描述时

**实现位置**: `tools.py:37-90` → `skill_loader.py:201-243`

**工作流程**:
```python
# tools.py
@tool
def load_skill(skill_name: str, runtime: ToolRuntime[SkillAgentContext]) -> str:
    loader = runtime.context.skill_loader
    skill_content = loader.load_skill(skill_name)
    return f"# Skill: {skill_name}\n\n{skill_content.instructions}"

# skill_loader.py
def load_skill(self, skill_name: str) -> Optional[SkillContent]:
    metadata = self._metadata_cache.get(skill_name)
    skill_md = metadata.skill_path / "SKILL.md"
    content = skill_md.read_text()
    # 提取 body（去除 frontmatter）
    return SkillContent(metadata=metadata, instructions=body)
```

**输出示例**:
```markdown
# Skill: news-extractor

## Instructions

当用户需要提取新闻内容时...

## Skill Path Info

- **Skill Directory**: `/path/to/.claude/skills/news-extractor`
- **Scripts Directory**: `/path/to/.claude/skills/news-extractor/scripts`

**Important**: When running scripts, use absolute paths like:
```bash
uv run {scripts_dir}/extract_news.py [args]
```
```

**Token 消耗**: 每个 skill 约 5k tokens

---

### Level 3: 执行时 - 运行脚本

**时机**: skill 指令中要求执行脚本时

**实现位置**: `tools.py:93-156`

**工作流程**:
```python
# tools.py
@tool
def bash(command: str, runtime: ToolRuntime[SkillAgentContext]) -> str:
    result = subprocess.run(
        command,
        shell=True,
        cwd=str(runtime.context.working_directory),
        capture_output=True,
        text=True,
        timeout=300,
    )
    # 返回带状态标记的输出
    if result.returncode == 0:
        return "[OK]\n\n{result.stdout}"
    else:
        return f"[FAILED] Exit code: {result.returncode}\n\n{result.stderr}"
```

**关键设计**:
- ⚠️ **脚本代码不进入上下文**，只有输出进入
- 支持状态检测：`[OK]` / `[FAILED]` 前缀
- 5 分钟超时保护
- 300 秒后自动终止

---

## 模块详解

### 1. agent.py - 核心实现

**LangChainSkillsAgent 类**

```python
class LangChainSkillsAgent:
    """基于 LangChain 1.0 的 Skills Agent"""

    def __init__(self, model, skill_paths, enable_thinking=True):
        # 1. 初始化 SkillLoader
        self.skill_loader = SkillLoader(skill_paths)

        # 2. Level 1: 构建 system prompt
        self.system_prompt = self._build_system_prompt()

        # 3. 创建上下文
        self.context = SkillAgentContext(
            skill_loader=self.skill_loader,
            working_directory=Path.cwd()
        )

        # 4. 创建 LangChain Agent
        self.agent = self._create_agent()
```

**关键方法**:

| 方法 | 功能 | 流模式 |
|------|------|--------|
| `invoke()` | 同步调用，等待完整响应 | ❌ |
| `stream()` | 状态级流式（每次完整状态更新） | ✅ values |
| `stream_events()` | 事件级流式（token 级） | ✅ messages |

**Extended Thinking 支持**:
```python
# 仅 Anthropic 模型支持
if enable_thinking and not is_glm_model:
    init_kwargs["thinking"] = {
        "type": "enabled",
        "budget_tokens": 10000
    }
```

---

### 2. skill_loader.py - Skills 加载器

**数据类**:

```python
@dataclass
class SkillMetadata:
    """Level 1: 元数据（~100 tokens）"""
    name: str
    description: str
    skill_path: Path

@dataclass
class SkillContent:
    """Level 2: 完整内容（~5k tokens）"""
    metadata: SkillMetadata
    instructions: str  # SKILL.md body
```

**SkillLoader 类**:

```python
class SkillLoader:
    DEFAULT_SKILL_PATHS = [
        Path.cwd() / ".claude" / "skills",    # 项目级 - 优先
        Path.home() / ".claude" / "skills",    # 用户级 - 兜底
    ]

    def scan_skills(self) -> list[SkillMetadata]:
        """遍历目录，解析 YAML frontmatter"""

    def load_skill(self, skill_name: str) -> Optional[SkillContent]:
        """读取 SKILL.md 完整内容"""

    def build_system_prompt(self, base_prompt: str) -> str:
        """生成包含 Skills 列表的 system prompt"""
```

**Skills 目录结构**:
```
my-skill/
├── SKILL.md          # 必需：YAML frontmatter + 指令
├── scripts/          # 可选：可执行脚本
│   └── script.py
├── references/       # 可选：参考文档
└── assets/           # 可选：模板和资源
```

**SKILL.md 格式**:
```markdown
---
name: skill-name
description: 何时使用此 skill 的描述
---

# Skill 详细指令

这里是完整的指令内容...
```

---

### 3. tools.py - LangChain 工具定义

**工具列表**:

| 工具名 | 用途 | 示例 |
|-------|------|------|
| `load_skill` | Level 2 入口 | `load_skill("news-extractor")` |
| `bash` | Level 3 执行 | `bash("uv run script.py")` |
| `read_file` | 读取文件 | `read_file("output.txt")` |
| `write_file` | 写入文件 | `write_file("out.txt", "content")` |
| `glob` | 文件匹配 | `glob("**/*.py")` |
| `grep` | 搜索内容 | `grep("TODO", ".")` |
| `edit` | 编辑文件 | `edit(file, old, new)` |
| `list_dir` | 列出目录 | `list_dir(".")` |

**SkillAgentContext**:

```python
@dataclass
class SkillAgentContext:
    """Agent 运行时上下文"""
    skill_loader: SkillLoader
    working_directory: Path
```

**ToolRuntime 访问**:

```python
@tool
def my_tool(arg: str, runtime: ToolRuntime[SkillAgentContext]) -> str:
    # 访问上下文
    loader = runtime.context.skill_loader
    cwd = runtime.context.working_directory

    # 访问状态
    state = runtime.state
```

---

### 4. stream/ - 流式处理模块

#### 4.1 emitter.py - 事件发射器

```python
@dataclass
class StreamEvent:
    type: str  # "thinking" | "text" | "tool_call" | "tool_result" | "done"
    data: dict

class StreamEventEmitter:
    def thinking(self, content: str) -> StreamEvent:
        """思考内容片段"""

    def text(self, content: str) -> StreamEvent:
        """响应文本片段"""

    def tool_call(self, name: str, args: dict, tool_id: str) -> StreamEvent:
        """工具调用"""

    def tool_result(self, name: str, content: str, success: bool) -> StreamEvent:
        """工具结果"""

    def done(self, response: str) -> StreamEvent:
        """完成标记"""
```

#### 4.2 tracker.py - 工具调用追踪器

```python
class ToolCallTracker:
    """处理增量到达的工具参数"""

    def update(self, tool_id: str, name: str, args: dict):
        """更新工具调用信息"""

    def append_json_delta(self, partial_json: str, index: int):
        """累积 input_json_delta 片段"""

    def finalize_all(self):
        """解析所有累积的 JSON 片段"""

    def is_ready(self, tool_id: str) -> bool:
        """检查是否准备好发送"""
```

**解决的问题**:
LangChain 流式传输中，工具参数可能分批到达：
1. `tool_use` 块先到达（`input` 可能为 `None` 或 `{}`）
2. `input_json_delta` 分批传递参数片段
3. `finalize_all()` 在收到 `tool_result` 前解析完整 JSON

#### 4.3 formatter.py - 输出格式化器

```python
class ToolResultFormatter:
    """工具结果格式化（检测状态、折叠长输出）"""

    SUCCESS_PREFIX = "[OK]"
    FAILURE_PREFIX = "[FAILED]"

    def format(self, content: str) -> FormattedResult:
        """格式化工具输出"""
```

---

## 工作流程

### 完整执行流程

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 用户输入                                                 │
│    "提取这篇公众号文章: https://mp.weixin.qq.com/s/xxx"      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Agent 检索 Level 1 (system_prompt)                      │
│                                                              │
│    System Prompt 包含:                                       │
│    - **news-extractor**: 新闻站点内容提取...                │
│    - **humanizer**: Remove signs of AI writing...          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Agent 匹配 skill 描述，决定调用 load_skill 工具           │
│                                                              │
│    Tool Call: load_skill("news-extractor")                 │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Level 2 加载详细指令                                     │
│                                                              │
│    返回 SKILL.md 完整内容 (~5k tokens):                     │
│    - 使用方法                                                │
│    - 脚本路径                                                │
│    - 参数说明                                                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Agent 根据指令执行脚本 (Level 3)                          │
│                                                              │
│    Tool Call: bash("uv run scripts/extract_news.py URL")   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. 脚本执行，输出进入上下文                                  │
│                                                              │
│    [OK]                                                     │
│                                                              │
│    {"title": "...", "content": "...", ...}                  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Agent 处理输出，生成最终响应                               │
│                                                              │
│    "已成功提取文章内容：\n                                    │
│     标题：XXX\n                                              │
│     内容：YYY..."                                            │
└─────────────────────────────────────────────────────────────┘
```

### 流式输出流程 (stream_events)

```
agent.stream_events(message)
    │
    ├─→ event 1: {"type": "thinking", "content": "用户想提取文章..."}
    │   └─→ 🧠 Thinking 面板更新（蓝色）
    │
    ├─→ event 2: {"type": "thinking", "content": "应该使用 news-extractor skill"}
    │   └─→ 🧠 Thinking 面板更新
    │
    ├─→ event 3: {"type": "tool_call", "name": "load_skill", "args": {...}}
    │   └─→ ● Skill(news-extractor) - 执行中（黄色）
    │
    ├─→ event 4: {"type": "tool_result", "name": "load_skill", "success": true}
    │   └─→ ● Skill(news-extractor) - 成功（绿色）
    │
    ├─→ event 5: {"type": "thinking", "content": "根据指令执行脚本..."}
    │   └─→ 🧠 Thinking 面板更新
    │
    ├─→ event 6: {"type": "tool_call", "name": "bash", "args": {...}}
    │   └─→ ● Bash(uv run extract_news.py...) - 执行中
    │
    ├─→ event 7: {"type": "tool_result", "name": "bash", "success": true}
    │   └─→ ● Bash(...) - 成功
    │       └─→ [OK]
    │           {"title": "...", ...}
    │
    ├─→ event 8: {"type": "text", "content": "已成功提取文章"}
    │   └─→ 💬 Response 面板更新
    │
    ├─→ event 9: {"type": "text", "content": "标题：XXX"}
    │   └─→ 💬 Response 面板更新
    │
    └─→ event 10: {"type": "done", "response": "..."}
        └─→ 💬 完成响应
```

---

## 流式处理架构

### Stream Mode 对比

| Mode | 用途 | 粒度 | 实现 |
|------|------|------|------|
| `values` | 状态级流式 | 完整状态更新 | `stream(mode="values")` |
| `messages` | 事件级流式 | token 级片段 | `stream(mode="messages")` |

**agent.py 实现**:

```python
def stream(self, message: str):
    """状态级流式 - 每次 yield 完整的 agent state"""
    for chunk in self.agent.stream(..., stream_mode="values"):
        yield chunk

def stream_events(self, message: str):
    """事件级流式 - token 级事件"""
    for chunk in self.agent.stream(..., stream_mode="messages"):
        # 解析 AIMessageChunk
        for block in chunk.content_blocks:
            if block.type == "thinking":
                yield emitter.thinking(block.thinking)
            elif block.type == "text":
                yield emitter.text(block.text)
            elif block.type == "tool_use":
                yield emitter.tool_call(...)
```

### CLI 渲染 (Rich Live Display)

**cli.py:72-119** - `StreamState` 类

```python
class StreamState:
    def __init__(self):
        self.thinking_text = ""      # 🧠 Thinking 面板
        self.response_text = ""      # 💬 Response 面板
        self.tool_calls = []         # ● Tool Calls 列表
        self.tool_results = []       # 工具执行结果

    def handle_event(self, event: dict):
        """处理事件，更新状态"""
        event_type = event.get("type")

        if event_type == "thinking":
            self.thinking_text += event.get("content", "")

        elif event_type == "tool_call":
            self.tool_calls.append(event)

        elif event_type == "tool_result":
            self.tool_results.append(event)

        elif event_type == "text":
            self.response_text += event.get("content", "")

    def render(self):
        """生成 Rich 可渲染对象"""
        return Group(
            Panel(self.thinking_text, title="🧠 Thinking", ...),
            self._render_tool_calls(),
            Panel(self.response_text, title="💬 Response", ...)
        )
```

**Rich Live Display**:
```python
with Live(console=console, refresh_per_second=10) as live:
    for event in agent.stream_events(message):
        state.handle_event(event)
        live.update(state.render())
```

---

## 与 Claude Agent SDK 对比

### Claude Agent SDK 实现

```python
from anthropic import Anthropic
from anthropic_skills import SkillsClient

client = Anthropic()
skills = SkillsClient(
    client=client,
    setting_sources=["user", "project"]  # 自动处理
)

# 自动三层加载
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "提取文章"}],
    skills=skills  # 自动注入
)
```

**特点**:
- ✅ 简洁：一行代码配置
- ❌ 不透明：内部实现隐藏
- ❌ 难调试：无法观察加载过程

### LangChain 实现

```python
from langchain_skills import LangChainSkillsAgent

agent = LangChainSkillsAgent()

# Level 1: 查看元数据
print(agent.get_system_prompt())

# Level 2: 手动加载（可选）
skill = agent.skill_loader.load_skill("news-extractor")

# 执行（自动 Level 2 + Level 3）
for event in agent.stream_events("提取文章"):
    print(event)
```

**特点**:
- ✅ 透明：每一步清晰可见
- ✅ 可控：可手动干预加载过程
- ✅ 教育性：适合学习底层原理
- ❌ 冗长：需要更多代码

---

## 关键设计决策

### 1. 为什么不自动收集 scripts？

**设计理念**:
> 让大模型从指令中自己发现脚本，而不是代码预先列出所有脚本。

**好处**:
- 减少 token 消耗（脚本代码不进入上下文）
- 更符合 LLM 的自然交互方式
- 指令可以动态更新脚本路径

**实现**:
```python
# ❌ 不这样做
def load_skill(name):
    scripts = list(skill_path.glob("scripts/*"))  # 预先收集
    return f"可用脚本：{scripts}"

# ✅ 这样做
def load_skill(name):
    instructions = read_skill_md()  # 只返回指令
    return f"脚本目录：{skill_path}/scripts/"
    # 指令中会说明如何使用脚本
```

### 2. 为什么使用 ToolRuntime 而不是全局变量？

**LangChain 1.0 设计**:
```python
@tool
def my_tool(arg: str, runtime: ToolRuntime[MyContext]) -> str:
    # ✅ 类型安全
    loader = runtime.context.skill_loader

# ❌ 避免全局变量
GLOBAL_LOADER = None
def my_tool(arg: str):
    loader = GLOBAL_LOADER
```

**好处**:
- 类型安全
- 易于测试（可 mock runtime）
- 避免全局状态

### 3. 为什么需要 ToolCallTracker？

**问题**: LangChain 流式传输中，工具参数分批到达

```python
# 第一批 chunk
{
    "type": "tool_use",
    "id": "tool_123",
    "input": {}  # 参数为空
}

# 第二批 chunk
{
    "type": "input_json_delta",
    "partial_json": '{"command": "ls',
    "index": 0
}

# 第三批 chunk
{
    "type": "input_json_delta",
    "partial_json": '"}',
    "index": 0
}
```

**解决**: 累积 JSON 片段，在 `tool_result` 前最终化

```python
tracker.append_json_delta('{"command": "ls')
tracker.append_json_delta('"}')
tracker.finalize_all()  # 解析完整 JSON
```

---

## 依赖关系图

```
langchain_skills/
│
├── agent.py
│   ├── langchain.agents (create_agent)
│   ├── langchain.chat_models (init_chat_model)
│   ├── langchain_core.messages (AIMessage)
│   ├── langgraph.checkpoint (InMemorySaver)
│   ├── .skill_loader (SkillLoader)
│   ├── .tools (ALL_TOOLS, SkillAgentContext)
│   └── .stream (StreamEventEmitter, ToolCallTracker)
│
├── skill_loader.py
│   ├── pathlib (Path)
│   ├── yaml (safe_load)
│   └── dataclasses (dataclass)
│
├── tools.py
│   ├── langchain.tools (@tool, ToolRuntime)
│   ├── subprocess (run)
│   ├── re (compile)
│   └── .skill_loader (SkillLoader)
│
├── cli.py
│   ├── rich (Console, Live, Panel)
│   ├── prompt_toolkit (PromptSession)
│   ├── .agent (LangChainSkillsAgent)
│   └── .stream (ToolResultFormatter)
│
└── stream/
    ├── emitter.py
    │   └── dataclasses (dataclass)
    │
    ├── tracker.py
    │   ├── json (loads)
    │   └── dataclasses (dataclass)
    │
    ├── formatter.py
    │   └── re (compile)
    │
    └── utils.py
        └── pathlib (Path)
```

---

## 配置与扩展

### 环境变量

| 变量名 | 说明 | 默认值 |
|-------|------|--------|
| `CLAUDE_MODEL` | 模型名称 | `claude-sonnet-4-5-20250929` |
| `ANTHROPIC_API_KEY` | 标准 API Key | - |
| `ANTHROPIC_AUTH_TOKEN` | 第三方代理 Token | - |
| `ANTHROPIC_BASE_URL` | 第三方代理 URL | - |
| `MAX_TOKENS` | 最大 tokens | 16000 |
| `MODEL_TEMPERATURE` | 温度参数 | 1.0 (thinking 时) |

### 支持的模型

| 模型 | Provider | Extended Thinking |
|------|----------|-------------------|
| `claude-sonnet-4-5-*` | anthropic | ✅ |
| `claude-opus-4-*` | anthropic | ✅ |
| `glm-*` | openai | ❌ |

### 自定义 Skills 路径

```python
from pathlib import Path
from langchain_skills import LangChainSkillsAgent

agent = LangChainSkillsAgent(
    skill_paths=[
        Path("/custom/skills/path"),
        Path.cwd() / ".claude" / "skills"
    ]
)
```

---

## 性能考虑

### Token 消耗

| 阶段 | 消耗 | 说明 |
|------|------|------|
| Level 1 | ~100 tokens/skill | 启动时一次性 |
| Level 2 | ~5k tokens/skill | 按需加载 |
| Level 3 | 0 tokens | 输出不计入 |

**优化策略**:
1. 只加载需要的 skill（Level 2 按需）
2. 脚本代码不进入上下文
3. 输出折叠（超过 2000 行截断）

### 超时配置

| 操作 | 超时 | 说明 |
|------|------|------|
| bash 工具 | 300 秒 | 5 分钟 |
| 流式传输 | 无限制 | 直到 agent 完成 |

---

## 测试与调试

### 调试模式

```bash
export SKILLS_DEBUG=1
uv run langchain-skills "你的问题"
```

**输出**:
```
[DEBUG] Event: AIMessageChunk
[DEBUG] Yielding: thinking
[DEBUG] Yielding: tool_call
[DEBUG] Processing tool result: load_skill
...
```

### 查看加载的 Skills

```bash
uv run langchain-skills --list-skills
```

### 查看 System Prompt

```bash
uv run langchain-skills --show-prompt
```

---

## 总结

LangChain Skills Agent 是一个优秀的教育项目，清晰展示了：

1. **三层加载机制**: Level 1（元数据）→ Level 2（指令）→ Level 3（执行）
2. **流式处理**: token 级事件流和 Rich Live Display
3. **工具系统**: 基于 LangChain 1.0 的 ToolRuntime
4. **透明性**: 每一步都清晰可见

适合用于：
- 📚 学习 Anthropic Skills 原理
- 🔧 自定义 agent 实现
- 🎓 教学和演示

**项目地址**: `src/langchain_skills/`

**关键文件**:
- `agent.py` - 核心逻辑
- `skill_loader.py` - Skills 加载
- `tools.py` - 工具定义
- `cli.py` - 命令行界面
- `stream/` - 流式处理

---

## 参考资料

- [LangChain 1.0 文档](https://python.langchain.com/docs/versions/introduction/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Skills 格式规范](https://docs.anthropic.com/docs/build-with-claude/skills)
- [Rich 库文档](https://rich.readthedocs.io/)

---

**生成时间**: 2026-02-14
**分析版本**: langchain-skills-agent 0.1.0
