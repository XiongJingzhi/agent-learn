# Level 4 代码示例集（03-06）

## 03_hybrid_rag.py - 混合检索示例

```python
from typing import List

class HybridRetriever:
    """混合检索器"""

    def __init__(self, alpha=0.5):
        self.alpha = alpha  # 稠密检索权重

    def retrieve(self, query: str, docs: List[str], k: int = 5):
        """混合检索"""

        # 模拟稠密检索分数
        dense_scores = [0.8, 0.6, 0.4, 0.2, 0.1]

        # 模拟稀疏检索分数
        sparse_scores = [0.5, 0.7, 0.3, 0.9, 0.2]

        # 融合
        combined = [
            self.alpha * d + (1 - self.alpha) * s
            for d, s in zip(dense_scores, sparse_scores)
        ]

        # 排序
        ranked = sorted(
            zip(docs, combined),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked[:k]]

# 使用
retriever = HybridRetriever(alpha=0.6)
docs = ["文档1", "文档2", "文档3", "文档4", "文档5"]
results = retriever.retrieve("查询", docs)
```

---

## 04_reranking_rag.py - 重排序示例

```python
def two_stage_retrieval(query: str, docs: List[str]):
    """两阶段检索"""

    # 阶段 1：初始检索
    print("[1] 初始检索")
    initial = docs[:10]  # Top-10

    # 阶段 2：重排序
    print("[2] 重排序")
    # 模拟重排序分数
    rerank_scores = [0.9, 0.7, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]

    reranked = sorted(
        zip(initial, rerank_scores),
        key=lambda x: x[1],
            reverse=True
    )

    return [doc for doc, score in reranked[:5]]
```

---

## 05_cached_agent.py - 缓存示例

```python
class CachedAgent:
    """带缓存的 Agent"""

    def __init__(self):
        self.cache = {}

    def run(self, query: str):
        """运行 Agent"""

        # 检查缓存
        if query in self.cache:
            print("✓ 缓存命中")
            return self.cache[query]

        # 缓存未命中，执行
        print("× 缓存未命中，执行中...")
        result = f"结果：{query}"

        # 存入缓存
        self.cache[query] = result

        return result
```

---

## 06_async_agent.py - 异步示例

```python
import asyncio
import time

async def async_task(name: str, delay: float):
    """异步任务"""
    print(f"开始 {name}")
    await asyncio.sleep(delay)
    print(f"完成 {name}")
    return f"{name} 结果"

async def main():
    """并发执行"""

    # 创建任务
    tasks = [
        async_task("任务1", 1),
        async_task("任务2", 1),
        async_task("任务3", 1)
    ]

    # 并发执行
    results = await asyncio.gather(*tasks)

    print(f"\n结果：{results}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

**提示**：这些是简化示例，展示核心概念。实际使用时需要集成真实的 LLM 和向量数据库。
