# 日志与可追溯性

> **目标**: 掌握如何设计有效的日志系统和可追溯性机制
> **预计时间**: 25 分钟
> **难度**: ⭐⭐

---

## 为什么需要日志与可追溯性？

**场景 1：调试问题**
- Agent 执行失败，需要找出原因
- 详细的日志可以重现执行过程

**场景 2：性能分析**
- 哪个任务执行最慢？
- 哪个环节是瓶颈？

**场景 3：审计合规**
- 记录所有决策和操作
- 满足合规要求

**场景 4：优化改进**
- 分析成功和失败的案例
- 找出改进空间

---

## 日志层次

### 层次 1：节点级日志

记录每个节点的执行情况。

```python
import logging
from typing import Dict, Any
from datetime import datetime

class NodeLogger:
    """节点日志记录器"""

    def __init__(self, node_name: str):
        self.node_name = node_name
        self.logger = logging.getLogger(f"node.{node_name}")
        self.logger.setLevel(logging.INFO)

        # 添加处理器
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_start(self, inputs: Dict[str, Any]):
        """记录节点开始"""
        self.logger.info(f"节点开始执行")
        self.logger.debug(f"输入: {inputs}")

    def log_end(self, outputs: Dict[str, Any], duration: float):
        """记录节点结束"""
        self.logger.info(f"节点执行完成，耗时: {duration:.2f}s")
        self.logger.debug(f"输出: {outputs}")

    def log_error(self, error: Exception):
        """记录错误"""
        self.logger.error(f"节点执行失败: {str(error)}")

    def log_decision(self, decision: str, reason: str):
        """记录决策"""
        self.logger.info(f"决策: {decision}")
        self.logger.debug(f"原因: {reason}")


# 使用示例
def example_node(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """示例节点函数"""
    logger = NodeLogger("example_node")

    logger.log_start(inputs)

    start_time = datetime.now()

    try:
        # 执行节点逻辑
        result = {"output": "处理结果"}

        # 记录决策
        logger.log_decision("使用策略 A", "输入数据量小")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.log_end(result, duration)
        return result

    except Exception as e:
        logger.log_error(e)
        raise
```

---

### 层次 2：执行追踪日志

记录整个执行流程。

```python
from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ExecutionTrace:
    """执行追踪记录"""
    trace_id: str
    start_time: datetime
    end_time: datetime = None
    steps: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_step(self,
                 step_type: str,
                 step_name: str,
                 inputs: Dict[str, Any],
                 outputs: Dict[str, Any] = None,
                 error: Exception = None,
                 duration: float = None):
        """添加执行步骤"""
        step = {
            "timestamp": datetime.now().isoformat(),
            "type": step_type,
            "name": step_name,
            "inputs": inputs,
            "outputs": outputs,
            "error": str(error) if error else None,
            "duration": duration
        }
        self.steps.append(step)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "trace_id": self.trace_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else None,
            "steps": self.steps,
            "metadata": self.metadata
        }


class Tracer:
    """执行追踪器"""

    def __init__(self):
        self.current_trace: ExecutionTrace = None
        self.trace_history: List[ExecutionTrace] = []

    def start_trace(self, trace_id: str, metadata: Dict[str, Any] = None):
        """开始新的追踪"""
        self.current_trace = ExecutionTrace(
            trace_id=trace_id,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
        print(f"[追踪] 开始追踪: {trace_id}")

    def end_trace(self):
        """结束当前追踪"""
        if self.current_trace:
            self.current_trace.end_time = datetime.now()
            self.trace_history.append(self.current_trace)
            print(f"[追踪] 结束追踪: {self.current_trace.trace_id}")
            print(f"[追踪] 总耗时: {(self.current_trace.end_time - self.current_trace.start_time).total_seconds():.2f}s")

    def trace_step(self,
                   step_type: str,
                   step_name: str,
                   inputs: Dict[str, Any],
                   outputs: Dict[str, Any] = None,
                   error: Exception = None):
        """追踪执行步骤"""
        if self.current_trace:
            self.current_trace.add_step(
                step_type=step_type,
                step_name=step_name,
                inputs=inputs,
                outputs=outputs,
                error=error
            )

    def get_trace(self, trace_id: str) -> ExecutionTrace:
        """获取指定追踪记录"""
        for trace in self.trace_history:
            if trace.trace_id == trace_id:
                return trace
        return None

    def export_trace(self, trace_id: str) -> Dict[str, Any]:
        """导出追踪记录"""
        trace = self.get_trace(trace_id)
        if trace:
            return trace.to_dict()
        return None
```

---

### 层次 3：结构化日志

使用 JSON 格式记录结构化日志，便于解析和分析。

```python
import json
import logging
from typing import Dict, Any

class StructuredLogger:
    """结构化日志记录器"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # JSON 格式化器
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        self.logger.addHandler(handler)

    def log(self, level: str, message: str, **kwargs):
        """记录结构化日志"""
        log_entry = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }

        if level == "INFO":
            self.logger.info(json.dumps(log_entry))
        elif level == "ERROR":
            self.logger.error(json.dumps(log_entry))
        elif level == "WARNING":
            self.logger.warning(json.dumps(log_entry))
        elif level == "DEBUG":
            self.logger.debug(json.dumps(log_entry))


class JsonFormatter(logging.Formatter):
    """JSON 格式化器"""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }

        # 添加额外字段
        if hasattr(record, 'extra'):
            log_entry.update(record.extra)

        return json.dumps(log_entry)
```

---

## 可追溯性设计

### 设计 1：执行链追踪

记录完整的执行链路。

```python
from typing import List, Optional

class ExecutionChain:
    """执行链"""

    def __init__(self, chain_id: str):
        self.chain_id = chain_id
        self.links: List[Dict[str, Any]] = []

    def add_link(self,
                 from_node: str,
                 to_node: str,
                 data: Dict[str, Any]):
        """添加链路"""
        link = {
            "from": from_node,
            "to": to_node,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.links.append(link)

    def visualize(self) -> str:
        """可视化执行链"""
        visualization = f"执行链: {self.chain_id}\n"
        for link in self.links:
            visualization += f"  {link['from']} -> {link['to']}\n"
        return visualization
```

---

### 设计 2：因果关系记录

记录决策的原因和结果。

```python
@dataclass
class CausalRecord:
    """因果记录"""
    timestamp: datetime
    decision: str
    reason: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    outcome: str  # success, failure, partial


class CausalLogger:
    """因果日志记录器"""

    def __init__(self):
        self.records: List[CausalRecord] = []

    def log_decision(self,
                    decision: str,
                    reason: str,
                    inputs: Dict[str, Any],
                    outputs: Dict[str, Any],
                    outcome: str):
        """记录决策及其因果"""
        record = CausalRecord(
            timestamp=datetime.now(),
            decision=decision,
            reason=reason,
            inputs=inputs,
            outputs=outputs,
            outcome=outcome
        )
        self.records.append(record)

    def analyze_causality(self, decision: str) -> List[Dict[str, Any]]:
        """分析特定决策的因果关系"""
        related = [r for r in self.records if r.decision == decision]

        analysis = []
        for record in related:
            analysis.append({
                "timestamp": record.timestamp.isoformat(),
                "reason": record.reason,
                "outcome": record.outcome,
                "success_rate": sum(1 for r in related if r.outcome == "success") / len(related)
            })

        return analysis
```

---

## 完整示例：日志与追踪系统

```python
import logging
import json
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass, field

# 配置根日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ObservableExecutor:
    """可观测的执行器"""

    def __init__(self):
        self.tracer = Tracer()
        self.causal_logger = CausalLogger()
        self.structured_logger = StructuredLogger("executor")

    def execute_with_observation(self,
                                 plan: Dict[str, Any],
                                 execution_id: str) -> Dict[str, Any]:
        """带观测的执行"""
        # 开始追踪
        self.tracer.start_trace(execution_id, metadata={
            "plan": plan.get("description", ""),
            "task_count": len(plan.get("tasks", []))
        })

        results = {}

        try:
            # 执行每个任务
            for task in plan.get("tasks", []):
                task_id = task["id"]
                task_type = task.get("type", "unknown")

                # 记录任务开始
                self.tracer.trace_step(
                    step_type="task_start",
                    step_name=task_id,
                    inputs={"task": task}
                )

                self.structured_logger.log(
                    "INFO",
                    f"执行任务: {task_id}",
                    task_type=task_type,
                    task_id=task_id
                )

                # 执行任务
                start_time = datetime.now()
                try:
                    result = self._execute_task(task)
                    duration = (datetime.now() - start_time).total_seconds()

                    # 记录成功
                    self.tracer.trace_step(
                        step_type="task_complete",
                        step_name=task_id,
                        inputs={"task": task},
                        outputs={"result": result}
                    )

                    # 记录因果关系
                    self.causal_logger.log_decision(
                        decision=f"execute_{task_id}",
                        reason=f"任务类型: {task_type}",
                        inputs={"task": task},
                        outputs={"result": result},
                        outcome="success"
                    )

                    results[task_id] = {
                        "status": "completed",
                        "result": result,
                        "duration": duration
                    }

                except Exception as e:
                    duration = (datetime.now() - start_time).total_seconds()

                    # 记录失败
                    self.tracer.trace_step(
                        step_type="task_failed",
                        step_name=task_id,
                        inputs={"task": task},
                        error=e
                    )

                    self.structured_logger.log(
                        "ERROR",
                        f"任务失败: {task_id}",
                        task_id=task_id,
                        error=str(e),
                        duration=duration
                    )

                    # 记录因果关系
                    self.causal_logger.log_decision(
                        decision=f"execute_{task_id}",
                        reason=f"任务类型: {task_type}",
                        inputs={"task": task},
                        outputs={},
                        outcome="failure"
                    )

                    results[task_id] = {
                        "status": "failed",
                        "error": str(e),
                        "duration": duration
                    }

        finally:
            # 结束追踪
            self.tracer.end_trace()

        return results

    def _execute_task(self, task: Dict[str, Any]) -> Any:
        """执行单个任务（模拟）"""
        task_id = task["id"]
        task_type = task.get("type", "default")

        # 模拟执行
        if task_type == "fail":
            raise Exception(f"任务 {task_id} 模拟失败")

        return f"{task_id} 的结果"

    def export_trace(self, trace_id: str) -> str:
        """导出追踪记录"""
        trace = self.tracer.export_trace(trace_id)
        if trace:
            return json.dumps(trace, indent=2, ensure_ascii=False)
        return None

    def analyze_execution(self, execution_id: str) -> Dict[str, Any]:
        """分析执行情况"""
        trace = self.tracer.get_trace(execution_id)
        if not trace:
            return None

        # 统计
        total_steps = len(trace.steps)
        successful_steps = len([s for s in trace.steps if s.get("error") is None])
        failed_steps = total_steps - successful_steps

        # 计算总耗时
        durations = [s.get("duration", 0) for s in trace.steps if s.get("duration")]
        total_duration = sum(durations)
        avg_duration = total_duration / len(durations) if durations else 0

        return {
            "execution_id": execution_id,
            "total_steps": total_steps,
            "successful_steps": successful_steps,
            "failed_steps": failed_steps,
            "success_rate": successful_steps / total_steps if total_steps > 0 else 0,
            "total_duration": total_duration,
            "average_duration": avg_duration
        }


# 运行示例
def main():
    print("=" * 70)
    print("日志与可追溯性示例")
    print("=" * 70)

    executor = ObservableExecutor()

    # 定义执行计划
    plan = {
        "description": "示例执行计划",
        "tasks": [
            {"id": "task_1", "type": "search"},
            {"id": "task_2", "type": "process"},
            {"id": "task_3", "type": "fail"},  # 这个会失败
            {"id": "task_4", "type": "summarize"},
        ]
    }

    # 执行并观察
    execution_id = "example_execution_001"
    results = executor.execute_with_observation(plan, execution_id)

    # 打印结果
    print("\n" + "=" * 70)
    print("执行结果")
    print("=" * 70)
    for task_id, result in results.items():
        print(f"{task_id}: {result['status']}")

    # 导出追踪记录
    print("\n" + "=" * 70)
    print("追踪记录")
    print("=" * 70)
    trace_json = executor.export_trace(execution_id)
    print(trace_json)

    # 分析执行情况
    print("\n" + "=" * 70)
    print("执行分析")
    print("=" * 70)
    analysis = executor.analyze_execution(execution_id)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：日志详细程度

**太详细**：
- 优点：信息全面
- 缺点：存储和性能开销大

**太简单**：
- 优点：开销小
- 缺点：信息不足

**推荐**：分级记录（DEBUG, INFO, WARNING, ERROR）

---

### 考虑 2：性能影响

**问题**：日志记录可能影响执行性能

**解决方案**：
- 异步日志记录
- 批量写入
- 日志采样

---

### 考虑 3：日志分析

**问题**：如何从大量日志中提取有价值的信息？

**解决方案**：
- 使用结构化日志（JSON）
- 集成日志分析工具（如 ELK）
- 设置关键指标和告警

---

## 最佳实践

### 实践 1：使用结构化日志

```python
# 好
logger.info("Task completed", extra={
    "task_id": "task_1",
    "duration": 1.23,
    "status": "success"
})

# 不好
logger.info("Task task_1 completed in 1.23 seconds with status success")
```

---

### 实践 2：记录关键决策点

```python
# 记录为什么选择某个策略
logger.info("Selected strategy A", extra={
    "reason": "input data size is small",
    "input_size": len(data),
    "alternatives": ["strategy A", "strategy B"]
})
```

---

### 实践 3：关联日志记录

使用 trace_id 关联所有相关日志：

```python
logger.info("Processing started", extra={"trace_id": trace_id})
logger.info("Task completed", extra={"trace_id": trace_id})
logger.info("Processing finished", extra={"trace_id": trace_id})
```

---

## 最小验证

- [ ] 能够实现节点级日志
- [ ] 能够实现执行追踪
- [ ] 能够实现结构化日志
- [ ] 能够分析和导出日志

---

## 下一步

- 📖 进入下一部分：记忆系统设计
- 🧪 `examples/08_logging_tracing.py` - 日志追踪示例

---

**记住：日志和可追溯性是调试和优化的基础，就像飞机的黑匣子！** 📊
