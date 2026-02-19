# 重试与错误处理

> **目标**: 掌握重试策略、降级策略、错误恢复
> **预计时间**: 30 分钟
> **前置**: 已完成工具调用契约学习

---

## 为什么需要重试与错误处理？

Agent 在执行过程中可能遇到各种错误：
- **网络错误**：超时、连接失败
- **API 错误**：限流、服务不可用
- **数据错误**：格式错误、数据缺失

良好的错误处理能够：
- **提高可靠性**：自动重试恢复临时错误
- **提高可用性**：降级策略保证核心功能
- **提高可观测性**：清晰的错误信息便于调试

**类比**：错误处理就像**备胎和保险**，确保在出现问题时继续前进。

---

## 重试策略

### 策略 1：固定间隔重试

每次重试之间等待固定时间。

```python
import time

def fixed_retry(func, max_retries: int = 3, delay: int = 1):
    """
    固定间隔重试

    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"重试 {attempt + 1}/{max_retries}，等待 {delay} 秒...")
                time.sleep(delay)
            else:
                raise e

# 使用
result = fixed_retry(lambda: risky_operation(), max_retries=3, delay=2)
```

---

### 策略 2：指数退避重试

每次重试间隔呈指数增长。

```python
def exponential_retry(func, max_retries: int = 3, base_delay: int = 1):
    """
    指数退避重试

    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        base_delay: 基础延迟（秒）
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 1, 2, 4, 8...
                print(f"重试 {attempt + 1}/{max_retries}，等待 {delay} 秒...")
                time.sleep(delay)
            else:
                raise e

# 使用
result = exponential_retry(lambda: risky_operation(), max_retries=4, base_delay=1)
```

---

### 策略 3：抖动重试

在指数退避基础上添加随机抖动，避免"惊群效应"。

```python
import random

def jittered_retry(func, max_retries: int = 3, base_delay: int = 1):
    """
    抖动重试

    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        base_delay: 基础延迟（秒）
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                # 指数退避 + 随机抖动
                exponential_delay = base_delay * (2 ** attempt)
                jitter = random.uniform(0, 0.5 * exponential_delay)
                delay = exponential_delay + jitter

                print(f"重试 {attempt + 1}/{max_retries}，等待 {delay:.2f} 秒...")
                time.sleep(delay)
            else:
                raise e
```

---

## 降级策略

### 策略 1：缓存降级

使用缓存数据作为降级方案。

```python
from functools import lru_cache
import time

class CacheFallback:
    """带缓存降级的工具"""

    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 小时

    def get_data(self, key: str) -> dict:
        """获取数据（带缓存降级）"""
        # 尝试从缓存获取
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                print(f"使用缓存数据: {key}")
                return cached_data

        # 尝试获取新数据
        try:
            data = self._fetch_data(key)
            self.cache[key] = (data, time.time())
            return data
        except Exception as e:
            print(f"获取失败，尝试缓存降级: {e}")

            # 缓存降级
            if key in self.cache:
                return self.cache[key][0]

            # 最终降级
            return {"error": "无法获取数据"}

    def _fetch_data(self, key: str) -> dict:
        """获取新数据"""
        # 模拟 API 调用
        return {"data": f"数据: {key}"}
```

---

### 策略 2：默认值降级

使用默认值作为降级方案。

```python
def with_default(func, default_value):
    """
    带默认值的函数执行

    Args:
        func: 要执行的函数
        default_value: 默认值
    """
    try:
        return func()
    except Exception as e:
        print(f"执行失败，使用默认值: {e}")
        return default_value

# 使用
result = with_default(lambda: fetch_data(), {"default": "data"})
```

---

### 策略 3：简化功能降级

提供简化版本的功能。

```python
def full_feature_operation(data: dict) -> dict:
    """完整功能（可能失败）"""
    # 复杂的处理逻辑
    if len(data) > 100:
        raise ValueError("数据太多")

    return {"processed": "完整处理", "data": data}

def simplified_feature_operation(data: dict) -> dict:
    """简化功能（总是成功）"""
    # 简化的处理逻辑
    return {"processed": "简化处理", "count": len(data)}

def with_fallback(data: dict) -> dict:
    """带降级的操作"""
    try:
        return full_feature_operation(data)
    except Exception as e:
        print(f"完整功能失败，使用简化功能: {e}")
        return simplified_feature_operation(data)
```

---

## 完整示例：健壮的 Agent 节点

```python
import time
import random
from typing import Dict, Callable
from langgraph.graph import StateGraph, END

class RobustAgentState(Dict):
    """Agent 状态"""
    input: str
    output: str
    error: str
    retry_count: int
    fallback_used: bool

# ===== 重试装饰器 =====

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0
):
    """
    重试装饰器

    Args:
        max_retries: 最大重试次数
        base_delay: 基础延迟
        backoff_factor: 退避因子
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        delay = base_delay * (backoff_factor ** attempt)
                        print(f"重试 {attempt + 1}/{max_retries}，等待 {delay:.2f} 秒...")
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator

# ===== 模拟不可靠的操作 =====

@retry_with_backoff(max_retries=3, base_delay=1.0)
def unreliable_operation(input: str) -> str:
    """模拟不可靠的操作"""
    # 50% 概率失败
    if random.random() < 0.5:
        raise ConnectionError("连接失败")

    return f"处理成功: {input}"

# ===== 带降级的节点 =====

def processing_node_with_fallback(state: RobustAgentState) -> Dict:
    """带降级的处理节点"""
    input_data = state.get("input", "")

    try:
        # 尝试完整处理
        result = unreliable_operation(input_data)

        return {
            "output": result,
            "error": None,
            "retry_count": state.get("retry_count", 0),
            "fallback_used": False
        }

    except Exception as e:
        print(f"主逻辑失败: {e}，使用降级方案")

        # 降级方案
        fallback_result = f"降级处理: {input_data}"

        return {
            "output": fallback_result,
            "error": str(e),
            "retry_count": state.get("retry_count", 0) + 1,
            "fallback_used": True
        }

def error_handling_node(state: RobustAgentState) -> Dict:
    """错误处理节点"""
    error = state.get("error", "")
    fallback_used = state.get("fallback_used", False)

    if fallback_used:
        message = f"使用降级方案完成，原始错误: {error}"
    else:
        message = f"处理成功"

    return {
        "output": f"最终状态: {message}"
    }

def should_retry(state: RobustAgentState) -> str:
    """判断是否需要重试"""
    retry_count = state.get("retry_count", 0)
    max_retries = 3

    if retry_count >= max_retries:
        return "end"

    if state.get("error"):
        return "retry"

    return "end"

# ===== 构建图 =====

def build_robust_graph():
    """构建健壮的图"""
    graph = StateGraph(RobustAgentState)

    # 添加节点
    graph.add_node("process", processing_node_with_fallback)
    graph.add_node("error_handler", error_handling_node)

    # 设置入口
    graph.set_entry_point("process")

    # 添加条件边
    graph.add_conditional_edges(
        "process",
        should_retry,
        {
            "retry": "process",      # 重试 -> 回到处理节点
            "end": "error_handler"   # 结束 -> 错误处理
        }
    )

    graph.add_edge("error_handler", END)

    return graph.compile()

# ===== 运行 =====

if __name__ == "__main__":
    graph = build_robust_graph()

    initial_state = {
        "input": "测试数据",
        "output": "",
        "error": None,
        "retry_count": 0,
        "fallback_used": False
    }

    result = graph.invoke(initial_state)

    print("\n=== 最终结果 ===")
    print(f"输出: {result['output']}")
    print(f"错误: {result.get('error', '无')}")
    print(f"重试次数: {result['retry_count']}")
    print(f"使用降级: {result['fallback_used']}")
```

---

## 错误处理最佳实践

### 实践 1：分类处理错误

根据错误类型采用不同策略。

```python
def smart_retry(func):
    """智能重试：根据错误类型决定策略"""
    try:
        return func()
    except ConnectionError:
        # 网络错误：短时间重试
        return retry(func, max_retries=3, delay=1)
    except TimeoutError:
        # 超时错误：长时间重试
        return retry(func, max_retries=2, delay=5)
    except ValueError:
        # 参数错误：不重试
        raise
    except Exception:
        # 其他错误：尝试一次
        return retry(func, max_retries=1, delay=2)
```

---

### 实践 2：记录错误详情

```python
import logging

logger = logging.getLogger(__name__)

def logged_retry(func, max_retries: int = 3):
    """带日志的重试"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            logger.error(
                f"尝试 {attempt + 1} 失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "attempt": attempt + 1
                }
            )

            if attempt == max_retries - 1:
                logger.critical("所有重试都失败")
                raise
```

---

## 最小验证

### 验证目标
- ✅ 理解重试策略
- ✅ 能够实现降级策略
- ✅ 能够处理错误恢复

### 验证步骤
1. 运行上面的完整示例
2. 修改重试参数，观察行为变化
3. 测试不同的错误场景
4. 验证降级策略是否生效

---

## 常见错误

### 错误 1：无限重试
```python
# 错误：没有重试次数限制
while True:
    try:
        return func()
    except:
        pass  # 永远重试！

# 正确：限制重试次数
for attempt in range(max_retries):
    try:
        return func()
    except:
        if attempt < max_retries - 1:
            continue
        raise
```

### 错误 2：重试所有错误
```python
# 错误：所有错误都重试
def bad_retry(func):
    for attempt in range(3):
        try:
            return func()
        except Exception as e:
            # ValueError 不应该重试
            pass

# 正确：只重试可恢复的错误
def good_retry(func):
    for attempt in range(3):
        try:
            return func()
        except (ConnectionError, TimeoutError):
            # 只重试网络和超时错误
            if attempt < 2:
                continue
            raise
        except ValueError:
            # 参数错误不重试
            raise
```

---

## 下一步

- 📖 `notes/06_memory_basics_short_term.md` - 短期记忆基础
- 🧪 `examples/07_retry_and_error_handling.py` - 重试与错误处理示例

---

**记住：错误处理就像备胎和保险，确保在出现问题时继续前进！** 🛡️
