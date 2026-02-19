# 执行状态机

> **目标**: 掌握任务执行的状态管理与状态转换
> **预计时间**: 45 分钟
> **难度**: ⭐⭐⭐

---

## 什么是执行状态机？

执行状态机管理任务的生命周期，定义了任务可能的状态以及状态之间的转换规则。

**类比**：状态机就像**快递跟踪系统**，每个包裹都有明确的状态（已下单、已揽收、运输中、已签收），状态转换遵循明确的规则。

---

## 任务生命周期状态

### 状态定义

```python
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"           # 待执行
    READY = "ready"               # 准备执行（依赖满足）
    IN_PROGRESS = "in_progress"   # 执行中
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 失败
    BLOCKED = "blocked"           # 被阻塞（依赖失败）
    CANCELLED = "cancelled"       # 已取消
    RETRYING = "retrying"         # 重试中


@dataclass
class TaskState:
    """任务状态"""
    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    retry_count: int = 0
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}
```

---

## 状态转换规则

### 状态转换图

```
                    ┌─────────────────┐
                    │    PENDING      │
                    └────────┬────────┘
                             │ 依赖满足
                             ▼
                    ┌─────────────────┐
                    │     READY       │
                    └────────┬────────┘
                             │ 开始执行
                             ▼
                    ┌─────────────────┐
              ┌────▶│  IN_PROGRESS    │
              │     └────────┬────────┘
              │              │
   ┌──────────┴──────────┐   │
   │                     │   │
   ▼                     ▼   ▼
┌───────────┐      ┌───────────┐
│ COMPLETED │      │  FAILED   │
└───────────┘      └─────┬─────┘
                         │
                         │ 可重试
                         ▼
                  ┌─────────────┐
                  │  RETRYING   │
                  └──────┬──────┘
                         │
                         │ 重试
                         └──────┐
                                ▼
                        ┌───────────────┐
                        │  IN_PROGRESS  │
                        └───────────────┘
```

---

### 状态转换实现

```python
class StateTransitionError(Exception):
    """非法状态转换异常"""
    pass


class TaskStateMachine:
    """任务状态机"""

    # 定义合法的状态转换
    VALID_TRANSITIONS = {
        TaskStatus.PENDING: [TaskStatus.READY, TaskStatus.CANCELLED],
        TaskStatus.READY: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED, TaskStatus.BLOCKED],
        TaskStatus.IN_PROGRESS: [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED],
        TaskStatus.FAILED: [TaskStatus.RETRYING, TaskStatus.BLOCKED],
        TaskStatus.RETRYING: [TaskStatus.IN_PROGRESS, TaskStatus.FAILED, TaskStatus.CANCELLED],
        TaskStatus.BLOCKED: [TaskStatus.READY, TaskStatus.CANCELLED],
        TaskStatus.COMPLETED: [],  # 终态
        TaskStatus.CANCELLED: [],  # 终态
    }

    def __init__(self, initial_status: TaskStatus = TaskStatus.PENDING):
        self.state = TaskState(
            task_id="",
            status=initial_status
        )

    def transition_to(self, new_status: TaskStatus, **kwargs) -> bool:
        """转换到新状态"""
        current = self.state.status

        # 检查是否是合法转换
        if new_status not in self.VALID_TRANSITIONS[current]:
            raise StateTransitionError(
                f"非法状态转换: {current.value} -> {new_status.value}"
            )

        # 执行状态转换
        old_status = self.state.status
        self.state.status = new_status

        # 更新时间戳
        if new_status == TaskStatus.IN_PROGRESS:
            self.state.started_at = datetime.now()
        elif new_status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            self.state.completed_at = datetime.now()

        # 更新附加信息
        for key, value in kwargs.items():
            setattr(self.state, key, value)

        return True

    def can_transition_to(self, new_status: TaskStatus) -> bool:
        """检查是否可以转换到指定状态"""
        current = self.state.status
        return new_status in self.VALID_TRANSITIONS.get(current, [])

    def is_terminal(self) -> bool:
        """是否是终态"""
        return self.state.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]

    def is_executable(self) -> bool:
        """是否可执行"""
        return self.state.status == TaskStatus.IN_PROGRESS
```

---

## 完整示例：任务执行状态机

```python
from typing import List, Dict, Optional
from datetime import datetime
import time

class TaskExecution:
    """任务执行器（带状态机）"""

    def __init__(self):
        self.tasks: Dict[str, TaskStateMachine] = {}
        self.dependencies: Dict[str, List[str]] = {}

    def add_task(self, task_id: str, dependencies: List[str] = None):
        """添加任务"""
        self.tasks[task_id] = TaskStateMachine(TaskStatus.PENDING)
        self.tasks[task_id].state.task_id = task_id
        self.dependencies[task_id] = dependencies or []

    def update_states(self):
        """更新所有任务状态"""
        for task_id, machine in self.tasks.items():
            if machine.state.status == TaskStatus.PENDING:
                # 检查依赖是否满足
                if self._dependencies_satisfied(task_id):
                    machine.transition_to(TaskStatus.READY)
                    print(f"[状态更新] {task_id}: PENDING -> READY")

            elif machine.state.status == TaskStatus.READY:
                # 可以开始执行
                machine.transition_to(TaskStatus.IN_PROGRESS)
                print(f"[状态更新] {task_id}: READY -> IN_PROGRESS")

    def execute_task(self, task_id: str) -> bool:
        """执行任务"""
        machine = self.tasks[task_id]

        if not machine.can_transition_to(TaskStatus.COMPLETED):
            print(f"[执行失败] {task_id} 状态不允许执行: {machine.state.status.value}")
            return False

        try:
            # 模拟执行
            print(f"[执行] {task_id}...")
            time.sleep(0.5)

            # 模拟成功
            machine.transition_to(
                TaskStatus.COMPLETED,
                result=f"{task_id} 的结果"
            )
            print(f"[成功] {task_id}: COMPLETED")
            return True

        except Exception as e:
            # 执行失败
            machine.transition_to(
                TaskStatus.FAILED,
                error=str(e)
            )
            print(f"[失败] {task_id}: FAILED - {e}")
            return False

    def retry_task(self, task_id: str) -> bool:
        """重试任务"""
        machine = self.tasks[task_id]

        if machine.state.status != TaskStatus.FAILED:
            print(f"[重试失败] {task_id} 不是失败状态")
            return False

        # 检查重试次数
        if machine.state.retry_count >= 3:
            print(f"[重试失败] {task_id} 已达到最大重试次数")
            machine.transition_to(TaskStatus.BLOCKED)
            return False

        # 增加重试计数
        machine.state.retry_count += 1

        # 转换到重试状态
        machine.transition_to(TaskStatus.RETRYING)
        print(f"[重试] {task_id} (第 {machine.state.retry_count} 次)")

        # 转换到执行中
        machine.transition_to(TaskStatus.IN_PROGRESS)

        return self.execute_task(task_id)

    def cancel_task(self, task_id: str):
        """取消任务"""
        machine = self.tasks[task_id]

        if machine.is_terminal():
            print(f"[取消失败] {task_id} 已是终态，无法取消")
            return False

        machine.transition_to(TaskStatus.CANCELLED)
        print(f"[取消] {task_id}: CANCELLED")
        return True

    def get_status(self, task_id: str) -> str:
        """获取任务状态"""
        return self.tasks[task_id].state.status.value

    def _dependencies_satisfied(self, task_id: str) -> bool:
        """检查依赖是否满足"""
        deps = self.dependencies.get(task_id, [])

        for dep_id in deps:
            dep_machine = self.tasks.get(dep_id)
            if not dep_machine:
                return False  # 依赖任务不存在

            if dep_machine.state.status != TaskStatus.COMPLETED:
                return False  # 依赖未完成

        return True

    def print_summary(self):
        """打印状态摘要"""
        print("\n[状态摘要]")
        print(f"{'任务ID':<15} {'状态':<15} {'重试次数':<10} {'开始时间':<20} {'完成时间':<20}")
        print("-" * 80)

        for task_id, machine in self.tasks.items():
            state = machine.state
            started = state.started_at.strftime("%H:%M:%S") if state.started_at else "N/A"
            completed = state.completed_at.strftime("%H:%M:%S") if state.completed_at else "N/A"

            print(f"{task_id:<15} {state.status.value:<15} {state.retry_count:<10} {started:<20} {completed:<20}")


# 运行示例
def main():
    print("=" * 80)
    print("任务执行状态机示例")
    print("=" * 80)

    executor = TaskExecution()

    # 添加任务
    executor.add_task("task_A", dependencies=[])
    executor.add_task("task_B", dependencies=[])
    executor.add_task("task_C", dependencies=["task_A", "task_B"])
    executor.add_task("task_D", dependencies=["task_C"])

    print("\n[阶段 1] 初始化状态")
    executor.print_summary()

    print("\n[阶段 2] 更新状态（检查依赖）")
    executor.update_states()
    executor.print_summary()

    print("\n[阶段 3] 执行 task_A")
    executor.execute_task("task_A")
    executor.update_states()  # 更新其他任务状态
    executor.print_summary()

    print("\n[阶段 4] 执行 task_B")
    executor.execute_task("task_B")
    executor.update_states()
    executor.print_summary()

    print("\n[阶段 5] 执行 task_C")
    executor.execute_task("task_C")
    executor.update_states()
    executor.print_summary()

    print("\n[阶段 6] 执行 task_D")
    executor.execute_task("task_D")
    executor.update_states()
    executor.print_summary()

    # 演示失败和重试
    print("\n[演示失败和重试]")
    executor.add_task("task_E", dependencies=[])

    # 模拟失败
    executor.update_states()
    machine_E = executor.tasks["task_E"]
    machine_E.transition_to(TaskStatus.IN_PROGRESS)
    machine_E.transition_to(TaskStatus.FAILED, error="模拟失败")
    executor.print_summary()

    # 重试
    print("\n[重试 task_E]")
    executor.retry_task("task_E")
    executor.print_summary()


if __name__ == "__main__":
    main()
```

---

## 状态持久化

### 为什么需要持久化？

- **恢复执行**：系统崩溃后可以恢复状态
- **审计追踪**：查看任务历史
- **调试分析**：分析执行问题

---

### 持久化实现

```python
import json
from pathlib import Path

class StatePersistence:
    """状态持久化"""

    def __init__(self, storage_dir: str = "./task_states"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def save_state(self, task_id: str, state: TaskState):
        """保存任务状态"""
        file_path = self.storage_dir / f"{task_id}.json"

        state_data = {
            "task_id": state.task_id,
            "status": state.status.value,
            "result": str(state.result) if state.result else None,
            "error": state.error,
            "retry_count": state.retry_count,
            "created_at": state.created_at.isoformat(),
            "started_at": state.started_at.isoformat() if state.started_at else None,
            "completed_at": state.completed_at.isoformat() if state.completed_at else None,
            "metadata": state.metadata,
        }

        with open(file_path, 'w') as f:
            json.dump(state_data, f, indent=2)

    def load_state(self, task_id: str) -> Optional[TaskState]:
        """加载任务状态"""
        file_path = self.storage_dir / f"{task_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r') as f:
            state_data = json.load(f)

        return TaskState(
            task_id=state_data["task_id"],
            status=TaskStatus(state_data["status"]),
            result=state_data["result"],
            error=state_data["error"],
            retry_count=state_data["retry_count"],
            created_at=datetime.fromisoformat(state_data["created_at"]),
            started_at=datetime.fromisoformat(state_data["started_at"]) if state_data["started_at"] else None,
            completed_at=datetime.fromisoformat(state_data["completed_at"]) if state_data["completed_at"] else None,
            metadata=state_data["metadata"],
        )

    def delete_state(self, task_id: str):
        """删除任务状态"""
        file_path = self.storage_dir / f"{task_id}.json"
        if file_path.exists():
            file_path.unlink()
```

---

## 关键设计考虑

### 考虑 1：状态粒度

**粗粒度**：只记录主要状态（pending, running, done）
- 优点：简单
- 缺点：信息不足

**细粒度**：记录所有中间状态
- 优点：详细追踪
- 缺点：存储开销大

**推荐**：中等粒度（7-10 个状态）

---

### 考虑 2：状态转换验证

**严格验证**：所有转换都必须预先定义
- 优点：安全
- 缺点：不够灵活

**宽松验证**：允许任意转换
- 优点：灵活
- 缺点：容易出现非法状态

**推荐**：严格验证 + 预留 escape hatch（强制转换方法）

---

### 考虑 3：并发安全

**问题**：多线程/多进程同时更新状态

**解决方案**：
- 使用锁保护状态转换
- 使用原子操作
- 使用事件溯源（Event Sourcing）

---

## 最小验证

- [ ] 能够定义任务状态枚举
- [ ] 能够实现状态转换规则
- [ ] 能够验证状态转换的合法性
- [ ] 能够持久化和恢复状态

---

## 下一步

- 📖 `notes/04_replanning_triggers.md` - 重规划触发机制
- 🧪 `examples/04_state_machine.py` - 状态机示例

---

**记住：状态机就像快递跟踪系统，清晰地记录任务的生命周期！** 📦
