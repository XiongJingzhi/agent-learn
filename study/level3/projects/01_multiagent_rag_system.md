# 01. 多智能体 RAG 系统 - Capstone 项目

> **难度**: ⭐⭐⭐⭐
> **预计时间**: 10-12 小时
> **类型**: 综合项目

---

## 🎯 项目目标

设计和实现一个**多智能体 RAG 问答系统**，该系统具有以下特点：

1. **多 Agent 协作**: 使用层次化架构，包含 Manager 和多个专业 Agent
2. **RAG 集成**: 所有 Agent 共享一个知识库
3. **智能路由**: Manager 根据问题类型路由到合适的 Agent
4. **结果汇总**: Manager 汇总多个 Agent 的结果，生成最终答案

---

## 📋 项目需求

### 功能需求

#### FR1: 知识库管理

- [ ] 支持添加文档到知识库
- [ ] 支持文档向量化
- [ ] 支持相似度检索
- [ ] 支持知识库更新

#### FR2: 多 Agent 架构

- [ ] 1 个 Manager Agent（任务协调）
- [ ] 3 个专业 Agent（研究者、分析者、写作者）
- [ ] 支持动态任务分配
- [ ] 支持结果汇总

#### FR3: 智能问答

- [ ] 接收用户问题
- [ ] 从知识库检索相关文档
- [ ] Agent 基于检索结果生成回答
- [ ] 汇总多个 Agent 的见解

#### FR4: 测试和验证

- [ ] 单元测试（每个组件）
- [ ] 集成测试（完整流程）
- [ ] 性能测试（响应时间）
- [ ] 质量评估（答案准确性）

---

### 非功能需求

#### NFR1: 性能

- [ ] 单个问题的响应时间 < 5 秒
- [ ] 支持并发处理 3 个问题
- [ ] 知识库检索时间 < 1 秒

#### NFR2: 可扩展性

- [ ] 支持添加新的专业 Agent
- [ ] 支持知识库扩展（100+ 文档）
- [ ] 支持不同的检索策略

#### NFR3: 可维护性

- [ ] 代码有类型提示
- [ ] 代码有文档字符串
- [ ] 测试覆盖率 >= 70%
- [ ] 有使用示例

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      User Interface                      │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    Manager Agent                         │
│  - 任务分析                                              │
│  - Agent 选择                                            │
│  - 结果汇总                                              │
└─────┬─────────┬─────────┬───────────────────────────────┘
      ↓         ↓         ↓
┌──────────┐ ┌──────────┐ ┌──────────┐
│Researcher│ │ Analyst  │ │  Writer  │
│  Agent   │ │  Agent   │ │  Agent   │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┴────────────┘
                  ↓
        ┌─────────────────┐
        │ Shared RAG System│
        │  - Vector Store  │
        │  - Retriever     │
        │  - LLM           │
        └─────────────────┘
```

---

## 📝 实现步骤

### Phase 1: 知识库实现（2-3 小时）

#### 1.1 创建向量存储

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class KnowledgeBase:
    def __init__(self, persist_directory: str = "./kb"):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents: List[str]):
        """添加文档到知识库"""
        # 加载文档
        loaders = [TextLoader(doc) for doc in documents]
        docs = []
        for loader in loaders:
            docs.extend(loader.load())

        # 分割文档
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        # 添加到向量存储
        self.vectorstore.add_documents(splits)

    def search(self, query: str, k: int = 3) -> List[str]:
        """搜索相关文档"""
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
```

#### 1.2 实现 RAG 查询

```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

class RAGSystem:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.llm = OpenAI(temperature=0)

    def query(self, question: str) -> str:
        """使用 RAG 回答问题"""
        retriever = self.kb.vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        return qa_chain.run(question)
```

**验证**:
- [ ] 能够添加文档到知识库
- [ ] 能够检索相关文档
- [ ] 能够基于检索结果回答问题

---

### Phase 2: Agent 实现（3-4 小时）

#### 2.1 实现 Manager Agent

```python
from typing import List, Dict, Any

class ManagerAgent:
    def __init__(self, agents: Dict[str, 'BaseAgent']):
        self.agents = agents
        self.rag = RAGSystem(knowledge_base)

    def analyze_question(self, question: str) -> str:
        """分析问题类型"""
        # 简化的分类逻辑
        if "是什么" in question or "定义" in question:
            return "research"
        elif "为什么" in question or "分析" in question:
            return "analysis"
        elif "写" in question or "总结" in question:
            return "writing"
        else:
            return "general"

    def route_to_agent(self, question: str, question_type: str) -> str:
        """路由问题到合适的 Agent"""
        if question_type == "research":
            agent = self.agents["researcher"]
        elif question_type == "analysis":
            agent = self.agents["analyst"]
        elif question_type == "writing":
            agent = self.agents["writer"]
        else:
            # 通用问题，使用所有 Agent
            return self.multi_agent_query(question)

        return agent.query(question, self.rag)

    def multi_agent_query(self, question: str) -> str:
        """多 Agent 查询"""
        results = {}
        for name, agent in self.agents.items():
            results[name] = agent.query(question, self.rag)

        # 汇总结果
        return self.aggregate_results(results)

    def aggregate_results(self, results: Dict[str, str]) -> str:
        """汇总多个 Agent 的结果"""
        summary = "## 综合分析\n\n"
        for name, result in results.items():
            summary += f"### {name.capitalize()} 的见解\n{result}\n\n"
        return summary

    def ask(self, question: str) -> str:
        """处理用户问题"""
        # 1. 分析问题
        question_type = self.analyze_question(question)

        # 2. 路由到 Agent
        answer = self.route_to_agent(question, question_type)

        return answer
```

#### 2.2 实现专业 Agent

```python
class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def query(self, question: str, rag: RAGSystem) -> str:
        """查询问题"""
        # 从知识库检索相关文档
        context = rag.kb.search(question)

        # 基于角色生成回答
        prompt = self._build_prompt(question, context)
        answer = rag.llm.predict(prompt)

        return answer

    def _build_prompt(self, question: str, context: List[str]) -> str:
        """构建提示词"""
        base_prompt = f"""你是一个{self.role}。

问题：{question}

参考信息：
{chr(10).join(context)}

请基于你的角色和参考信息，提供专业的见解。"""

        return base_prompt


class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("研究员", "研究员，负责收集和整理信息")


class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__("分析师", "分析师，负责深入分析和解释")


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("写作者", "写作者，负责撰写和总结内容")
```

**验证**:
- [ ] Manager 能够分析问题类型
- [ ] Manager 能够路由问题到合适的 Agent
- [ ] 每个 Agent 能够基于 RAG 生成回答
- [ ] Manager 能够汇总多个 Agent 的结果

---

### Phase 3: 系统集成（2-3 小时）

#### 3.1 创建完整系统

```python
class MultiAgentRAGSystem:
    def __init__(self):
        # 创建知识库
        self.kb = KnowledgeBase()

        # 创建 RAG 系统
        self.rag = RAGSystem(self.kb)

        # 创建 Agents
        agents = {
            "researcher": ResearcherAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent()
        }

        # 创建 Manager
        self.manager = ManagerAgent(agents)

    def initialize(self, documents: List[str]):
        """初始化系统"""
        print("正在初始化知识库...")
        self.kb.add_documents(documents)
        print("知识库初始化完成！")

    def ask(self, question: str) -> str:
        """提问"""
        print(f"\n问题: {question}")
        answer = self.manager.ask(question)
        return answer

    def interactive_mode(self):
        """交互模式"""
        print("\n=== 多智能体 RAG 问答系统 ===")
        print("输入 'quit' 退出\n")

        while True:
            question = input("请输入问题: ")
            if question.lower() == 'quit':
                break

            answer = self.ask(question)
            print(f"\n回答:\n{answer}\n")
```

**验证**:
- [ ] 系统能够正确初始化
- [ ] 交互模式正常工作
- [ ] 能够处理各种类型的问题

---

### Phase 4: 测试和优化（2-3 小时）

#### 4.1 单元测试

```python
import pytest

def test_knowledge_base():
    """测试知识库"""
    kb = KnowledgeBase()
    kb.add_documents(["test.txt"])

    results = kb.search("测试")
    assert len(results) > 0

def test_manager():
    """测试 Manager"""
    agents = {
        "researcher": ResearcherAgent(),
        "analyst": AnalystAgent(),
        "writer": WriterAgent()
    }
    manager = ManagerAgent(agents)

    question_type = manager.analyze_question("什么是 Agent？")
    assert question_type == "research"

def test_system():
    """测试完整系统"""
    system = MultiAgentRAGSystem()
    system.initialize(["doc1.txt", "doc2.txt"])

    answer = system.ask("什么是 Agent？")
    assert answer is not None
    assert len(answer) > 0
```

#### 4.2 性能测试

```python
import time

def test_performance():
    """测试性能"""
    system = MultiAgentRAGSystem()
    system.initialize(["doc1.txt"])

    # 测试响应时间
    start = time.time()
    answer = system.ask("测试问题")
    end = time.time()

    response_time = end - start
    assert response_time < 5.0  # 响应时间 < 5 秒
```

**验证**:
- [ ] 所有单元测试通过
- [ ] 性能测试满足要求
- [ ] 测试覆盖率 >= 70%

---

## 📊 验收标准

### 必须完成（P0）

- [ ] 完整实现 Manager-Agent 架构
- [ ] 集成 RAG 系统
- [ ] 能够回答用户问题
- [ ] 有完整的测试套件
- [ ] 代码有文档和类型提示

### 应该完成（P1）

- [ ] 支持多种问题类型
- [ ] 能够汇总多个 Agent 的结果
- [ ] 性能满足要求（< 5 秒）
- [ ] 有使用示例和文档

### 可以完成（P2）

- [ ] 支持流式输出
- [ ] 支持多轮对话
- [ ] 有 Web UI
- [ ] 支持并发查询

---

## 🎁 额外挑战

完成基础功能后，可以尝试以下挑战：

1. **动态 Agent 创建**: 根据问题动态创建专门的 Agent
2. **Agent 通信**: 允许 Agent 之间直接通信和协作
3. **知识图谱**: 使用知识图谱增强 RAG
4. **多模态**: 支持图片、视频等多模态检索
5. **个性化**: 根据用户历史个性化回答

---

## 📝 交付物

### 代码

- [ ] 完整的系统代码（`multiagent_rag.py`）
- [ ] 测试代码（`test_multiagent_rag.py`）
- [ ] 使用示例（`example.py`）

### 文档

- [ ] README（系统介绍和使用说明）
- [ ] 设计文档（架构设计和技术选型）
- [ ] API 文档（接口说明）

### 其他

- [ ] 性能测试报告
- [ ] 质量评估报告
- [ ] 使用演示视频（可选）

---

## ✅ 自检清单

提交项目前，检查以下内容：

### 功能完整性

- [ ] 所有 P0 功能都已实现
- [ ] 核心功能正常工作
- [ ] 边界情况得到处理

### 代码质量

- [ ] 代码符合 PEP 8 规范
- [ ] 有类型提示
- [ ] 有文档字符串
- [ ] 有错误处理

### 测试覆盖

- [ ] 单元测试 >= 70%
- [ ] 集成测试覆盖主要流程
- [ ] 性能测试通过

### 文档完整

- [ ] README 清晰
- [ ] 使用示例可运行
- [ ] API 文档完整

---

## 🚀 开始开发

1. 创建项目目录
2. 设置虚拟环境
3. 安装依赖
4. 按照 Phase 顺序实现
5. 每个完成后进行验证
6. 最终集成和测试

---

**祝你顺利完成这个多智能体 RAG 系统项目！** 🎉
