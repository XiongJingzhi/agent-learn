# 02. 层次化架构深入

> **主题**: 深入理解 Manager-Agent 架构
> **时间**: 60 分钟
> **难度**: ⭐⭐⭐

---

## 🎯 学习目标

1. ✅ 理解层次化架构的设计原理
2. ✅ 掌握 Manager 的职责和实现
3. ✅ 掌握 Worker 的设计和实现
4. ✅ 能够设计完整的层次化系统

---

## 📚 核心概念

### 什么是层次化架构？

**定义**: 一种有明确层级关系的多智能体架构，通常包含一个 Manager 和多个 Worker Agents。

**结构**:
```
        Level 1: Manager
       /      |      \
  Level 2:  W1      W2      W3
            |      |      |
  Level 3:  T1     T2     T3  (子任务)
```

**核心特点**:
1. **明确的指挥链**: Manager → Worker → 子任务
2. **集中决策**: Manager 负责全局决策
3. **职责分离**: 每个 Agent 有明确的职责
4. **结果汇总**: 所有结果最终汇总到 Manager

---

## 🏗️ 架构设计

### 组件职责

#### 1. Manager Agent

**职责**:
- 接收用户请求
- 分析和分解任务
- 分配任务给 Workers
- 协调 Workers 的执行
- 汇总结果
- 返回最终答案

**能力要求**:
- 任务理解能力
- 任务分解能力
- 资源调度能力
- 结果综合能力

#### 2. Worker Agents

**职责**:
- 接收 Manager 分配的任务
- 执行具体工作
- 返回执行结果
- 可能需要与其他 Workers 协作

**类型**:
- **专业型**: 擅长特定领域（如研究员、分析师）
- **通用型**: 可处理多种任务
- **辅助型**: 支持其他 Workers

---

## 💡 设计模式

### 模式 1: 任务分解树

```python
class TaskDecomposer:
    """任务分解器"""

    def __init__(self):
        self.decomposition_rules = {}

    def add_rule(self, pattern: str, subtasks: List[str]):
        """添加分解规则"""
        self.decomposition_rules[pattern] = subtasks

    def decompose(self, task: str) -> List[Task]:
        """分解任务"""
        # 查找匹配的规则
        for pattern, subtasks in self.decomposition_rules.items():
            if pattern in task:
                return [Task(f"{subtask}: {task}") for subtask in subtasks]

        # 默认分解
        return [Task(task)]

# 使用
decomposer = TaskDecomposer()
decomposer.add_rule("写文章", ["研究", "写作", "审核"])
decomposer.add_rule("分析数据", ["收集", "分析", "报告"])

tasks = decomposer.decompose("写一篇关于 AI 的文章")
# 输出: [Task("研究: 写一篇关于 AI 的文章"),
#        Task("写作: 写一篇关于 AI 的文章"),
#        Task("审核: 写一篇关于 AI 的文章")]
```

---

### 模式 2: 技能路由

```python
class SkillRouter:
    """技能路由器"""

    def __init__(self):
        self.worker_skills = {}  # worker -> [skills]

    def register_worker(self, worker: str, skills: List[str]):
        """注册 Worker 及其技能"""
        self.worker_skills[worker] = skills

    def route(self, task: str) -> str:
        """根据任务路由到合适的 Worker"""
        best_worker = None
        best_score = 0

        for worker, skills in self.worker_skills.items():
            score = self._calculate_match(task, skills)
            if score > best_score:
                best_score = score
                best_worker = worker

        return best_worker

    def _calculate_match(self, task: str, skills: List[str]) -> int:
        """计算任务与技能的匹配度"""
        score = 0
        for skill in skills:
            if skill.lower() in task.lower():
                score += 1
        return score

# 使用
router = SkillRouter()
router.register_worker("研究员", ["研究", "调查", "分析"])
router.register_worker("作家", ["写作", "创作", "编辑"])
router.register_worker("审核员", ["审核", "校对", "检查"])

worker = router.route("研究 AI 技术")
# 输出: "研究员"
```

---

### 模式 3: 结果聚合

```python
class ResultAggregator:
    """结果聚合器"""

    def __init__(self):
        self.aggregation_strategies = {}

    def add_strategy(self, result_type: str, strategy: callable):
        """添加聚合策略"""
        self.aggregation_strategies[result_type] = strategy

    def aggregate(self, results: List[dict]) -> dict:
        """聚合多个结果"""
        if not results:
            return {}

        # 判断结果类型
        result_type = self._identify_type(results[0])

        # 使用对应的聚合策略
        if result_type in self.aggregation_strategies:
            return self.aggregation_strategies[result_type](results)

        # 默认聚合：合并
        return self._merge_results(results)

    def _identify_type(self, result: dict) -> str:
        """识别结果类型"""
        if "text" in result:
            return "text"
        elif "data" in result:
            return "data"
        elif "score" in result:
            return "score"
        else:
            return "general"

    def _merge_results(self, results: List[dict]) -> dict:
        """合并结果"""
        merged = {}
        for result in results:
            merged.update(result)
        return merged

# 使用
aggregator = ResultAggregator()

# 文本聚合策略
def aggregate_text(results):
    return {"text": "\n".join(r["text"] for r in results)}

aggregator.add_strategy("text", aggregate_text)

# 数据聚合策略
def aggregate_data(results):
    merged_data = {}
    for result in results:
        merged_data.update(result["data"])
    return {"data": merged_data}

aggregator.add_strategy("data", aggregate_data)

results = [
    {"text": "研究结果：AI 很重要"},
    {"text": "分析结果：AI 发展迅速"},
    {"text": "总结：AI 值得学习"}
]

aggregated = aggregator.aggregate(results)
# 输出: {"text": "研究结果：AI 很重要\n分析结果：AI 发展迅速\n总结：AI 值得学习"}
```

---

## 🔧 完整实现

### 高级 Manager Agent

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    description: str
    assigned_to: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    dependencies: List[str] = None
    priority: int = 0

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class AdvancedManager:
    """高级 Manager Agent"""

    def __init__(self, name: str = "AdvancedManager"):
        self.name = name
        self.workers: Dict[str, 'WorkerAgent'] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: Dict[str, Task] = {}
        self.failed_tasks: Dict[str, Task] = {}

        # 组件
        self.decomposer = TaskDecomposer()
        self.router = SkillRouter()
        self.aggregator = ResultAggregator()

        # 统计
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_time": 0
        }

    def add_worker(self, worker: 'WorkerAgent'):
        """添加 Worker"""
        self.workers[worker.name] = worker
        # 注册技能
        self.router.register_worker(worker.name, worker.skills)

    def process(self, user_request: str) -> str:
        """处理用户请求"""
        start_time = time.time()

        print(f"\n[{self.name}] 处理请求: {user_request}")

        # 1. 分解任务
        tasks = self.decompose_task(user_request)

        # 2. 分配任务
        self.assign_tasks(tasks)

        # 3. 执行任务
        results = self.execute_tasks(tasks)

        # 4. 聚合结果
        final_result = self.aggregate_results(results)

        # 5. 更新统计
        elapsed = time.time() - start_time
        self.stats["total_time"] += elapsed
        self.stats["total_tasks"] += len(tasks)

        return final_result

    def decompose_task(self, request: str) -> List[Task]:
        """分解任务"""
        print(f"[{self.name}] 分解任务...")

        subtasks = self.decomposer.decompose(request)

        for i, subtask in enumerate(subtasks):
            subtask.id = f"task_{i}"

        print(f"[{self.name}] 分解为 {len(subtasks)} 个子任务")
        return subtasks

    def assign_tasks(self, tasks: List[Task]):
        """分配任务"""
        print(f"[{self.name}] 分配任务...")

        for task in tasks:
            worker = self.router.route(task.description)
            if worker:
                task.assigned_to = worker
                task.status = TaskStatus.ASSIGNED
                self.workers[worker].receive_task(task)
                print(f"  ✓ {task.description} → {worker}")
            else:
                print(f"  ✗ 无法分配任务: {task.description}")

    def execute_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        """执行任务"""
        print(f"[{self.name}] 执行任务...")

        results = {}

        # 按依赖关系排序
        sorted_tasks = self._sort_by_dependencies(tasks)

        for task in sorted_tasks:
            # 检查依赖是否完成
            if not self._check_dependencies(task):
                print(f"  ⏳ {task.description} 等待依赖...")
                continue

            worker = self.workers.get(task.assigned_to)
            if worker:
                task.status = TaskStatus.IN_PROGRESS
                result = worker.execute(task)
                task.result = result
                task.status = TaskStatus.COMPLETED
                results[task.id] = result
                self.completed_tasks[task.id] = task
                self.stats["completed_tasks"] += 1

        return results

    def aggregate_results(self, results: Dict[str, Any]) -> str:
        """聚合结果"""
        print(f"[{self.name}] 聚合结果...")

        # 转换为列表格式
        results_list = [{"result": r} for r in results.values()]

        aggregated = self.aggregator.aggregate(results_list)

        return str(aggregated)

    def _sort_by_dependencies(self, tasks: List[Task]) -> List[Task]:
        """按依赖关系排序（拓扑排序）"""
        # 简化实现：按优先级排序
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def _check_dependencies(self, task: Task) -> bool:
        """检查依赖是否完成"""
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
        return True

    def get_statistics(self) -> dict:
        """获取统计信息"""
        return {
            **self.stats,
            "success_rate": self.stats["completed_tasks"] / max(1, self.stats["total_tasks"]),
            "avg_time_per_task": self.stats["total_time"] / max(1, self.stats["completed_tasks"])
        }
```

---

### 高级 Worker Agent

```python
class WorkerAgent:
    """高级 Worker Agent"""

    def __init__(self, name: str, role: str, skills: List[str]):
        self.name = name
        self.role = role
        self.skills = skills
        self.current_task: Optional[Task] = None
        self.completed_tasks: List[Task] = []

        # 统计
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_time": 0
        }

    def receive_task(self, task: Task):
        """接收任务"""
        self.current_task = task
        print(f"[{self.name}] 接收任务: {task.description}")

    def execute(self, task: Task) -> Any:
        """执行任务"""
        import time
        start = time.time()

        print(f"[{self.name}] 执行任务: {task.description}")

        # 根据角色执行不同的工作
        if "研究" in self.role:
            result = self._do_research(task.description)
        elif "作家" in self.role or "写作" in self.role:
            result = self._do_writing(task.description)
        elif "审核" in self.role:
            result = self._do_review(task.description)
        else:
            result = self._do_general_work(task.description)

        elapsed = time.time() - start

        # 更新统计
        self.stats["total_tasks"] += 1
        self.stats["completed_tasks"] += 1
        self.stats["total_time"] += elapsed

        self.completed_tasks.append(task)
        self.current_task = None

        return result

    def _do_research(self, topic: str) -> dict:
        """研究工作"""
        return {
            "type": "research",
            "findings": f"关于 {topic} 的研究发现",
            "sources": ["论文1", "论文2", "论文3"],
            "confidence": 0.9
        }

    def _do_writing(self, topic: str) -> dict:
        """写作工作"""
        return {
            "type": "writing",
            "content": f"关于 {topic} 的文章内容",
            "word_count": 1000,
            "readability": 0.8
        }

    def _do_review(self, content: str) -> dict:
        """审核工作"""
        return {
            "type": "review",
            "feedback": "内容质量良好",
            "suggestions": ["增加案例", "补充数据"],
            "approval": True
        }

    def _do_general_work(self, task: str) -> dict:
        """通用工作"""
        return {
            "type": "general",
            "result": f"完成 {task}",
            "status": "success"
        }

    def get_statistics(self) -> dict:
        """获取统计信息"""
        return {
            **self.stats,
            "success_rate": self.stats["completed_tasks"] / max(1, self.stats["total_tasks"]),
            "avg_time_per_task": self.stats["total_time"] / max(1, self.stats["completed_tasks"])
        }
```

---

## 🎯 设计考虑

### 1. 任务分解策略

#### 策略 A: 并行分解

```python
# 原任务可以并行执行
原任务: "研究 AI、区块链、量子计算"

分解为:
- Worker1: 研究 AI
- Worker2: 研究区块链
- Worker3: 研究量子计算
```

#### 策略 B: 串行分解

```python
# 原任务需要顺序执行
原任务: "写一篇文章"

分解为:
- Worker1: 研究主题
- Worker2: 撰写草稿 (依赖 Worker1)
- Worker3: 审核修改 (依赖 Worker2)
```

#### 策略 C: 混合分解

```python
# 部分并行，部分串行
原任务: "完成市场分析报告"

分解为:
- Worker1: 收集数据 (并行)
- Worker2: 分析趋势 (并行，依赖 Worker1)
- Worker3: 撰写报告 (串行，依赖 Worker1, Worker2)
```

---

### 2. 负载均衡

```python
class LoadBalancer:
    """负载均衡器"""

    def __init__(self):
        self.worker_loads = {}  # worker -> task_count

    def select_worker(self, candidates: List[str]) -> str:
        """选择负载最少的 Worker"""
        min_load = float('inf')
        selected = None

        for worker in candidates:
            load = self.worker_loads.get(worker, 0)
            if load < min_load:
                min_load = load
                selected = worker

        if selected:
            self.worker_loads[selected] = min_load + 1

        return selected

    def release_worker(self, worker: str):
        """释放 Worker"""
        if worker in self.worker_loads:
            self.worker_loads[worker] -= 1
```

---

### 3. 错误处理

```python
class ErrorHandler:
    """错误处理器"""

    def __init__(self):
        self.retry_policies = {}
        self.fallback_workers = {}

    def set_retry_policy(self, task_type: str, max_retries: int):
        """设置重试策略"""
        self.retry_policies[task_type] = max_retries

    def set_fallback_worker(self, primary: str, fallback: str):
        """设置备用 Worker"""
        self.fallback_workers[primary] = fallback

    def handle_failure(self, task: Task, error: Exception) -> bool:
        """处理失败"""
        print(f"[ErrorHandler] 任务失败: {task.description}, 错误: {error}")

        # 尝试重试
        task_type = task.description.split()[0]
        if task_type in self.retry_policies:
            max_retries = self.retry_policies[task_type]
            if task.failed_attempts < max_retries:
                task.failed_attempts += 1
                print(f"[ErrorHandler] 重试 ({task.failed_attempts}/{max_retries})")
                return True

        # 尝试备用 Worker
        if task.assigned_to in self.fallback_workers:
            fallback = self.fallback_workers[task.assigned_to]
            print(f"[ErrorHandler] 使用备用 Worker: {fallback}")
            task.assigned_to = fallback
            return True

        # 无法恢复
        print(f"[ErrorHandler] 任务永久失败")
        return False
```

---

## 🎓 费曼解释

### 给 5 岁孩子的解释

**层次化架构就像一个建筑团队**：

```
    工地经理 (Manager)
       /   |   \
   木匠  水管工  电工 (Workers)
     |      |      |
   做门   装水管   装灯 (子任务)
```

**工作流程**:
1. **经理**接收任务："建造一个房子"
2. **经理**分解任务："做门、装水管、装灯"
3. **经理**分配任务：木匠做门、水管工装水管、电工装灯
4. **Workers**各司其职，完成任务
5. **经理**检查结果，确认房子建好了

### 关键要点

1. **Manager 是大脑** - 负责思考和指挥
2. **Workers 是手脚** - 负责执行具体工作
3. **清晰的分工** - 每个人都知道自己的职责
4. **结果汇总** - 所有人向 Manager 汇报

---

## 💡 最佳实践

### 1. Manager 设计

- ✅ 保持简洁，只做协调
- ✅ 明确任务分解规则
- ✅ 提供清晰的反馈
- ❌ 不要做所有工作
- ❌ 不要过度控制 Worker

### 2. Worker 设计

- ✅ 专注自己的职责
- ✅ 返回结构化结果
- ✅ 处理异常情况
- ❌ 不要越权决策
- ❌ 不要直接与其他 Worker 通信

### 3. 系统设计

- ✅ 明确的职责边界
- ✅ 清晰的通信协议
- ✅ 完善的错误处理
- ❌ 避免循环依赖
- ❌ 避免过度嵌套

---

## 🔗 相关资源

- [Manager-Worker Pattern](https://en.wikipedia.org/wiki/Manager%E2%80%93worker_pattern)
- [Task Decomposition](https://en.wikipedia.org/wiki/Decomposition_(computer_science))
- [Hierarchical Planning](https://en.wikipedia.org/wiki/Hierarchical_task_network)

---

## ✅ 最小验证

### 任务

1. 实现一个任务分解器（15 分钟）
2. 实现一个技能路由器（15 分钟）
3. 实现一个结果聚合器（15 分钟）
4. 集成到完整系统中（15 分钟）

### 期望输出

- [ ] 可运行的任务分解代码
- [ ] 可运行的技能路由代码
- [ ] 可运行的结果聚合代码
- [ ] 集成测试通过

---

## 🚀 下一步

学习完本笔记后，继续学习：
- `notes/03_flat_architecture.md` - 扁平化架构
- `examples/01_hierarchical_agents.py` - 完整实现

---

**记住：层次化架构的核心是清晰的职责分工和有效的协调！** 🏗️
