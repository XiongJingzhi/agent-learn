# Bub 代码深度分析

> **文档目的**: 深入分析 Bub 的核心代码实现  
> **分析日期**: 2026-02-19  
> **代码版本**: 0.2.1

---

## 📋 目录

1. [核心模块分析](#核心模块分析)
2. [关键算法分析](#关键算法分析)
3. [数据流分析](#数据流分析)
4. [并发与异步](#并发与异步)
5. [错误处理机制](#错误处理机制)
6. [性能优化](#性能优化)

---

## 🔧 核心模块分析

### 1. Core - 核心模块

#### 1.1 agent_loop.py

**核心类**: `AgentLoop`

**职责**:
- 确定性的单会话循环
- 基于 tape 的状态管理
- 输入路由和模型执行协调

**关键方法**:
```python
class AgentLoop:
    def __init__(
        self,
        router: InputRouter,
        model_runner: ModelRunner,
        tape: TapeService
    ) -> None:
        """
        初始化 Agent Loop
        
        Args:
            router: 输入路由器
            model_runner: 模型运行器
            tape: 磁带服务
        """
        self._router = router
        self._model_runner = model_runner
        self._tape = tape
    
    async def handle_input(self, raw: str) -> LoopResult:
        """
        处理用户输入（核心方法）
        
        流程:
        1. 创建 tape 分支（上下文隔离）
        2. 路由用户输入
        3. 检查退出请求
        4. 检查是否需要进入模型
        5. 运行模型
        6. 记录结果
        7. 返回 LoopResult
        """
        with self._tape.fork_tape():
            # 步骤 1: 路由用户输入
            route = await self._router.route_user(raw)
            
            # 步骤 2: 检查是否请求退出
            if route.exit_requested:
                return LoopResult(
                    immediate_output=route.immediate_output,
                    assistant_output="",
                    exit_requested=True,
                    steps=0,
                    error=None,
                )
            
            # 步骤 3: 检查是否需要进入模型
            if not route.enter_model:
                return LoopResult(
                    immediate_output=route.immediate_output,
                    assistant_output="",
                    exit_requested=False,
                    steps=0,
                    error=None,
                )
            
            # 步骤 4: 运行模型
            model_result = await self._model_runner.run(route.model_prompt)
            
            # 步骤 5: 记录结果
            self._record_result(model_result)
            
            # 步骤 6: 返回结果
            return LoopResult(
                immediate_output=route.immediate_output,
                assistant_output=model_result.visible_text,
                exit_requested=model_result.exit_requested,
                steps=model_result.steps,
                error=model_result.error,
            )
    
    def _record_result(self, result: ModelTurnResult) -> None:
        """
        记录模型运行结果到磁带
        
        记录内容包括:
        - 步骤数
        - 后续命令
        - 退出请求
        - 错误信息
        """
        self._tape.append_event(
            "loop.result",
            {
                "steps": result.steps,
                "followups": result.command_followups,
                "exit_requested": result.exit_requested,
                "error": result.error,
            },
        )
```

**设计亮点**:
- ✅ **上下文隔离**: 使用 `fork_tape()` 实现上下文隔离
- ✅ **确定性路由**: 同样的输入产生同样的输出
- ✅ **完整记录**: 所有步骤都记录到磁带

---

#### 1.2 router.py

**核心类**: `InputRouter`

**职责**:
- 命令感知的路由
- 用户输入和助手输出的统一路由
- 命令执行和回退机制

**关键方法**:
```python
class InputRouter:
    def __init__(
        self,
        registry: ToolRegistry,
        tool_view: ProgressiveToolView,
        tape: TapeService,
        workspace: Path,
    ) -> None:
        """
        初始化输入路由器
        
        Args:
            registry: 工具注册表
            tool_view: 工具视图
            tape: 磁带服务
            workspace: 工作目录
        """
        self._registry = registry
        self._tool_view = tool_view
        self._tape = tape
        self._workspace = workspace
    
    async def route_user(self, raw: str) -> UserRouteResult:
        """
        路由用户输入
        
        流程:
        1. 清空输入
        2. 尝试解析 JSON（用于 Telegram 消息）
        3. 解析命令
        4. 如果不是命令，进入模型
        5. 如果是命令，执行命令
        6. 如果命令成功，直接返回
        7. 如果命令失败，回退到模型
        """
        # 步骤 1: 清空输入
        stripped = raw.strip()
        if not stripped:
            return UserRouteResult(
                enter_model=False,
                model_prompt="",
                immediate_output="",
                exit_requested=False
            )
        
        # 步骤 2: 尝试解析 JSON（用于 Telegram 消息）
        try:
            parsed = json.loads(stripped)
            text = parsed.get("message", stripped)
        except json.JSONDecodeError:
            text = stripped
        
        # 步骤 3: 解析命令
        command = self._parse_comma_prefixed_command(text)
        
        # 步骤 4: 如果不是命令，进入模型
        if command is None:
            return UserRouteResult(
                enter_model=True,
                model_prompt=stripped,
                immediate_output="",
                exit_requested=False
            )
        
        # 步骤 5: 执行命令
        result = await self._execute_command(command, origin="human")
        
        # 步骤 6: 如果命令成功，直接返回
        if result.status == "ok" and result.name != "bash":
            if result.name == "quit" and result.output == "exit":
                return UserRouteResult(
                    enter_model=False,
                    model_prompt="",
                    immediate_output="",
                    exit_requested=True,
                )
            return UserRouteResult(
                enter_model=False,
                model_prompt="",
                immediate_output=result.output,
                exit_requested=False,
            )
        
        # 步骤 7: 如果命令失败，回退到模型
        if result.status == "ok" and result.name == "bash":
            return UserRouteResult(
                enter_model=False,
                model_prompt="",
                immediate_output=result.output,
                exit_requested=False,
            )
        
        # 失败的命令回退到模型，带上结构化上下文
        return UserRouteResult(
            enter_model=True,
            model_prompt=result.block(),
            immediate_output=result.output,
            exit_requested=False,
        )
    
    def _parse_comma_prefixed_command(self, stripped: str) -> DetectedCommand | None:
        """
        解析逗号前缀的命令
        
        解析规则:
        1. 必须以 `,` 开头
        2. 逗号后可以有空格
        3. 解析命令名称和参数
        """
        # 检查是否以逗号开头
        if not stripped.startswith(","):
            return None
        
        # 去掉逗号和空格
        body = stripped[1:].lstrip()
        if not body:
            return None
        
        # 尝试解析为内部命令
        name, args_tokens = parse_internal_command(stripped)
        if name:
            resolved = self._resolve_internal_name(name)
            if self._registry.has(resolved):
                return DetectedCommand(
                    kind="internal",
                    raw=stripped,
                    name=name,
                    args_tokens=args_tokens
                )
        
        # 解析为 Shell 命令
        words = parse_command_words(body)
        if not words:
            return None
        
        return DetectedCommand(
            kind="shell",
            raw=body,
            name=words[0],
            args_tokens=words[1:]
        )
    
    async def _execute_command(
        self,
        command: DetectedCommand,
        *,
        origin: str
    ) -> CommandExecutionResult:
        """
        执行命令
        
        流程:
        1. 记录开始时间
        2. 根据命令类型执行
        3. 捕获异常
        4. 记录到磁带
        5. 返回结果
        """
        start = time.time()
        
        try:
            # 执行命令
            if command.kind == "shell":
                result = await self._execute_shell(command, origin=origin, start=start)
            else:
                result = await self._execute_internal(command, origin=origin, start=start)
            
            status = "ok"
            text = str(result)
        except Exception as exc:
            status = "error"
            text = f"{exc!s}"
        
        elapsed_ms = int((time.time() - start) * 1000)
        
        # 记录到磁带
        self._record_command(
            command=command,
            status=status,
            output=text,
            elapsed_ms=elapsed_ms,
            origin=origin
        )
        
        return CommandExecutionResult(
            command=command.raw,
            name=command.name,
            status=status,
            output=text,
            elapsed_ms=elapsed_ms,
        )
```

**设计亮点**:
- ✅ **统一路由**: 同样的路由逻辑应用于用户和助手
- ✅ **智能回退**: 失败的命令自动回退到模型
- ✅ **结构化上下文**: 回退时带上结构化的错误上下文

---

### 2. Tools - 工具模块

#### 2.1 registry.py

**核心类**: `ToolRegistry`

**职责**:
- 统一的工具注册表
- 工具的动态加载和执行
- 工具的权限控制

**关键方法**:
```python
class ToolRegistry:
    def __init__(self, allowed_tools: set[str] | None = None) -> None:
        """
        初始化工具注册表
        
        Args:
            allowed_tools: 允许的工具列表（白名单）
        """
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
        source: str = "builtin",
    ) -> Callable:
        """
        注册工具（装饰器）
        
        流程:
        1. 检查工具是否允许
        2. 创建异步包装器
        3. 记录工具调用
        4. 执行工具
        5. 处理异常
        6. 创建 Tool 对象
        7. 存储工具描述符
        """
        def decorator[**P, T](func: Callable[P, T | Awaitable[T]]) -> ToolDescriptor | None:
            # 步骤 1: 检查工具是否允许
            if (
                self._allowed_tools is not None
                and name.casefold() not in self._allowed_tools
                and self.to_model_name(name).casefold() not in self._allowed_tools
            ):
                return None
            
            # 步骤 2: 创建异步包装器
            @wraps(func)
            async def handler(*args: P.args, **kwargs: P.kwargs) -> T:
                # 提取上下文参数
                context_arg = kwargs.get("context") if context else None
                call_kwargs = {key: value for key, value in kwargs.items() if key != "context"}
                
                # 如果第一个参数是 BaseModel，解构它
                if args and isinstance(args[0], BaseModel):
                    call_kwargs.update(args[0].model_dump())
                
                # 步骤 3: 记录工具调用开始
                self._log_tool_call(name, call_kwargs, cast("ToolContext | None", context_arg))
                
                start = time.monotonic()
                try:
                    # 步骤 4: 执行工具
                    result = func(*args, **kwargs)
                    if inspect.isawaitable(result):
                        result = await result
                except Exception:
                    # 步骤 5: 记录错误
                    logger.exception("tool.call.error name={}", name)
                    raise
                else:
                    return result
                finally:
                    # 记录执行时间
                    duration = time.monotonic() - start
                    logger.info("tool.call.end name={} duration={:.3f}ms", name, duration * 1000)
            
            # 步骤 6: 创建 Tool 对象
            if model is not None:
                tool = tool_from_model(model, handler, name=name, description=short_description, context=context)
            else:
                tool = Tool.from_callable(handler, name=name, description=short_description, context=context)
            
            # 步骤 7: 存储工具描述符
            tool_desc = ToolDescriptor(
                name=name,
                short_description=short_description,
                detail=tool_detail,
                tool=tool,
                source=source
            )
            self._tools[name] = tool_desc
            
            return tool_desc
        
        return decorator
    
    async def execute(
        self,
        name: str,
        *,
        kwargs: dict[str, Any],
        context: ToolContext | None = None,
    ) -> Any:
        """
        执行工具
        
        流程:
        1. 获取工具描述符
        2. 检查工具是否存在
        3. 注入上下文（如果需要）
        4. 运行工具
        5. 等待异步结果
        6. 返回结果
        """
        descriptor = self.get(name)
        if descriptor is None:
            raise KeyError(name)
        
        # 注入上下文（如果工具需要）
        if descriptor.tool.context:
            kwargs["context"] = context
        
        # 运行工具
        result = descriptor.tool.run(context=context, **kwargs)
        
        # 等待异步结果
        if inspect.isawaitable(result):
            result = await result
        
        return result
```

**设计亮点**:
- ✅ **装饰器模式**: 使用装饰器简化工具注册
- ✅ **异步支持**: 完全支持异步工具
- ✅ **上下文注入**: 自动注入上下文给需要上下文的工具
- ✅ **执行追踪**: 记录所有工具调用和执行时间

---

### 3. Tape - 磁带模块

#### 3.1 store.py

**核心类**: `FileTapeStore`, `TapeFile`

**职责**:
- 磁带的持久化存储
- 磁带的读写操作
- 磁带的分支管理

**关键方法**:
```python
class TapeFile:
    """单个磁带文件的操作类"""
    
    def __init__(self, path: Path) -> None:
        """
        初始化磁带文件
        
        Args:
            path: 磁带文件路径
        """
        self.path = path
        self.fork_start_id: int | None = None
        self._lock = threading.Lock()
        self._read_entries: list[TapeEntry] = []
        self._read_offset = 0
    
    def read(self) -> list[TapeEntry]:
        """
        读取磁带文件
        
        流程:
        1. 检查文件是否存在
        2. 检查文件是否被截断
        3. 从上次偏移量开始读取
        4. 解析每一行为 TapeEntry
        5. 更新缓存和偏移量
        6. 返回所有条目
        """
        with self._lock:
            return self._read_locked()
    
    def _read_locked(self) -> list[TapeEntry]:
        """加锁读取磁带文件"""
        if not self.path.exists():
            self._reset()
            return []
        
        file_size = self.path.stat().st_size
        
        # 检查文件是否被截断
        if file_size < self._read_offset:
            # 文件被截断或替换，缓存条目已过期
            self._reset()
        
        # 从上次偏移量开始读取
        with self.path.open("r", encoding="utf-8") as handle:
            handle.seek(self._read_offset)
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                entry = self.entry_from_payload(payload)
                if entry is not None:
                    self._read_entries.append(entry)
            self._read_offset = handle.tell()
        
        return list(self._read_entries)
    
    def append(self, entry: TapeEntry) -> None:
        """
        追加条目到磁带文件
        
        流程:
        1. 刷新缓存（确保与文件同步）
        2. 分配新的 ID
        3. 追加条目到文件
        4. 更新缓存和偏移量
        """
        return self._append_many([entry])
    
    def _append_many(self, entries: list[TapeEntry]) -> None:
        """追加多个条目"""
        if not entries:
            return
        
        with self._lock:
            # 刷新缓存，确保与文件同步
            self._read_locked()
            
            # 追加条目到文件
            with self.path.open("a", encoding="utf-8") as handle:
                next_id = self._next_id()
                for entry in entries:
                    stored = TapeEntry(
                        next_id,
                        entry.kind,
                        dict(entry.payload),
                        dict(entry.meta)
                    )
                    handle.write(json.dumps(self.entry_to_payload(stored), ensure_ascii=False) + "\n")
                    self._read_entries.append(stored)
                    next_id += 1
                self._read_offset = handle.tell()
    
    @staticmethod
    def entry_to_payload(entry: TapeEntry) -> dict[str, object]:
        """将 TapeEntry 转换为字典"""
        return {
            "id": entry.id,
            "kind": entry.kind,
            "payload": dict(entry.payload),
            "meta": dict(entry.meta),
        }
    
    @staticmethod
    def entry_from_payload(payload: object) -> TapeEntry | None:
        """将字典转换为 TapeEntry"""
        if not isinstance(payload, dict):
            return None
        
        entry_id = payload.get("id")
        kind = payload.get("kind")
        entry_payload = payload.get("payload")
        meta = payload.get("meta")
        
        if not isinstance(entry_id, int):
            return None
        if not isinstance(kind, str):
            return None
        if not isinstance(entry_payload, dict):
            return None
        if not isinstance(meta, dict):
            meta = {}
        
        return TapeEntry(entry_id, kind, dict(entry_payload), dict(meta))


class FileTapeStore:
    """文件磁带存储"""
    
    def __init__(self, home: Path, workspace_path: Path) -> None:
        """
        初始化文件磁带存储
        
        Args:
            home: 主目录
            workspace_path: 工作目录路径
        """
        self._paths = self._resolve_paths(home, workspace_path)
        self._tape_files: dict[str, TapeFile] = {}
        self._fork_start_ids: dict[str, int] = {}
        self._lock = threading.Lock()
    
    def fork(self, source: str) -> str:
        """
        创建磁带分支
        
        流程:
        1. 生成唯一的分支名称
        2. 获取源磁带文件
        3. 复制到目标磁带文件
        4. 记录分支起始 ID
        5. 返回分支名称
        """
        fork_suffix = uuid.uuid4().hex[:8]
        new_name = f"{source}__{fork_suffix}"
        
        source_file = self._tape_file(source)
        target_file = self._tape_file(new_name)
        
        source_file.copy_to(target_file)
        
        return new_name
```

**设计亮点**:
- ✅ **线程安全**: 使用锁确保线程安全
- ✅ **增量读取**: 只读取新增的内容
- ✅ **文件检测**: 检测文件是否被截断
- ✅ **分支支持**: 支持创建磁带分支

---

## 🚀 关键算法分析

### 1. 命令解析算法

**算法**: `_parse_comma_prefixed_command`

**复杂度**: O(n)，其中 n 是输入字符串的长度

**伪代码**:
```
function parse_command(stripped):
    # 步骤 1: 检查是否以逗号开头
    if not stripped.startswith(","):
        return None
    
    # 步骤 2: 去掉逗号和空格
    body = stripped[1:].lstrip()
    if not body:
        return None
    
    # 步骤 3: 尝试解析为内部命令
    name, args_tokens = parse_internal_command(stripped)
    if name and registry.has(resolved):
        return InternalCommand(name, args_tokens)
    
    # 步骤 4: 解析为 Shell 命令
    words = parse_command_words(body)
    if not words:
        return None
    
    return ShellCommand(words[0], words[1:])
```

**优化点**:
- ✅ **提前返回**: 尽早返回，避免不必要的解析
- ✅ **懒加载**: 只在需要时解析参数
- ✅ **缓存**: 缓存解析结果（如果适用）

---

### 2. 工具路由算法

**算法**: 命令执行和回退

**复杂度**: O(1) 命令查找 + O(k) 工具执行，其中 k 是工具执行时间

**伪代码**:
```
function execute_command(command, origin):
    start = time.now()
    
    try:
        # 步骤 1: 执行命令
        if command.kind == "shell":
            output = execute_shell(command)
        else:
            output = execute_internal(command)
        
        status = "ok"
        text = str(output)
    except Exception as exc:
        status = "error"
        text = str(exc)
    
    elapsed_ms = (time.now() - start) * 1000
    
    # 步骤 2: 记录到磁带
    tape.append_event("command", {
        "origin": origin,
        "kind": command.kind,
        "raw": command.raw,
        "name": command.name,
        "status": status,
        "elapsed_ms": elapsed_ms,
        "output": text
    })
    
    return CommandExecutionResult(
        command=command.raw,
        name=command.name,
        status=status,
        output=text,
        elapsed_ms=elapsed_ms
    )
```

**优化点**:
- ✅ **异步执行**: 所有工具都是异步的
- ✅ **超时控制**: 可以设置工具执行超时
- ✅ **错误隔离**: 捕获所有异常，不影响主循环

---

## 📊 数据流分析

### 用户输入数据流

```
用户输入
  ↓
InputRouter.route_user()
  ↓
┌─────────────────────┐
│ 解析命令           │
│ - 检查逗号前缀     │
│ - 解析命令名称     │
│ - 解析参数         │
└─────────────────────┘
  ↓
┌─────────────────────┐
│ 命令？             │
│ ├─ 是 → 执行命令   │
│ │   ├─ 成功 → 返回 │
│ │   └─ 失败 → 回退 │
│ └─ 否 → 进入模型   │
└─────────────────────┘
  ↓
┌─────────────────────┐
│ 执行命令           │
│ - 查找工具         │
│ - 调用工具         │
│ - 捕获异常         │
└─────────────────────┘
  ↓
┌─────────────────────┐
│ 记录到磁带         │
│ - 追加事件         │
│ - 持久化到文件     │
└─────────────────────┘
  ↓
返回给用户
```

---

## 🔐 并发与异步

### 异步模型

Bub 使用 `asyncio` 实现完全异步的执行模型。

**关键点**:
- ✅ 所有工具都是异步的
- ✅ 所有命令执行都是异步的
- ✅ 模型调用是异步的
- ✅ 磁带操作是线程安全的

**示例**:
```python
# 异步工具
@register_tool(
    name="fs.read",
    short_description="读取文件"
)
async def read_file(path: str) -> str:
    """异步读取文件"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 异步命令执行
async def _execute_command(self, command):
    result = await self._registry.execute(name, kwargs)
    return result
```

**优势**:
- 🚀 **高性能**: 可以并发执行多个操作
- 🔄 **非阻塞**: I/O 操作不会阻塞主循环
- 📊 **可扩展**: 容易扩展到高并发场景

---

### 线程安全

Bub 使用线程锁确保线程安全。

**关键点**:
- ✅ 磁带操作使用线程锁
- ✅ 文件操作使用线程锁
- ✅ 缓存更新使用线程锁

**示例**:
```python
class TapeFile:
    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.Lock()
        self._read_entries = []
    
    def read(self) -> list[TapeEntry]:
        with self._lock:
            return self._read_locked()
```

---

## ⚠️ 错误处理机制

### 错误处理策略

1. **捕获所有异常**: 所有工具调用都捕获异常
2. **记录错误日志**: 所有错误都记录到日志
3. **回退到模型**: 失败的命令回退到模型
4. **结构化错误信息**: 错误信息结构化传递

**示例**:
```python
try:
    output = await self._registry.execute(name, kwargs)
    status = "ok"
    text = str(output)
except Exception as exc:
    status = "error"
    text = f"{exc!s}"

# 记录到磁带
tape.append_event("command", {
    "status": status,
    "output": text
})
```

---

## ⚡ 性能优化

### 1. 增量读取

**问题**: 每次都读取整个磁带文件很慢

**解决方案**: 只读取新增的内容

**实现**:
```python
class TapeFile:
    def __init__(self, path: Path):
        self._read_offset = 0  # 记录上次读取的偏移量
    
    def read(self) -> list[TapeEntry]:
        with self.path.open("r") as handle:
            handle.seek(self._read_offset)  # 从上次偏移量开始
            for line in handle:
                # 处理新行
                pass
            self._read_offset = handle.tell()  # 更新偏移量
```

---

### 2. 缓存机制

**问题**: 频繁读取相同的磁带文件

**解决方案**: 缓存磁带条目

**实现**:
```python
class TapeFile:
    def __init__(self, path: Path):
        self._read_entries = []  # 缓存条目
    
    def read(self) -> list[TapeEntry]:
        # 只返回缓存
        return list(self._read_entries)
```

---

## 📚 总结

### 核心设计原则

1. ✅ **确定性**: 相同的输入产生相同的输出
2. ✅ **可检查**: 所有操作都记录到磁带
3. ✅ **可恢复**: 支持从任何点恢复
4. ✅ **可扩展**: 支持自定义工具和技能
5. ✅ **异步优先**: 完全异步的执行模型

### 代码质量

- ✅ **类型提示**: 完整的类型提示
- ✅ **文档字符串**: 所有函数都有文档
- ✅ **错误处理**: 完善的错误处理
- ✅ **日志记录**: 详细的日志记录

---

**文档版本**: 1.0  
**最后更新**: 2026-02-19  
**作者**: 镜子 (Jìngzi) 🪞
