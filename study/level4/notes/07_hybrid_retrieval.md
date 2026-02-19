# 07. 混合检索

> **目标**: 掌握稠密检索与稀疏检索的混合使用
> **预计时间**: 50 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 什么是混合检索？

### 定义

**混合检索（Hybrid Retrieval）** = **稠密检索（Dense）** + **稀疏检索（Sparse）**

> **类比**：
> - **稠密检索**：像"理解意思"，找语义相似的内容
> - **稀疏检索**：像"关键词匹配"，找包含相同词汇的内容
> - **混合检索**：两者结合，既理解意思又匹配关键词

---

## 两种检索方式

### 稠密检索（Dense Retrieval）

**原理**：将文本向量化，计算向量相似度

**优点**：
- ✓ 理解语义
- ✓ 能找到同义表达
- ✓ 适合长文本

**缺点**：
- ✗ 计算成本高
- ✗ 可能忽略精确关键词
- ✗ 需要训练好的模型

**示例**：
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 稠密检索
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)

query = "如何提高机器学习模型的准确率？"
results = vectorstore.similarity_search(query, k=5)

# 能找到语义相似的内容，如：
# "提升模型精度的方法"
# "优化深度学习性能"
```

---

### 稀疏检索（Sparse Retrieval）

**原理**：基于关键词匹配（如 BM25）

**优点**：
- ✓ 速度快
- ✓ 精确匹配关键词
- ✓ 可解释性强

**缺点**：
- ✗ 不理解语义
- ✗ 受词汇变化影响
- ✗ 可能漏掉相关内容

**示例**：
```python
from rank_bm25 import BM25Okapi

# 稀疏检索（BM25）
tokenized_corpus = [doc.split() for doc in docs]
bm25 = BM25Okapi(tokenized_corpus)

query = "如何提高机器学习模型的准确率？"
tokenized_query = query.split()

scores = bm25.get_scores(tokenized_query)

# 只能找到包含关键词的内容，如：
# "机器学习模型准确率"
# 但会漏掉"模型精度"、"模型性能"等同义表达
```

---

## 混合检索的实现

### 方法 1：分数融合（Score Fusion）

**原理**：分别计算稠密和稀疏的分数，加权融合

```python
class HybridRetriever:
    """混合检索器"""

    def __init__(self, dense_retriever, sparse_retriever, alpha=0.5):
        self.dense_retriever = dense_retriever
        self.sparse_retriever = sparse_retriever
        self.alpha = alpha  # 稠密检索权重

    def retrieve(self, query: str, k: int = 10):
        """混合检索"""

        # 1. 稠密检索
        dense_results = self.dense_retriever.retrieve(query, k=k*2)
        dense_scores = {r.doc_id: r.score for r in dense_results}

        # 2. 稀疏检索
        sparse_results = self.sparse_retriever.retrieve(query, k=k*2)
        sparse_scores = {r.doc_id: r.score for r in sparse_results}

        # 3. 分数归一化
        dense_scores = self.normalize(dense_scores)
        sparse_scores = self.normalize(sparse_scores)

        # 4. 融合分数
        combined_scores = {}
        all_doc_ids = set(dense_scores.keys()) | set(sparse_scores.keys())

        for doc_id in all_doc_ids:
            dense_score = dense_scores.get(doc_id, 0)
            sparse_score = sparse_scores.get(doc_id, 0)

            # 加权融合
            combined_scores[doc_id] = (
                self.alpha * dense_score +
                (1 - self.alpha) * sparse_score
            )

        # 5. 排序并返回 Top-K
        sorted_results = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]

        return [
            {"doc_id": doc_id, "score": score}
            for doc_id, score in sorted_results
        ]

    def normalize(self, scores: Dict) -> Dict:
        """归一化分数到 [0, 1]"""

        if not scores:
            return {}

        max_score = max(scores.values())
        min_score = min(scores.values())

        if max_score == min_score:
            return {k: 1.0 for k in scores.keys()}

        return {
            k: (v - min_score) / (max_score - min_score)
            for k, v in scores.items()
        }
```

---

### 方法 2：RRF（Reciprocal Rank Fusion）

**原理**：基于排名融合，不依赖具体分数值

```python
def rrffusion(dense_results, sparse_results, k=60):
    """RRF 融合"""

    # 1. 提取排名
    dense_ranks = {r.doc_id: rank for rank, r in enumerate(dense_results)}
    sparse_ranks = {r.doc_id: rank for rank, r in enumerate(sparse_results)}

    # 2. 融合排名
    combined_scores = {}
    all_doc_ids = set(dense_ranks.keys()) | set(sparse_ranks.keys())

    for doc_id in all_doc_ids:
        dense_rank = dense_ranks.get(doc_id, len(dense_results))
        sparse_rank = sparse_ranks.get(doc_id, len(sparse_results))

        # RRF 公式
        combined_scores[doc_id] = (
            1 / (k + dense_rank) +
            1 / (k + sparse_rank)
        )

    # 3. 排序
    sorted_results = sorted(
        combined_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_results
```

**RRF 优势**：
- ✓ 不需要分数归一化
- ✓ 对异常值不敏感
- ✓ 简单有效

---

## 权重调优

### 如何确定最佳 alpha 值？

**方法 1：网格搜索**

```python
def find_best_alpha(train_queries, train_labels):
    """寻找最佳 alpha"""

    best_alpha = 0.5
    best_score = 0

    for alpha in [i/10 for i in range(0, 11)]:
        # 使用当前 alpha
        retriever = HybridRetriever(
            dense_retriever,
            sparse_retriever,
            alpha=alpha
        )

        # 评估
        score = evaluate(retriever, train_queries, train_labels)

        if score > best_score:
            best_score = score
            best_alpha = alpha

        print(f"Alpha={alpha:.1f}: {score:.3f}")

    print(f"\n最佳 Alpha: {best_alpha}")
    return best_alpha
```

**方法 2：基于查询类型动态调整**

```python
class AdaptiveHybridRetriever(HybridRetriever):
    """自适应混合检索器"""

    def retrieve(self, query: str, k: int = 10):
        """根据查询类型动态调整"""

        # 分析查询类型
        query_type = self.classify_query(query)

        # 动态调整 alpha
        if query_type == "factual":
            # 事实查询：关键词更重要
            alpha = 0.3
        elif query_type == "semantic":
            # 语义查询：理解更重要
            alpha = 0.7
        else:
            # 默认均衡
            alpha = 0.5

        # 使用动态 alpha 检索
        self.alpha = alpha
        return super().retrieve(query, k)

    def classify_query(self, query: str):
        """分类查询类型"""

        # 简单规则
        factual_keywords = ["什么", "哪里", "谁", "何时", "多少"]
        semantic_keywords = ["如何", "为什么", "解释", "分析"]

        if any(kw in query for kw in factual_keywords):
            return "factual"
        elif any(kw in query for kw in semantic_keywords):
            return "semantic"
        else:
            return "general"
```

---

## 完整示例

### 使用 LangChain 实现混合检索

```python
from langchain.retrievers import BM25Retriever
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 1. 准备文档
docs = [
    "机器学习是人工智能的一个分支",
    "深度学习使用神经网络学习数据表示",
    "提高模型准确率的方法包括数据增强和正则化",
    "模型优化可以通过调整超参数实现",
]

# 2. 创建稠密检索器
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(docs, embeddings)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 3. 创建稀疏检索器
sparse_retriever = BM25Retriever.from_texts(docs)
sparse_retriever.k = 5

# 4. 混合检索
query = "如何让模型更准确？"

# 稠密检索
dense_results = dense_retriever.get_relevant_documents(query)

# 稀疏检索
sparse_results = sparse_retriever.get_relevant_documents(query)

# 融合（简单实现）
def merge_results(dense, sparse, alpha=0.5):
    """融合结果"""

    # 提取文档
    dense_docs = {d.page_content: d for d in dense}
    sparse_docs = {d.page_content: d for d in sparse}

    # 合并
    all_docs = set(dense_docs.keys()) | set(sparse_docs.keys())

    # 计算融合分数
    scored_docs = []
    for doc in all_docs:
        dense_score = 1.0 if doc in dense_docs else 0.0
        sparse_score = 1.0 if doc in sparse_docs else 0.0

        combined_score = alpha * dense_score + (1 - alpha) * sparse_score
        scored_docs.append((doc, combined_score))

    # 排序
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return [d[0] for d in scored_docs[:5]]

# 执行混合检索
hybrid_results = merge_results(dense_results, sparse_results, alpha=0.5)

print("混合检索结果：")
for i, result in enumerate(hybrid_results, 1):
    print(f"{i}. {result}")
```

---

## 最小验证

### 验证目标
- ✅ 理解稠密检索和稀疏检索的区别
- ✅ 能够实现混合检索
- ✅ 能够调优融合权重

### 验证步骤
1. 实现稠密检索和稀疏检索
2. 实现分数融合和 RRF 融合
3. 对比不同融合方法的效果

### 预期输出
混合检索的准确率应该高于单一检索方法。

---

## 常见错误

### 错误 1：直接相加未归一化的分数

**问题**：稠密和稀疏分数的范围不同

**解决**：归一化后再融合

---

### 错误 2：固定 alpha 值

**问题**：所有查询使用相同的 alpha

**解决**：根据查询类型动态调整

---

### 错误 3：忽略检索质量

**问题**：单个检索器质量差，融合后也差

**解决**：先优化单个检索器，再融合

---

## 下一步

- 📖 `notes/08_reranking_strategies.md` - 重排序策略
- 🧪 `examples/03_hybrid_rag.py` - 混合 RAG 示例
- ✏ `exercises/01_basic_exercises.md` - 基础练习

---

**记住：混合检索就像用两只眼睛看世界，既看到细节（关键词），又理解整体（语义）！** 👀📖
