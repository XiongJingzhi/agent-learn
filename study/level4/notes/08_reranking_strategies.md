# 08. 重排序策略

> **目标**: 掌握 RAG 中的重排序技术
> **预计时间**: 45 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 什么是重排序？

### 定义

**重排序（Reranking）** 是对初始检索结果进行重新排序的过程，使用更强大的模型提高精确度。

> **类比**：
> - **初始检索**：就像快速筛选，找出可能相关的 100 个文档
> - **重排序**：就像仔细审查，从这 100 个中选出最相关的 10 个

---

## 为什么需要重排序？

### 初始检索的问题

**问题 1：召回 vs 精确度**

```
初始检索：召回优先
- 检索 Top-100 文档
- 速度快，但可能包含不相关的内容

重排序：精确优先
- 从 Top-100 中选出 Top-10
- 速度慢，但结果更准确
```

**问题 2：向量检索的局限**

```python
# 查询："机器学习模型的性能优化"

# 向量检索可能返回：
# 1. "机器学习模型"（相关，但不具体）
# 2. "深度学习性能优化"（语义相似，但不是机器学习）
# 3. "数据库性能优化"（都有"性能优化"，但领域不同）

# 重排序后：
# 1. "提高机器学习模型准确率的方法"（最相关）
# 2. "优化深度学习模型性能"（次相关）
# 3. "机器学习模型调参技巧"（相关）
```

---

## 重排序方法

### 方法 1：Cross-Encoder

**原理**：同时输入查询和文档，直接输出相关性分数

```python
from sentence_transformers import CrossEncoder

# 加载 Cross-Encoder 模型
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# 初始检索结果
query = "机器学习模型的性能优化"
candidates = [
    "提高模型准确率的方法",
    "数据库性能优化",
    "深度学习模型调优"
]

# 重排序
scores = model.predict([
    [query, doc] for doc in candidates
])

# 排序
reranked = sorted(
    zip(candidates, scores),
    key=lambda x: x[1],
    reverse=True
)

print("重排序结果：")
for doc, score in reranked:
    print(f"{score:.3f}: {doc}")
```

**优点**：
- ✓ 准确率高
- ✓ 理解查询-文档关系

**缺点**：
- ✗ 速度慢（需要 N 次前向传播）
- ✗ 成本高

---

### 方法 2：LLM 重排序

**原理**：使用 LLM 判断文档相关性

```python
def llm_rerank(query: str, documents: List[str], top_k: int = 5):
    """使用 LLM 重排序"""

    # 构建提示词
    prompt = f"""
    查询：{query}

    文档列表：
    {format_documents(documents)}

    请评估每个文档与查询的相关性（0-10 分）。
    返回格式：JSON，包含文档索引和分数

    {{
        "scores": [
            {{"index": 0, "score": 8}},
            {{"index": 1, "score": 3}},
            ...
        ]
    }}
    """

    # 调用 LLM
    response = llm.invoke(prompt)
    scores_data = parse_json(response)

    # 排序
    scored_docs = [
        (documents[s["index"]], s["score"])
        for s in scores_data["scores"]
    ]
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # 返回 Top-K
    return [doc for doc, score in scored_docs[:top_k]]
```

**优点**：
- ✓ 理解能力强
- ✓ 灵活性高

**缺点**：
- ✗ 成本高
- ✗ 速度慢
- ✗ 输出格式不稳定

---

### 方法 3：轻量级重排序

**原理**：使用轻量级模型快速重排序

```python
from sentence_transformers import CrossEncoder

# 使用轻量级模型
model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2')

def lightweight_rerank(query, documents, top_k=10):
    """轻量级重排序"""

    # 批量处理
    pairs = [[query, doc] for doc in documents]
    scores = model.predict(pairs, batch_size=32)

    # 排序
    reranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, score in reranked[:top_k]]
```

**优点**：
- ✓ 速度快
- ✓ 成本低

**缺点**：
- ✗ 准确率略低

---

## 两阶段检索流程

### 完整流程

```python
class TwoStageRetriever:
    """两阶段检索器"""

    def __init__(self, retriever, reranker, rerank_top_k=50):
        self.retriever = retriever  # 初始检索器
        self.reranker = reranker    # 重排序器
        self.rerank_top_k = rerank_top_k

    def retrieve(self, query: str, top_k: int = 10):
        """两阶段检索"""

        # 阶段 1：初始检索（召回）
        print(f"[1] 初始检索，获取 Top-{self.rerank_top_k}")
        initial_results = self.retriever.retrieve(
            query,
            k=self.rerank_top_k
        )

        # 阶段 2：重排序（精确）
        print(f"[2] 重排序 {len(initial_results)} 个结果")
        reranked_results = self.reranker.rerank(
            query,
            initial_results
        )

        # 返回 Top-K
        final_results = reranked_results[:top_k]

        print(f"[3] 返回 Top-{top_k}")
        return final_results
```

**性能对比**：

| 方法 | 召回率 | 精确率 | 延迟 |
|------|-------|--------|------|
| **单阶段检索（Top-100）** | 95% | 60% | 50ms |
| **两阶段检索（100→10）** | 90% | 85% | 200ms |

---

## 实用技巧

### 技巧 1：自适应重排序

**根据查询复杂度决定是否重排序**

```python
class AdaptiveReranker:
    """自适应重排序器"""

    def __init__(self, reranker):
        self.reranker = reranker

    def rerank(self, query, initial_results):
        """自适应重排序"""

        # 评估查询复杂度
        complexity = self.assess_complexity(query)

        if complexity < 0.3:
            # 简单查询：不需要重排序
            print("查询简单，跳过重排序")
            return initial_results[:10]
        else:
            # 复杂查询：需要重排序
            print("查询复杂，执行重排序")
            return self.reranker.rerank(query, initial_results)

    def assess_complexity(self, query: str):
        """评估查询复杂度"""

        # 简单指标
        indicators = [
            len(query.split()),  # 词数
            query.count("?"),    # 问号数量
            query.count("和"),   # 连接词
        ]

        # 归一化
        complexity = min(sum(indicators) / 20, 1.0)

        return complexity
```

---

### 技巧 2：分层重排序

**先粗排，再精排**

```python
def hierarchical_rerank(query, candidates):
    """分层重排序"""

    # 第 1 层：快速粗排（轻量级模型）
    print("[1] 粗排（轻量级）")
    coarse_reranker = CrossEncoder('tinybert-reranker')
    coarse_scores = coarse_reranker.predict([
        [query, doc] for doc in candidates
    ])

    # 选择 Top-30
    top_30_indices = np.argsort(coarse_scores)[-30:]
    top_30 = [candidates[i] for i in top_30_indices]

    # 第 2 层：精确精排（重量级模型）
    print("[2] 精排（重量级）")
    fine_reranker = CrossEncoder('large-reranker')
    fine_scores = fine_reranker.predict([
        [query, doc] for doc in top_30
    ])

    # 排序并返回 Top-10
    reranked = sorted(
        zip(top_30, fine_scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, score in reranked[:10]]
```

---

### 技巧 3：多样化重排序

**考虑结果多样性**

```python
def diverse_rerank(query, candidates, lambda_mmr=0.5):
    """多样化重排序（MMR 算法）"""

    # 计算查询-文档相关性
    relevance_scores = compute_relevance(query, candidates)

    # 初始化
    selected = []
    remaining = list(range(len(candidates)))

    # 贪心选择
    while len(selected) < 10 and remaining:
        best_score = -float('inf')
        best_idx = None

        for idx in remaining:
            # 相关性分数
            relevance = relevance_scores[idx]

            # 多样性分数（与已选文档的相似度）
            diversity = 0
            if selected:
                similarity = max([
                    compute_similarity(candidates[idx], candidates[s])
                    for s in selected
                ])
                diversity = -similarity

            # MMR 分数
            mmr_score = lambda_mm_r * relevance + (1 - lambda_mm_r) * diversity

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx

        # 选择最佳文档
        selected.append(best_idx)
        remaining.remove(best_idx)

    return [candidates[i] for i in selected]
```

---

## 最小验证

### 验证目标
- ✅ 理解重排序的作用
- ✅ 能够实现 Cross-Encoder 重排序
- ✅ 掌握两阶段检索流程

### 验证步骤
1. 实现初始检索
2. 实现重排序
3. 对比重排序前后的效果

### 预期输出
重排序后的 Top-10 应该比直接检索的 Top-10 更相关。

---

## 常见错误

### 错误 1：重排序太多文档

**问题**：对全部 100 个文档重排序

**解决**：只对 Top-50 重排序，然后返回 Top-10

---

### 错误 2：忽略成本

**问题**：每次查询都用 LLM 重排序

**解决**：只在复杂查询时使用 LLM 重排序

---

### 错误 3：不评估效果

**问题**：不知道重排序是否有效

**解决**：建立评估指标，如 NDCG、MRR

---

## 下一步

- 📖 `notes/09_knowledge_graph_rag.md` - 知识图谱 RAG
- 🧪 `examples/04_reranking_rag.py` - 重排序示例
- ✏ `exercises/02_intermediate_exercises.md` - 进阶练习

---

**记住：重排序就像从一堆候选者中精选最优，用更强的模型做更精细的判断！** 🎯📊
