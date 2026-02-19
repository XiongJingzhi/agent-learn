# 09. 知识图谱 RAG

> **目标**: 理解知识图谱在 RAG 中的应用
> **预计时间**: 50 分钟
> **难度**: ⭐⭐⭐⭐ 高级

---

## 什么是知识图谱 RAG？

### 定义

**知识图谱 RAG（KG-RAG）** 是将知识图谱与向量检索结合，利用结构化知识增强 RAG 系统。

> **类比**：
> - **传统 RAG**：像在散乱的文档中搜索
> - **知识图谱 RAG**：像在结构化的百科全书中搜索，不仅有内容，还有关联关系

---

## 为什么需要知识图谱？

### 传统 RAG 的局限

**局限 1：缺乏结构化信息**

```python
# 查询："马斯克和 OpenAI 的关系"

# 传统 RAG 可能返回：
# "埃隆·马斯克是特斯拉 CEO"
# "OpenAI 是一家人工智能公司"

# 但无法直接回答：
# "马斯克是 OpenAI 的联合创始人之一，但于 2018 年离开"
```

**局限 2：多跳推理困难**

```python
# 查询："投资了 OpenAI 的公司有哪些？"

# 传统 RAG 需要多轮检索
# 知识图谱可以直接遍历关系
```

---

## 知识图谱基础

### 图结构

```
实体（节点）
  │
  ├── 关系（边）
  │     │
  │     └── 实体（节点）

示例：
[马斯克] --创始人--> [特斯拉]
  │
  ├──联合创始人--> [OpenAI]
  │
  └──CEO--> [X（推特）]
```

---

### 常用图数据库

| 数据库 | 类型 | 特点 |
|--------|------|------|
| **Neo4j** | 属性图 | 成熟、易用 |
| **NetworkX** | 内存图 | 轻量、适合研究 |
| **ArangoDB** | 多模型 | 图 + 文档 |

---

## 构建 KG-RAG

### 步骤 1：提取知识图谱

```python
from langchain.graphs import KnowledgeGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer

# 文档
docs = [
    "埃隆·马斯克是特斯拉和 SpaceX 的 CEO",
    "马斯克是 OpenAI 的联合创始人之一",
    "OpenAI 成立于 2015 年",
    "微软是 OpenAI 的主要投资者"
]

# 使用 LLM 提取知识图谱
llm_transformer = LLMGraphTransformer(llm=ChatOpenAI())

graph_documents = []
for doc in docs:
    graph_doc = llm_transformer.convert_to_graph_documents([doc])
    graph_documents.extend(graph_doc)

# 查看提取的实体和关系
for graph_doc in graph_documents:
    print(f"节点: {graph_doc.nodes}")
    print(f"关系: {graph_doc.relationships}")
```

---

### 步骤 2：存储到图数据库

```python
from langchain.graphs import Neo4jGraph

# 连接 Neo4j
kg = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password"
)

# 添加图谱数据
for graph_doc in graph_documents:
    # 添加节点
    for node in graph_doc.nodes:
        kg.query("""
            MERGE (n:Entity {id: $id})
            SET n.type = $type
        """, params={"id": node.id, "type": node.type})

    # 添加关系
    for rel in graph_doc.relationships:
        kg.query("""
            MATCH (a:Entity {id: $source})
            MATCH (b:Entity {id: $target})
            MERGE (a)-[r:RELATION]->(b)
            SET r.type = $type
        """, params={
            "source": rel.source.id,
            "target": rel.target.id,
            "type": rel.type
        })
```

---

### 步骤 3：图谱检索

```python
class GraphRetriever:
    """图谱检索器"""

    def __init__(self, kg):
        self.kg = kg

    def retrieve(self, query: str, top_k: int = 10):
        """从知识图谱检索相关信息"""

        # 1. 识别查询中的实体
        entities = self.extract_entities(query)

        # 2. 检索相关子图
        relevant_info = []
        for entity in entities:
            # 查询实体的一跳邻居
            result = self.kg.query("""
                MATCH (e:Entity {id: $entity})
                OPTIONAL MATCH (e)-[r]->(neighbor)
                RETURN e, r, neighbor
            """, params={"entity": entity})

            relevant_info.extend(result)

        # 3. 格式化结果
        context = self.format_graph_results(relevant_info)

        return context

    def extract_entities(self, query: str):
        """从查询中提取实体"""

        # 使用 NER 或简单的关键词匹配
        # 这里简化处理
        keywords = query.split()
        return keywords

    def format_graph_results(self, results):
        """格式化图谱查询结果"""

        formatted = []
        for record in results:
            entity = record["e"]["id"]
            relation = record["r"]["type"] if record["r"] else None
            neighbor = record["neighbor"]["id"] if record["neighbor"] else None

            if relation and neighbor:
                formatted.append(f"{entity} {relation} {neighbor}")
            else:
                formatted.append(f"{entity}")

        return "\n".join(formatted)
```

---

## 混合检索：向量 + 图谱

### 架构设计

```
用户查询
    │
    ├─→ 向量检索 ──→ 文档上下文
    │
    └─→ 图谱检索 ──→ 结构化知识
           │
           └───────────────┘
                  │
                  ▼
            融合上下文
                  │
                  ▼
             LLM 生成
```

---

### 实现

```python
class HybridGraphRetriever:
    """混合图谱检索器"""

    def __init__(self, vectorstore, kg):
        self.vector_retriever = vectorstore.as_retriever()
        self.graph_retriever = GraphRetriever(kg)

    def retrieve(self, query: str, top_k: int = 5):
        """混合检索"""

        # 1. 向量检索
        vector_docs = self.vector_retriever.get_relevant_documents(query)

        # 2. 图谱检索
        graph_context = self.graph_retriever.retrieve(query)

        # 3. 融合结果
        enriched_docs = []
        for doc in vector_docs[:top_k]:
            # 为每个文档添加图谱信息
            enriched_content = f"""
            文档内容：{doc.page_content}

            相关知识：
            {graph_context}
            """

            enriched_docs.append(
                Document(page_content=enriched_content.strip())
            )

        return enriched_docs
```

---

## 多跳推理

### 场景：复杂查询

```python
# 查询："投资了 OpenAI 的公司，其CEO 还投资了哪些公司？"

# 需要多跳推理：
# 第1跳：OpenAI <-投资者- 微软
# 第2跳：微软 <-CEO- 萨提亚·纳德拉
# 第3跳：萨提亚·纳德拉 -投资-> ?

class MultiHopRetriever:
    """多跳检索器"""

    def __init__(self, kg):
        self.kg = kg

    def multi_hop_query(self, query: str, max_hops: int = 3):
        """多跳查询"""

        # 解析查询（简化）
        # 实际需要更复杂的 NLU
        hops = self.parse_hops(query)

        # 执行多跳
        current_entities = [hops[0]["entity"]]
        results = []

        for i in range(max_hops):
            next_entities = []
            for entity in current_entities:
                # 查询一跳邻居
                result = self.kg.query(f"""
                    MATCH (e:Entity {{id: '{entity}'}})-[r]->(neighbor)
                    RETURN neighbor.id, r.type
                """)

                next_entities.extend([r["neighbor.id"] for r in result])
                results.extend(result)

            current_entities = list(set(next_entities))

            if not current_entities:
                break

        return results
```

---

## 最小验证

### 验证目标
- ✅ 理解知识图谱在 RAG 中的作用
- ✅ 能够构建简单的 KG-RAG 系统
- ✅ 理解混合检索的架构

### 验证步骤
1. 准备简单的文档集
2. 提取知识图谱
3. 实现图谱检索
4. 对比向量检索和混合检索的效果

### 预期输出
混合检索应该能回答需要结构化信息的问题。

---

## 常见错误

### 错误 1：图谱提取质量差

**问题**：LLM 提取的实体和关系不准确

**解决**：
- 使用更好的提示词
- 人工校验关键图谱
- 使用专门的实体关系抽取模型

---

### 错误 2：过度依赖图谱

**问题**：所有查询都用图谱

**解决**：图谱适合结构化信息查询，向量检索适合语义查询

---

### 错误 3：忽略图谱维护

**问题**：图谱不更新，信息过时

**解决**：定期更新图谱，处理知识时效性

---

## 下一步

- 📖 `notes/10_performance_optimization.md` - 性能优化（阶段 3）
- ✏ `exercises/02_intermediate_exercises.md` - 进阶练习
- 🎯 完成阶段 1-2 的所有练习

---

**记住：知识图谱就像一张智能地图，不仅能找到你要的信息，还能告诉你信息之间的关系！** 🗺️🔗
