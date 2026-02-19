# 06. 高级 RAG 简介

> **目标**: 理解高级 RAG 技术的发展方向和应用场景
> **预计时间**: 30 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 什么是高级 RAG？

### 从基础到高级

**基础 RAG**（Level 3）：
```
用户查询 → 向量检索 → LLM 生成 → 回答
```

**高级 RAG**（Level 4）：
```
用户查询 → 查询重写 → 混合检索 → 重排序 → LLM 生成 → 回答
               ↓
         知识图谱增强
         多模态融合
```

> **类比**：
> - **基础 RAG**：就像在图书馆用关键词搜书
> - **高级 RAG**：就像有个专业图书管理员，能理解你的需求，从多个来源找最相关的资料

---

## 为什么需要高级 RAG？

### 基础 RAG 的局限

| 问题 | 说明 | 影响 |
|------|------|------|
| **检索不准确** | 向量检索可能找不到最相关的内容 | 回答质量差 |
| **单一信息源** | 只依赖文档向量，缺乏外部知识 | 信息不全面 |
| **查询理解差** | 不能理解复杂的查询意图 | 检索结果不相关 |
| **结果排序差** | 简单的相似度排序不够准确 | 重要信息被埋没 |

---

### 高级 RAG 的改进

**改进 1：混合检索**
- 稠密检索（语义）+ 稀疏检索（关键词）
- 互补优势，提高召回率

**改进 2：重排序**
- 对检索结果重新排序
- 提高精确度

**改进 3：查询优化**
- 查询重写、扩展、分解
- 更好地理解用户意图

**改进 4：知识增强**
- 知识图谱补充
- 结构化数据融合

---

## 高级 RAG 技术栈

### 核心技术

```
┌─────────────────────────────────────────────────┐
│              高级 RAG 技术栈                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────┐    ┌────────────┐              │
│  │ 查询优化   │    │  检索优化  │              │
│  │ - 重写     │    │ - 混合检索 │              │
│  │ - 扩展     │    │ - 重排序   │              │
│  │ - 分解     │    │ - 递归检索 │              │
│  └────────────┘    └────────────┘              │
│          │                  │                   │
│          └────────┬─────────┘                   │
│                   ▼                             │
│          ┌────────────┐                        │
│          │ 知识增强   │                        │
│          │ - 知识图谱 │                        │
│          │ - 多模态   │                        │
│          │ - 融合策略 │                        │
│          └────────────┘                        │
│                   │                             │
│                   ▼                             │
│          ┌────────────┐                        │
│          │ 生成优化   │                        │
│          │ - 上下文   │                        │
│          │ - 引用     │                        │
│          │ - 验证     │                        │
│          └────────────┘                        │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 技术对比

### 基础 RAG vs 高级 RAG

| 维度 | 基础 RAG | 高级 RAG |
|------|---------|---------|
| **检索方式** | 单一向量检索 | 混合检索 + 重排序 |
| **查询处理** | 直接使用原查询 | 查询重写和优化 |
| **信息源** | 文档向量 | 文档 + 知识图谱 + 结构化数据 |
| **排序方法** | 向量相似度 | 神经重排序 |
| **上下文** | 简单拼接 | 智能截断和重组 |
| **准确率** | 60-70% | 80-90% |
| **成本** | 低 | 中等 |
| **延迟** | 低 | 中等 |

---

## 应用场景

### 场景 1：企业知识库

**需求**：
- 准确检索内部文档
- 整合多个数据源
- 支持复杂查询

**高级 RAG 方案**：
```python
class EnterpriseRAG:
    """企业级 RAG"""

    def __init__(self):
        # 多个检索器
        self.doc_retriever = VectorRetriever()  # 文档检索
        self.kg_retriever = GraphRetriever()    # 知识图谱
        self.db_retriever = SQLRetriever()      # 数据库

        # 重排序模型
        self.reranker = CrossEncoderReranker()

    def query(self, user_query: str):
        """查询"""

        # 1. 查询优化
        optimized_query = self.optimize_query(user_query)

        # 2. 多路检索
        doc_results = self.doc_retriever.retrieve(optimized_query)
        kg_results = self.kg_retriever.retrieve(optimized_query)
        db_results = self.db_retriever.retrieve(optimized_query)

        # 3. 合并结果
        all_results = doc_results + kg_results + db_results

        # 4. 重排序
        reranked = self.reranker.rerank(
            optimized_query,
            all_results
        )

        # 5. 选择 Top-K
        top_results = reranked[:10]

        # 6. 生成回答
        answer = self.generate_answer(optimized_query, top_results)

        return answer
```

---

### 场景 2：客户支持

**需求**：
- 理解客户问题
- 检索相关文档
- 生成准确回答

**高级 RAG 方案**：
```python
class SupportRAG:
    """客户支持 RAG"""

    def __init__(self):
        self.query_rewriter = QueryRewriter()
        self.hybrid_retriever = HybridRetriever()
        self.reranker = Reranker()
        self.citation_generator = CitationGenerator()

    def handle_query(self, customer_query: str):
        """处理客户查询"""

        # 1. 理解意图
        intent = self.classify_intent(customer_query)

        # 2. 查询重写
        rewritten = self.query_rewriter.rewrite(
            customer_query,
            intent
        )

        # 3. 混合检索
        results = self.hybrid_retriever.retrieve(rewritten)

        # 4. 重排序
        reranked = self.reranker.rerank(
            customer_query,
            results
        )

        # 5. 生成回答（带引用）
        answer = self.generate_with_citation(
            customer_query,
            reranked[:5]
        )

        return answer
```

---

## 性能考虑

### 准确率 vs 成本

| 技术 | 准确率提升 | 成本增加 | 推荐场景 |
|------|-----------|---------|---------|
| **混合检索** | +10-15% | 低（1.2x）| 所有场景 |
| **重排序** | +15-20% | 中（1.5x）| 高质量要求 |
| **查询优化** | +5-10% | 低（1.1x）| 复杂查询 |
| **知识图谱** | +10-15% | 高（2x）| 专业领域 |

**建议**：
- 小规模应用：混合检索 + 轻量重排序
- 中等规模：混合检索 + 重排序 + 查询优化
- 大规模/高要求：全部技术

---

## 最小验证

### 验证目标
- ✅ 理解高级 RAG 的必要性
- ✅ 了解高级 RAG 的技术栈
- ✅ 能够选择合适的技术组合

### 验证步骤
1. 列出基础 RAG 的 3 个主要问题
2. 说明高级 RAG 如何解决这些问题
3. 为给定场景选择合适的技术

### 预期输出
能够根据应用场景选择合适的 RAG 技术。

---

## 常见错误

### 错误 1：过度设计

**问题**：在简单场景使用复杂技术

**解决**：从简单方案开始，按需优化

---

### 错误 2：忽视成本

**问题**：盲目追求高准确率，不考虑成本

**解决**：评估准确率与成本的权衡

---

### 错误 3：忽略数据质量

**问题**：技术再好，数据质量差也没用

**解决**：先优化数据质量，再应用高级技术

---

## 下一步

- 📖 `notes/07_hybrid_retrieval.md` - 混合检索详解
- 📖 `notes/08_reranking_strategies.md` - 重排序策略
- 🧪 `examples/03_hybrid_rag.py` - 混合 RAG 示例

---

**记住：高级 RAG 不是技术的堆砌，而是根据需求选择合适的工具组合！** 🛠️📚
