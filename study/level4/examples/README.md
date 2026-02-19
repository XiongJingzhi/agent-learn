# Level 4 代码示例

本目录包含 Level 4 的所有代码示例。

## 示例列表

### 01_babyagi_agent.py
BabyAGI 的简化实现，展示任务生成、排序、执行的核心循环。

**核心功能**：
- 任务生成
- 优先级排序
- 任务执行
- 结果存储

**运行方式**：
```bash
python 01_babyagi_agent.py
```

---

### 02_autogpt_agent.py
AutoGPT 的简化实现，展示规划-执行-反思循环。

**核心功能**：
- 目标规划
- 执行子目标
- 反思调整

**运行方式**：
```bash
python 02_autogpt_agent.py
```

---

### 03_hybrid_rag.py
混合检索示例，结合稠密和稀疏检索。

**核心功能**：
- 向量检索
- BM25 检索
- 分数融合

**运行方式**：
```bash
python 03_hybrid_rag.py
```

---

### 04_reranking_rag.py
重排序示例，使用 Cross-Encoder 提升精确度。

**核心功能**：
- 初始检索
- Cross-Encoder 重排序
- 两阶段检索

**运行方式**：
```bash
python 04_reranking_rag.py
```

---

### 05_cached_agent.py
带缓存的 Agent 示例，减少重复计算。

**核心功能**：
- 精确匹配缓存
- 语义缓存
- 多层缓存策略

**运行方式**：
```bash
python 05_cached_agent.py
```

---

### 06_async_agent.py
异步并发 Agent 示例，提升执行效率。

**核心功能**：
- 异步任务执行
- 并发控制
- 结果聚合

**运行方式**：
```bash
python 06_async_agent.py
```

---

## 依赖安装

```bash
pip install langchain langchain-openai langchain-community
pip install sentence-transformers
pip install rank-bm25
pip install chromadb
```

## 环境变量

```bash
export OPENAI_API_KEY="your-api-key"
```

---

**提示**：每个示例都可以独立运行，建议按顺序学习。
