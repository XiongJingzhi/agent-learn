# 回滚与恢复

> **目标**: 掌握任务执行失败后的回滚和恢复机制
> **预计时间**: 30 分钟
> **难度**: ⭐⭐⭐

---

## 为什么需要回滚与恢复？

在 Agent 执行过程中，可能会遇到各种失败：

**场景 1：外部服务失败**
- API 超时、限流、服务不可用
- 需要回滚到之前的状态，稍后重试

**场景 2：数据损坏**
- 获取的数据格式错误或内容不完整
- 需要回滚并尝试其他数据源

**场景 3：依赖任务失败**
- 前置任务失败，导致后续任务无法执行
- 需要回滚到依赖任务之前的状态

**场景 4：资源不足**
- 内存不足、配额用尽
- 需要回滚并释放资源

---

## 回滚策略

### 策略 1：检查点（Checkpoint）

在关键点保存执行状态，失败时可以恢复到最近的检查点。

```python
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json

@dataclass
class Checkpoint:
    """检查点"""
    checkpoint_id: str
    timestamp: datetime
    execution_state: Dict[str, Any]
    task_results: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


class CheckpointManager:
    """检查点管理器"""

    def __init__(self):
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.current_checkpoint_id: Optional[str] = None

    def create_checkpoint(self,
                          checkpoint_id: str,
                          execution_state: Dict[str, Any],
                          task_results: Dict[str, Any],
                          metadata: Dict[str, Any] = None) -> Checkpoint:
        """创建检查点"""
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            timestamp=datetime.now(),
            execution_state=execution_state.copy(),
            task_results=task_results.copy(),
            metadata=metadata or {}
        )

        self.checkpoints[checkpoint_id] = checkpoint
        self.current_checkpoint_id = checkpoint_id

        print(f"[检查点] 创建检查点: {checkpoint_id}")
        return checkpoint

    def restore_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """恢复到指定检查点"""
        if checkpoint_id not in self.checkpoints:
            print(f"[检查点] 检查点不存在: {checkpoint_id}")
            return None

        checkpoint = self.checkpoints[checkpoint_id]
        self.current_checkpoint_id = checkpoint_id

        print(f"[检查点] 恢复到检查点: {checkpoint_id}")
        print(f"[检查点] 时间: {checkpoint.timestamp}")
        print(f"[检查点] 任务结果数: {len(checkpoint.task_results)}")

        return checkpoint

    def get_latest_checkpoint(self) -> Optional[Checkpoint]:
        """获取最新的检查点"""
        if not self.checkpoints:
            return None

        latest = max(self.checkpoints.values(), key=lambda c: c.timestamp)
        return latest

    def delete_checkpoint(self, checkpoint_id: str):
        """删除检查点"""
        if checkpoint_id in self.checkpoints:
            del self.checkpoints[checkpoint_id]
            print(f"[检查点] 删除检查点: {checkpoint_id}")

    def clear_old_checkpoints(self, keep_latest: int = 5):
        """清理旧检查点，只保留最新的几个"""
        if len(self.checkpoints) <= keep_latest:
            return

        # 按时间排序
        sorted_checkpoints = sorted(
            self.checkpoints.items(),
            key=lambda x: x[1].timestamp
        )

        # 删除旧的
        to_delete = len(self.checkpoints) - keep_latest
        for checkpoint_id, _ in sorted_checkpoints[:to_delete]:
            self.delete_checkpoint(checkpoint_id)
```

---

### 策略 2：事务性执行

要么全部成功，要么全部失败（回滚）。

```python
class TransactionalExecutor:
    """事务性执行器"""

    def __init__(self):
        self.executed_tasks = []
        self.checkpoint_manager = CheckpointManager()

    def execute_transaction(self, tasks: list) -> dict:
        """事务性执行一批任务"""
        # 创建检查点
        self.checkpoint_manager.create_checkpoint(
            checkpoint_id="transaction_start",
            execution_state={},
            task_results={}
        )

        results = {}

        try:
            for task in tasks:
                print(f"[事务] 执行任务: {task['id']}")

                # 执行任务
                result = self._execute_single_task(task)
                results[task['id']] = result

                # 记录已执行的任务
                self.executed_tasks.append(task)

            # 所有任务都成功，提交事务
            print(f"[事务] 提交事务: {len(tasks)} 个任务")
            return results

        except Exception as e:
            # 发生错误，回滚事务
            print(f"[事务] 回滚事务: {str(e)}")
            self._rollback_transaction()
            raise

    def _execute_single_task(self, task: dict) -> any:
        """执行单个任务（模拟）"""
        task_id = task['id']
        task_type = task.get('type', 'default')

        # 模拟执行
        if task_type == 'fail':
            raise Exception(f"任务 {task_id} 执行失败")

        return f"{task_id} 的结果"

    def _rollback_transaction(self):
        """回滚事务"""
        print(f"[回滚] 回滚 {len(self.executed_tasks)} 个任务")

        # 恢复到检查点
        checkpoint = self.checkpoint_manager.restore_checkpoint("transaction_start")
        if checkpoint:
            # 清空已执行的任务
            self.executed_tasks = []

            print(f"[回滚] 已恢复到初始状态")
```

---

### 策略 3：增量恢复

只恢复失败的部分，保留成功执行的结果。

```python
class IncrementalRecovery:
    """增量恢复"""

    def __init__(self):
        self.task_results = {}
        self.failed_tasks = []

    def execute_with_recovery(self, tasks: list) -> dict:
        """执行任务，支持增量恢复"""
        for task in tasks:
            task_id = task['id']

            # 如果任务已经成功，跳过
            if task_id in self.task_results:
                print(f"[恢复] 跳过已完成的任务: {task_id}")
                continue

            try:
                # 执行任务
                print(f"[执行] 执行任务: {task_id}")
                result = self._execute_task(task)
                self.task_results[task_id] = result

                print(f"[成功] 任务 {task_id} 完成")

            except Exception as e:
                # 记录失败的任务
                self.failed_tasks.append({
                    'task': task,
                    'error': str(e),
                    'timestamp': datetime.now()
                })

                print(f"[失败] 任务 {task_id} 失败: {e}")

                # 决定是否继续
                should_continue = self._should_continue_after_failure(task, e)
                if not should_continue:
                    print("[停止] 停止执行")
                    break

        return {
            'results': self.task_results,
            'failed': self.failed_tasks
        }

    def _execute_task(self, task: dict) -> any:
        """执行单个任务"""
        # 模拟执行
        return f"{task['id']} 的结果"

    def _should_continue_after_failure(self, task: dict, error: Exception) -> bool:
        """判断失败后是否继续执行"""
        # 如果任务标记为 critical，失败后停止
        if task.get('critical', False):
            return False

        # 否则继续执行
        return True

    def retry_failed_tasks(self) -> dict:
        """重试失败的任务"""
        if not self.failed_tasks:
            print("[重试] 没有失败的任务需要重试")
            return self.task_results

        print(f"[重试] 重试 {len(self.failed_tasks)} 个失败的任务")

        # 复制失败任务列表
        failed_copy = self.failed_tasks.copy()
        self.failed_tasks = []

        for item in failed_copy:
            task = item['task']
            task_id = task['id']

            try:
                print(f"[重试] 重试任务: {task_id}")
                result = self._execute_task(task)
                self.task_results[task_id] = result
                print(f"[重试] 任务 {task_id} 成功")

            except Exception as e:
                print(f"[重试] 任务 {task_id} 再次失败: {e}")
                self.failed_tasks.append({
                    'task': task,
                    'error': str(e),
                    'timestamp': datetime.now()
                })

        return {
            'results': self.task_results,
            'failed': self.failed_tasks
        }
```

---

## 完整示例：回滚与恢复系统

```python
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

class RollbackRecoverySystem:
    """回滚与恢复系统"""

    def __init__(self):
        self.checkpoint_manager = CheckpointManager()
        self.transaction_executor = TransactionalExecutor()
        self.incremental_recovery = IncrementalRecovery()

    def execute_with_checkpoint(self, tasks: List[Dict]) -> Dict[str, Any]:
        """使用检查点执行任务"""
        print("\n[策略 1: 检查点]")

        # 创建初始检查点
        self.checkpoint_manager.create_checkpoint(
            checkpoint_id="initial",
            execution_state={"task_count": len(tasks)},
            task_results={}
        )

        results = {}
        completed_tasks = []

        try:
            for i, task in enumerate(tasks):
                task_id = task['id']
                print(f"\n[执行] 任务 {i+1}/{len(tasks)}: {task_id}")

                # 每隔 3 个任务创建一个检查点
                if i > 0 and i % 3 == 0:
                    checkpoint_id = f"checkpoint_{i}"
                    self.checkpoint_manager.create_checkpoint(
                        checkpoint_id=checkpoint_id,
                        execution_state={"completed": i},
                        task_results=results.copy()
                    )

                # 执行任务
                result = self._execute_task(task)
                results[task_id] = result
                completed_tasks.append(task_id)

                print(f"[成功] {task_id}: {result}")

            return {"status": "success", "results": results}

        except Exception as e:
            print(f"\n[失败] 执行失败: {e}")

            # 恢复到最近的检查点
            latest = self.checkpoint_manager.get_latest_checkpoint()
            if latest:
                print(f"\n[恢复] 恢复到检查点: {latest.checkpoint_id}")
                self.checkpoint_manager.restore_checkpoint(latest.checkpoint_id)

                return {
                    "status": "recovered",
                    "checkpoint_id": latest.checkpoint_id,
                    "results": latest.task_results,
                    "error": str(e)
                }

            return {"status": "failed", "error": str(e)}

    def execute_transactional(self, tasks: List[Dict]) -> Dict[str, Any]:
        """事务性执行"""
        print("\n[策略 2: 事务性执行]")

        executor = TransactionalExecutor()

        try:
            results = executor.execute_transaction(tasks)
            return {"status": "success", "results": results}

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def execute_incremental(self, tasks: List[Dict]) -> Dict[str, Any]:
        """增量恢复执行"""
        print("\n[策略 3: 增量恢复]")

        recovery = IncrementalRecovery()

        # 第一次执行
        result = recovery.execute_with_recovery(tasks)

        # 如果有失败的任务，尝试重试
        if result['failed']:
            print(f"\n[重试] 第一次执行后有 {len(result['failed'])} 个失败任务")

            # 模拟一些任务重试成功
            print("\n[重试] 重试失败的任务...")
            time.sleep(1)

            result = recovery.retry_failed_tasks()

        return {
            "status": "partial" if result['failed'] else "success",
            "results": result['results'],
            "failed": result['failed']
        }

    def _execute_task(self, task: Dict) -> str:
        """执行单个任务（模拟）"""
        task_id = task['id']
        task_type = task.get('type', 'normal')

        # 模拟执行延迟
        time.sleep(0.2)

        # 模拟不同类型的任务
        if task_type == 'fail':
            raise Exception(f"任务 {task_id} 执行失败")
        elif task_type == 'timeout':
            time.sleep(2)
            raise Exception(f"任务 {task_id} 超时")
        else:
            return f"{task_id} 的结果"


# 运行示例
def main():
    print("=" * 70)
    print("回滚与恢复系统示例")
    print("=" * 70)

    system = RollbackRecoverySystem()

    # 定义任务列表
    tasks = [
        {"id": "task_1", "type": "normal"},
        {"id": "task_2", "type": "normal"},
        {"id": "task_3", "type": "fail"},  # 这个任务会失败
        {"id": "task_4", "type": "normal"},
    ]

    # 示例 1：检查点恢复
    print("\n" + "=" * 70)
    print("示例 1：检查点恢复")
    print("=" * 70)
    result1 = system.execute_with_checkpoint(tasks)
    print(f"\n结果: {result1['status']}")

    # 示例 2：事务性执行
    print("\n" + "=" * 70)
    print("示例 2：事务性执行")
    print("=" * 70)
    result2 = system.execute_transactional(tasks)
    print(f"\n结果: {result2['status']}")

    # 示例 3：增量恢复
    print("\n" + "=" * 70)
    print("示例 3：增量恢复")
    print("=" * 70)
    result3 = system.execute_incremental(tasks)
    print(f"\n结果: {result3['status']}")
    print(f"成功: {len(result3['results'])} 个任务")
    print(f"失败: {len(result3.get('failed', []))} 个任务")


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：检查点频率

**太频繁**：
- 优点：可以恢复到更精确的状态
- 缺点：存储和性能开销大

**太稀疏**：
- 优点：开销小
- 缺点：恢复时损失更多工作

**推荐**：根据任务重要性和执行时间动态调整

---

### 考虑 2：状态一致性

**问题**：恢复后如何保证状态一致？

**解决方案**：
- 使用不可变数据结构
- 记录完整的执行上下文
- 实现幂等性（重复执行结果相同）

---

### 考虑 3：恢复策略选择

| 场景 | 推荐策略 |
|------|----------|
| 任务之间有强依赖 | 事务性执行 |
| 任务相对独立 | 增量恢复 |
| 执行时间长，任务多 | 检查点 |
| 需要精确控制 | 手动检查点 |

---

## 最小验证

- [ ] 能够实现检查点机制
- [ ] 能够实现事务性执行
- [ ] 能够实现增量恢复
- [ ] 能够根据场景选择合适的恢复策略

---

## 下一步

- 📖 `notes/06_reflection_loop_design.md` - 反思循环设计
- 🧪 `examples/06_rollback_recovery.py` - 回滚恢复示例

---

**记住：回滚与恢复是应对执行失败的关键安全机制！** 🛡️
