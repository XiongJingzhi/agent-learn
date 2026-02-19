# 记忆检索策略

> **目标**: 掌握如何高效地从记忆系统中检索信息
> **预计时间**: 45 分钟
> **难度**: ⭐⭐⭐⭐

---

## 为什么需要检索策略？

随着记忆的增长，如何快速找到相关信息成为关键问题：

**问题 1：信息过载**
- 记忆太多，找不到需要的信息
- 需要高效的检索方法

**问题 2：语义理解**
- 关键词匹配不够准确
- 需要语义相似度搜索

**问题 3：时效性**
- 有些信息有时效性
- 需要考虑时间因素

---

## 检索策略分类

### 策略 1：精确匹配

根据 ID 或关键字精确匹配。

```python
class ExactMatchRetriever:
    """精确匹配检索器"""

    def __init__(self, memory_system):
        self.memory = memory_system

    def retrieve_by_id(self, memory_id: str):
        """根据 ID 检索"""
        return self.memory.long_term.get_memory(memory_id)

    def retrieve_by_keyword(self, keyword: str) -> list:
        """根据关键词检索"""
        return self.memory.long_term.search_by_keyword(keyword)

    def retrieve_by_metadata(self, key: str, value: any) -> list:
        """根据元数据检索"""
        return self.memory.long_term.search_by_metadata(key, value)
```

---

### 策略 2：相似度搜索

使用向量相似度进行语义搜索。

```python
import numpy as np
from typing import List, Dict, Any, Optional

class VectorRetriever:
    """向量检索器"""

    def __init__(self, memory_system, embedding_model=None):
        self.memory = memory_system
        self.embedding_model = embedding_model

    def retrieve_similar(self,
                        query: str,
                        top_k: int = 5,
                        threshold: float = 0.7) -> List[Dict[str, Any]]:
        """检索相似的记忆"""
        # 生成查询向量
        query_embedding = self._get_embedding(query)

        # 计算相似度
        results = []
        for memory_id, memory in self.memory.long_term.memories.items():
            if memory.embedding is None:
                continue

            similarity = self._cosine_similarity(query_embedding, memory.embedding)

            if similarity >= threshold:
                results.append({
                    "memory_id": memory_id,
                    "memory": memory,
                    "similarity": similarity
                })

        # 按相似度排序
        results.sort(key=lambda x: x["similarity"], reverse=True)

        return results[:top_k]

    def _get_embedding(self, text: str) -> List[float]:
        """获取文本的向量表示"""
        if self.embedding_model:
            return self.embedding_model.encode(text)
        else:
            # 简化：使用词频统计（实际应使用真正的 embedding）
            return self._simple_embedding(text)

    def _simple_embedding(self, text: str) -> List[float]:
        """简化的向量表示（仅用于示例）"""
        # 实际应用中应该使用真实的 embedding 模型
        words = text.lower().split()
        vocab = set(words)

        # 创建简单的词频向量
        embedding = np.zeros(100)  # 假设 100 维
        for i, word in enumerate(words):
            idx = hash(word) % 100
            embedding[idx] += 1

        # 归一化
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding.tolist()

    def _cosine_similarity(self,
                          vec1: List[float],
                          vec2: List[float]) -> float:
        """计算余弦相似度"""
        arr1 = np.array(vec1)
        arr2 = np.array(vec2)

        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
```

---

### 策略 3：混合检索

结合多种检索策略。

```python
class HybridRetriever:
    """混合检索器"""

    def __init__(self, memory_system):
        self.memory = memory_system
        self.exact_retriever = ExactMatchRetriever(memory_system)
        self.vector_retriever = VectorRetriever(memory_system)

    def retrieve(self,
                query: str,
                strategy: str = "auto",
                top_k: int = 5) -> List[Dict[str, Any]]:
        """混合检索"""
        if strategy == "exact":
            return self._exact_search(query, top_k)
        elif strategy == "vector":
            return self._vector_search(query, top_k)
        elif strategy == "hybrid":
            return self._hybrid_search(query, top_k)
        elif strategy == "auto":
            return self._auto_search(query, top_k)
        else:
            raise ValueError(f"未知策略: {strategy}")

    def _exact_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """精确搜索"""
        results = self.exact_retriever.retrieve_by_keyword(query)
        return [
            {"memory_id": m.memory_id, "memory": m, "score": 1.0}
            for m in results[:top_k]
        ]

    def _vector_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """向量搜索"""
        return self.vector_retriever.retrieve_similar(query, top_k=top_k)

    def _hybrid_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """混合搜索：结合精确和向量搜索"""
        # 获取精确匹配结果
        exact_results = self._exact_search(query, top_k)

        # 获取向量搜索结果
        vector_results = self._vector_search(query, top_k)

        # 合并去重
        combined = {}
        for result in exact_results + vector_results:
            memory_id = result["memory_id"]
            if memory_id in combined:
                # 取最高分
                if result["score"] > combined[memory_id]["score"]:
                    combined[memory_id] = result
            else:
                combined[memory_id] = result

        # 排序并返回
        results = list(combined.values())
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]

    def _auto_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """自动选择最佳搜索策略"""
        # 如果查询很短（< 5 个词），使用精确搜索
        if len(query.split()) < 5:
            return self._exact_search(query, top_k)

        # 否则使用混合搜索
        return self._hybrid_search(query, top_k)
```

---

## 时间衰减检索

考虑信息的新鲜度。

```python
from datetime import datetime, timedelta

class TimeDecayRetriever:
    """时间衰减检索器"""

    def __init__(self, memory_system):
        self.memory = memory_system
        self.decay_rate = 0.1  # 衰减率：每天衰减 10%

    def retrieve_with_decay(self,
                           query: str,
                           top_k: int = 5) -> List[Dict[str, Any]]:
        """带时间衰减的检索"""
        # 先进行基础检索
        retriever = HybridRetriever(self.memory)
        base_results = retriever.retrieve(query, strategy="hybrid", top_k=20)

        # 应用时间衰减
        now = datetime.now()
        for result in base_results:
            memory = result["memory"]
            days_old = (now - memory.timestamp).days

            # 计算衰减系数
            decay_factor = np.exp(-self.decay_rate * days_old)

            # 调整分数
            result["decay_score"] = result["score"] * decay_factor

        # 按衰减后的分数排序
        base_results.sort(key=lambda x: x["decay_score"], reverse=True)

        return base_results[:top_k]
```

---

## 上下文感知检索

根据当前上下文调整检索策略。

```python
class ContextAwareRetriever:
    """上下文感知检索器"""

    def __init__(self, memory_system):
        self.memory = memory_system
        self.base_retriever = HybridRetriever(memory_system)

    def retrieve(self,
                query: str,
                context: Dict[str, Any] = None,
                top_k: int = 5) -> List[Dict[str, Any]]:
        """上下文感知检索"""
        # 基础检索
        results = self.base_retriever.retrieve(query, top_k=20)

        if context:
            # 根据上下文调整排序
            results = self._rerank_by_context(results, context)

        return results[:top_k]

    def _rerank_by_context(self,
                          results: List[Dict[str, Any]],
                          context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """根据上下文重新排序"""
        user_id = context.get("user_id")
        session_id = context.get("session_id")
        current_task = context.get("current_task")

        for result in results:
            memory = result["memory"]
            metadata = memory.metadata

            # 如果是同一用户的记忆，加权
            if user_id and metadata.get("user_id") == user_id:
                result["context_score"] = result["score"] * 1.5
            else:
                result["context_score"] = result["score"]

            # 如果是同一会话的记忆，进一步加权
            if session_id and metadata.get("session_id") == session_id:
                result["context_score"] *= 1.3

            # 如果与当前任务相关，加权
            if current_task and current_task in memory.content:
                result["context_score"] *= 1.2

        # 按上下文分数排序
        results.sort(key=lambda x: x.get("context_score", x["score"]), reverse=True)

        return results
```

---

## 完整示例：智能检索系统

```python
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np

class IntelligentRetrievalSystem:
    """智能检索系统"""

    def __init__(self, memory_system):
        self.memory = memory_system

        # 组合多种检索器
        self.exact_retriever = ExactMatchRetriever(memory_system)
        self.vector_retriever = VectorRetriever(memory_system)
        self.hybrid_retriever = HybridRetriever(memory_system)
        self.time_decay_retriever = TimeDecayRetriever(memory_system)
        self.context_retriever = ContextAwareRetriever(memory_system)

    def retrieve(self,
                query: str,
                strategy: str = "intelligent",
                context: Dict[str, Any] = None,
                top_k: int = 5) -> List[Dict[str, Any]]:
        """智能检索"""

        if strategy == "exact":
            return self.exact_retriever.retrieve_by_keyword(query)[:top_k]

        elif strategy == "vector":
            return self.vector_retriever.retrieve_similar(query, top_k)

        elif strategy == "hybrid":
            return self.hybrid_retriever.retrieve(query, "hybrid", top_k)

        elif strategy == "time_decay":
            return self.time_decay_retriever.retrieve_with_decay(query, top_k)

        elif strategy == "context_aware":
            return self.context_retriever.retrieve(query, context, top_k)

        elif strategy == "intelligent":
            return self._intelligent_retrieve(query, context, top_k)

        else:
            raise ValueError(f"未知策略: {strategy}")

    def _intelligent_retrieve(self,
                             query: str,
                             context: Dict[str, Any],
                             top_k: int) -> List[Dict[str, Any]]:
        """智能检索：自动选择最佳策略"""

        # 1. 分析查询特征
        query_features = self._analyze_query(query)

        # 2. 选择最佳策略
        if query_features["is_short"] and query_features["has_entity"]:
            # 短查询且有实体，使用精确匹配
            results = self.exact_retriever.retrieve_by_keyword(query)
        elif query_features["is_question"]:
            # 问题类型，使用向量搜索
            results = self.vector_retriever.retrieve_similar(query, top_k=20)
        elif context:
            # 有上下文，使用上下文感知检索
            results = self.context_retriever.retrieve(query, context, top_k=20)
        else:
            # 默认使用混合检索
            results = self.hybrid_retriever.retrieve(query, "hybrid", top_k=20)

        # 3. 应用时间衰减
        if query_features["needs_fresh_info"]:
            for result in results:
                memory = result["memory"]
                days_old = (datetime.now() - memory.timestamp).days
                decay = np.exp(-0.1 * days_old)
                result["final_score"] = result["score"] * decay
        else:
            for result in results:
                result["final_score"] = result.get("score", 0)

        # 4. 排序并返回
        results.sort(key=lambda x: x["final_score"], reverse=True)

        return results[:top_k]

    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """分析查询特征"""
        words = query.split()

        return {
            "is_short": len(words) < 5,
            "has_entity": any(word[0].isupper() for word in words),
            "is_question": query.strip().endswith("?"),
            "needs_fresh_info": any(word in query for word in ["最近", "latest", "new", "当前"])
        }

    def explain_retrieval(self,
                         query: str,
                         results: List[Dict[str, Any]]) -> str:
        """解释检索结果"""
        explanation = f"查询: {query}\n"
        explanation += f"找到 {len(results)} 条结果\n\n"

        for i, result in enumerate(results, 1):
            memory = result["memory"]
            score = result.get("final_score", result.get("score", 0))

            explanation += f"{i}. [{memory.memory_id}]\n"
            explanation += f"   内容: {memory.content[:100]}...\n"
            explanation += f"   分数: {score:.3f}\n"
            explanation += f"   时间: {memory.timestamp.strftime('%Y-%m-%d %H:%M')}\n\n"

        return explanation


# 运行示例
def main():
    print("=" * 70)
    print("智能检索系统示例")
    print("=" * 70)

    # 假设已有记忆系统
    class MockMemorySystem:
        def __init__(self):
            from types import SimpleType
            self.long_term = SimpleType()
            self.long_term.memories = {}

    memory_system = MockMemorySystem()

    # 创建检索系统
    retrieval_system = IntelligentRetrievalSystem(memory_system)

    # 示例查询
    queries = [
        "Python 编程",  # 短查询
        "如何使用 LangGraph 构建多智能体系统？",  # 问题
        "用户张三的偏好",  # 实体查询
    ]

    for query in queries:
        print(f"\n[查询] {query}")
        results = retrieval_system.retrieve(
            query,
            strategy="intelligent",
            top_k=3
        )

        print(retrieval_system.explain_retrieval(query, results))


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：检索准确度

**问题**：如何提高检索准确度？

**方案**：
- 使用高质量的 embedding 模型
- 结合多种检索策略
- 根据用户反馈优化排序

---

### 考虑 2：检索效率

**问题**：如何提高检索速度？

**方案**：
- 建立索引（关键词索引、向量索引）
- 使用近似最近邻搜索（如 FAISS）
- 缓存热门查询结果

---

### 考虑 3：个性化

**问题**：如何实现个性化检索？

**方案**：
- 考虑用户历史偏好
- 考虑当前会话上下文
- 学习用户反馈

---

## 最小验证

- [ ] 能够实现至少一种检索策略
- [ ] 能够实现混合检索
- [ ] 能够实现时间衰减
- [ ] 能够解释检索结果

---

## 下一步

- 📖 进入下一部分：推理机制对比
- 🧪 `examples/10_retrieval_system.py` - 检索系统示例

---

**记住：检索策略决定了记忆系统的实用性，就像图书馆的索引系统！** 🔍
