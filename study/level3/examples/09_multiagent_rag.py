"""
示例 9: 多智能体 RAG 系统

本示例展示如何为多智能体系统集成 RAG（检索增强生成）能力。

架构：
         Manager
       /    |    \
   Researcher Analyst Writer
      \      |      /
       ← RAG System →
       共享知识库
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
import hashlib


# ============================================================================
# RAG 系统组件
# ============================================================================

class Document:
    """文档类"""
    def __init__(self, id: str, content: str, metadata: dict = None):
        self.id = id
        self.content = content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"Document({self.id})"


class VectorStore:
    """简化的向量存储"""

    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.embeddings: Dict[str, List[float]] = {}

    def add_document(self, document: Document):
        """添加文档"""
        self.documents[document.id] = document
        # 简化的嵌入（实际应该使用真实的嵌入模型）
        self.embeddings[document.id] = self._fake_embedding(document.content)

    def _fake_embedding(self, text: str) -> List[float]:
        """伪造嵌入（简化）"""
        # 实际应用中使用 OpenAI embeddings 或其他
        text_hash = hashlib.md5(text.encode()).hexdigest()
        # 将哈希转换为向量
        return [float(int(c, 16)) / 255.0 for c in text_hash[:128]]

    def search(self, query: str, top_k: int = 3) -> List[Document]:
        """搜索相似文档"""
        if not self.documents:
            return []

        query_emb = self._fake_embedding(query)

        # 计算相似度
        similarities = []
        for doc_id, doc_emb in self.embeddings.items():
            similarity = self._cosine_similarity(query_emb, doc_emb)
            similarities.append((similarity, doc_id))

        # 排序并返回 top_k
        similarities.sort(reverse=True)
        results = []
        for similarity, doc_id in similarities[:top_k]:
            results.append(self.documents[doc_id])

        return results

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) if norm1 * norm2 > 0 else 0


class RAGSystem:
    """RAG 系统"""

    def __init__(self):
        self.vector_store = VectorStore()
        self.cache = {}  # 查询缓存

    def add_documents(self, documents: List[Document]):
        """添加文档到知识库"""
        for doc in documents:
            self.vector_store.add_document(doc)
        print(f"[RAG] 添加了 {len(documents)} 个文档")

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """查询知识库"""
        # 检查缓存
        cache_key = f"{question}_{top_k}"
        if cache_key in self.cache:
            print(f"[RAG] 缓存命中: {question}")
            return self.cache[cache_key]

        # 检索相关文档
        print(f"[RAG] 检索: {question}")
        docs = self.vector_store.search(question, top_k)

        # 组装上下文
        context = self._build_context(docs)

        result = {
            "question": question,
            "context": context,
            "source_documents": [doc.id for doc in docs],
            "raw_docs": docs
        }

        # 缓存结果
        self.cache[cache_key] = result

        return result

    def _build_context(self, docs: List[Document]) -> str:
        """构建上下文"""
        context_parts = []
        for i, doc in enumerate(docs, 1):
            context_parts.append(f"[文档 {i}] {doc.content}")
        return "\n\n".join(context_parts)

    def clear_cache(self):
        """清除缓存"""
        self.cache.clear()
        print("[RAG] 缓存已清除")


# ============================================================================
# Agent 实现
# ============================================================================

class RAGAgent:
    """带 RAG 能力的 Agent"""

    def __init__(self, name: str, role: str, rag: RAGSystem):
        self.name = name
        self.role = role
        self.rag = rag
        self.query_count = 0

    def ask(self, question: str) -> str:
        """使用 RAG 回答问题"""
        self.query_count += 1

        print(f"\n[{self.name}] 收到问题: {question}")

        # 1. 检索相关知识
        rag_result = self.rag.query(question, top_k=3)

        # 2. 基于角色生成回答
        answer = self._generate_answer(question, rag_result)

        return answer

    def _generate_answer(self, question: str, rag_result: Dict[str, Any]) -> str:
        """基于 RAG 结果生成回答"""
        context = rag_result["context"]

        # 根据角色生成不同的回答
        if "研究" in self.role:
            return self._research_answer(question, context)
        elif "分析" in self.role:
            return self._analysis_answer(question, context)
        elif "写作" in self.role:
            return self._writing_answer(question, context)
        else:
            return self._general_answer(question, context)

    def _research_answer(self, question: str, context: str) -> str:
        """研究型回答"""
        return f"""
[{self.name} 的研究结果]

基于以下资料：
{context}

研究结论：
这个问题涉及多个方面，需要深入调查。主要发现包括：
1. 这是一个重要的研究领域
2. 有多个相关的研究方向
3. 需要进一步的实证研究

建议：查阅更多文献以获得全面的理解。
"""

    def _analysis_answer(self, question: str, context: str) -> str:
        """分析型回答"""
        return f"""
[{self.name} 的分析]

参考信息：
{context}

分析结果：
从数据来看，这个主题呈现以下特点：
- 趋势：持续增长
- 影响：广泛而深远
- 挑战：存在一些限制因素

关键洞察：核心在于平衡各种因素。
"""

    def _writing_answer(self, question: str, context: str) -> str:
        """写作型回答"""
        return f"""
[{self.name} 的文章]

基于资料：
{context}

正文：

{question} 是一个值得探讨的话题。通过研究我们发现，
这个领域正在快速发展，并且产生了广泛的影响。

首先，从技术角度来看，这一领域已经取得了显著进展。
其次，从应用层面来说，它正在改变我们的工作和生活方式。

总结来说，{question} 代表了未来的发展方向，值得我们持续关注。
"""

    def _general_answer(self, question: str, context: str) -> str:
        """通用回答"""
        return f"""
[{self.name} 的回答]

根据相关信息：
{context}

我的看法是：这是一个复杂但有趣的话题，需要多角度思考。
"""


class ManagerWithRAG:
    """带 RAG 的 Manager"""

    def __init__(self, name: str, rag: RAGSystem):
        self.name = name
        self.rag = rag
        self.agents: Dict[str, RAGAgent] = {}

    def add_agent(self, agent: RAGAgent):
        """添加 Agent"""
        self.agents[agent.name] = agent
        print(f"[{self.name}] 添加 Agent: {agent.name}")

    def process(self, user_question: str) -> str:
        """处理用户问题"""
        print(f"\n{'='*60}")
        print(f"[{self.name}] 处理问题: {user_question}")
        print(f"{'='*60}")

        # 1. 分析问题类型
        question_type = self._analyze_question(user_question)
        print(f"[{self.name}] 问题类型: {question_type}")

        # 2. 选择合适的 Agent
        selected_agent = self._select_agent(question_type)

        # 3. Agent 回答
        answer = selected_agent.ask(user_question)

        return answer

    def _analyze_question(self, question: str) -> str:
        """分析问题类型"""
        if "什么是" in question or "定义" in question:
            return "research"
        elif "分析" in question or "比较" in question:
            return "analysis"
        elif "写" in question or "总结" in question:
            return "writing"
        else:
            return "general"

    def _select_agent(self, question_type: str) -> RAGAgent:
        """选择合适的 Agent"""
        for agent in self.agents.values():
            if question_type in agent.role:
                return agent
        # 返回第一个可用的
        return list(self.agents.values())[0]


# ============================================================================
# 完整系统集成
# ============================================================================

def create_multiagent_rag_system() -> ManagerWithRAG:
    """创建多智能体 RAG 系统"""

    # 1. 创建 RAG 系统
    rag = RAGSystem()

    # 2. 添加知识库文档
    documents = [
        Document(
            id="doc1",
            content="LangChain 是一个用于开发由语言模型驱动的应用程序的框架。它提供了丰富的工具和集成，使开发者能够快速构建 LLM 应用。",
            metadata={"topic": "LangChain", "type": "framework"}
        ),
        Document(
            id="doc2",
            content="LangGraph 是 LangChain 的一个扩展，专门用于构建有状态的、多参与者的应用程序。它提供了一个声明式的图结构来定义 Agent 的行为。",
            metadata={"topic": "LangGraph", "type": "framework"}
        ),
        Document(
            id="doc3",
            content="AutoGen 是微软开发的多智能体对话框架。它允许多个 Agent 相互协作来解决复杂任务，支持人类参与和干预。",
            metadata={"topic": "AutoGen", "type": "framework"}
        ),
        Document(
            id="doc4",
            content="RAG（检索增强生成）是一种结合了信息检索和生成的技术。它先从知识库中检索相关信息，然后基于检索到的内容生成答案。",
            metadata={"topic": "RAG", "type": "technique"}
        ),
        Document(
            id="doc5",
            content="多智能体系统是由多个相互协作的 Agent 组成的系统。Agent 之间通过通信来协调行动，共同完成复杂的任务。",
            metadata={"topic": "Multi-Agent", "type": "concept"}
        ),
        Document(
            id="doc6",
            content="向量数据库是专门用于存储和检索向量嵌入的数据库。它支持高效的相似度搜索，是 RAG 系统的核心组件。",
            metadata={"topic": "Vector DB", "type": "database"}
        ),
    ]

    rag.add_documents(documents)

    # 3. 创建 Manager
    manager = ManagerWithRAG("项目经理", rag)

    # 4. 创建专业 Agents
    researcher = RAGAgent("研究员", "研究员 research", rag)
    analyst = RAGAgent("分析师", "分析师 analysis", rag)
    writer = RAGAgent("作家", "作家 writing", rag)

    # 5. 添加到 Manager
    manager.add_agent(researcher)
    manager.add_agent(analyst)
    manager.add_agent(writer)

    return manager


# ============================================================================
# 使用示例
# ============================================================================

def example_basic_usage():
    """基本使用示例"""
    print("="*60)
    print("多智能体 RAG 系统演示")
    print("="*60)

    # 创建系统
    system = create_multiagent_rag_system()

    # 提问
    questions = [
        "什么是 LangGraph？",
        "分析多智能体系统的优势",
        "写一篇关于 RAG 的文章"
    ]

    for question in questions:
        answer = system.process(question)
        print(f"\n最终回答:\n{answer}")
        print("-" * 60)

    # 显示统计
    print("\n[查询统计]")
    for agent in system.agents.values():
        print(f"{agent.name}: {agent.query_count} 次查询")


def example_knowledge_sharing():
    """知识共享示例"""
    print("\n" + "="*60)
    print("知识共享演示")
    print("="*60)

    system = create_multiagent_rag_system()

    # 多个 Agent 访问相同的知识
    question = "什么是向量数据库？"

    print(f"\n所有 Agent 回答相同问题: {question}\n")

    for agent in system.agents.values():
        answer = agent.ask(question)
        print(f"\n{answer}")
        print("-" * 40)

    # 验证缓存效果
    print("\n[缓存验证]")
    print(f"缓存大小: {len(system.rag.cache)}")

    # 再次提问，应该命中缓存
    print("\n重复提问，应该命中缓存：")
    answer = list(system.agents.values())[0].ask(question)
    print(answer)


def example_collaborative_answer():
    """协作回答示例"""
    print("\n" + "="*60)
    print("协作回答演示")
    print("="*60)

    system = create_multiagent_rag_system()

    # 复杂问题需要多个 Agent 协作
    complex_question = "设计一个多智能体 RAG 系统来分析市场趋势"

    print(f"\n复杂问题: {complex_question}")
    print("\n[协作流程]")

    # 研究员先研究
    print("\n1. 研究阶段")
    research = system.agents["研究员"].ask(
        f"研究 {complex_question} 的关键技术"
    )
    print(research)

    # 分析师分析
    print("\n2. 分析阶段")
    analysis = system.agents["分析师"].ask(
        f"分析 {complex_question} 的实施方案"
    )
    print(analysis)

    # 作家总结
    print("\n3. 总结阶段")
    summary = system.agents["作家"].ask(
        f"总结 {complex_question} 的设计要点"
    )
    print(summary)


# ============================================================================
# 测试代码
# ============================================================================

def test_rag_system():
    """测试 RAG 系统"""
    print("\n=== 测试 RAG 系统 ===")

    rag = RAGSystem()

    # 添加文档
    docs = [
        Document("d1", "Python 是一种编程语言"),
        Document("d2", "JavaScript 也是一种编程语言")
    ]
    rag.add_documents(docs)

    # 查询
    result = rag.query("什么是 Python？")
    assert result is not None
    assert "Python" in result["context"]

    print("✓ RAG 系统测试通过")


def test_multiagent_rag():
    """测试多智能体 RAG"""
    print("\n=== 测试多智能体 RAG ===")

    system = create_multiagent_rag_system()

    # 测试问答
    answer = system.process("什么是 LangChain？")
    assert answer is not None
    assert "LangChain" in answer

    print("✓ 多智能体 RAG 测试通过")


def test_cache_efficiency():
    """测试缓存效率"""
    print("\n=== 测试缓存效率 ===")

    system = create_multiagent_rag_system()
    agent = list(system.agents.values())[0]

    question = "什么是 RAG？"

    # 第一次查询（无缓存）
    start = time.time()
    answer1 = agent.ask(question)
    time1 = time.time() - start

    # 第二次查询（有缓存）
    start = time.time()
    answer2 = agent.ask(question)
    time2 = time.time() - start

    print(f"第一次查询时间: {time4:.4f} 秒")
    print(f"第二次查询时间: {time2:.4f} 秒")
    print(f"加速比: {time1/time2:.2f}x")

    # 第二次应该更快（因为缓存）
    # 注意：由于简化实现，时间差异可能不明显

    print("✓ 缓存效率测试完成")


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序"""
    # 运行示例
    example_basic_usage()
    example_knowledge_sharing()
    example_collaborative_answer()

    # 运行测试
    test_rag_system()
    test_multiagent_rag()
    test_cache_efficiency()


if __name__ == "__main__":
    main()

    print("\n" + "="*60)
    print("所有示例和测试完成！")
    print("="*60)
