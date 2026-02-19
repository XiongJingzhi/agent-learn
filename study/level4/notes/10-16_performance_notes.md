# Level 4 性能优化与测试笔记集

本文件包含阶段3-4的所有笔记，以简洁形式呈现。

---

## 10. 性能优化简介

### 优化方向

1. **Token 优化**：减少 LLM 调用的 Token 数量
2. **缓存策略**：避免重复计算
3. **并发执行**：并行处理独立任务
4. **成本监控**：实时跟踪和控制成本

### 优化流程

```
测量 → 识别瓶颈 → 优化 → 验证 → 迭代
```

---

## 11. Token 优化

### 压缩技巧

```python
# ❌ 不好：冗长的提示词
prompt = """
你是一个专业的助手，请帮我...
（省略 200 字）
"""

# ✓ 好：简洁的提示词
prompt = "助手：{task}"
```

### 选择性调用

```python
def smart_llm_call(task: str):
    """智能 LLM 调用"""

    # 简单任务：使用小模型
    if is_simple_task(task):
        return small_llm.invoke(task)

    # 复杂任务：使用大模型
    return large_llm.invoke(task)
```

---

## 12. 缓存策略

### 多层缓存

```python
class MultiLevelCache:
    """多层缓存"""

    def __init__(self):
        self.l1 = {}  # 精确匹配缓存
        self.l2 = VectorStore()  # 语义缓存

    def get(self, query: str):
        # L1：精确匹配
        if query in self.l1:
            return self.l1[query]

        # L2：语义相似
        similar = self.l2.similarity_search(query, k=1)
        if similar and similarity > 0.95:
            return similar[0]

        # 缓存未命中
        return None
```

---

## 13. 异步执行

### 并发处理

```python
import asyncio

async def parallel_execute(tasks: List[Task]):
    """并行执行任务"""

    # 创建并发任务
    coroutines = [execute_task(task) for task in tasks]

    # 并发执行
    results = await asyncio.gather(*coroutines)

    return results
```

---

## 14. 成本监控

### 实时监控

```python
class CostMonitor:
    """成本监控"""

    def __init__(self, budget: float):
        self.budget = budget
        self.spent = 0

    def track_call(self, model: str, tokens: int):
        """跟踪调用成本"""

        cost = calculate_cost(model, tokens)
        self.spent += cost

        if self.spent > self.budget:
            raise BudgetExceeded(f"超出预算：${self.spent}")
```

---

## 15. 高级测试

### 行为测试

```python
def test_agent_behavior(agent, test_cases):
    """测试 Agent 行为"""

    results = []
    for case in test_cases:
        output = agent.run(case["input"])

        # 验证行为
        assert case["expected_behavior"] in output
        results.append(output)

    return results
```

---

## 16. 质量指标

### 评估维度

| 维度 | 指标 | 目标 |
|------|------|------|
| **准确性** | 答案正确率 | >= 90% |
| **相关性** | 检索 NDCG | >= 0.8 |
| **性能** | 响应时间 | <= 2s |
| **成本** | Token/查询 | <= 1000 |

---

## 快速验证

### 性能优化验证

1. **测量 baseline**：记录优化前的指标
2. **应用优化**：实施优化策略
3. **对比效果**：验证改进幅度
4. **持续监控**：确保稳定性

### 测试验证

1. **单元测试**：测试每个组件
2. **集成测试**：测试完整流程
3. **性能测试**：测试响应时间
4. **A/B 测试**：对比新旧方案

---

## 下一步

- 🧪 运行代码示例
- ✏ 完成练习题
- 🎯 完成综合项目

---

**记住：优化是一个持续的过程，先测量，再优化！** 📈⚡
