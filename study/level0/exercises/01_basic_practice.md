# 01. 基础练习题 - Level 0

> **目标**: 测试你对 Agent 核心概念的理解和代码实践

---

## 📊 练习统计

- **总题数**: 30 题
- **选择题**: 15 题
- **代码题**: 10 题
- **设计题**: 5 题
- **预计时间**: 45 分钟

---

## 🎯 选择题（1-15）

### 第 1 部分：核心概念（1-8）

**Q1. Agent 的四个核心组件不包括：**

A. 感知
B. 推理
C. 存储
D. 执行

**答案**: D

**Q2. ReAct 循环的四个阶段不包括：**

A. 思考
B. 行动
C. 观察
D. 编译

**答案**: D

**Q3. Agent 的记忆类型不包括：**

A. 短期记忆
B. 中期记忆
C. 长期记忆
D. 永久记忆

**答案**: D

**Q4. Chatbot 的特点不包括：**

A. 预定义对话
B. 模式匹配
C. 状态跟踪
D. 自主决策

**答案**: D

**Q5. Agent 状态更新的策略不包括：**

A. 直接更新
B. 追加更新
C. 分层更新
D. 随机更新

**答案**: D

**Q6. Agent 的常见失败模式不包括：**

A. 无限循环
B. 死锁
C. 资源耗尽
D. 幻觉
E. 代码优化

**答案**: E

**Q7. Agent 工具的类型不包括：**

A. 文本处理工具
B. 数据查询工具
C. 计算工具
D. 搜索工具
E. 网络攻击工具

**答案**: E

**Q8. 环境检查的步骤不包括：**

A. 检查 Python 版本
B. 检查 pip 版本
C. 检查依赖安装
D. 检查代码质量

**答案**: D

---

### 第 2 部分：代码实现（9-15）

**Q9. 以下哪个代码片段创建了一个简单的 Tool？**

A.
```python
def tool(input: str) -> str:
    return f"Tool: {input}"
```

B.
```python
from langchain.tools import Tool
tool = Tool(name="tool", func=lambda x: f"Tool: {x}")
```

C.
```python
from langchain.agents import create_react_agent
agent = create_react_agent(llm, tools)
```

D. 以上都是

**答案**: D

**Q10. 以下哪个代码片段创建了一个 ReAct Agent？**

A.
```python
from langchain.agents import create_react_agent
agent = create_react_agent(llm, tools)
```

B.
```python
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
```

C.
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
```

D. 以上都是

**答案**: A

**Q11. 以下哪个代码片段创建了一个 ConversationBufferMemory？**

A.
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
```

B.
```python
from langchain.agents import AgentExecutor
executor = AgentExecutor.from_agent_and_tools(agent, tools)
```

C.
```python
from langchain.tools import Tool
tool = Tool(name="tool", func=func, description="...")
```

D. 以上都是

**答案**: A

**Q12. 以下哪个代码片段用于测试 Agent？**

A.
```python
import pytest

def test_agent():
    result = agent.invoke({"input": "test"})
    assert result["output"] is not None
```

B.
```python
from unittest.mock import Mock

def test_agent_with_mock():
    mock_llm = Mock(return_value="Mock 回复")
    agent = create_react_agent(mock_llm, [])
    result = agent.invoke({"input": "test"})
    assert result["output"] == "Mock 回复"
```

C.
```python
from langchain.memory import ConversationBufferMemory

def test_memory():
    memory = ConversationBufferMemory()
    memory.save_context({"input": "test"}, {"output": "result"})
    vars = memory.load_memory_variables({})
    assert "test" in str(vars)
```

D. 以上都是

**答案**: D

**Q13. 以下哪个是 ReAct 循环的正确执行顺序？**

A. 观察 → 思考 → 行动 → 循环
B. 思考 → 行动 → 观察 → 循环
C. 思考 → 观察 → 行动 → 循环
D. 行动 → 思考 → 观察 → 循环

**答案**: B

**Q14. 以下哪个是 Agent 和 Chatbot 的主要区别？**

A. Agent 能自主决策，Chatbot 只能按固定规则执行
B. Agent 有推理能力，Chatbot 没有
C. Agent 有学习能力，Chatbot 没有
D. 以上都是

**答案**: D

**Q15. 以下哪个是 Agent 状态更新的正确策略？**

A. 总是直接更新
B. 总是追加更新
C. 根据信息类型和重要性选择不同的更新策略
D. 不需要更新状态

**答案**: C

---

## 🎯 代码题（16-25）

### 代码填空题（16-20）

**Q16. 补充完整创建 Tool 的代码**

```python
from langchain.tools import Tool

def search_tool(query: str) -> str:
    """搜索工具"""
    return f"搜索结果：{query}"

# 创建 Tool
tool = ________(
    name="search",
    func=search_tool,
    description="搜索关键词"
)
```

**答案**: Tool

---

**Q17. 补充完整创建 ReAct Agent 的代码**

```python
from langchain.agents import create_react_agent
from langchain.tools import Tool

# 创建 LLM
llm = OpenAI(temperature=0)

# 创建 Agent
agent = ________(llm=llm, tools=[search_tool])
```

**答案**: create_react_agent

---

**Q18. 补充完整创建 AgentExecutor 的代码**

```python
from langchain.agents import AgentExecutor

# 创建 Agent 执行器
agent_executor = AgentExecutor.______(
    agent=agent,
    tools=[search_tool],
    verbose=True
)
```

**答案**: from_agent_and_tools

---

**Q19. 补充完整创建 ConversationBufferMemory 的代码**

```python
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=______
)
```

**答案**: True

---

**Q20. 补充完整调用 Agent 的代码**

```python
# 执行 Agent
result = agent_executor.______({"input": "搜索 LangChain"})
```

**答案**: invoke

---

## 🎯 设计题（26-30）

### 设计场景（26-30）

**Q26. 设计一个简单的天气查询 Agent**

**要求**：
- 有一个查询天气的工具
- 能够根据城市名返回天气信息
- 如果城市名不存在，返回友好提示

**答案**:
```python
from langchain.tools import Tool

def get_weather(city: str) -> str:
    """获取天气信息（模拟）"""
    weather_map = {
        "北京": "北京今天天气晴，气温 25℃",
        "上海": "上海今天天气多云，气温 28℃",
        "广州": "广州今天天气雨，气温 26℃"
    }
    
    return weather_map.get(city, f"抱歉，我们还没有 {city} 的天气信息。")

weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="获取指定城市的天气信息，参数：city（城市名）"
)
```

---

**Q27. 设计一个带记忆的对话 Agent**

**要求**：
- 能够记住用户的姓名
- 能够记住用户的偏好设置
- 能够根据记忆提供个性化服务

**答案**:
```python
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 保存用户信息
def save_user_info(user_name: str, user_preferences: dict):
    """保存用户信息"""
    memory.save_context(
        {"input": f"我的名字是{user_name}，我喜欢{user_preferences.get('language', '中文')}"},
        {"output": f"你好，{user_name}！我会记住你的偏好：{user_preferences}"}
    )
```

---

**Q28. 设计一个带工具的搜索 Agent**

**要求**：
- 有一个搜索工具
- 有一个计算工具
- 能够根据用户的需求调用合适的工具

**答案**:
```python
from langchain.tools import Tool

def search_tool(query: str) -> str:
    """搜索工具"""
    return f"搜索结果：{query}"

def calculator_tool(expression: str) -> str:
    """计算工具"""
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except:
        return f"无法计算：{expression}"

tools = [Tool(name="search", func=search_tool, description="搜索关键词"),
          Tool(name="calculator", func=calculator_tool, description="计算数学表达式")]
```

---

**Q29. 设计一个带错误处理的 Agent**

**要求**：
- 能够处理工具调用失败的情况
- 能够优雅地处理异常
- 能够给用户友好的错误提示

**答案**:
```python
from langchain.agents import AgentExecutor

# 创建带错误处理的 Agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,  # 处理解析错误
    return_intermediate_steps=True  # 返回中间步骤
)
```

---

**Q30. 设计一个多轮对话 Agent**

**要求**：
- 能够处理多轮对话
- 能够记住之前的对话历史
- 能够根据上下文生成回复

**答案**:
```python
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5  # 保留最近 5 条消息
)

# 创建对话链
from langchain.chains import ConversationChain

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)
```

---

## 🎯 核心要点总结

### Agent 的核心组件

| 组件 | 作用 | 类比 |
|------|------|------|
| **感知** | 接收输入、解析信息 | 眼睛和耳朵 |
| **推理** | 分析情况、制定计划 | 大脑 |
| **执行** | 执行决策、调用工具 | 手和脚 |
| **记忆** | 存储历史、学习经验 | 大脑 |

### ReAct 循环的四个阶段

| 阶段 | 作用 | 类比 |
|------|------|------|
| **思考** | 分析情况、制定计划 | 医生问诊 |
| **行动** | 执行计划、调用工具 | 医生开药 |
| **观察** | 观察结果、更新状态 | 医生观察病情 |
| **循环** | 判断是否继续、结束循环 | 医生判断是否康复 |

### Agent 的记忆类型

| 类型 | 容量 | 时间 | 适用场景 |
|------|------|------|----------|
| **短期记忆** | 小 | 短 | 最近对话、当前任务状态 |
| **中期记忆** | 中 | 中 | 用户上下文、任务进度 |
| **长期记忆** | 大 | 长 | 用户偏好、重要历史 |

### Agent 的常见失败模式

| 模式 | 原因 | 解决方法 |
|------|------|----------|
| **无限循环** | 循环条件错误、状态不变 | 设置循环最大次数、更新状态 |
| **死锁** | 资源竞争、循环等待 | 超时检测、调整锁顺序 |
| **资源耗尽** | 内存泄漏、API 限制 | 资源限制、内存管理 |
| **幻觉** | 知识不足、推理错误 | 知识库更新、验证机制 |

---

## 📊 练习总结

### 统计信息

- **选择题**: 15 题
- **代码题**: 10 题
- **设计题**: 5 题
- **总计**: 30 题

### 难度分布

- ⭐ 简单: 10 题 (1-10)
- ⭐⭐ 中等: 10 题 (11-20)
- ⭐⭐⭐ 困难: 10 题 (21-30)

### 预计时间

- 快速完成: 30 分钟
- 仔细完成: 45 分钟
- 深入思考: 60 分钟

---

## 🎯 完成标准

当你完成以下所有项，就说明基础练习达标了：

- [ ] 完成 15 道选择题
- [ ] 完成 10 道代码题
- [ ] 完成 5 道设计题
- [ ] 正确率 >= 80%
- [ ] 能够编写简单的 Agent 代码
- [ ] 能够创建简单的 Tool
- [ ] 能够理解 ReAct 循环的执行流程

---

## 🚀 下一步

完成基础练习后，你将：

✅ 掌握 Agent 的核心概念  
✅ 掌握 ReAct 循环的执行流程  
✅ 掌握 Agent 的记忆管理  
✅ 掌握 Agent 的工具集成  
✅ 掌握 Agent 的错误处理  
✅ 为 Level 1：动手实践做好准备  

**继续学习**: Level 1 - 动手实践 🚀
