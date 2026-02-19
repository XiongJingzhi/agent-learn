# 07. LangChain 基础 - Feynman Technique

> **费曼技巧**：如果不能简单解释，说明没有真正理解。
> **目标**：用简单的语言和类比，解释 LangChain 的核心概念。

---

## 🎯 学习目标

通过本章学习，你将能够：

1. ✅ 理解 **LangChain 是什么**，以及它为什么重要
2. ✅ 掌握 **LangChain 的六大核心组件**
3. ✅ 理解 **Chains、Agents、Tools 的关系**
4. ✅ 能够使用 **LangChain 构建简单的应用**
5. ✅ 能够用简单的语言向"5岁孩子"解释 LangChain

---

## 📚 核心概念

### 概念 1：LangChain 是什么？

> **类比**：LangChain 就像一个**乐高积木套装**，提供了各种预制件（模块），你可以用它们搭建出各种 AI 应用（城堡、汽车、飞机）。

**LangChain 的定义**：

LangChain 是一个**开发框架**，用于构建基于 LLM（大语言模型）的应用。它提供了一套**标准化的组件**和**接口**，让开发者能够更容易地：
- 连接到各种 LLM（OpenAI、Claude、Llama 等）
- 管理提示词（Prompt）
- 链式调用多个组件
- 构建智能 Agent
- 集成外部数据源

**核心思想**：**不要重复造轮子**，使用 LangChain 提供的"乐高积木"，快速搭建 AI 应用。

---

### 概念 2：LangChain 的六大核心组件

#### 组件 1：Model I/O（模型输入输出）

> **类比**：就像**打电话**，Model I/O 负责拨号（输入）、通话（处理）、挂断（输出）。

**Model I/O 的作用**：
- ✅ **输入**：将你的消息发送给 LLM
- ✅ **输出**：接收 LLM 的回复
- ✅ **格式化**：处理输入输出的格式

**示例**：
```python
from langchain_openai import ChatOpenAI

# 创建 LLM
llm = ChatOpenAI(model="gpt-4")

# 输入消息
message = "你好，请介绍一下自己"

# 获取输出
response = llm.invoke(message)
print(response.content)
```

---

#### 组件 2：Chains（链）

> **类比**：就像**工厂流水线**，原材料经过一道道工序，最终变成成品。

**Chains 的作用**：
- ✅ **连接多个组件**：将 LLM、工具、数据处理等连接起来
- ✅ **定义执行流程**：按照预定义的顺序执行
- ✅ **传递数据**：在组件之间传递数据

**示例**：
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# 创建提示模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="请写一个关于{topic}的简短介绍"
)

# 创建链
chain = LLMChain(llm=llm, prompt=prompt)

# 执行链
result = chain.run(topic="LangChain")
print(result)
```

---

#### 组件 3：Agents（智能体）

> **类比**：就像一个**智能管家**，你只需要告诉他目标，他会自己思考、规划、执行。

**Agents 的作用**：
- ✅ **自主决策**：根据用户目标决定做什么
- ✅ **使用工具**：调用各种工具完成任务
- ✅ **循环执行**：思考→行动→观察→循环

**示例**：
```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

# 创建工具
def search_tool(query: str) -> str:
    return "这是搜索结果"

tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="搜索网络信息"
    )
]

# 创建 Agent
agent = create_react_agent(llm, tools)

# 执行
agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": "搜索 LangChain 的信息"})
```

---

#### 组件 4：Tools（工具）

> **类比**：就像**瑞士军刀**，每一把刀片都是一个工具，用于不同的场景。

**Tools 的作用**：
- ✅ **扩展能力**：让 LLM 能够执行实际操作（搜索、计算、文件操作等）
- ✅ **标准化接口**：统一的工具调用方式
- ✅ **可组合**：工具可以组合使用

**示例**：
```python
from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"结果是：{result}"
    except Exception as e:
        return f"错误：{str(e)}"

# 使用工具
result = calculator.invoke("2 + 2")
print(result)  # 结果是：4
```

---

#### 组件 5：Memory（记忆）

> **类比**：就像**人的记忆**，短期记忆记住刚才说的话，长期记忆保存重要信息。

**Memory 的作用**：
- ✅ **保存历史**：记住之前的对话
- ✅ **提供上下文**：让 LLM 能够理解历史信息
- ✅ **多种类型**：支持不同的记忆策略

**示例**：
```python
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory()

# 添加对话
memory.save_context({"input": "你好"}, {"output": "你好！有什么可以帮助你的吗？"})

# 获取历史
history = memory.load_memory_variables({})
print(history)
# {'history': 'Human: 你好\nAI: 你好！有什么可以帮助你的吗？'}
```

---

#### 组件 6：Retrieval（检索）

> **类比**：就像**图书馆检索系统**，根据你的需求找到相关的书籍。

**Retrieval 的作用**：
- ✅ **文档加载**：从各种来源加载文档
- ✅ **文本分割**：将长文档切分成小块
- ✅ **向量存储**：将文本向量化并存储
- ✅ **相似度检索**：找到最相关的文档

**示例**：
```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 1. 加载文档
loader = TextLoader("document.txt")
documents = loader.load()

# 2. 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

# 3. 创建向量存储
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)

# 4. 检索
retriever = vectorstore.as_retriever()
docs = retriever.get_relevant_documents("查询内容")
```

---

### 概念 3：Chains、Agents、Tools 的关系

> **类比**：
> - **Chains** = 预定的**食谱**（按步骤做菜）
> - **Agents** = **厨师**（根据实际情况调整）
> - **Tools** = **厨具**（刀、锅、烤箱等）

**关系图**：
```
┌─────────────────────────────────────────────────┐
│                    应用层                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────┐      ┌────────────┐            │
│  │  Chains    │      │  Agents    │            │
│  │  (预定流程) │      │  (自主决策) │            │
│  └────────────┘      └────────────┘            │
│         │                    │                   │
│         └────────┬───────────┘                   │
│                  │                               │
│                  ▼                               │
│          ┌────────────┐                         │
│          │   Tools    │                         │
│          │  (工具集)  │                         │
│          └────────────┘                         │
│                  │                               │
│                  ▼                               │
│          ┌────────────┐                         │
│          │  Model I/O │                         │
│          │   (LLM)    │                         │
│          └────────────┘                         │
│                                                  │
└──────────────────────────────────────────────────┘
```

**使用场景**：
- **简单任务**：用 Chains（如：翻译文本）
- **复杂任务**：用 Agents（如：研究助手）
- **所有场景**：都需要 Tools（如：搜索、计算）

---

## 🛠️ 实践示例

### 示例 1：第一个 Chain

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# 1. 创建 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. 创建提示模板
prompt = ChatPromptTemplate.from_template(
    "你是一个{role}。请回答：{question}"
)

# 3. 创建 Chain
chain = LLMChain(llm=llm, prompt=prompt)

# 4. 执行
result = chain.run(
    role="Python 专家",
    question="什么是列表推导式？"
)

print(result)
```

---

### 示例 2：带工具的 Agent

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

# 1. 定义工具
@tool
def get_word_length(word: str) -> str:
    """返回单词的长度"""
    return f"单词 '{word}' 的长度是 {len(word)}"

tools = [get_word_length]

# 2. 创建 Agent
llm = ChatOpenAI(model="gpt-3.5-turbo")
agent = create_react_agent(llm, tools)

# 3. 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # 显示执行过程
)

# 4. 执行
result = agent_executor.invoke({
    "input": "单词 'LangChain' 有多长？"
})

print(result["output"])
```

---

### 示例 3：带记忆的对话

```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 1. 创建 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. 创建记忆
memory = ConversationBufferMemory()

# 3. 创建对话 Chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# 4. 多轮对话
response1 = conversation.predict(input="我叫小明")
print(f"AI: {response1}")

response2 = conversation.predict(input="我叫什么名字？")
print(f"AI: {response2}")  # AI 应该记得你叫小明
```

---

## 🔍 费曼学习检查

### 向"5岁孩子"解释

**假设你正在向5岁孩子解释 LangChain，你能这样说吗？**

1. **LangChain 是什么？**
   > "LangChain 就像一个**智能玩具套装**，里面有各种积木块。你可以用这些积木块搭建出会说话、会思考的机器人朋友！"

2. **Chains 是什么？**
   > "Chain 就像**做蛋糕的步骤**：先打鸡蛋、再加面粉、然后烘烤。每一步都要按顺序做，最后才能做出美味的蛋糕。"

3. **Agents 是什么？**
   > "Agent 就像一个**聪明的助手**，你告诉他想要什么，他会自己想办法帮你完成。就像你让妈妈帮你拿玩具，她会自己知道玩具在哪里。"

4. **Tools 是什么？**
   > "Tools 就像**工具箱里的工具**，有锤子、螺丝刀、扳手。每个工具都有自己的用途，Agent 会根据需要选择合适的工具。"

---

## 🎯 核心要点总结

### LangChain 的六大组件

| 组件 | 作用 | 类比 |
|------|------|------|
| **Model I/O** | 连接 LLM | 打电话 |
| **Chains** | 连接多个组件 | 工厂流水线 |
| **Agents** | 自主决策 | 智能管家 |
| **Tools** | 执行具体操作 | 瑞士军刀 |
| **Memory** | 保存历史信息 | 人的记忆 |
| **Retrieval** | 检索相关文档 | 图书馆检索 |

### 何时使用什么

| 场景 | 推荐方案 |
|------|---------|
| **简单任务**（如翻译） | Chains |
| **复杂任务**（如研究） | Agents + Tools |
| **需要对话** | Chains + Memory |
| **需要外部信息** | Chains + Retrieval |
| **完全自主** | Agents + Tools + Memory |

---

## 🚀 下一步

现在你已经理解了 LangChain 的核心概念，让我们继续学习：

- 📖 `examples/07_langchain_basics.py` - LangChain 基础示例代码
- 📖 `examples/08_first_agent.py` - 构建第一个 Agent
- 🧪 `exercises/01_basic_exercises.md` - 基础练习题

---

## 💡 学习建议

1. **先理解，后实践**：确保理解概念后再写代码
2. **从简单开始**：先用 Chains，再尝试 Agents
3. **多做实验**：修改参数，观察效果变化
4. **查看文档**：遇到问题时查阅 [LangChain 文档](https://python.langchain.com/)

---

**记住：LangChain 就像乐高积木，掌握了基础组件，你就能搭建出任何想象中的 AI 应用！** 🧱🤖
