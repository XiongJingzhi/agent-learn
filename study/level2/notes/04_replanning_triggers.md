# 重规划触发机制

> **目标**: 掌握何时以及如何触发重新规划
> **预计时间**: 30 分钟
> **难度**: ⭐⭐⭐

---

## 为什么需要重规划？

在执行过程中，可能遇到各种意外情况：

**情况 1：执行失败**
- 任务执行失败，原计划无法继续
- 需要调整策略或寻找替代方案

**情况 2：发现新信息**
- 执行过程中发现了新的关键信息
- 原计划可能不再最优

**情况 3：目标变化**
- 用户修改了目标或要求
- 需要重新制定计划

**情况 4：资源限制**
- 遇到 API 限制、超时等资源问题
- 需要调整执行策略

---

## 重规划触发条件

### 条件 1：失败率过高

```python
class FailureRateTrigger:
    """失败率触发器"""

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold  # 失败率阈值
        self.total_tasks = 0
        self.failed_tasks = 0

    def record_success(self):
        """记录成功"""
        self.total_tasks += 1

    def record_failure(self):
        """记录失败"""
        self.total_tasks += 1
        self.failed_tasks += 1

    def should_replan(self) -> bool:
        """判断是否需要重规划"""
        if self.total_tasks == 0:
            return False

        failure_rate = self.failed_tasks / self.total_tasks
        return failure_rate >= self.threshold

    def reset(self):
        """重置计数器"""
        self.total_tasks = 0
        self.failed_tasks = 0
```

---

### 条件 2：发现新信息

```python
class NewInformationTrigger:
    """新信息触发器"""

    def __init__(self):
        self.initial_knowledge = set()
        self.current_knowledge = set()

    def set_initial_knowledge(self, knowledge: set):
        """设置初始知识"""
        self.initial_knowledge = knowledge.copy()
        self.current_knowledge = knowledge.copy()

    def add_information(self, info: str):
        """添加新信息"""
        self.current_knowledge.add(info)

    def should_replan(self) -> bool:
        """判断是否有足够的新信息触发重规划"""
        new_info = self.current_knowledge - self.initial_knowledge

        # 如果新信息超过初始信息的 50%
        if len(self.initial_knowledge) == 0:
            return len(new_info) > 5

        return len(new_info) / len(self.initial_knowledge) >= 0.5
```

---

### 条件 3：执行超时

```python
import time
from datetime import datetime, timedelta

class TimeoutTrigger:
    """超时触发器"""

    def __init__(self, max_duration_minutes: int = 30):
        self.max_duration = timedelta(minutes=max_duration_minutes)
        self.start_time = None

    def start(self):
        """开始计时"""
        self.start_time = datetime.now()

    def should_replan(self) -> bool:
        """判断是否超时"""
        if self.start_time is None:
            return False

        elapsed = datetime.now() - self.start_time
        return elapsed >= self.max_duration
```

---

### 条件 4：用户干预

```python
class UserInterventionTrigger:
    """用户干预触发器"""

    def __init__(self):
        self.intervention_requested = False
        self.intervention_reason = None

    def request_intervention(self, reason: str):
        """请求干预"""
        self.intervention_requested = True
        self.intervention_reason = reason

    def should_replan(self) -> bool:
        """判断是否需要重规划"""
        return self.intervention_requested

    def reset(self):
        """重置"""
        self.intervention_requested = False
        self.intervention_reason = None
```

---

## 重规划决策器

```python
from typing import List

class ReplanningDecision:
    """重规划决策"""

    def __init__(self):
        self.triggers = []

    def add_trigger(self, trigger):
        """添加触发器"""
        self.triggers.append(trigger)

    def should_replan(self) -> tuple[bool, str]:
        """判断是否需要重规划"""
        reasons = []

        for trigger in self.triggers:
            if trigger.should_replan():
                reason = self._get_trigger_reason(trigger)
                reasons.append(reason)

        if reasons:
            return True, "; ".join(reasons)

        return False, ""

    def _get_trigger_reason(self, trigger) -> str:
        """获取触发原因"""
        if isinstance(trigger, FailureRateTrigger):
            rate = trigger.failed_tasks / trigger.total_tasks if trigger.total_tasks > 0 else 0
            return f"失败率过高: {rate:.2%}"

        elif isinstance(trigger, NewInformationTrigger):
            new_count = len(trigger.current_knowledge - trigger.initial_knowledge)
            return f"发现新信息: {new_count} 条"

        elif isinstance(trigger, TimeoutTrigger):
            return "执行超时"

        elif isinstance(trigger, UserInterventionTrigger):
            return f"用户干预: {trigger.intervention_reason}"

        return "未知原因"
```

---

## 重规划策略

### 策略 1：完全重规划

丢弃当前计划，从零开始重新规划。

```python
def full_replan(planner, input: str, context: dict):
    """完全重规划"""
    print("[重规划] 完全重新规划")

    # 保留已完成的有效结果
    completed_results = {
        k: v for k, v in context.items()
        if v.get("status") == "completed"
    }

    # 重新制定计划
    new_plan = planner.plan(input, context.get("available_tools", []))

    # 融入已完成的结果
    for task_id, result in completed_results.items():
        if task_id in [t.id for t in new_plan.tasks]:
            # 保留已完成任务的结果
            task = next(t for t in new_plan.tasks if t.id == task_id)
            task.result = result["data"]

    return new_plan
```

---

### 策略 2：增量重规划

保留已完成的部分，只调整剩余任务。

```python
def incremental_replan(planner, current_plan, failed_tasks: list, context: dict):
    """增量重规划"""
    print("[重规划] 增量重规划")

    # 获取已完成和待执行的任务
    completed = [t for t in current_plan.tasks if t.status == "completed"]
    remaining = [t for t in current_plan.tasks if t.status not in ["completed", "failed"]]

    # 分析失败原因
    failure_reasons = {t.id: t.result for t in failed_tasks}

    # 调整剩余任务的顺序或参数
    for task in remaining:
        # 如果任务依赖失败任务，需要调整
        for dep in task.dependencies:
            if dep in failure_reasons:
                # 策略 1：移除依赖（如果可能）
                # 策略 2：添加替代任务
                # 策略 3：调整任务参数
                pass

    return current_plan
```

---

### 策略 3：局部重规划

只重新规划受影响的子任务。

```python
def local_replan(planner, current_plan, affected_task_ids: list, context: dict):
    """局部重规划"""
    print("[重规划] 局部重规划")

    # 找出受影响的任务及其依赖者
    affected_tasks = set(affected_task_ids)
    for task_id in affected_task_ids:
        # 找出依赖此任务的其他任务
        dependents = [
            t.id for t in current_plan.tasks
            if task_id in t.dependencies
        ]
        affected_tasks.update(dependents)

    # 只重新规划受影响的任务
    # （具体实现取决于规划器的设计）

    return current_plan
```

---

## 完整示例：重规划系统

```python
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class ReplanningSystem:
    """重规划系统"""

    def __init__(self, planner):
        self.planner = planner
        self.decision = ReplanningDecision()
        self.max_replans = 3
        self.replan_count = 0

        # 设置触发器
        self.decision.add_trigger(FailureRateTrigger(threshold=0.5))
        self.decision.add_trigger(TimeoutTrigger(max_duration_minutes=30))
        self.decision.add_trigger(NewInformationTrigger())
        self.decision.add_trigger(UserInterventionTrigger())

    def check_replanning(self, execution_context: dict) -> Optional[str]:
        """检查是否需要重规划"""
        should_replan, reason = self.decision.should_replan()

        if should_replan and self.replan_count < self.max_replans:
            return reason

        return None

    def replan(self, input: str, current_plan, execution_context: dict, strategy: str = "incremental"):
        """执行重规划"""
        if self.replan_count >= self.max_replans:
            print("[重规划] 已达到最大重规划次数")
            return current_plan

        self.replan_count += 1
        print(f"\n[重规划] 第 {self.replan_count} 次重规划")
        print(f"原因: {execution_context.get('replan_reason', '未知')}")

        # 选择策略
        if strategy == "full":
            return full_replan(self.planner, input, execution_context)
        elif strategy == "incremental":
            failed_tasks = [t for t in current_plan.tasks if t.status == "failed"]
            return incremental_replan(self.planner, current_plan, failed_tasks, execution_context)
        elif strategy == "local":
            affected = execution_context.get("affected_tasks", [])
            return local_replan(self.planner, current_plan, affected, execution_context)
        else:
            print(f"[重规划] 未知策略: {strategy}，使用增量重规划")
            return incremental_replan(self.planner, current_plan, [], execution_context)

    def reset(self):
        """重置重规划计数"""
        self.replan_count = 0
        # 重置触发器
        for trigger in self.decision.triggers:
            if hasattr(trigger, 'reset'):
                trigger.reset()


# 使用示例
def main():
    print("=" * 70)
    print("重规划触发机制示例")
    print("=" * 70)

    # 模拟规划器
    class MockPlanner:
        def plan(self, input: str, tools: list):
            print(f"[规划] 重新规划: {input}")
            # 返回模拟计划
            from dataclasses import dataclass
            from typing import List

            @dataclass
            class Task:
                id: str
                status: str = "pending"
                result: Optional[str] = None
                dependencies: List[str] = None

                def __post_init__(self):
                    if self.dependencies is None:
                        self.dependencies = []

            return type('Plan', (), {
                'tasks': [
                    Task(id="task_1"),
                    Task(id="task_2")
                ]
            })()

    planner = MockPlanner()
    replanning_system = ReplanningSystem(planner)

    # 模拟执行过程
    print("\n[模拟执行]")

    # 记录一些成功
    for _ in range(3):
        replanning_system.decision.triggers[0].record_success()

    # 记录一些失败
    for _ in range(3):
        replanning_system.decision.triggers[0].record_failure()

    # 检查是否需要重规划
    reason = replanning_system.check_replanning({})
    if reason:
        print(f"\n触发重规划: {reason}")

        # 执行重规划
        current_plan = planner.plan("原始输入", [])
        new_plan = replanning_system.replan(
            "原始输入",
            current_plan,
            {"replan_reason": reason}
        )

        print(f"\n重规划完成，当前重规划次数: {replanning_system.replan_count}")
    else:
        print("\n不需要重规划")


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：重规划频率

**问题**：过于频繁的重规划会导致执行不稳定

**解决方案**：
- 设置最小重规划间隔
- 限制最大重规划次数
- 使用重规划冷却期

---

### 考虑 2：状态保留

**问题**：重规划时如何处理已完成任务？

**策略**：
- 保留成功任务的结果
- 分析失败任务的原因
- 调整失败任务的策略

---

### 考虑 3：策略选择

**完全重规划**：
- 适用于：目标变化、发现新信息
- 成本：高

**增量重规划**：
- 适用于：部分任务失败
- 成本：中

**局部重规划**：
- 适用于：单个任务问题
- 成本：低

---

## 最小验证

- [ ] 能够实现失败率触发
- [ ] 能够实现超时触发
- [ ] 能够实现重规划决策
- [ ] 能够实现至少一种重规划策略

---

## 下一步

- 📖 `notes/05_rollback_and_recovery.md` - 回滚与恢复
- 🧪 `examples/05_replanning.py` - 重规划示例

---

**记住：重规划是在执行中发现问题时调整策略的关键机制！** 🔄
