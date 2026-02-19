# Bub 项目架构分析文档

> **项目名称**: Bub  
> **版本**: 0.2.1  
> **作者**: Chojan Shang  
> **分析日期**: 2026-02-19  
> **分析目标**: 深入理解 Bub 的架构设计和核心机制

---

## 📋 目录

1. [项目概述](#项目概述)
2. [核心概念](#核心概念)
3. [架构设计](#架构设计)
4. [核心组件](#核心组件)
5. [工作流程](#工作流程)
6. [关键特性](#关键特性)
7. [技术栈](#技术栈)
8. [最佳实践](#最佳实践)

---

## 📊 项目概述

### 项目定位

Bub 是一个**基于 `republic` 的编码 Agent CLI**，专为真实的工程工作流设计，其执行必须是**可预测、可检查和可恢复**的。

### 核心理念

- **Tape-first**: 基于磁带（tape）的记录和恢复机制
- **Strict Command Boundary**: 严格的命令边界（只有以 `,` 开头的行才被视为命令）
- **Deterministic Routing**: 确定性的路由机制
- **Context Anchoring**: 上下文锚定和移交机制

### 四大核心原则

1. **Command boundary is strict**: 只有以 `,` 开头的行才被视为命令
2. **The same routing model is applied to both user input and assistant output**: 同样的路由模型应用于用户输入和助手输出
3. **Successful commands return directly; failed commands fall back to model with structured context**: 成功的命令直接返回；失败的命令回退到带有结构化上下文的模型
4. **Session context is append-only tape with explicit `anchor/handoff` transitions**: 会话上下文是仅追加的磁带，具有显式的 `anchor/handoff` 转换

---

## 🎯 核心概念

### 1. Tape（磁带）

> **定义**: Tape 是一个**仅追加的 JSONL 日志系统**，记录会话中的所有事件。

**核心特性**:
- ✅ **仅追加**: 只能追加，不能修改
- ✅ **持久化**: 所有事件都保存到磁盘
- ✅ **可查询**: 可以查询历史事件
- ✅ **可分支**: 支持创建分支
- ✅ **可归档**: 支持归档旧数据

**事件类型**:
```python
# 命令事件
"command": {
    "origin": "human" | "assistant",
    "kind": "shell" | "internal",
    "raw": "命令原文",
    "name": "命令名称",
    "status": "ok" | "error",
    "elapsed_ms": 执行时间,
    "output": "命令输出"
}

# 循环结果事件
"loop.result": {
    "steps": 步骤数,
    "followups": 后续命令,
    "exit_requested": 是否请求退出,
    "error": 错误信息
}
```

**Tape 作用**:
- 📝 **记录历史**: 记录所有命令和结果
- 🔍 **调试支持**: 提供完整的历史记录用于调试
- 🔄 **恢复机制**: 支持从任意点恢复会话
- 📊 **分析工具**: 提供数据用于分析用户行为

---

### 2. Command（命令）

> **定义**: Command 是 Bub 的**基本操作单元**，分为内部命令和 Shell 命令。

**命令类型**:

| 类型 | 前缀 | 示例 | 说明 |
|------|------|------|------|
| **内部命令** | `,` | `,help`, `,tools`, `,tape.info` | Bub 内置命令 |
| **Shell 命令** | `,` | `,git status`, `,ls -la` | 系统命令 |
| **自然语言** | 无 | `hello`, `如何使用 bub` | 发送给模型的自然语言 |

**命令解析规则**:
```python
# 内部命令
",help" → 解析为内部命令 help
",tool.describe name=fs.read" → 解析为内部命令 tool.describe

# Shell 命令
",git status" → 解析为 Shell 命令 git status
",ls -la" → 解析为 Shell 命令 ls -la

# 自然语言
"hello" → 不解析为命令，发送给模型
```

---

### 3. Router（路由器）

> **定义**: Router 是**命令路由和执行的核心组件**，负责判断输入是命令还是自然语言。

**路由流程**:

```
输入 → 解析 → 判断 → 执行
 ↓      ↓      ↓      ↓
原始文本  命令类型  路由决策  结果返回
```

**路由决策树**:
```
输入
  ├─ 以 `,` 开头？
  │   ├─ 是 → 解析为命令
  │   │   ├─ 内部命令？ → 执行内部命令
  │   │   └─ Shell 命令？ → 执行 Shell 命令
  │   └─ 否 → 发送给模型
```

**路由特性**:
- ✅ **双路由模型**: 同样的路由模型应用于用户输入和助手输出
- ✅ **上下文感知**: 失败的命令会回退到模型，带上结构化上下文
- ✅ **执行追踪**: 记录所有命令执行的时间和结果

---

### 4. Tool（工具）

> **定义**: Tool 是**可扩展的功能单元**，可以是内置工具、内部命令或技能支持的。

**工具分类**:

| 类型 | 来源 | 示例 |
|------|------|------|
| **内置工具** | Bub 内置 | `fs.read`, `fs.write`, `git.status` |
| **内部命令** | Bub 核心 | `help`, `tools`, `tape.info`, `handoff` |
| **技能工具** | 动态加载 | 从 `skills/` 目录加载的工具 |

**工具注册**:
```python
# 装饰器注册
@register_tool(
    name="fs.read",
    short_description="读取文件",
    detail="读取指定路径的文件内容"
)
async def read_file(path: str) -> str:
    """读取文件"""
    with open(path, 'r') as f:
        return f.read()
```

**工具执行**:
```python
# 异步执行
result = await registry.execute("fs.read", kwargs={"path": "README.md"})
```

---

### 5. Anchor / Handoff（锚定/移交）

> **定义**: Anchor / Handoff 是**上下文转换机制**，用于在会话中创建明确的阶段划分。

**Handoff 用途**:
- 🎯 **阶段划分**: 将长期任务划分为多个阶段
- 📍 **锚点标记**: 在磁带上标记关键节点
- 🔄 **上下文切换**: 在不同的阶段之间切换上下文
- 📝 **摘要记录**: 为每个阶段生成摘要

**Handoff 示例**:
```python
# 使用 handoff 命令
",handoff name=phase-1 summary='bootstrap done'"

# 创建一个新的锚点
# 阶段名称: phase-1
# 摘要: bootstrap done
```

**Anchor 用途**:
- 📍 **标记位置**: 在磁带上标记重要位置
- 🔍 **快速跳转**: 快速跳转到标记的位置
- 📊 **分析阶段**: 分析不同阶段的表现

---

## 🏗️ 架构设计

### 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                       用户界面层                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  CLI 交互   │  │   Telegram  │  │   Discord   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│                      路由层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  InputRouter │  │CommandDetector│ │ToolRegistry │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
┌──────────────┐          ┌──────────────┐
│  核心循环层   │          │   工具层      │
│  ┌────────┐  │          │  ┌────────┐  │
│  │AgentLoop│  │          │  │ Tools  │  │
│  └────────┘  │          │  └────────┘  │
│  ┌────────┐  │          │  ┌────────┐  │
│  │ModelRun │  │          │  │ Skills │  │
│  └────────┘  │          │  └────────┘  │
└──────────────┘          └──────────────┘
        │                           │
        └─────────────┬─────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│                    数据持久层                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  TapeStore  │  │  FileTape   │  │JobStore     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

### 核心层职责

| 层 | 职责 | 组件 |
|------|------|------|
| **用户界面层** | 用户交互 | CLI, Telegram, Discord |
| **路由层** | 命令路由和执行 | InputRouter, CommandDetector, ToolRegistry |
| **核心循环层** | Agent 循环和模型运行 | AgentLoop, ModelRunner |
| **工具层** | 工具管理和执行 | Tools, Skills |
| **数据持久层** | 数据存储和恢复 | TapeStore, FileTape, JobStore |

---

## 🔧 核心组件

### 1. AgentLoop（Agent 循环）

> **职责**: 确定性的单会话循环，基于无尽的磁带。

**核心方法**:
```python
class AgentLoop:
    def __init__(
        self,
        router: InputRouter,
        model_runner: ModelRunner,
        tape: TapeService
    ):
        self._router = router
        self._model_runner = model_runner
        self._tape = tape
    
    async def handle_input(self, raw: str) -> LoopResult:
        """处理用户输入"""
        # 1. 路由用户输入
        route = await self._router.route_user(raw)
        
        # 2. 检查是否请求退出
        if route.exit_requested:
            return LoopResult(...)
        
        # 3. 检查是否需要进入模型
        if not route.enter_model:
            return LoopResult(...)
        
        # 4. 运行模型
        model_result = await self._model_runner.run(route.model_prompt)
        
        # 5. 记录结果
        self._record_result(model_result)
        
        # 6. 返回结果
        return LoopResult(...)
```

**关键特性**:
- ✅ **确定性**: 相同的输入产生相同的输出
- ✅ **可恢复**: 可以从任何点恢复会话
- ✅ **可检查**: 所有步骤都记录在磁带上

---

### 2. InputRouter（输入路由器）

> **职责**: 命令感知的路由器，用于用户和助手输出。

**核心方法**:
```python
class InputRouter:
    def __init__(
        self,
        registry: ToolRegistry,
        tool_view: ProgressiveToolView,
        tape: TapeService,
        workspace: Path
    ):
        self._registry = registry
        self._tool_view = tool_view
        self._tape = tape
        self._workspace = workspace
    
    async def route_user(self, raw: str) -> UserRouteResult:
        """路由用户输入"""
        # 1. 解析命令
        command = self._parse_comma_prefixed_command(text)
        
        # 2. 如果不是命令，进入模型
        if command is None:
            return UserRouteResult(
                enter_model=True,
                model_prompt=stripped,
                immediate_output="",
                exit_requested=False
            )
        
        # 3. 执行命令
        result = await self._execute_command(command, origin="human")
        
        # 4. 如果命令成功，直接返回
        if result.status == "ok" and result.name != "bash":
            return UserRouteResult(
                enter_model=False,
                model_prompt="",
                immediate_output=result.output,
                exit_requested=False
            )
        
        # 5. 如果命令失败，回退到模型
        return UserRouteResult(
            enter_model=True,
            model_prompt=result.block(),
            immediate_output=result.output,
            exit_requested=False
        )
    
    async def route_assistant(self, raw: str) -> AssistantRouteResult:
        """路由助手输出"""
        # 1. 解析助手输出中的命令
        # 2. 执行命令
        # 3. 返回可见文本和下一个提示
        pass
```

**关键特性**:
- ✅ **双路由**: 支持用户输入和助手输出
- ✅ **上下文回退**: 失败的命令回退到模型
- ✅ **执行追踪**: 记录所有命令执行

---

### 3. ToolRegistry（工具注册表）

> **职责**: 统一的工具注册表，管理内置工具、内部命令和技能支持的工具。

**核心方法**:
```python
class ToolRegistry:
    def __init__(self, allowed_tools: set[str] | None = None):
        self._tools: dict[str, ToolDescriptor] = {}
        self._allowed_tools = allowed_tools
    
    def register(
        self,
        *,
        name: str,
        short_description: str,
        detail: str | None = None,
        model: type[BaseModel] | None = None,
        context: bool = False,
        source: str = "builtin"
    ) -> Callable:
        """注册工具"""
        def decorator(func):
            # 1. 检查工具是否允许
            if (self._allowed_tools is not None and
                name not in self._allowed_tools):
                return None
            
            # 2. 创建工具包装器
            async def handler(*args, **kwargs):
                # 3. 记录工具调用
                self._log_tool_call(name, kwargs)
                
                # 4. 执行工具
                result = func(*args, **kwargs)
                
                # 5. 返回结果
                return result
            
            # 6. 创建工具对象
            tool = Tool.from_callable(handler, ...)
            
            # 7. 存储工具描述符
            self._tools[name] = ToolDescriptor(
                name=name,
                short_description=short_description,
                detail=detail,
                tool=tool,
                source=source
            )
            
            return tool_desc
        
        return decorator
    
    async def execute(
        self,
        name: str,
        *,
        kwargs: dict[str, Any],
        context: ToolContext | None = None
    ) -> Any:
        """执行工具"""
        descriptor = self.get(name)
        if descriptor is None:
            raise KeyError(name)
        
        result = descriptor.tool.run(context=context, **kwargs)
        if inspect.isawaitable(result):
            result = await result
        return result
```

**关键特性**:
- ✅ **统一管理**: 所有工具统一注册和管理
- ✅ **权限控制**: 支持白名单机制
- ✅ **异步执行**: 支持异步工具执行
- ✅ **执行追踪**: 记录所有工具调用

---

### 4. TapeService（磁带服务）

> **职责**: 磁带的持久化、查询和分支管理。

**核心方法**:
```python
class TapeService:
    def __init__(self, store: FileTapeStore, tape: str):
        self._store = store
        self._tape = tape
        self._fork_tape = None
    
    def append_event(self, kind: str, payload: dict):
        """追加事件到磁带"""
        entry = TapeEntry(
            id=self._next_id(),
            kind=kind,
            payload=payload,
            meta={}
        )
        self._store.append(self._tape, entry)
    
    def read_events(self, kind: str | None = None) -> list[TapeEntry]:
        """读取磁带事件"""
        entries = self._store.read(self._tape)
        if entries is None:
            return []
        
        if kind is None:
            return entries
        
        return [e for e in entries if e.kind == kind]
    
    def search_events(self, query: str) -> list[TapeEntry]:
        """搜索磁带事件"""
        entries = self._store.read(self._tape)
        if entries is None:
            return []
        
        query_lower = query.lower()
        return [
            e for e in entries
            if query_lower in str(e.payload).lower()
        ]
    
    def fork_tape(self) -> TapeService:
        """创建磁带分支"""
        if self._fork_tape is not None:
            return self._fork_tape
        
        fork_name = self._store.fork(self._tape)
        self._fork_tape = TapeService(self._store, fork_name)
        return self._fork_tape
    
    def reset_tape(self, archive: bool = False):
        """重置磁带"""
        if archive:
            self._store.archive(self._tape)
        else:
            self._store.reset(self._tape)
```

**关键特性**:
- ✅ **仅追加**: 只能追加事件，不能修改
- ✅ **持久化**: 所有事件都保存到磁盘
- ✅ **可查询**: 支持按类型和关键词查询
- ✅ **可分支**: 支持创建分支

---

### 5. ModelRunner（模型运行器）

> **职责**: 运行 LLM 模型，处理模型输出中的命令。

**核心方法**:
```python
class ModelRunner:
    def __init__(
        self,
        router: InputRouter,
        model: str,
        client: Any
    ):
        self._router = router
        self._model = model
        self._client = client
    
    async def run(self, prompt: str) -> ModelTurnResult:
        """运行模型"""
        # 1. 调用 LLM
        response = await self._call_llm(prompt)
        
        # 2. 路由模型输出
        route = await self._router.route_assistant(response)
        
        # 3. 返回结果
        return ModelTurnResult(
            visible_text=route.visible_text,
            next_prompt=route.next_prompt,
            exit_requested=route.exit_requested,
            steps=1,
            command_followups=[],
            error=None
        )
```

**关键特性**:
- ✅ **命令处理**: 处理模型输出中的命令
- ✅ **循环控制**: 支持多轮对话
- ✅ **退出控制**: 支持显式退出

---

## 🔄 工作流程

### 用户输入流程

```
用户输入
  ↓
解析命令（InputRouter.route_user）
  ↓
判断是否为命令
  ├─ 是 → 执行命令
  │   ├─ 成功 → 返回结果
  │   └─ 失败 → 回退到模型（带上下文）
  └─ 否 → 发送给模型
    ↓
  运行模型（ModelRunner.run）
    ↓
  路由模型输出（InputRouter.route_assistant）
    ↓
  执行模型输出中的命令
    ↓
  记录结果（TapeService.append_event）
    ↓
  返回给用户
```

### 具体示例

**示例 1: 执行内部命令**
```python
用户输入: ",tools"

1. 解析命令 → 内部命令 "tools"
2. 执行命令 → 返回工具列表
3. 记录事件 → tape.append_event("command", ...)
4. 返回结果 → 显示工具列表
```

**示例 2: 执行 Shell 命令**
```python
用户输入: ",git status"

1. 解析命令 → Shell 命令 "git status"
2. 执行命令 → 返回 git status 输出
3. 记录事件 → tape.append_event("command", ...)
4. 返回结果 → 显示 git status 输出
```

**示例 3: 自然语言输入**
```python
用户输入: "如何使用 bub？"

1. 解析命令 → 不是命令
2. 发送给模型 → 模型生成回复
3. 记录事件 → tape.append_event("loop.result", ...)
4. 返回结果 → 显示模型回复
```

---

## 🌟 关键特性

### 1. Tape-First 架构

**特点**:
- ✅ 所有事件都记录在磁带上
- ✅ 磁带是仅追加的，不能修改
- ✅ 支持从任何点恢复会话
- ✅ 支持创建磁带分支

**优势**:
- 📝 **完整历史**: 保留完整的会话历史
- 🔍 **易于调试**: 可以追溯所有操作
- 🔄 **可恢复**: 可以从任何点恢复
- 📊 **可分析**: 可以分析用户行为

---

### 2. 严格的命令边界

**特点**:
- ✅ 只有以 `,` 开头的行才被视为命令
- ✅ 其他所有输入都发送给模型
- ✅ 命令和自然语言完全分离

**优势**:
- 🎯 **明确性**: 用户清楚知道何时发送命令
- 🛡️ **安全性**: 避免意外的命令执行
- 🤖 **灵活性**: 允许模型生成命令

---

### 3. 双路由模型

**特点**:
- ✅ 同样的路由模型应用于用户输入和助手输出
- ✅ 失败的命令回退到模型
- ✅ 结构化上下文传递

**优势**:
- 🔄 **一致性**: 路由逻辑一致
- 🧠 **智能回退**: 失败命令自动回退
- 📝 **上下文保留**: 保留错误上下文

---

### 4. Anchor / Handoff 机制

**特点**:
- ✅ 明确的阶段划分
- ✅ 锚点标记和摘要
- ✅ 上下文切换

**优势**:
- 🎯 **阶段性管理**: 清晰的阶段划分
- 📍 **快速跳转**: 快速跳转到锚点
- 📝 **摘要记录**: 记录阶段摘要

---

## 🛠️ 技术栈

### 核心依赖

| 库 | 版本 | 用途 |
|------|------|------|
| **republic** | >=0.3.0 | Agent 框架核心 |
| **pydantic** | >=2.0.0 | 数据验证 |
| **typer** | >=0.9.0 | CLI 框架 |
| **rich** | >=13.0.0 | 终端输出 |
| **loguru** | >=0.7.2 | 日志记录 |

### 可选依赖

| 库 | 版本 | 用途 |
|------|------|------|
| **python-telegram-bot** | >=21.0 | Telegram 集成 |
| **discord-py** | >=2.6.4 | Discord 集成 |
| **any-llm-sdk** | >=1.8.0 | LLM 集成 |

### Python 版本

- **最小版本**: Python 3.12
- **支持版本**: 3.12, 3.13, 3.14

---

## 📚 最佳实践

### 1. 命令命名

**原则**:
- ✅ 使用小写和下划线
- ✅ 使用清晰的动词
- ✅ 避免缩写

**示例**:
```python
# 好的命名
",file.read"
",git.status"
",tape.search"

# 不好的命名
",fr"  # 缩写不清晰
",gs"   # 缩写不清晰
",s"    # 太短
```

---

### 2. 工具设计

**原则**:
- ✅ 工具应该有明确的输入和输出
- ✅ 工具应该有清晰的描述
- ✅ 工具应该有错误处理
- ✅ 工具应该支持异步

**示例**:
```python
@register_tool(
    name="fs.read",
    short_description="读取文件",
    detail="读取指定路径的文件内容"
)
async def read_file(path: str) -> str:
    """读取文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {path}")
```

---

### 3. 错误处理

**原则**:
- ✅ 捕获所有异常
- ✅ 提供友好的错误信息
- ✅ 记录错误日志
- ✅ 回退到模型（如果可能）

**示例**:
```python
try:
    result = await self._registry.execute(name, kwargs)
except Exception as exc:
    logger.error(f"工具执行失败: {exc}")
    # 回退到模型
    return UserRouteResult(
        enter_model=True,
        model_prompt=f"命令失败: {exc}",
        immediate_output=f"错误: {exc}",
        exit_requested=False
    )
```

---

### 4. 磁带记录

**原则**:
- ✅ 记录所有重要事件
- ✅ 使用清晰的事件类型
- ✅ 包含足够的上下文信息

**示例**:
```python
# 记录命令执行
self._tape.append_event(
    "command",
    {
        "origin": "human",
        "kind": "shell",
        "raw": ",git status",
        "name": "git",
        "status": "ok",
        "elapsed_ms": 150,
        "output": "On branch main..."
    }
)

# 记录循环结果
self._tape.append_event(
    "loop.result",
    {
        "steps": 3,
        "followups": [],
        "exit_requested": False,
        "error": None
    }
)
```

---

## 📊 总结

### 核心优势

1. ✅ **可预测**: 确定性的路由和执行
2. ✅ **可检查**: 完整的磁带记录
3. ✅ **可恢复**: 支持从任何点恢复
4. ✅ **可扩展**: 支持自定义工具和技能
5. ✅ **多通道**: 支持 CLI、Telegram、Discord

### 适用场景

- 🤖 **编码 Agent**: 需要与文件系统交互的编码任务
- 🔧 **自动化脚本**: 需要执行系统命令的自动化任务
- 📝 **代码审查**: 需要分析和理解代码的任务
- 🚀 **项目引导**: 需要引导用户完成项目的任务

---

**文档版本**: 1.0  
**最后更新**: 2026-02-19  
**作者**: 镜子 (Jìngzi) 🪞
