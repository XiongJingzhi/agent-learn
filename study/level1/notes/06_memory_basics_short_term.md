# 短期记忆基础

> **目标**: 理解会话上下文管理、窗口大小控制、记忆存储
> **预计时间**: 25 分钟
> **前置**: 已完成重试与错误处理学习

---

## 为什么需要短期记忆？

短期记忆（Short-term Memory）让 Agent 能够：
- **保持上下文**：记住对话历史，提供连贯的对话
- **引用前文**：引用之前的内容，避免重复
- **个性化服务**：记住用户的偏好和设置

**类比**：短期记忆就像**人的工作记忆**，能记住当前对话的内容。

---

## LangChain 记忆类型

### 类型 1：ConversationBufferMemory

保存完整的对话历史。

```python
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True  # 返回消息对象
)

# 保存对话
memory.save_context(
    {"input": "我叫张三"},
    {"output": "你好，张三！"}
)

memory.save_context(
    {"input": "我叫什么名字？"},
    {"output": "你叫张三。"}
)

# 加载对话
history = memory.load_memory_variables({})
print(history["chat_history"])
# 输出：包含 4 条消息（2 轮对话）
```

**特点**：
- ✅ 完整保留所有历史
- ❌ 消耗大量 token
- ❌ 可能超出上下文窗口

---

### 类型 2：ConversationBufferWindowMemory

只保留最近 N 条消息。

```python
from langchain.memory import ConversationBufferWindowMemory

# 创建窗口记忆（保留最近 3 条消息）
memory = ConversationBufferWindowMemory(
    k=3,  # 窗口大小
    memory_key="chat_history",
    return_messages=True
)

# 保存对话
for i in range(5):
    memory.save_context(
        {"input": f"消息 {i}"},
        {"output": f"回复 {i}"}
    )

# 加载对话
history = memory.load_memory_variables({})
print(f"消息数: {len(history['chat_history'])}")
# 输出：消息数: 6（最近 3 轮对话，每轮 2 条）
```

**特点**：
- ✅ 控制记忆大小
- ✅ 适合长对话
- ❌ 丢失早期上下文

---

### 类型 3：ConversationSummaryMemory

使用 LLM 总结对话历史。

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

# 创建总结记忆
memory = ConversationSummaryMemory(
    llm=ChatOpenAI(temperature=0),
    memory_key="chat_history"
)

# 保存对话
memory.save_context(
    {"input": "我学习了 Python"},
    {"output": "很好！Python 是一门流行的语言"}
)

memory.save_context(
    {"input": "我还学习了 LangChain"},
    {"output": "LangChain 是一个 LLM 应用框架"}
)

# 加载对话
history = memory.load_memory_variables({})
print(history["chat_history"])
# 输出：AI 生成的总结，而不是原始对话
```

**特点**：
- ✅ 压缩对话内容
- ✅ 节省 token
- ❌ 可能丢失细节

---

## 记忆在 Agent 中的使用

### 使用 1：与 Agent 集成

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 创建 LLM
llm = ChatOpenAI(temperature=0)

# 创建工具
tools = [
    Tool(name="search", func=lambda x: f"搜索 {x} 的结果", description="搜索")
]

# 创建 Agent
agent = create_react_agent(llm, tools)

# 创建执行器（带记忆）
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,  # 传入记忆
    verbose=True
)

# 执行（会自动保存对话）
result1 = executor.invoke({"input": "搜索 LangChain"})
result2 = executor.invoke({"input": "刚才搜索了什么？"})
# Agent 能回答之前的问题
```

---

### 使用 2：手动管理记忆

```python
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 创建 LLM
llm = ChatOpenAI(temperature=0)

# 对话循环
while True:
    user_input = input("你: ")

    if user_input.lower() in ["quit", "exit"]:
        break

    # 加载历史
    history = memory.load_memory_variables({})
    chat_history = history.get("chat_history", [])

    # 构建提示
    messages = [
        {"role": "system", "content": "你是一个有用的助手。"}
    ] + chat_history + [
        {"role": "user", "content": user_input}
    ]

    # 调用 LLM
    response = llm.invoke(messages)

    # 输出
    print(f"助手: {response.content}")

    # 保存对话
    memory.save_context(
        {"input": user_input},
        {"output": response.content}
    )
```

---

## 记忆管理策略

### 策略 1：窗口大小控制

根据 token 限制动态调整窗口。

```python
def estimate_tokens(text: str) -> int:
    """估算 token 数量（粗略估计）"""
    return len(text.split())

def dynamic_window_memory(max_tokens: int = 2000):
    """动态窗口记忆"""
    memory = ConversationBufferMemory(return_messages=True)

    class DynamicWindowMemory:
        def save_context(self, inputs, outputs):
            memory.save_context(inputs, outputs)
            self._trim_to_fit()

        def load_memory_variables(self, variables):
            return memory.load_memory_variables(variables)

        def _trim_to_fit(self):
            """修剪历史以适应 token 限制"""
            while True:
                history = memory.load_memory_variables({})
                messages = history.get("chat_history", [])

                # 计算 token 数量
                total_tokens = sum(
                    estimate_tokens(msg.content)
                    for msg in messages
                )

                if total_tokens <= max_tokens:
                    break

                # 删除最旧的消息
                if len(messages) >= 2:
                    # 删除一轮对话（输入+输出）
                    messages = messages[2:]
                    memory.chat_memory.messages = messages
                else:
                    break

    return DynamicWindowMemory()
```

---

### 策略 2：关键信息保留

保留重要信息，丢弃冗余信息。

```python
from typing import List
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage

class KeyInfoMemory:
    """关键信息记忆"""

    def __init__(self):
        self.memory = ConversationBufferMemory(return_messages=True)
        self.key_info = {}  # 存储关键信息

    def save_context(self, inputs: dict, outputs: dict):
        """保存上下文"""
        # 保存到普通记忆
        self.memory.save_context(inputs, outputs)

        # 提取关键信息
        user_input = inputs.get("input", "")
        self._extract_key_info(user_input)

    def _extract_key_info(self, text: str):
        """提取关键信息"""
        # 示例：提取名字
        if "我叫" in text or "我是" in text:
            # 简单的提取逻辑
            if "我叫" in text:
                name = text.split("我叫")[1].strip()
            else:
                name = text.split("我是")[1].strip()
            self.key_info["name"] = name

    def load_memory_variables(self, variables: dict) -> dict:
        """加载记忆变量"""
        # 加载普通历史
        history = self.memory.load_memory_variables(variables)

        # 添加关键信息摘要
        if self.key_info:
            summary = "记住的信息: " + ", ".join(
                f"{k}={v}" for k, v in self.key_info.items()
            )
            # 在历史前添加摘要
            return {
                "chat_history": history.get("chat_history", []),
                "key_info_summary": summary
            }

        return history
```

---

### 策略 3：分层记忆

短期、中期、长期记忆分离。

```python
class TieredMemory:
    """分层记忆"""

    def __init__(self):
        # 短期：当前对话（最近 10 条）
        self.short_term = ConversationBufferWindowMemory(k=10)
        # 中期：重要信息（名字、偏好）
        self.medium_term = {}
        # 长期：持久化存储
        self.long_term = None

    def save_context(self, inputs: dict, outputs: dict):
        """保存上下文"""
        # 保存到短期记忆
        self.short_term.save_context(inputs, outputs)

        # 提取并保存到中期记忆
        self._extract_medium_term(inputs)

    def _extract_medium_term(self, inputs: dict):
        """提取中期记忆信息"""
        text = inputs.get("input", "")

        # 提取用户名字
        if "我叫" in text or "我是" in text:
            if "我叫" in text:
                name = text.split("我叫")[1].strip()
            else:
                name = text.split("我是")[1].strip()
            self.medium_term["user_name"] = name

    def load_memory_variables(self, variables: dict) -> dict:
        """加载记忆变量"""
        # 加载短期记忆
        short_history = self.short_term.load_memory_variables({})

        # 构建完整上下文
        context_parts = []

        # 添加中期记忆
        if self.medium_term:
            context_parts.append(
                "用户信息: " + str(self.medium_term)
            )

        # 添加短期记忆
        if short_history.get("chat_history"):
            context_parts.append(
                "最近对话: " + str(short_history["chat_history"][-3:])
            )

        return {
            "context": "\n".join(context_parts),
            "chat_history": short_history.get("chat_history", [])
        }
```

---

## 完整示例：带记忆的对话 Agent

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory

class MemoryAgentState(TypedDict):
    input: str
    output: str
    chat_history: list

# 创建记忆
memory = ConversationBufferWindowMemory(k=6, return_messages=True)
llm = ChatOpenAI(temperature=0.7)

def chat_node(state: MemoryAgentState) -> dict:
    """聊天节点"""
    user_input = state["input"]

    # 加载历史
    history = memory.load_memory_variables({})
    chat_history = history.get("chat_history", [])

    # 构建消息
    messages = [
        {"role": "system", "content": "你是一个友好的助手。"}
    ]

    # 添加历史
    for msg in chat_history:
        if hasattr(msg, 'type'):
            role = "user" if msg.type == "human" else "assistant"
            messages.append({"role": role, "content": msg.content})

    # 添加当前输入
    messages.append({"role": "user", "content": user_input})

    # 调用 LLM
    response = llm.invoke(messages)

    # 保存到记忆
    memory.save_context(
        {"input": user_input},
        {"output": response.content}
    )

    return {
        "output": response.content,
        "chat_history": memory.load_memory_variables({})["chat_history"]
    }

# 构建图
graph = StateGraph(MemoryAgentState)
graph.add_node("chat", chat_node)
graph.set_entry_point("chat")
graph.add_edge("chat", END)

app = graph.compile()

# 测试
print("=== 对话测试 ===")
test_inputs = [
    "你好",
    "我叫张三",
    "我叫什么名字？",
    "我喜欢编程",
    "我喜欢什么？"
]

for inp in test_inputs:
    print(f"\n用户: {inp}")
    result = app.invoke({"input": inp, "chat_history": []})
    print(f"助手: {result['output']}")
```

---

## 最小验证

### 验证目标
- ✅ 理解不同记忆类型
- ✅ 能够集成记忆到 Agent
- ✅ 能够控制记忆窗口大小

### 验证步骤
1. 创建 ConversationBufferWindowMemory
2. 集成到 Agent 中
3. 测试多轮对话
4. 验证窗口大小限制

---

## 常见错误

### 错误 1：忘记保存对话
```python
# 错误：没有保存对话
memory = ConversationBufferMemory()
# ... 使用对话但没有保存
result = agent.invoke({"input": "你好"})

# 正确：使用 AgentExecutor 自动保存
executor = AgentExecutor(agent=agent, tools=tools, memory=memory)
result = executor.invoke({"input": "你好"})  # 自动保存
```

### 错误 2：窗口太小
```python
# 错误：窗口太小，丢失上下文
memory = ConversationBufferWindowMemory(k=2)  # 只保留 2 条消息
# 在长对话中无法回答关于之前内容的问题

# 正确：根据对话长度调整
memory = ConversationBufferWindowMemory(k=10)  # 保留 10 条消息
```

---

## 下一步

- 📖 `notes/07_debugging_and_observability_basics.md` - 调试与可观测基础
- 🧪 `examples/08_memory_management.py` - 记忆管理示例

---

**记住：短期记忆就像人的工作记忆，能记住当前对话的内容！** 🧠
