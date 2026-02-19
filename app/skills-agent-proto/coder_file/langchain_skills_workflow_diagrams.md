# LangChain Skills Agent 工作流程图

## 1. 完整执行流程图

```mermaid
sequenceDiagram
    participant User as 用户
    participant CLI as CLI
    participant Agent as LangChainSkillsAgent
    participant LLM as LLM (Claude/GLM)
    participant Loader as SkillLoader
    participant Tools as Tools (load_skill, bash)
    participant Skill as Skill File System

    User->>CLI: 输入: "提取这篇公众号文章"
    CLI->>Agent: stream_events(message)

    Note over Agent: 启动时已完成 Level 1<br/>system_prompt 包含 Skills 元数据

    Agent->>LLM: 发送请求 (带 system_prompt)
    activate LLM

    LLM->>LLM: Thinking: 分析用户请求<br/>匹配 skill 描述
    LLM-->>Agent: event: thinking
    Agent-->>CLI: 🧠 Thinking 更新

    LLM->>LLM: 决定: 需要 news-extractor skill
    LLM-->>Agent: event: tool_call(load_skill)
    Agent-->>CLI: ● Skill(news-extractor) - 执行中

    Agent->>Tools: load_skill("news-extractor")
    Tools->>Loader: load_skill("news-extractor")
    Loader->>Skill: 读取 SKILL.md
    Skill-->>Loader: 完整指令 (~5k tokens)
    Loader-->>Tools: SkillContent
    Tools-->>Agent: 返回指令内容
    Agent-->>LLM: tool_result (指令)

    LLM->>LLM: Reading: 阅读指令<br/>发现需要执行脚本
    LLM-->>Agent: event: thinking
    Agent-->>CLI: 🧠 Thinking 更新

    LLM-->>Agent: event: tool_call(bash)
    Agent-->>CLI: ● Bash(uv run script.py) - 执行中

    Agent->>Tools: bash("uv run extract_news.py URL")
    Tools->>Tools: subprocess.run()
    Tools-->>Agent: [OK] {"title": "...", ...}
    Agent-->>LLM: tool_result (文章数据)

    LLM->>LLM: Processing: 处理数据<br/>生成响应
    LLM-->>Agent: event: text("已成功提取")
    Agent-->>CLI: 💬 Response 更新

    LLM-->>Agent: event: text("标题：XXX")
    Agent-->>CLI: 💬 Response 更新

    LLM-->>Agent: event: done
    Agent-->>CLI: 💬 完成响应

    deactivate LLM
    CLI-->>User: 显示最终结果
```

---

## 2. Skills 三层加载机制时序图

```mermaid
sequenceDiagram
    participant Agent as Agent 初始化
    participant Loader as SkillLoader
    participant FS as 文件系统
    participant LLM as LLM 运行时
    participant Tools as Tool Runtime

    Note over Agent: === Level 1: 启动时 ===

    Agent->>Loader: __init__(skill_paths)
    activate Loader

    Loader->>FS: 扫描 .claude/skills/
    FS-->>Loader: 发现 news-extractor/, humanizer/

    loop 每个 skill 目录
        Loader->>FS: 读取 SKILL.md
        FS-->>Loader: 文件内容
        Loader->>Loader: 解析 YAML frontmatter
        Note right of Loader: 提取 name, description<br/>~100 tokens
    end

    Loader-->>Agent: SkillMetadata[] (元数据列表)
    deactivate Loader

    Agent->>Agent: build_system_prompt()
    Note right of Agent: 将 Skills 元数据<br/>注入 system_prompt

    Note over Agent: === 等待用户请求 ===

    Note over Agent: === Level 2: 请求匹配时 ===

    Agent->>LLM: 发送请求 (含 Skills 元数据)
    activate LLM

    LLM->>LLM: 匹配 skill 描述<br/>决定调用 load_skill
    LLM-->>Agent: tool_call: load_skill("news-extractor")

    Agent->>Tools: 调用 load_skill 工具
    Tools->>Loader: load_skill("news-extractor")
    activate Loader

    Loader->>FS: 读取 SKILL.md 完整内容
    FS-->>Loader: 文件内容
    Loader->>Loader: 提取 body (去除 frontmatter)
    Note right of Loader: 返回完整指令<br/>~5k tokens

    Loader-->>Tools: SkillContent(instructions)
    deactivate Loader

    Tools-->>Agent: 返回指令内容
    Agent-->>LLM: tool_result (指令)

    Note over LLM: === Level 3: 执行时 ===

    LLM->>LLM: 阅读指令<br/>发现脚本路径
    LLM-->>Agent: tool_call: bash("uv run script.py")

    Agent->>Tools: 调用 bash 工具
    Tools->>Tools: subprocess.run(script)
    Tools-->>Agent: [OK] 输出结果

    Note right of Agent: ⚠️ 脚本代码不进入上下文<br/>只有输出进入

    Agent-->>LLM: tool_result (输出)
    LLM->>LLM: 处理结果<br/>生成最终响应
    LLM-->>Agent: AIMessage (响应)

    deactivate LLM
```

---

## 3. 流式处理事件流图

```mermaid
flowchart TD
    Start([用户请求]) --> Stream[agent.stream_events]
    Stream --> Loop{循环处理事件}

    Loop --> |event 1| E1[🧠 thinking: 分析请求]
    Loop --> |event 2| E2[🧠 thinking: 匹配 skill]
    Loop --> |event 3| TC1[● tool_call: load_skill]
    Loop --> |event 4| TR1[● tool_result: 成功]
    Loop --> |event 5| E3[🧠 thinking: 阅读指令]
    Loop --> |event 6| TC2[● tool_call: bash]
    Loop --> |event 7| TR2[● tool_result: 成功]
    Loop --> |event 8| T1[💬 text: 已成功提取]
    Loop --> |event 9| T2[💬 text: 标题：XXX]
    Loop --> |event 10| Done[✅ done: 完成]

    E1 --> UI[Rich Live Display 更新]
    E2 --> UI
    TC1 --> UI
    TR1 --> UI
    E3 --> UI
    TC2 --> UI
    TR2 --> UI
    T1 --> UI
    T2 --> UI
    Done --> End([显示最终响应])

    UI --> Display
    style E1 fill:#e1f5fe
    style E2 fill:#e1f5fe
    style E3 fill:#e1f5fe
    style TC1 fill:#fff9c4
    style TC2 fill:#fff9c4
    style TR1 fill:#c8e6c9
    style TR2 fill:#c8e6c9
    style T1 fill:#c8e6c9
    style T2 fill:#c8e6c9
    style Done fill:#c8e6c9
```

---

## 4. ToolCallTracker 工作流程

```mermaid
sequenceDiagram
    participant Stream as 流式数据流
    participant Tracker as ToolCallTracker
    participant Buffer as JSON Buffer
    participant Parser as JSON Parser

    Note over Stream: LangChain 流式输出

    Stream->>Tracker: tool_use 块
    Note right of Tracker: id="tool_123"<br/>name="bash"<br/>input={}
    Tracker->>Tracker: update(tool_123, name="bash")

    Stream->>Tracker: input_json_delta #1
    Note right of Tracker: partial_json='{"command'
    Tracker->>Buffer: append('{"command')

    Stream->>Tracker: input_json_delta #2
    Note right of Tracker: partial_json='": "ls"'
    Tracker->>Buffer: append('": "ls"')

    Stream->>Tracker: input_json_delta #3
    Note right of Tracker: partial_json='"}'
    Tracker->>Buffer: append('"}')

    Note over Stream: 收到 tool_result 事件

    Stream->>Tracker: tool_result 事件
    Tracker->>Tracker: finalize_all()
    Tracker->>Parser: json.loads(buffer)
    Parser-->>Tracker: {"command": "ls"}
    Tracker->>Tracker: update(tool_123, args={...})
    Tracker->>Tracker: mark_emitted(tool_123)

    Tracker-->>Stream: 返回完整 tool_call
    Note right of Stream: name="bash"<br/>args={"command": "ls"}<br/>ready to send
```

---

## 5. 目录结构映射图

```
.claude/skills/                    (DEFAULT_SKILL_PATHS[0])
│
├── news-extractor/                ← SkillMetadata
│   ├── SKILL.md                   ← YAML frontmatter
│   │   ├── name: news-extractor
│   │   ├── description: 新闻提取...
│   │   └── body (instructions)   ← Level 2 加载内容
│   │
│   ├── scripts/                   ← Level 3 执行
│   │   ├── extract_news.py
│   │   └── crawlers/
│   │
│   ├── references/                (可选)
│   │   └── api_docs.md
│   │
│   └── assets/                    (可选)
│       └── templates/
│
└── humanizer/                     ← SkillMetadata
    ├── SKILL.md
    └── scripts/
        └── humanize.py

~/.claude/skills/                  (DEFAULT_SKILL_PATHS[1])
│
└── custom-skill/                  (用户级兜底)
    └── SKILL.md
```

---

## 6. 数据流图

```mermaid
graph LR
    A[用户输入] --> B[Agent]
    B --> C{Level 1}
    C -->|system_prompt| D[Skills 元数据]
    D --> E[LLM]

    E -->|tool_call| F[load_skill]
    F --> G{Level 2}
    G -->|SkillContent| H[SKILL.md 完整内容]
    H --> E

    E -->|tool_call| I[bash]
    I --> J{Level 3}
    J -->|subprocess| K[脚本执行]
    K -->|stdout/stderr| L[输出结果]
    L --> E

    E --> M[最终响应]
    M --> N[用户]
```

---

## 7. 模块依赖关系图

```mermaid
graph TD
    A[agent.py] --> B[skill_loader.py]
    A --> C[tools.py]
    A --> D[stream/]

    C --> B
    C --> E[subprocess]

    D --> F[emitter.py]
    D --> G[tracker.py]
    D --> H[formatter.py]
    D --> I[utils.py]

    J[cli.py] --> A
    J --> D

    K[web_api.py] --> A

    L[__init__.py] --> A
    L --> B
    L --> C
```

---

## 8. 状态机图

```mermaid
stateDiagram-v2
    [*] --> Idle: Agent 启动

    Idle --> Thinking: 收到用户请求
    Thinking --> Thinking: 处理中
    Thinking --> ToolCall: 决定调用工具

    ToolCall --> ToolExecuting: 工具执行中
    ToolExecuting --> ToolResult: 执行完成

    ToolResult --> Thinking: 继续处理
    ToolResult --> Responding: 准备响应

    Responding --> Responding: 生成响应
    Responding --> Done: 完成

    Done --> Idle: 等待下一轮

    note right of Thinking
        Level 1: 检查元数据
        Level 2: 加载指令
    end note

    note right of ToolCall
        load_skill / bash
        / read_file / etc.
    end note

    note right of ToolResult
        [OK] 或 [FAILED]
        输出进入上下文
    end note
```

---

## 9. 扩展点

```mermaid
graph TD
    A[LangChain Skills Agent] --> B[添加新 Tool]
    A --> C[添加新 Skill]
    A --> D[自定义输出格式]

    B --> B1[@tool 装饰器]
    B1 --> B2[访问 ToolRuntime]

    C --> C1[创建 SKILL.md]
    C1 --> C2[添加 scripts/]

    D --> D1[自定义 StreamEvent]
    D --> D2[自定义 Formatter]
    D --> D3[自定义 CLI Renderer]
```

---

## 10. 错误处理流程

```mermaid
sequenceDiagram
    participant Agent as Agent
    participant Tool as Tool
    participant LLM as LLM
    participant User as User

    Agent->>Tool: load_skill("unknown")
    Tool-->>Agent: Error: Skill not found

    Agent->>LLM: tool_result (错误)
    LLM->>LLM: 分析错误<br/>尝试恢复

    alt 可恢复
        LLM->>Agent: tool_call: list_dir (查看可用技能)
        Agent-->>LLM: tool_result: 技能列表
        LLM-->>User: "可用的技能有：news-extractor, humanizer"

    else 不可恢复
        LLM-->>User: "错误：未找到技能，请检查名称"
    end
```

---

## 使用说明

### 查看这些图表

1. **Mermaid Live Editor**: https://mermaid.live/
2. **VS Code**: 安装 Mermaid Preview 插件
3. **GitHub/GitLab**: 直接在 Markdown 中渲染
4. **Obsidian**: 原生支持 Mermaid

### 修改图表

所有图表使用 Mermaid 语法编写，可以直接在文档中修改：

1. 打开 `.md` 文件
2. 找到对应的 ```mermaid 代码块
3. 修改代码
4. 保存即可自动更新

---

**生成时间**: 2026-02-14
**配套文档**: `langchain_skills_architecture_analysis.md`
