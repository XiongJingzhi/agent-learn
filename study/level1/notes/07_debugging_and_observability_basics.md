# 调试与可观测基础

> **目标**: 掌握节点级日志、链路跟踪、调试技巧
> **预计时间**: 30 分钟
> **前置**: 已完成短期记忆学习

---

## 为什么需要可观测性？

Agent 的执行过程复杂且不透明，可观测性能够：
- **理解执行流程**：查看节点执行顺序
- **诊断问题**：快速定位错误和瓶颈
- **优化性能**：分析时间和资源消耗

**类比**：可观测性就像**汽车的仪表盘**，显示速度、油量、引擎状态。

---

## 日志记录

### 级别 1：节点级日志

为每个节点添加日志。

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def logged_node(state: AgentState) -> dict:
    """带日志的节点"""
    node_name = "processing_node"

    # 入口日志
    logger.info(f"[{node_name}] 开始执行")
    logger.debug(f"[{node_name}] 输入状态: {state}")

    try:
        # 执行逻辑
        result = process(state['input'])

        # 成功日志
        logger.info(f"[{node_name}] 执行成功")
        logger.debug(f"[{node_name}] 输出结果: {result}")

        return {"output": result}

    except Exception as e:
        # 错误日志
        logger.error(f"[{node_name}] 执行失败: {str(e)}", exc_info=True)
        raise
```

---

### 级别 2：结构化日志

使用结构化格式记录日志。

```python
import json
import logging

class StructuredLogger:
    """结构化日志记录器"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.context = {}

    def with_context(self, **kwargs):
        """添加上下文"""
        self.context.update(kwargs)
        return self

    def log(self, level: str, message: str, **extra):
        """记录结构化日志"""
        log_entry = {
            "timestamp": time.time(),
            "level": level,
            "message": message,
            "context": {**self.context, **extra}
        }

        # 输出 JSON 格式
        log_json = json.dumps(log_entry, ensure_ascii=False)

        if level == "INFO":
            self.logger.info(log_json)
        elif level == "ERROR":
            self.logger.error(log_json)
        elif level == "DEBUG":
            self.logger.debug(log_json)

# 使用
logger = StructuredLogger("agent")

def node_with_structured_log(state: AgentState) -> dict:
    """带结构化日志的节点"""
    logger.with_context(
        node_name="processing",
        state_id=state.get("id", "unknown")
    )

    logger.log("INFO", "节点开始执行", input=state.get("input"))

    try:
        result = process(state['input'])
        logger.log("INFO", "节点执行成功", output=result)
        return {"output": result}
    except Exception as e:
        logger.log("ERROR", "节点执行失败", error=str(e))
        raise
```

---

## LangSmith 跟踪

### 设置 LangSmith

```python
import os
from langchain_openai import ChatOpenAI

# 配置 LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "agent-debugging"

# 创建 LLM
llm = ChatOpenAI(temperature=0)

# 所有调用会自动跟踪到 LangSmith
response = llm.invoke("Hello")
# 查看 https://smith.langchain.com
```

---

### 自定义跟踪

```python
from langchain.callbacks.manager import tracing_context

def custom_traced_node(state: AgentState) -> dict:
    """带自定义跟踪的节点"""
    with tracing_context("custom_node"):
        # 在 LangSmith 中显示为 "custom_node"
        result = process(state['input'])
        return {"output": result}
```

---

## 链路跟踪

### 跟踪执行流程

```python
from typing import Dict, Any
from langgraph.graph import StateGraph

class Tracer:
    """简单的链路跟踪器"""

    def __init__(self):
        self.trace = []
        self.start_time = None
        self.end_time = None

    def start(self):
        """开始跟踪"""
        self.start_time = time.time()
        self.trace.append({
            "event": "start",
            "timestamp": self.start_time
        })

    def record_node(self, node_name: str, state: Dict):
        """记录节点执行"""
        self.trace.append({
            "event": "node_execution",
            "node": node_name,
            "state": state,
            "timestamp": time.time()
        })

    def record_edge(self, from_node: str, to_node: str):
        """记录边执行"""
        self.trace.append({
            "event": "edge_traversal",
            "from": from_node,
            "to": to_node,
            "timestamp": time.time()
        })

    def end(self):
        """结束跟踪"""
        self.end_time = time.time()
        self.trace.append({
            "event": "end",
            "timestamp": self.end_time
        })

    def get_summary(self) -> Dict:
        """获取跟踪摘要"""
        duration = (self.end_time - self.start_time) if self.start_time else 0

        node_count = sum(
            1 for t in self.trace
            if t["event"] == "node_execution"
        )

        return {
            "duration": duration,
            "node_count": node_count,
            "trace": self.trace
        }

# 使用跟踪器
tracer = Tracer()

def traced_node(state: AgentState) -> dict:
    """带跟踪的节点"""
    tracer.record_node("my_node", state)
    result = process(state['input'])
    return {"output": result}
```

---

## 性能监控

### 监控节点执行时间

```python
import time
from functools import wraps

def timed_node(func):
    """节点执行时间装饰器"""
    @wraps(func)
    def wrapper(state: AgentState) -> dict:
        start = time.time()
        logger.info(f"[{func.__name__}] 节点开始执行")

        try:
            result = func(state)
            duration = time.time() - start

            logger.info(
                f"[{func.__name__}] 节点执行完成",
                extra={"duration": duration}
            )

            # 如果执行时间过长，发出警告
            if duration > 5.0:
                logger.warning(
                    f"[{func.__name__}] 节点执行时间过长",
                    extra={"duration": duration}
                )

            return result

        except Exception as e:
            duration = time.time() - start
            logger.error(
                f"[{func.__name__}] 节点执行失败",
                extra={"duration": duration, "error": str(e)}
            )
            raise

    return wrapper

# 使用
@timed_node
def processing_node(state: AgentState) -> dict:
    """带时间监控的节点"""
    result = process(state['input'])
    return {"output": result}
```

---

## 完整示例：可观测的 Agent

```python
import time
import logging
from typing import TypedDict
from langgraph.graph import StateGraph, END

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ObservableState(TypedDict):
    input: str
    output: str
    step: int

# ===== 可观测的节点 =====

def observable_node_1(state: ObservableState) -> dict:
    """可观测的节点 1"""
    node_name = "node_1"
    step = state.get("step", 0) + 1

    logger.info(f"[{node_name}] 开始执行 (步骤 {step})")
    logger.debug(f"[{node_name}] 输入: {state['input']}")

    start = time.time()

    try:
        # 模拟处理
        time.sleep(0.5)
        result = f"处理结果: {state['input']}"

        duration = time.time() - start

        logger.info(
            f"[{node_name}] 执行完成",
            extra={"duration": duration, "step": step}
        )

        return {
            "output": result,
            "step": step
        }

    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"[{node_name}] 执行失败: {str(e)}",
            extra={"duration": duration, "step": step},
            exc_info=True
        )
        raise

def observable_node_2(state: ObservableState) -> dict:
    """可观测的节点 2"""
    node_name = "node_2"
    step = state.get("step", 0) + 1

    logger.info(f"[{node_name}] 开始执行 (步骤 {step})")
    logger.debug(f"[{node_name}] 输入: {state.get('output', state['input'])}")

    start = time.time()

    try:
        # 模拟处理
        time.sleep(0.3)
        result = f"二次处理: {state.get('output', '')}"

        duration = time.time() - start

        logger.info(
            f"[{node_name}] 执行完成",
            extra={"duration": duration, "step": step}
        )

        return {
            "output": result,
            "step": step
        }

    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"[{node_name}] 执行失败: {str(e)}",
            extra={"duration": duration, "step": step},
            exc_info=True
        )
        raise

# ===== 构建可观测的图 =====

def build_observable_graph():
    """构建可观测的图"""
    graph = StateGraph(ObservableState)

    # 添加节点
    graph.add_node("node_1", observable_node_1)
    graph.add_node("node_2", observable_node_2)

    # 设置入口
    graph.set_entry_point("node_1")

    # 添加边
    graph.add_edge("node_1", "node_2")
    graph.add_edge("node_2", END)

    return graph.compile()

# ===== 运行并观察 =====

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("开始执行可观测的 Agent")
    logger.info("=" * 60)

    start_time = time.time()

    # 构建并运行
    graph = build_observable_graph()

    initial_state = {
        "input": "测试输入",
        "output": "",
        "step": 0
    }

    result = graph.invoke(initial_state)

    duration = time.time() - start_time

    # 输出摘要
    logger.info("=" * 60)
    logger.info("Agent 执行完成")
    logger.info("=" * 60)
    logger.info(
        f"总执行时间: {duration:.2f} 秒",
        extra={"total_duration": duration}
    )
    logger.info(f"总步骤数: {result['step']}")
    logger.info(f"最终输出: {result['output']}")
```

---

## 调试技巧

### 技巧 1：使用 verbose=True

```python
from langchain.agents import AgentExecutor

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # 打印详细执行过程
)

result = executor.invoke({"input": "测试"})
```

---

### 技巧 2：启用中间步骤

```python
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True  # 返回中间步骤
)

result = executor.invoke({"input": "测试"})

# 查看中间步骤
for step in result["intermediate_steps"]:
    print(step)
```

---

### 技巧 3：使用 pdb 调试

```python
import pdb

def debuggable_node(state: AgentState) -> dict:
    """可调试的节点"""
    # 设置断点
    pdb.set_trace()

    # 在这里可以检查 state 的值
    result = process(state['input'])

    return {"output": result}
```

---

## 最小验证

### 验证目标
- ✅ 理解日志记录方法
- ✅ 能够跟踪节点执行
- ✅ 能够监控性能

### 验证步骤
1. 运行上面的可观测 Agent 示例
2. 查看日志输出
3. 修改日志级别（DEBUG/INFO/WARNING/ERROR）
4. 测试不同的监控场景

---

## 常见错误

### 错误 1：日志级别太低
```python
# 错误：日志级别太高，看不到调试信息
logging.basicConfig(level=logging.WARNING)

# 正确：设置为 INFO 或 DEBUG
logging.basicConfig(level=logging.INFO)
```

### 错误 2：忘记记录关键信息
```python
# 错误：只记录成功，不记录输入输出
logger.info("节点执行完成")

# 正确：记录关键上下文
logger.info("节点执行完成", extra={
    "input": state['input'],
    "output": result
})
```

---

## 下一步

- 🧪 `examples/09_debugging_and_observability.py` - 调试与可观测示例
- ✏ `exercises/01_basic_exercises.md` - 基础练习题

---

**记住：可观测性就像汽车的仪表盘，显示速度、油量、引擎状态！** 📊
