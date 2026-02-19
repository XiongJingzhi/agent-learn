# 02. 工具开发实践 - Feynman Technique

> **费曼技巧**：如果不能简单解释，说明没有真正理解。  
> **目标**：用简单的语言和类比，解释工具开发的实践。

---

## 🎯 学习目标

通过本章学习，你将能够：

1. ✅ 理解 **Tool 的定义和作用**
2. ✅ 掌握 **Tool 的开发和注册**
3. ✅ 掌握 **Tool 的最佳实践**
4. ✅ 掌握 **Tool 的测试**
5. ✅ 能够用简单的语言向"资深开发"解释工具开发

---

## 📚 核心概念

### 概念 1：Tool 的定义和作用

> **类比**：Tool 就像一个**工具箱里的工具**，如：锤子、螺丝刀、扳手等，每个工具都有特定的用途。

**Tool 的定义**：

Tool 是一个**可调用的函数**，它能够：

1. ✅ **执行特定任务**：如：搜索、计算、数据库查询
2. ✅ **有明确的输入和输出**：输入和输出的类型都明确
3. ✅ **有描述和说明**：有清晰的描述和说明，方便 Agent 调用
4. ✅ **可以注册和调用**：可以注册到 Agent 中，被 Agent 调用

**核心思想**：Tool 是 Agent 的执行组件，用于完成具体动作；Skill 才是可复用的能力包。

---

### 概念 2：Tool 的开发和注册

#### 1. Tool 的定义

**示例**：
```python
from langchain.tools import Tool

def search_tool(query: str) -> str:
    """搜索工具（模拟）"""
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架",
        "langgraph": "LangGraph 是一个状态管理框架",
        "openai": "OpenAI 是一个 AI 研究实验室"
    }
    
    return results.get(query.lower(), f"未找到与 '{query}' 相关的结果")

# 创建 Tool
tool = Tool(
    name="search",
    func=search_tool,
    description="搜索关键词，返回相关信息"
)
```

---

#### 2. Tool 的注册

**示例**：
```python
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI

# 创建 LLM
llm = ChatOpenAI(temperature=0)

# 创建 Tool
tools = [tool]

# 创建 Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    verbose=True
)
```

---

### 概念 3：Tool 的最佳实践

#### 1. 明确的输入和输出

**示例**：
```python
def good_tool(input: str) -> str:
    """好的工具：输入输出明确"""
    return f"Tool: {input}"

def bad_tool(input) -> str:
    """不好的工具：输入输出不明确"""
    # 不清楚输入是什么类型
    # 不清楚输出是什么类型
    return "Tool: " + str(input)
```

---

#### 2. 清晰的描述

**示例**：
```python
good_tool = Tool(
    name="search",
    func=search_tool,
    description="搜索关键词，返回相关信息（支持：langchain, langgraph, openai）"
)

bad_tool = Tool(
    name="search",
    func=search_tool,
    description="搜索"  # 描述不清晰
)
```

---

#### 3. 错误处理

**示例**：
```python
def tool_with_error_handling(input: str) -> str:
    """带错误处理的工具"""
    try:
        result = some_operation(input)
        return result
    except Exception as e:
        return f"错误：{str(e)}"
```

---

### 概念 4：Tool 执行必须经过沙盒（Sandbox）

> 关键原则：只要 Tool 会访问文件系统、网络、命令执行，就必须在受限环境中运行。

**为什么必须有沙盒？**
1. 防止误执行危险命令（如删除文件、覆盖配置）
2. 防止越权访问（读到不该读的文件或密钥）
3. 防止资源耗尽（CPU/内存/磁盘打满）

**最小沙盒策略（学习阶段可执行）**
1. 使用隔离工作目录（只允许读写指定路径）
2. 禁止访问敏感目录（如 `~/.ssh`、系统目录、密钥目录）
3. 限制命令执行时间（timeout）
4. 限制资源（CPU/内存）
5. 记录每次 Tool 调用日志（参数、执行结果、退出码）

**落地检查清单**
- [ ] Tool 是否声明了允许访问的路径范围？
- [ ] Tool 是否设置了执行超时？
- [ ] Tool 是否有失败返回而不是静默异常？
- [ ] Tool 执行日志是否可审计？

---

## 🔍 费曼学习检查

### 向"资深开发"解释

**假设你正在向资深开发解释工具开发，你能这样说吗？**

1. **Tool 是什么？**
   > "Tool 就像工具箱里的单个工具，如锤子、螺丝刀、扳手。它是一个可调用函数，负责具体动作（搜索、计算、查询）。它不等于 Skill。Skill 是由 SKILL.md、流程说明、资源和脚本组成的能力包。"

2. **Tool 的开发和注册有哪些步骤？**
   > "Tool 的开发和注册的步骤有：1）定义 Tool 的函数（包括输入、输出、描述）；2）创建 Tool 对象；3）将 Tool 注册到 Agent 中。"

3. **Tool 的最佳实践有哪些？**
   > "Tool 的最佳实践有：1）明确的输入和输出；2）清晰的描述和说明；3）完善的错误处理；4）沙盒隔离执行；5）单元测试和审计日志。"

---

## 🎯 核心要点总结

### Tool 的定义

| 组件 | 说明 | 示例 |
|------|------|------|
| **函数** | 可调用的函数 | `def search_tool(query: str) -> str:` |
| **输入** | 明确的输入类型 | `query: str` |
| **输出** | 明确的输出类型 | `-> str` |
| **描述** | 清晰的描述和说明 | `description="搜索关键词，返回相关信息"` |

### Tool 的注册

| 步骤 | 说明 |
|------|------|
| **1. 定义函数** | 定义 Tool 的函数 |
| **2. 创建对象** | 使用 `Tool` 类创建 Tool 对象 |
| **3. 注册到 Agent** | 将 Tool 注册到 Agent 中 |

### Tool 的最佳实践

| 实践 | 说明 | 示例 |
|------|------|------|
| **明确的输入输出** | 输入和输出类型明确 | `def tool(input: str) -> str:` |
| **清晰的描述** | 有清晰的描述和说明 | `description="搜索关键词"` |
| **错误处理** | 完善的错误处理 | `try-except` |
| **沙盒隔离** | 在受限环境执行 | 限制路径/权限/超时 |

---

## 🚀 下一步

现在你已经理解了工具开发的实践，让我们继续学习：

- 📖 `notes/03_feynman_memory_code_intuition.md` - 费曼记忆与代码直觉
- 📖 `notes/04_unit_testing_mock.md` - 单元测试与 Mock
- 🧪 `examples/01_complete_react_agent.py` - 完整的 ReAct Agent 示例

---

**记住：Tool 负责执行动作，Skill 负责组织与复用能力。** 🛠️
