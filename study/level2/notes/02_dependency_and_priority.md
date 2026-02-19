# 依赖管理与任务优先级

> **目标**: 掌握 DAG 中的依赖关系管理和优先级调度
> **预计时间**: 40 分钟
> **难度**: ⭐⭐⭐

---

## 为什么需要依赖管理？

在任务执行中，依赖关系决定了执行顺序：

**问题 1：执行顺序**
- 某些任务必须先完成，其他任务才能开始
- 例如：必须先"获取数据"，才能"分析数据"

**问题 2：死锁风险**
- 循环依赖会导致死锁
- 例如：A 依赖 B，B 依赖 A（无法执行）

**问题 3：优先级冲突**
- 多个可执行任务，应该先执行哪个？
- 例如：同时有"搜索"和"计算"任务，哪个更重要？

---

## 依赖关系表示

### 方式 1：前置依赖列表

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Task:
    """任务定义"""
    id: str
    description: str
    dependencies: List[str]  # 前置任务 ID 列表
    priority: int = 0  # 优先级（越大越重要）
```

**示例**：
```python
tasks = [
    Task(id="A", description="搜索文档", dependencies=[]),
    Task(id="B", description="搜索示例", dependencies=[]),
    Task(id="C", description="提取特性", dependencies=["A", "B"]),
    Task(id="D", description="总结要点", dependencies=["C"]),
]
```

**可视化**：
```
A ─┐
    ├─> C ─> D
B ─┘
```

---

### 方式 2：依赖图（邻接表）

```python
class DependencyGraph:
    """依赖图"""

    def __init__(self):
        self.graph: Dict[str, List[str]] = {}  # task -> dependencies

    def add_task(self, task_id: str, dependencies: List[str]):
        """添加任务及其依赖"""
        self.graph[task_id] = dependencies

    def get_ready_tasks(self, completed: set) -> List[str]:
        """获取可执行任务（所有依赖都已完成）"""
        ready = []
        for task_id, deps in self.graph.items():
            if all(dep in completed for dep in deps):
                ready.append(task_id)
        return ready
```

---

## 优先级调度

### 策略 1：静态优先级

基于任务类型或业务重要性设置固定优先级。

```python
class StaticPriorityScheduler:
    """静态优先级调度器"""

    def __init__(self):
        # 定义任务类型的优先级
        self.type_priority = {
            "search": 10,      # 搜索最优先
            "calculate": 8,    # 计算次之
            "llm_query": 5,    # LLM 查询
            "summarize": 3,    # 总结
        }

    def get_priority(self, task: Task) -> int:
        """获取任务优先级"""
        return self.type_priority.get(task.type, 0)

    def select_task(self, ready_tasks: List[Task]) -> Task:
        """从可执行任务中选择优先级最高的"""
        return max(ready_tasks, key=self.get_priority)
```

---

### 策略 2：动态优先级

根据执行状态动态调整优先级。

```python
class DynamicPriorityScheduler:
    """动态优先级调度器"""

    def __init__(self):
        self.waiting_time = {}  # 任务等待时间
        self.failed_attempts = {}  # 失败尝试次数

    def update_priority(self, task: Task, base_priority: int) -> int:
        """动态更新优先级"""
        # 等待越久，优先级越高
        waiting_bonus = self.waiting_time.get(task.id, 0) * 2

        # 失败越多，优先级越低
        failed_penalty = self.failed_attempts.get(task.id, 0) * 5

        return base_priority + waiting_bonus - failed_penalty

    def select_task(self, ready_tasks: List[Task]) -> Task:
        """选择优先级最高的任务"""
        prioritized = []
        for task in ready_tasks:
            priority = self.update_priority(task, task.priority)
            prioritized.append((task, priority))

        return max(prioritized, key=lambda x: x[1])[0]
```

---

### 策略 3：多因素优先级

综合考虑多个因素。

```python
class MultiFactorScheduler:
    """多因素优先级调度器"""

    def calculate_score(self, task: Task, context: Dict) -> float:
        """计算任务综合得分"""
        score = 0.0

        # 因素 1：基础优先级（权重 0.3）
        score += task.priority * 0.3

        # 因素 2：依赖数量（权重 0.2）
        # 依赖越多的任务越先执行（解锁其他任务）
        dep_count = len(task.dependencies)
        score += min(dep_count * 2, 10) * 0.2

        # 因素 3：估计时间（权重 0.2）
        # 短任务优先（快速反馈）
        est_time = context.get("estimated_time", {}).get(task.id, 10)
        score += max(10 - est_time, 0) * 0.2

        # 因素 4：失败率（权重 0.3）
        # 失败率低的任务优先
        fail_rate = context.get("fail_rate", {}).get(task.id, 0)
        score += (1 - fail_rate) * 10 * 0.3

        return score

    def select_task(self, ready_tasks: List[Task], context: Dict) -> Task:
        """选择综合得分最高的任务"""
        return max(ready_tasks, key=lambda t: self.calculate_score(t, context))
```

---

## 依赖检查与验证

### 检查 1：循环依赖检测

```python
class CycleDetector:
    """循环依赖检测器"""

    def has_cycle(self, graph: Dict[str, List[str]]) -> bool:
        """检测是否存在循环依赖"""
        visited = set()
        rec_stack = set()

        def visit(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if visit(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if visit(node):
                    return True

        return False
```

**示例**：
```python
# 无环图
graph1 = {
    "A": [],
    "B": [],
    "C": ["A", "B"],
    "D": ["C"]
}
print(cycle_detector.has_cycle(graph1))  # False

# 有环图
graph2 = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A"]  # 循环！
}
print(cycle_detector.has_cycle(graph2))  # True
```

---

### 检查 2：依赖完整性验证

```python
class DependencyValidator:
    """依赖验证器"""

    def validate(self, tasks: List[Task]) -> List[str]:
        """验证依赖关系，返回错误列表"""
        errors = []
        task_ids = {t.id for t in tasks}

        for task in tasks:
            for dep_id in task.dependencies:
                # 检查依赖的任务是否存在
                if dep_id not in task_ids:
                    errors.append(
                        f"任务 {task.id} 依赖不存在的任务: {dep_id}"
                    )

        return errors
```

---

## 完整示例：依赖管理与优先级调度

```python
from typing import List, Dict, Set
from dataclasses import dataclass
import time

@dataclass
class Task:
    """任务定义"""
    id: str
    type: str
    description: str
    dependencies: List[str]
    priority: int = 0
    estimated_time: int = 10  # 分钟


class DependencyManager:
    """依赖管理器"""

    def __init__(self, tasks: List[Task]):
        self.tasks = {t.id: t for t in tasks}
        self.completed: Set[str] = set()
        self.failed: Set[str] = set()

    def get_ready_tasks(self) -> List[Task]:
        """获取可执行任务"""
        ready = []
        for task in self.tasks.values():
            if task.id in self.completed or task.id in self.failed:
                continue

            # 检查所有依赖是否完成
            if all(dep in self.completed for dep in task.dependencies):
                ready.append(task)

        return ready

    def mark_completed(self, task_id: str):
        """标记任务完成"""
        self.completed.add(task_id)

    def mark_failed(self, task_id: str):
        """标记任务失败"""
        self.failed.add(task_id)


class PriorityScheduler:
    """优先级调度器"""

    def __init__(self):
        self.waiting_time = {}  # task_id -> seconds
        self.fail_count = {}    # task_id -> count

    def select_task(self, ready_tasks: List[Task]) -> Task:
        """选择优先级最高的任务"""
        best_task = None
        best_score = -1

        for task in ready_tasks:
            score = self._calculate_score(task)
            if score > best_score:
                best_score = score
                best_task = task

        return best_task

    def _calculate_score(self, task: Task) -> float:
        """计算任务得分"""
        # 基础优先级
        score = task.priority

        # 等待时间加成（每等待 10 秒 +1 分）
        waiting = self.waiting_time.get(task.id, 0)
        score += waiting / 10

        # 失败次数惩罚（每次失败 -5 分）
        fails = self.fail_count.get(task.id, 0)
        score -= fails * 5

        # 短任务优先（快速反馈）
        score += max(10 - task.estimated_time, 0)

        return score

    def update_waiting(self, task_id: str, seconds: int):
        """更新等待时间"""
        self.waiting_time[task_id] = self.waiting_time.get(task_id, 0) + seconds

    def record_failure(self, task_id: str):
        """记录失败"""
        self.fail_count[task_id] = self.fail_count.get(task_id, 0) + 1


class TaskExecutor:
    """任务执行器"""

    def __init__(self):
        self.dependency_manager = None
        self.scheduler = PriorityScheduler()

    def execute(self, tasks: List[Task]) -> Dict[str, str]:
        """执行所有任务"""
        self.dependency_manager = DependencyManager(tasks)
        results = {}

        print("[任务执行] 开始执行")
        print(f"任务总数: {len(tasks)}\n")

        start_time = time.time()

        while True:
            # 获取可执行任务
            ready = self.dependency_manager.get_ready_tasks()

            if not ready:
                break  # 没有可执行任务

            # 选择优先级最高的任务
            task = self.scheduler.select_task(ready)

            print(f"[执行] {task.id}: {task.description}")
            print(f"  类型: {task.type}")
            print(f"  优先级: {task.priority}")

            # 执行任务
            try:
                result = self._execute_task(task)
                results[task.id] = result
                self.dependency_manager.mark_completed(task.id)
                print(f"  ✓ 完成\n")

            except Exception as e:
                results[task.id] = f"失败: {str(e)}"
                self.dependency_manager.mark_failed(task.id)
                self.scheduler.record_failure(task.id)
                print(f"  ✗ 失败: {e}\n")

        # 更新等待时间
        elapsed = int(time.time() - start_time)
        for task in tasks:
            if task.id not in self.dependency_manager.completed:
                self.scheduler.update_waiting(task.id, elapsed)

        completed = len(self.dependency_manager.completed)
        failed = len(self.dependency_manager.failed)

        print(f"[执行完成] 成功: {completed}, 失败: {failed}")
        return results

    def _execute_task(self, task: Task) -> str:
        """执行单个任务（模拟）"""
        if task.type == "search":
            return f"搜索完成: {task.description}"
        elif task.type == "calculate":
            return f"计算完成: {task.description}"
        elif task.type == "llm_query":
            return f"LLM 处理完成: {task.description}"
        else:
            return f"执行完成: {task.description}"


# 运行示例
def main():
    print("=" * 70)
    print("依赖管理与优先级调度示例")
    print("=" * 70)

    # 定义任务
    tasks = [
        Task(
            id="search_docs",
            type="search",
            description="搜索 LangGraph 文档",
            dependencies=[],
            priority=10,
            estimated_time=5
        ),
        Task(
            id="search_examples",
            type="search",
            description="搜索 LangGraph 示例",
            dependencies=[],
            priority=10,
            estimated_time=5
        ),
        Task(
            id="extract_features",
            type="llm_query",
            description="提取关键特性",
            dependencies=["search_docs", "search_examples"],
            priority=8,
            estimated_time=8
        ),
        Task(
            id="summarize",
            type="llm_query",
            description="总结核心要点",
            dependencies=["extract_features"],
            priority=6,
            estimated_time=6
        ),
        Task(
            id="calculate_metrics",
            type="calculate",
            description="计算统计指标",
            dependencies=[],
            priority=7,
            estimated_time=3
        ),
    ]

    # 执行任务
    executor = TaskExecutor()
    results = executor.execute(tasks)

    print("\n" + "=" * 70)
    print("执行结果汇总")
    print("=" * 70)
    for task_id, result in results.items():
        print(f"{task_id}: {result}")


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：优先级策略选择

**静态优先级**：
- 优点：简单、可预测
- 适用：任务重要性固定不变

**动态优先级**：
- 优点：自适应、公平
- 适用：需要平衡等待时间和成功率

**多因素优先级**：
- 优点：综合决策
- 适用：复杂场景

---

### 考虑 2：依赖检查时机

**计划时检查**：在创建计划时检查
- 优点：早期发现问题
- 缺点：无法处理运行时变化

**执行时检查**：在执行前检查
- 优点：灵活处理变化
- 缺点：可能在后期才发现问题

**推荐**：两者结合

---

### 考虑 3：失败处理策略

**策略 1：跳过失败任务**
- 继续执行其他任务
- 适用：失败任务不重要

**策略 2：停止执行**
- 遇到失败立即停止
- 适用：失败任务影响后续

**策略 3：部分完成**
- 标记失败，继续执行不依赖的任务
- 适用：允许部分成功

---

## 最小验证

- [ ] 能够实现依赖图检查
- [ ] 能够检测循环依赖
- [ ] 能够实现优先级调度
- [ ] 能够处理任务失败

---

## 下一步

- 📖 `notes/03_execution_state_machine.md` - 执行状态机
- 🧪 `examples/03_dependency_manager.py` - 依赖管理示例

---

**记住：依赖管理决定了执行顺序，优先级调度决定了执行效率！** 🎯
