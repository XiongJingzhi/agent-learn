# 00. Hello 项目 - Level 0

> **项目名称**: Hello Agent - 你的第一个 Agent  
> **难度**: ⭐ 简单  
> **预计时间**: 1-2 小时  
> **目标**: 创建一个简单的 Agent，理解 Agent 的基本概念

---

## 🎯 项目目标

通过这个项目，你将能够：

1. ✅ 创建一个简单的 Agent
2. ✅ 理解 ReAct 循环的执行流程
3. ✅ 掌握 Tool 的定义和使用
4. ✅ 理解 Agent 的状态管理
5. ✅ 掌握 Agent 的错误处理

---

## 📚 前置知识

在开始这个项目之前，请确保你：

1. ✅ 完成了 Level 0 的所有学习笔记（6 个）
2. ✅ 理解了 Agent 的核心概念
3. ✅ 理解了 ReAct 循环的基本原理
4. ✅ 理解了 Agent 的记忆管理
5. ✅ 理解了 Agent 的工具集成
6. ✅ 完成了 Level 0 的练习题（2 个，共 40 题）

---

## 🏗️ 项目架构

```
hello_agent/
├── agent.py              # Agent 定义
├── tools.py               # 工具定义
├── memory.py              # 记忆定义
├── state.py               # 状态定义
└── main.py                 # 主程序
```

---

## 🔧 技术栈

- **Python**: 3.8+
- **LangChain**: 最新版本
- **LangGraph**: 最新版本
- **OpenAI API**: GPT-3.5 或 GPT-4

---

## 📝 项目要求

### 1. 创建 Agent 定义（30 分钟）

**文件**: `agent.py`

**要求**:
- 使用 `create_react_agent` 创建一个 ReAct Agent
- 至少定义 2 个工具（Tool）
- 使用 `ChatOpenAI` 作为 LLM
- 添加适当的错误处理

**代码模板**:
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# 创建 LLM
llm = ChatOpenAI(temperature=0.7)

# 创建工具
def tool1(input: str) -> str:
    """工具 1"""
    return f"工具 1: {input}"

def tool2(input: str) -> str:
    """工具 2"""
    return f"工具 2: {input}"

tools = [
    Tool(name="tool1", func=tool1, description="工具 1 的描述"),
    Tool(name="tool2", func=tool2, description="工具 2 的描述")
]

# 创建 Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    verbose=True
)

# 创建 Agent 执行器
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)
```

---

### 2. 创建工具定义（20 分钟）

**文件**: `tools.py`

**要求**:
- 定义至少 2 个工具
- 工具需要有明确的名称和描述
- 工具需要有输入输出的类型提示

**代码模板**:
```python
from langchain.tools import Tool

def search_tool(query: str) -> str:
    """搜索工具"""
    # 模拟搜索
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架",
        "langgraph": "LangGraph 是一个状态管理框架"
    }
    
    for key, value in results.items():
        if query.lower() in key.lower():
            return value
    
    return f"未找到与 '{query}' 相关的结果"

def calculator_tool(expression: str) -> str:
    """计算器工具"""
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except:
        return f"无法计算：{expression}"

# 创建工具
tools = [
    Tool(name="search", func=search_tool, description="搜索关键词，返回相关信息"),
    Tool(name="calculator", func=calculator_tool, description="计算数学表达式")
]
```

---

### 3. 创建记忆定义（20 分钟）

**文件**: `memory.py`

**要求**:
- 定义一个短期记忆（Short-term Memory）
- 使用 `ConversationBufferMemory`
- 设置合适的参数（如：memory_key, return_messages）

**代码模板**:
```python
from langchain.memory import ConversationBufferMemory

# 创建短期记忆
short_term_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5  # 保留最近 5 条消息
)
```

---

### 4. 创建状态定义（10 分钟）

**文件**: `state.py`

**要求**:
- 使用 `TypedDict` 定义 Agent 的状态
- 包含必要的字段（如：user_input, tool_result, chat_history）

**代码模板**:
```python
from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """Agent 状态"""
    user_input: str
    tool_result: str
    chat_history: List[str]
    memory_variables: Dict[str, Any]
    error_message: str
```

---

### 5. 创建主程序（20 分钟）

**文件**: `main.py`

**要求**:
- 整合 Agent、工具、记忆和状态
- 实现一个简单的用户交互
- 添加适当的日志和错误处理

**代码模板**:
```python
import logging
from agent import agent_executor
from tools import tools
from memory import short_term_memory
from state import AgentState

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    print("=" * 60)
    print("Hello Agent - 你的第一个 Agent")
    print("=" * 60)
    print()
    
    # 初始状态
    state = {
        "user_input": "",
        "tool_result": "",
        "chat_history": [],
        "memory_variables": {},
        "error_message": ""
    }
    
    # 用户交互
    while True:
        try:
            # 获取用户输入
            user_input = input("请输入你的问题（输入 'quit' 退出）：")
            
            # 退出条件
            if user_input.lower() == "quit":
                print("再见！")
                break
            
            # 更新状态
            state["user_input"] = user_input
            
            # 执行 Agent
            logger.info(f"执行 Agent，输入：{user_input}")
            result = agent_executor.invoke({"input": user_input})
            
            # 输出结果
            print()
            print(f"用户: {user_input}")
            print(f"Agent: {result['output']}")
            print()
            
            # 更新记忆
            short_term_memory.save_context(
                {"input": user_input},
                {"output": result['output']}
            )
            
            # 更新状态
            state["tool_result"] = result['output']
            state["chat_history"] = short_term_memory.load_memory_variables({})["chat_history"]
            
        except KeyboardInterrupt:
            print("\n程序被用户中断")
            break
        except Exception as e:
            logger.error(f"发生错误：{e}")
            print(f"错误：{e}")
            continue

if __name__ == "__main__":
    main()
```

---

## 🧪 测试要求

### 单元测试

**要求**:
- 测试每个工具的功能
- 测试 Agent 的执行流程
- 测试记忆的保存和加载
- 测试主程序的错误处理

**代码模板**:
```python
import pytest
from unittest.mock import Mock, patch
from agent import agent_executor
from tools import tools

def test_search_tool():
    """测试搜索工具"""
    # 测试正常情况
    result = tools[0].func("langchain")
    assert "LangChain" in result
    
    # 测试边界条件
    result = tools[0].func("")
    assert "未找到" in result

def test_calculator_tool():
    """测试计算器工具"""
    # 测试正常情况
    result = tools[1].func("1 + 1")
    assert "2" in result
    
    # 测试异常情况
    result = tools[1].func("1 / 0")
    assert "无法计算" in result

def test_agent_execution():
    """测试 Agent 执行"""
    # 测试正常情况
    result = agent_executor.invoke({"input": "搜索 LangChain"})
    assert result["output"] is not None
    
    # 测试工具调用
    result = agent_executor.invoke({"input": "计算 1 + 1"})
    assert "2" in result["output"]

def test_memory():
    """测试记忆"""
    # 测试保存
    short_term_memory.save_context(
        {"input": "test"},
        {"output": "result"}
    )
    
    # 测试加载
    vars = short_term_memory.load_memory_variables({})
    assert "test" in str(vars)
```

---

## 🎯 项目验收标准

当你完成以下所有项，就说明 Hello 项目达标了：

### 代码实现

- [ ] 创建了 5 个文件（agent.py, tools.py, memory.py, state.py, main.py）
- [ ] 实现了一个简单的 ReAct Agent
- [ ] 实现了至少 2 个工具（Tool）
- [ ] 实现了一个短期记忆（Short-term Memory）
- [ ] 实现了一个主程序，包含用户交互
- [ ] 添加了适当的错误处理

### 测试覆盖

- [ ] 编写了单元测试（至少 4 个测试用例）
- [ ] 测试了每个工具的功能
- [ ] 测试了 Agent 的执行流程
- [ ] 测试了记忆的保存和加载
- [ ] 测试覆盖率 >= 70%

### 文档和注释

- [ ] 所有文件都有类型提示
- [ ] 所有函数都有文档字符串（docstring）
- [ ] 关键代码有注释说明
- [ ] README.md 文档，说明项目结构和使用方法

### 功能正确性

- [ ] Agent 能够正常工作
- [ ] 工具能够正常调用
- [ ] 记忆能够正常保存和加载
- [ ] 错误能够优雅地处理

---

## 🚀 开始项目

### 1. 创建项目结构

```bash
cd /Users/xiongfeng/SourceCode/agent-learn/study/level0/projects/00_hello_project

# 创建项目目录
mkdir -p hello_agent
cd hello_agent

# 创建文件
touch agent.py tools.py memory.py state.py main.py README.md
```

---

### 2. 实现项目文件

按照上面的代码模板，实现每个文件。

---

### 3. 运行和测试

```bash
# 运行主程序
python main.py

# 运行测试
pytest test_hello_agent.py -v
```

---

### 4. 完成项目

- [ ] 完成所有代码文件
- [ ] 完成所有测试文件
- [ ] 完成 README.md
- [ ] 运行测试，确保通过
- [ ] 提交项目

---

## 📝 项目总结

### 项目产出

- ✅ 5 个代码文件（agent.py, tools.py, memory.py, state.py, main.py）
- ✅ 至少 4 个测试用例
- ✅ 1 个 README.md 文件
- ✅ 能够运行的 Agent 应用

### 项目收获

- ✅ 理解了 Agent 的基本概念
- ✅ 掌握了 ReAct 循环的执行流程
- ✅ 掌握了 Tool 的定义和使用
- ✅ 掌握了 Agent 的记忆管理
- ✅ 掌握了 Agent 的错误处理
- ✅ 具备了编写简单 Agent 的能力

---

**项目完成标准**: ✅ **代码实现 + 测试覆盖 + 文档注释**

**继续学习**: `study/level1/` - Level 1: 动手实践 🚀
