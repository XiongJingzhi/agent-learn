# 12. RAG 系统集成

> **主题**: 为多智能体系统添加知识检索能力
> **时间**: 60 分钟
> **难度**: ⭐⭐⭐⭐

---

## 🎯 学习目标

1. ✅ 理解 RAG 在多智能体系统中的作用
2. ✅ 掌握知识共享机制的设计
3. ✅ 理解分布式检索的策略
4. ✅ 能够实现多智能体 RAG 系统

---

## 📚 核心概念

### 什么是 RAG？

**RAG (Retrieval-Augmented Generation)** = 检索增强生成

**核心思想**: 在生成回答前，先从知识库中检索相关信息，然后基于检索到的内容生成回答。

**类比**:
- 没有 RAG = 闭卷考试（只靠记忆回答）
- 有 RAG = 开卷考试（可以查阅资料后回答）

---

## 🔍 为什么多智能体系统需要 RAG？

### 问题 1: 知识过时

LLM 的训练数据有截止日期，无法回答新发生的事情。

**解决方案**: 通过 RAG 实时检索最新信息。

### 问题 2: 专业领域知识不足

通用 LLM 在某些专业领域（如医疗、法律）知识不够深入。

**解决方案**: 集成专业知识库。

### 问题 3: 多 Agent 需要共享知识

不同 Agent 可能需要访问相同的知识。

**解决方案**: 共享知识库。

---

## 🏗️ 多智能体 RAG 架构

### 架构 1: 集中式 RAG

```
         ┌─────────────┐
         │ Shared RAG  │
         │   System    │
         └──────┬──────┘
                ↑
      ┌─────────┼─────────┐
      |         |         |
   Agent1   Agent2    Agent3
```

**特点**:
- 所有 Agent 共享一个 RAG 系统
- 统一的知识库和检索策略

**优势**:
- 知识一致性
- 资源利用率高
- 易于维护

**劣势**:
- 可能成为性能瓶颈
- 难以满足个性化需求

---

### 架构 2: 分布式 RAG

```
   ┌────────┐  ┌────────┐  ┌────────┐
   │ RAG-1  │  │ RAG-2  │  │ RAG-3  │
   └───┬────┘  └───┬────┘  └───┬────┘
       │           │           │
   Agent1      Agent2      Agent3
       └───────────┼───────────┘
                   ↓
              ┌────────┐
              │  Sync  │
              └────────┘
```

**特点**:
- 每个 Agent 有自己的 RAG 系统
- 需要同步机制保持一致性

**优势**:
- 高性能（并行检索）
- 支持个性化
- 容错性好

**劣势**:
- 知识同步复杂
- 资源消耗大
- 维护成本高

---

### 架构 3: 混合式 RAG

```
         ┌─────────────┐
         │ Shared Base │
         │  Knowledge  │
         └──────┬──────┘
                ↑
      ┌─────────┼─────────┐
      |         |         |
   ┌───┴───┐ ┌─┴───┐ ┌──┴───┐
   │Local  │ │Local│ │Local│
   │Cache  │ │Cache│ │Cache│
   └───┬───┘ └──┬──┘ └──┬───┘
       │        |       |
   Agent1  Agent2  Agent3
```

**特点**:
- 共享基础知识库
- 每个 Agent 有本地缓存

**优势**:
- 平衡性能和一致性
- 支持个性化缓存
- 资源利用率高

**劣势**:
- 实现复杂
- 需要缓存策略

---

## 🔧 实现示例

### 示例 1: 集中式 RAG

```python
from typing import List, Dict, Any
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

class SharedRAG:
    """共享的 RAG 系统"""

    def __init__(self, knowledge_base_path: str):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            persist_directory=knowledge_base_path,
            embedding_function=self.embeddings
        )
        self.llm = OpenAI(temperature=0)

    def query(self, question: str, top_k: int = 3) -> str:
        """查询知识库"""
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        return qa_chain.run(question)

# 创建共享 RAG 系统
shared_rag = SharedRAG("./knowledge_base")

# 多个 Agent 共享同一个 RAG
class Agent:
    def __init__(self, name: str, rag: SharedRAG):
        self.name = name
        self.rag = rag

    def ask(self, question: str) -> str:
        """使用共享 RAG 回答问题"""
        answer = self.rag.query(question)
        return f"[{self.name}] {answer}"

# 创建多个 Agent
agent1 = Agent("研究者", shared_rag)
agent2 = Agent("分析师", shared_rag)
agent3 = Agent("顾问", shared_rag)

# 所有 Agent 共享知识库
print(agent1.ask("什么是 LangChain？"))
print(agent2.ask("什么是 LangGraph？"))
print(agent3.ask("什么是 AutoGen？"))
```

---

### 示例 2: 分布式 RAG

```python
from typing import List, Dict, Any
import threading

class LocalRAG:
    """本地 RAG 系统"""

    def __init__(self, knowledge_base_path: str):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            persist_directory=knowledge_base_path,
            embedding_function=self.embeddings
        )
        self.llm = OpenAI(temperature=0)
        self.local_cache = {}

    def query(self, question: str, use_cache: bool = True) -> str:
        """查询知识库"""
        # 检查缓存
        if use_cache and question in self.local_cache:
            return self.local_cache[question]

        # 检索知识库
        retriever = self.vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever
        )
        answer = qa_chain.run(question)

        # 更新缓存
        if use_cache:
            self.local_cache[question] = answer

        return answer

class KnowledgeSync:
    """知识同步器"""

    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.lock = threading.Lock()

    def sync(self, new_knowledge: str):
        """同步新知识到所有 Agent"""
        with self.lock:
            for agent in self.agents:
                agent.rag.add_knowledge(new_knowledge)

# 创建多个 Agent，每个有自己的 RAG
agent1 = Agent("研究者", LocalRAG("./kb_research"))
agent2 = Agent("分析师", LocalRAG("./kb_analysis"))
agent3 = Agent("顾问", LocalRAG("./kb_consulting"))

# 创建同步器
sync = KnowledgeSync([agent1, agent2, agent3])

# 同步新知识
sync.sync("LangGraph 是一个用于构建有状态的、多参与者的应用程序的库")
```

---

## 📊 3 种架构对比

| 特性 | 集中式 | 分布式 | 混合式 |
|------|--------|--------|--------|
| **性能** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **一致性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **可扩展性** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **资源消耗** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **实现复杂度** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **适用场景** | 小规模系统 | 大规模系统 | 通用场景 |

---

## 💡 实践建议

### 如何选择 RAG 架构？

#### 决策树

```
开始
  ↓
Agent 数量 > 10？
  ├─ 是 → Agent 是否需要个性化知识？
  │      ├─ 是 → 分布式 RAG
  │      └─ 否 → 混合式 RAG
  └─ 否 → 集中式 RAG
```

### 设计原则

1. **知识一致性**
   - 确保所有 Agent 访问相同的基础知识
   - 设计合理的同步机制

2. **性能优化**
   - 使用缓存减少重复检索
   - 批量处理检索请求
   - 预加载常用知识

3. **可扩展性**
   - 支持动态添加知识
   - 支持知识版本管理
   - 支持知识更新和删除

---

## 🎓 费曼解释

### 给 5 岁孩子的解释

**多智能体 RAG 就像一个图书馆系统**：

1. **集中式 RAG** = 一个大图书馆，大家都在这里借书
2. **分布式 RAG** = 每个人有自己的小图书馆，定期交换新书
3. **混合式 RAG** = 有一个中心图书馆，每个人也可以存一些常用书在身边

### 关键要点

1. **RAG 让 Agent 能够访问最新、最专业的知识**
2. **选择合适的架构很重要**
3. **需要在性能和一致性之间找到平衡**

---

## 🔗 相关资源

- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [LangGraph RAG Patterns](https://langchain-ai.github.io/langgraph/use_cases/qA/)
- [Multi-Agent RAG](https://www.anthropic.com/index/building-effective-agents)

---

## ✅ 最小验证

### 任务

1. 实现一个简单的集中式 RAG 系统（30 分钟）
2. 创建 3 个 Agent 共享同一个 RAG 系统（10 分钟）
3. 测试 Agent 的问答能力（10 分钟）
4. 添加一个新知识到知识库，验证所有 Agent 都能访问（10 分钟）

### 期望输出

- [ ] 可运行的 RAG 系统代码
- [ ] 3 个 Agent 的问答示例
- [ ] 知识更新的验证结果

---

## 🚀 下一步

学习完本笔记后，继续学习：
- `notes/13_knowledge_sharing.md` - 深入了解知识共享机制
- `examples/09_multiagent_rag.py` - 实现多智能体 RAG 系统

---

**记住：RAG 让多智能体系统变得更强大，能够访问和共享知识！** 📚
