# 进阶练习

> **目标**: 深入理解 Level 2 复杂概念
> **预计时间**: 3 小时
> **难度**: ⭐⭐⭐

---

## 练习 1：高级任务分解

### 问题 1.1
设计一个支持优先级的任务调度器。

要求：
1. 任务有 `priority` 字段（1-10，10 最高）
2. 优先执行高优先级任务
3. 相同优先级按依赖顺序执行

<details>
<summary>查看答案</summary>

```python
class PriorityScheduler:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def get_next_task(self, completed: set) -> Task:
        # 获取所有可执行任务
        ready = [
            t for t in self.tasks.values()
            if t.id not in completed and
            all(dep in completed for dep in t.dependencies)
        ]

        if not ready:
            return None

        # 按优先级排序
        ready.sort(key=lambda t: t.priority, reverse=True)
        return ready[0]
```
</details>

---

### 问题 1.2
实现一个支持"跳过失败任务"的执行器。

当任务失败时：
1. 记录失败
2. 继续执行其他不依赖失败任务的任务

<details>
<summary>查看答案</summary>

```python
class FaultTolerantExecutor:
    def execute(self, dag: TaskDAG) -> Dict:
        completed = set()
        failed = set()
        results = {}

        while True:
            ready = [
                t for t in dag.tasks.values()
                if t.id not in completed and t.id not in failed and
                all(dep in completed for dep in t.dependencies)
            ]

            if not ready:
                break

            for task in ready:
                try:
                    result = self._execute(task)
                    results[task.id] = result
                    completed.add(task.id)
                except Exception as e:
                    failed.add(task.id)
                    results[task.id] = f"失败: {e}"

        return {"results": results, "completed": completed, "failed": failed}
```
</details>

---

## 练习 2：复杂状态管理

### 问题 2.1
实现支持"子状态"的状态机。

例如：`IN_PROGRESS` 状态可以有子状态：
- `IN_PROGRESS.fetching`
- `IN_PROGRESS.processing`
- `IN_PROGRESS.finalizing`

<details>
<summary>查看答案</summary>

```python
class HierarchicalStateMachine:
    def __init__(self):
        self.states = {
            "PENDING": {},
            "READY": {},
            "IN_PROGRESS": {
                "fetching": {},
                "processing": {},
                "finalizing": {}
            },
            "COMPLETED": {},
            "FAILED": {}
        }
        self.current_state = "PENDING"
        self.current_substate = None

    def transition_to(self, new_state: str, substate: str = None):
        # 检查主状态转换
        if substate and new_state in self.states:
            if substate not in self.states[new_state]:
                raise ValueError(f"无效的子状态: {substate}")

        self.current_state = new_state
        self.current_substate = substate
```
</details>

---

### 问题 2.2
实现一个支持"回滚"的状态机。

允许回滚到之前的某个状态。

<details>
<summary>查看答案</summary>

```python
class RollbackStateMachine:
    def __init__(self):
        self.current_state = "PENDING"
        self.history = []  # 状态历史

    def transition_to(self, new_state: str):
        # 保存当前状态到历史
        self.history.append(self.current_state)
        self.current_state = new_state

    def rollback(self, steps: int = 1):
        """回滚指定步数"""
        if steps > len(self.history):
            raise ValueError("无法回滚那么多步")

        for _ in range(steps):
            if self.history:
                self.current_state = self.history.pop()

    def rollback_to_state(self, target_state: str):
        """回滚到指定状态"""
        while self.current_state != target_state and self.history:
            self.current_state = self.history.pop()

        if self.current_state != target_state:
            raise ValueError(f"历史中不存在状态: {target_state}")
```
</details>

---

## 练习 3：记忆系统优化

### 问题 3.1
实现记忆的"重要性评分"系统。

根据以下因素计算重要性：
- 消息长度（越长越重要）
- 是否包含实体（人名、地名等）
- 用户显式标记

<details>
<summary>查看答案</summary>

```python
class ImportanceScorer:
    def score(self, message: str, user_marked: bool = False) -> float:
        score = 0.0

        # 长度因子（最多 0.3 分）
        length_score = min(len(message) / 500, 0.3)
        score += length_score

        # 实体因子（最多 0.4 分）
        entities = self._extract_entities(message)
        entity_score = min(len(entities) * 0.1, 0.4)
        score += entity_score

        # 用户标记（0.3 分）
        if user_marked:
            score += 0.3

        return min(score, 1.0)

    def _extract_entities(self, text: str) -> List[str]:
        # 简化：查找大写开头的词
        import re
        return re.findall(r'\b[A-Z][a-z]+\b', text)
```
</details>

---

### 问题 3.2
实现"记忆合并"功能。

当相似的记忆出现时，合并而不是重复存储。

<details>
<summary>查看答案</summary>

```python
class MemoryMerger:
    def __init__(self, similarity_threshold: float = 0.8):
        self.threshold = similarity_threshold

    def should_merge(self, mem1: str, mem2: str) -> bool:
        similarity = self._calculate_similarity(mem1, mem2)
        return similarity >= self.threshold

    def merge(self, mem1: str, mem2: str) -> str:
        # 简化：取较长的那个
        return mem1 if len(mem1) > len(mem2) else mem2

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        # 简化：使用词重叠率
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0
```
</details>

---

## 练习 4：推理机制实现

### 问题 4.1
实现一个简单的 CoT 推理器。

```python
class SimpleCoTReasoner:
    def reason(self, query: str) -> tuple[List[str], str]:
        """
        返回: (推理步骤, 最终答案)

        示例：
        query: "如果 3x + 5 = 20，x 是多少？"

        返回:
        ([
            "首先，我需要解方程 3x + 5 = 20",
            "然后，我减去 5：3x = 15",
            "最后，除以 3：x = 5"
        ], "x = 5")
        """
        # TODO: 实现推理逻辑
        pass
```

<details>
<summary>提示</summary>

1. 识别问题类型
2. 生成推理步骤
3. 执行推理
4. 生成答案
</details>

---

### 问题 4.2
实现一个两阶段 ToT 推理器。

阶段 1：生成多个解决方案
阶段 2：评估并选择最优

<details>
<summary>查看答案</summary>

```python
class TwoStageToT:
    def __init__(self, num_solutions: int = 3):
        self.num_solutions = num_solutions

    def reason(self, query: str) -> str:
        # 阶段 1：生成多个解决方案
        solutions = self._generate_solutions(query)

        # 阶段 2：评估并选择
        best = self._evaluate_and_select(solutions)

        return best

    def _generate_solutions(self, query: str) -> List[str]:
        solutions = []
        for i in range(self.num_solutions):
            solution = f"解决方案 {i+1}: ..."
            solutions.append(solution)
        return solutions

    def _evaluate_and_select(self, solutions: List[str]) -> str:
        # 简化：选择最长的
        return max(solutions, key=len)
```
</details>

---

## 练习 5：测试 Mock 设计

### 问题 5.1
设计一个 Mock LLM，支持：
1. 预定义响应列表
2. 基于输入的动态响应
3. 模拟延迟

<details>
<summary>查看答案</summary>

```python
class MockLLM:
    def __init__(self):
        self.responses = []
        self.response_map = {}
        self.delay = 0

    def set_responses(self, responses: List[str]):
        """设置预定义响应列表"""
        self.responses = responses

    def set_response_map(self, mapping: Dict[str, str]):
        """设置输入-响应映射"""
        self.response_map = mapping

    def set_delay(self, seconds: float):
        """设置模拟延迟"""
        self.delay = seconds

    def generate(self, input: str) -> str:
        """生成响应"""
        import time

        # 模拟延迟
        if self.delay > 0:
            time.sleep(self.delay)

        # 优先使用映射
        if input in self.response_map:
            return self.response_map[input]

        # 使用预定义列表
        if self.responses:
            return self.responses.pop(0)

        # 默认响应
        return f"Mock response for: {input}"
```
</details>

---

## 练习 6：性能优化

### 问题 6.1
如何优化记忆检索性能？

列出至少 3 种优化方法。

<details>
<summary>查看答案</summary>

1. **建立索引**：
   - 关键词索引
   - 向量索引（FAISS）

2. **缓存热门查询**：
   - LRU 缓存
   - 查询结果缓存

3. **批量处理**：
   - 批量向量计算
   - 批量数据库查询

4. **分区**：
   - 按时间分区
   - 按用户分区

5. **异步检索**：
   - 并行检索不同层次
</details>

---

## 代码挑战

### 挑战 7：实现完整的 PER Agent

结合所有概念，实现一个完整的 PER Agent：

1. **Planner**：支持多种任务类型的分解
2. **Executor**：支持重试和错误恢复
3. **Reflector**：支持多轮反思

<details>
<summary>要求</summary>

- 支持至少 3 种任务类型
- 有完整的错误处理
- 有日志记录
- 有测试覆盖
</details>

---

## 完成标准

完成本练习后，你应该能够：
- ✅ 设计复杂的任务调度系统
- ✅ 实现高级状态管理
- ✅ 优化记忆系统
- ✅ 实现多种推理机制
- ✅ 设计合理的测试 Mock
- ✅ 理解性能优化方法

---

## 下一步

- 📖 `exercises/03_challenge_projects.md` - 挑战项目
- 🚀 开始 Capstone 项目
- `projects/01_capstone_project.md`

---

**记住：进阶练习是掌握复杂概念的关键！** 🎯
