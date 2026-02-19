# 01. 单一 Agent 项目 - Level 1

> **项目名称**: 智能助手 - 你的第一个完整 Agent  
> **难度**: ⭐⭐ 中等  
> **预计时间**: 2-3 小时  
> **目标**: 构建一个完整的单一 Agent 系统

---

## 🎯 项目目标

通过这个项目，你将能够：

1. ✅ 构建一个完整的单一 Agent 系统
2. ✅ 集成多个工具（至少 3 个）
3. ✅ 实现记忆系统
4. ✅ 实现错误处理和重试机制
5. ✅ 实现日志记录
6. ✅ 编写单元测试（覆盖率 >= 70%）

---

## 📚 前置知识

在开始这个项目之前，请确保你：

1. ✅ 完成了 Level 0 的所有学习笔记和练习
2. ✅ 完成了 Level 1 的所有学习笔记
3. ✅ 理解了单一 Agent 架构
4. ✅ 理解了工具开发和集成
5. ✅ 理解了记忆管理
6. ✅ 理解了错误处理和测试

---

## 🏗️ 项目架构

```
intelligent_assistant/
├── agent.py              # Agent 定义
├── tools/                # 工具目录
│   ├── __init__.py
│   ├── search.py         # 搜索工具
│   ├── calculator.py     # 计算工具
│   └── weather.py        # 天气工具
├── memory/               # 记忆目录
│   ├── __init__.py
│   └── conversation_memory.py  # 对话记忆
├── state/                # 状态目录
│   ├── __init__.py
│   └── agent_state.py    # Agent 状态
├── error_handler/        # 错误处理目录
│   ├── __init__.py
│   └── retry_handler.py  # 重试处理器
├── logger/               # 日志目录
│   ├── __init__.py
│   └── agent_logger.py   # 日志记录器
└── tests/                # 测试目录
    ├── __init__.py
    ├── test_tools.py     # 工具测试
    ├── test_memory.py    # 记忆测试
    └── test_agent.py     # Agent 测试
```

---

## 🔧 技术栈

- **Python**: 3.8+
- **LangChain**: 最新版本
- **LangGraph**: 最新版本
- **OpenAI API**: GPT-3.5 或 GPT-4
- **pytest**: 测试框架
- **logging**: 日志记录

---

## 📝 项目要求

### 1. 工具实现（30 分钟）

**文件**: `tools/search.py`, `tools/calculator.py`, `tools/weather.py`

**要求**:
- 实现至少 3 个工具
- 工具需要有明确的输入和输出
- 工具需要有清晰的描述
- 工具需要有错误处理

**示例**:
```python
# tools/search.py
from langchain.tools import Tool

def search_tool(query: str) -> str:
    """搜索工具"""
    if not query:
        return "查询不能为空"
    
    # 模拟搜索结果
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架",
        "langgraph": "LangGraph 是一个状态管理框架"
    }
    
    for key, value in results.items():
        if query.lower() in key.lower():
            return value
    
    return f"未找到与 '{query}' 相关的结果"

# 创建 Tool
search_tool_obj = Tool(
    name="search",
    func=search_tool,
    description="搜索关键词，返回相关信息"
)
```

---

### 2. 记忆系统实现（20 分钟）

**文件**: `memory/conversation_memory.py`

**要求**:
- 使用 `ConversationBufferMemory`
- 保存对话历史
- 加载对话历史
- 支持上下文查询

**示例**:
```python
# memory/conversation_memory.py
from langchain.memory import ConversationBufferMemory

class ConversationMemory:
    """对话记忆"""
    
    def __init__(self, max_history: int = 10):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            k=max_history
        )
    
    def save_context(self, input: str, output: str):
        """保存对话上下文"""
        self.memory.save_context(
            {"input": input},
            {"output": output}
        )
    
    def load_history(self) -> list:
        """加载对话历史"""
        vars = self.memory.load_memory_variables({})
        return vars.get("chat_history", [])
    
    def clear_history(self):
        """清理对话历史"""
        self.memory.clear()
```

---

### 3. 错误处理实现（20 分钟）

**文件**: `error_handler/retry_handler.py`

**要求**:
- 实现重试机制
- 使用指数退避
- 记录错误日志
- 提供友好的错误提示

**示例**:
```python
# error_handler/retry_handler.py
import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class RetryHandler:
    """重试处理器"""
    
    def __init__(self, max_retries: int = 3, backoff_factor: int = 2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """执行函数，带重试机制"""
        retry_count = 0
        delay = 1
        
        while retry_count < self.max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                retry_count += 1
                
                if retry_count < self.max_retries:
                    logger.warning(f"重试 {retry_count}/{self.max_retries}，错误：{e}")
                    time.sleep(delay)
                    delay *= self.backoff_factor
                else:
                    logger.error(f"重试 {self.max_retries} 次后仍然失败")
                    raise e
```

---

### 4. 日志记录实现（10 分钟）

**文件**: `logger/agent_logger.py`

**要求**:
- 记录所有工具调用
- 记录所有中间步骤
- 记录错误和异常
- 支持导出日志到文件

**示例**:
```python
# logger/agent_logger.py
import logging
from typing import Any, Dict

class AgentLogger:
    """Agent 日志记录器"""
    
    def __init__(self, name: str = "agent", log_file: str = "agent.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_input(self, input: str):
        """记录输入"""
        self.logger.info(f"输入：{input}")
    
    def log_output(self, output: str):
        """记录输出"""
        self.logger.info(f"输出：{output}")
    
    def log_tool_call(self, tool_name: str, tool_input: Any):
        """记录工具调用"""
        self.logger.info(f"工具调用：{tool_name}({tool_input})")
    
    def log_error(self, error: Exception):
        """记录错误"""
        self.logger.error(f"错误：{str(error)}")
```

---

### 5. Agent 实现（30 分钟）

**文件**: `agent.py`

**要求**:
- 集成 LLM、工具、记忆、错误处理、日志
- 实现 Agent 的基本功能
- 支持用户交互
- 实现优雅的错误处理

**示例**:
```python
# agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from tools.search import search_tool_obj
from tools.calculator import calculator_tool_obj
from tools.weather import weather_tool_obj
from memory.conversation_memory import ConversationMemory
from error_handler.retry_handler import RetryHandler
from logger.agent_logger import AgentLogger
from typing import Optional

class IntelligentAgent:
    """智能助手"""
    
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI(temperature=0.7)
        
        # 工具
        self.tools = [
            search_tool_obj,
            calculator_tool_obj,
            weather_tool_obj
        ]
        
        # 记忆
        self.memory = ConversationMemory(max_history=10)
        
        # 错误处理
        self.retry_handler = RetryHandler(max_retries=3, backoff_factor=2)
        
        # 日志
        self.logger = AgentLogger()
        
        # Agent
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """创建 Agent"""
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools
        )
        
        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        return executor
    
    def execute(self, input: str) -> Optional[str]:
        """执行 Agent"""
        try:
            # 记录输入
            self.logger.log_input(input)
            
            # 带重试的执行
            result = self.retry_handler.execute_with_retry(
                self._execute_internal,
                input
            )
            
            # 保存对话
            self.memory.save_context(input, result)
            
            # 记录输出
            self.logger.log_output(result)
            
            return result
        
        except Exception as e:
            # 记录错误
            self.logger.log_error(e)
            return f"抱歉，发生错误：{str(e)}"
    
    def _execute_internal(self, input: str) -> str:
        """内部执行逻辑"""
        # 加载对话历史
        chat_history = self.memory.load_history()
        
        # 执行 Agent
        result = self.agent.invoke({
            "input": input,
            "chat_history": chat_history
        })
        
        return result["output"]
    
    def chat(self):
        """交互式聊天"""
        print("=" * 80)
        print("智能助手 - 你的第一个 Agent")
        print("=" * 80)
        print()
        
        while True:
            try:
                # 获取用户输入
                user_input = input("你：")
                
                # 退出条件
                if user_input.lower() in ["quit", "exit", "退出"]:
                    print("再见！")
                    break
                
                # 执行 Agent
                response = self.execute(user_input)
                
                # 输出回复
                print(f"助手：{response}")
                print()
            
            except KeyboardInterrupt:
                print("\n程序被用户中断")
                break
            except Exception as e:
                print(f"错误：{e}")
                continue


def main():
    """主函数"""
    # 创建 Agent
    agent = IntelligentAgent()
    
    # 开始聊天
    agent.chat()


if __name__ == "__main__":
    main()
```

---

## 🧪 测试要求

### 1. 工具测试

**文件**: `tests/test_tools.py`

**要求**:
- 测试所有工具的基本功能
- 测试工具的异常处理
- 测试工具的边界条件

**示例**:
```python
import pytest
from tools.search import search_tool_obj
from tools.calculator import calculator_tool_obj
from tools.weather import weather_tool_obj

def test_search_tool():
    """测试搜索工具"""
    # 测试正常情况
    result = search_tool_obj.func("langchain")
    assert "LangChain" in result
    
    # 测试边界条件
    result = search_tool_obj.func("")
    assert "不能为空" in result

def test_calculator_tool():
    """测试计算工具"""
    # 测试正常情况
    result = calculator_tool_obj.func("1 + 1")
    assert "2" in result
    
    # 测试异常情况
    result = calculator_tool_obj.func("1 / 0")
    assert "失败" in result

def test_weather_tool():
    """测试天气工具"""
    # 测试正常情况
    result = weather_tool_obj.func("北京")
    assert "北京" in result
    
    # 测试异常情况
    result = weather_tool_obj.func("未知城市")
    assert "抱歉" in result
```

---

### 2. 记忆测试

**文件**: `tests/test_memory.py`

**要求**:
- 测试对话历史的保存
- 测试对话历史的加载
- 测试对话历史的清理

**示例**:
```python
import pytest
from memory.conversation_memory import ConversationMemory

def test_memory():
    """测试记忆系统"""
    memory = ConversationMemory(max_history=10)
    
    # 测试保存
    memory.save_context("你好", "你好！")
    
    # 测试加载
    history = memory.load_history()
    assert len(history) > 0
    
    # 测试清理
    memory.clear_history()
    history = memory.load_history()
    assert len(history) == 0
```

---

### 3. Agent 测试

**文件**: `tests/test_agent.py`

**要求**:
- 测试 Agent 的基本功能
- 测试 Agent 的工具调用
- 测试 Agent 的记忆系统
- 测试 Agent 的错误处理

**示例**:
```python
import pytest
from agent import IntelligentAgent

def test_agent():
    """测试 Agent"""
    agent = IntelligentAgent()
    
    # 测试基本功能
    result = agent.execute("搜索 LangChain")
    assert result is not None
    
    # 测试记忆系统
    history = agent.memory.load_history()
    assert len(history) > 0
```

---

### 4. 测试覆盖率

**要求**:
- 测试覆盖率 >= 70%
- 所有核心功能都有测试
- 所有边界条件都有测试

**运行测试**:
```bash
# 运行所有测试
pytest tests/ -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

---

## 🎯 项目验收标准

当你完成以下所有项，就说明单一 Agent 项目达标了：

### 代码实现

- [ ] 实现了至少 3 个工具
- [ ] 实现了记忆系统
- [ ] 实现了错误处理和重试机制
- [ ] 实现了日志记录
- [ ] 实现了完整的 Agent

### 测试覆盖

- [ ] 编写了工具测试
- [ ] 编写了记忆测试
- [ ] 编写了 Agent 测试
- [ ] 测试覆盖率 >= 70%

### 文档和注释

- [ ] 所有文件都有类型提示
- [ ] 所有函数都有文档字符串（docstring）
- [ ] 关键代码有注释说明
- [ ] 有 README.md 文档

### 功能正确性

- [ ] Agent 能够正常工作
- [ ] 工具能够正常调用
- [ ] 记忆能够正常保存和加载
- [ ] 错误能够优雅地处理

---

## 🚀 开始项目

### 1. 创建项目结构

```bash
cd /Users/xiongfeng/SourceCode/agent-learn/study/level1/projects

# 创建项目目录
mkdir -p intelligent_assistant
cd intelligent_assistant

# 创建目录结构
mkdir -p tools memory state error_handler logger tests

# 创建文件
touch agent.py README.md

# 创建 Python 包文件
touch tools/__init__.py
touch memory/__init__.py
touch state/__init__.py
touch error_handler/__init__.py
touch logger/__init__.py
touch tests/__init__.py
```

---

### 2. 实现项目文件

按照上面的代码示例，实现每个文件。

---

### 3. 运行和测试

```bash
# 运行 Agent
python agent.py

# 运行测试
pytest tests/ -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
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

- ✅ 3 个工具（搜索、计算、天气）
- ✅ 1 个记忆系统（对话记忆）
- ✅ 1 个错误处理器（重试处理器）
- ✅ 1 个日志记录器（Agent 日志）
- ✅ 1 个完整的 Agent 系统
- ✅ 至少 3 个测试文件（工具、记忆、Agent）

### 项目收获

- ✅ 掌握了单一 Agent 的架构设计
- ✅ 掌握了工具的开发和集成
- ✅ 掌握了记忆系统的实现
- ✅ 掌握了错误处理和重试机制
- ✅ 掌握了日志记录的方法
- ✅ 掌握了单元测试的编写

---

## 🎯 核心要点总结

### 单一 Agent 架构

| 组件 | 作用 | 状态 |
|------|------|------|
| **LLM** | 提供推理和生成能力 | ✅ 已实现 |
| **Tools** | 提供执行特定任务的能力 | ✅ 已实现（3 个工具）|
| **Memory** | 提供存储和检索历史信息的能力 | ✅ 已实现 |
| **Error Handler** | 提供错误处理和重试的能力 | ✅ 已实现 |
| **Logger** | 提供日志记录的能力 | ✅ 已实现 |

### 工具列表

| 工具 | 功能 | 状态 |
|------|------|------|
| **搜索工具** | 搜索关键词 | ✅ 已实现 |
| **计算工具** | 计算数学表达式 | ✅ 已实现 |
| **天气工具** | 查询天气信息 | ✅ 已实现 |

---

**项目完成标准**: ✅ **代码实现 + 测试覆盖 + 文档注释**

**继续学习**: `study/level2/` - Level 2: 深度理解 🚀
