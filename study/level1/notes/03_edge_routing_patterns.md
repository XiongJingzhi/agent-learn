# 边路由模式

> **目标**: 掌握条件边、循环边、终止边的使用
> **预计时间**: 35 分钟
> **前置**: 已完成节点设计学习

---

## 为什么需要边路由？

边（Edge）定义了节点之间的连接关系，边路由决定了：
- **执行流程**：节点按什么顺序执行
- **条件分支**：根据状态选择不同的路径
- **循环控制**：何时重复执行，何时结束

**类比**：边就像**道路的岔路口**，根据目的地选择不同的路线。

---

## 边的类型

### 类型 1：普通边（Normal Edge）

从一个节点直接连接到另一个节点。

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)

# 添加节点
graph.add_node("node_a", node_a_function)
graph.add_node("node_b", node_b_function)

# 普通边：从 node_a 到 node_b
graph.add_edge("node_a", "node_b")

# 终止边：从 node_b 到结束
graph.add_edge("node_b", END)
```

**特点**：
- 总是执行
- 单向连接
- 无条件跳转

---

### 类型 2：条件边（Conditional Edge）

根据状态决定下一个节点。

```python
def route_function(state: AgentState) -> str:
    """路由函数：返回下一个节点的名称"""
    if state['status'] == 'success':
        return 'success_node'
    elif state['status'] == 'retry':
        return 'retry_node'
    else:
        return 'error_node'

# 添加条件边
graph.add_conditional_edges(
    'current_node',           # 当前节点
    route_function,           # 路由函数
    {
        'success_node': 'node_success',   # 映射到目标节点
        'retry_node': 'node_retry',
        'error_node': 'node_error'
    }
)
```

**特点**：
- 根据状态动态选择
- 支持多个分支
- 需要明确的映射

---

### 类型 3：循环边（Loop Edge）

形成循环，重复执行节点。

```python
def should_continue(state: AgentState) -> str:
    """判断是否继续循环"""
    if state['count'] >= 3:
        return 'end'
    return 'continue'

# 条件边形成循环
graph.add_conditional_edges(
    'process_node',
    should_continue,
    {
        'continue': 'process_node',  # 循环回自己
        'end': END                    # 或到其他节点
    }
)
```

**特点**：
- 支持重复执行
- 需要终止条件
- 避免无限循环

---

## 路由函数设计

### 设计原则 1：纯函数

路由函数应该是纯函数，只根据状态做决策。

```python
# 好的路由函数：纯函数
def good_route(state: AgentState) -> str:
    """只根据状态做决策"""
    if state.get('is_valid', False):
        return 'process'
    return 'reject'

# 不好的路由函数：有副作用
def bad_route(state: AgentState) -> str:
    """修改了状态"""
    state['visited'] = True  # 副作用！
    return 'next'
```

---

### 设计原则 2：明确的返回值

路由函数的返回值必须在映射中定义。

```python
def route_function(state: AgentState) -> str:
    """路由函数"""
    # 只返回映射中定义的值
    if condition_a:
        return 'option_a'  # 必须在映射中
    elif condition_b:
        return 'option_b'  # 必须在映射中
    else:
        return 'option_c'  # 必须在映射中

graph.add_conditional_edges(
    'node',
    route_function,
    {
        'option_a': 'node_a',
        'option_b': 'node_b',
        'option_c': 'node_c'
    }
)
```

---

### 设计原则 3：处理边界情况

考虑所有可能的状态组合。

```python
def robust_route(state: AgentState) -> str:
    """健壮的路由函数"""
    # 检查关键字段
    if 'status' not in state:
        return 'error'

    status = state['status']

    # 处理所有可能的状态
    if status == 'success':
        return 'success'
    elif status == 'pending':
        return 'pending'
    elif status == 'failed':
        return 'retry'
    else:
        # 未知状态
        return 'error'
```

---

## 常见路由模式

### 模式 1：状态检查路由

根据状态字段决定路由。

```python
def status_route(state: AgentState) -> str:
    """状态检查路由"""
    status = state.get('status', '')

    if status == 'approved':
        return 'approve'
    elif status == 'rejected':
        return 'reject'
    elif status == 'review':
        return 'review'
    else:
        return 'default'

graph.add_conditional_edges(
    'check_status',
    status_route,
    {
        'approve': 'approved_node',
        'reject': 'rejected_node',
        'review': 'review_node',
        'default': 'default_node'
    }
)
```

---

### 模式 2：计数器路由

根据计数器决定路由。

```python
def counter_route(state: AgentState) -> str:
    """计数器路由"""
    count = state.get('count', 0)
    max_count = state.get('max_count', 3)

    if count >= max_count:
        return 'end'
    elif count < max_count // 2:
        return 'early'
    else:
        return 'late'

graph.add_conditional_edges(
    'process',
    counter_route,
    {
        'early': 'early_node',
        'late': 'late_node',
        'end': END
    }
)
```

---

### 模式 3：错误处理路由

根据错误类型决定路由。

```python
def error_route(state: AgentState) -> str:
    """错误处理路由"""
    error = state.get('error')

    if not error:
        return 'continue'  # 没有错误，继续

    # 根据错误类型路由
    if 'timeout' in str(error).lower():
        return 'retry'
    elif 'permission' in str(error).lower():
        return 'auth_error'
    elif 'not_found' in str(error).lower():
        return 'not_found'
    else:
        return 'generic_error'

graph.add_conditional_edges(
    'check_error',
    error_route,
    {
        'continue': 'next_node',
        'retry': 'retry_node',
        'auth_error': 'auth_node',
        'not_found': 'search_node',
        'generic_error': 'error_node'
    }
)
```

---

### 模式 4：复杂条件路由

根据多个条件决定路由。

```python
def complex_route(state: AgentState) -> str:
    """复杂条件路由"""
    # 检查多个条件
    is_valid = state.get('is_valid', False)
    is_authorized = state.get('is_authorized', False)
    priority = state.get('priority', 'normal')

    # 组合条件
    if not is_valid:
        return 'validate'
    elif not is_authorized:
        return 'authorize'
    elif priority == 'urgent':
        return 'urgent_process'
    elif priority == 'high':
        return 'high_process'
    else:
        return 'normal_process'

graph.add_conditional_edges(
    'check_conditions',
    complex_route,
    {
        'validate': 'validation_node',
        'authorize': 'auth_node',
        'urgent_process': 'urgent_node',
        'high_process': 'high_node',
        'normal_process': 'normal_node'
    }
)
```

---

## 完整示例：ReAct 循环的边路由

```python
from typing import TypedDict, Annotated, Sequence
from operator import add
from langgraph.graph import StateGraph, END

class ReActState(TypedDict):
    input: str
    thoughts: Annotated[Sequence[str], add]
    actions: Annotated[Sequence[str], add]
    observations: Annotated[Sequence[str], add]
    loop_count: int
    max_loops: int
    final_answer: str

def thought_node(state: ReActState) -> dict:
    """思考节点"""
    print(f"\n[思考 {state['loop_count']}]")
    thought = f"思考步骤 {state['loop_count']}"
    return {"thoughts": [thought], "loop_count": state['loop_count'] + 1}

def action_node(state: ReActState) -> dict:
    """行动节点"""
    print("[行动] 执行搜索")
    action = "搜索"
    observation = "找到相关信息"
    return {"actions": [action], "observations": [observation]}

def answer_node(state: ReActState) -> dict:
    """答案节点"""
    print("\n[答案] 生成最终答案")
    return {"final_answer": f"基于 {state['loop_count']} 次循环的答案"}

def should_continue(state: ReActState) -> str:
    """
    路由函数：决定是继续还是结束

    条件：
    1. 如果有最终答案，结束
    2. 如果达到最大循环次数，结束
    3. 否则继续
    """
    # 检查是否有最终答案
    if state.get('final_answer'):
        return 'end'

    # 检查是否达到最大循环次数
    if state['loop_count'] >= state['max_loops']:
        return 'end'

    # 继续循环
    return 'continue'

def build_react_graph():
    """构建 ReAct 循环图"""
    graph = StateGraph(ReActState)

    # 添加节点
    graph.add_node("thought", thought_node)
    graph.add_node("action", action_node)
    graph.add_node("answer", answer_node)

    # 设置入口
    graph.set_entry_point("thought")

    # 添加边：思考 -> (继续/结束)
    graph.add_conditional_edges(
        "thought",
        should_continue,
        {
            "continue": "action",  # 继续 -> 行动
            "end": "answer"        # 结束 -> 答案
        }
    )

    # 添加边：行动 -> 思考（形成循环）
    graph.add_edge("action", "thought")

    # 添加边：答案 -> 结束
    graph.add_edge("answer", END)

    return graph.compile()

# 运行
if __name__ == "__main__":
    graph = build_react_graph()

    initial_state = {
        "input": "什么是 LangGraph？",
        "thoughts": [],
        "actions": [],
        "observations": [],
        "loop_count": 0,
        "max_loops": 3,
        "final_answer": ""
    }

    result = graph.invoke(initial_state)

    print("\n=== 最终结果 ===")
    print(f"循环次数: {result['loop_count']}")
    print(f"思考过程: {result['thoughts']}")
    print(f"执行行动: {result['actions']}")
    print(f"观察结果: {result['observations']}")
    print(f"最终答案: {result['final_answer']}")
```

**输出示例**：
```
[思考 0]
[行动] 执行搜索

[思考 1]
[行动] 执行搜索

[思考 2]
[行动] 执行搜索

[答案] 生成最终答案

=== 最终结果 ===
循环次数: 3
思考过程: ['思考步骤 0', '思考步骤 1', '思考步骤 2']
执行行动: ['搜索', '搜索', '搜索']
观察结果: ['找到相关信息', '找到相关信息', '找到相关信息']
最终答案: 基于 3 次循环的答案
```

---

## 路由最佳实践

### 实践 1：使用常量定义路由值

```python
# 定义路由常量
ROUTE_CONTINUE = "continue"
ROUTE_END = "end"
ROUTE_RETRY = "retry"
ROUTE_ERROR = "error"

# 使用常量
def route_function(state: AgentState) -> str:
    if state.get('should_continue'):
        return ROUTE_CONTINUE
    return ROUTE_END

graph.add_conditional_edges(
    'node',
    route_function,
    {
        ROUTE_CONTINUE: 'next_node',
        ROUTE_END: END
    }
)
```

---

### 实践 2：组合多个条件

```python
def combined_route(state: AgentState) -> str:
    """组合多个条件"""
    # 提取常用字段
    is_valid = state.get('is_valid', False)
    count = state.get('count', 0)
    has_permission = state.get('has_permission', False)

    # 组合判断
    if not is_valid:
        return 'validate'
    if not has_permission:
        return 'permission'
    if count >= 3:
        return 'end'
    return 'continue'
```

---

### 实践 3：添加日志和调试

```python
def debug_route(state: AgentState) -> str:
    """带调试信息的路由函数"""
    # 记录状态
    print(f"[路由] 当前状态: {state.get('status')}")
    print(f"[路由] 计数: {state.get('count')}")

    # 路由逻辑
    result = actual_route(state)

    # 记录结果
    print(f"[路由] 决策: {result}")

    return result
```

---

## 最小验证

### 验证目标
- ✅ 理解三种边的类型
- ✅ 能够设计条件边
- ✅ 能够实现循环控制

### 验证步骤
1. 运行上面的 ReAct 循环示例
2. 修改 `should_continue` 函数，改变循环逻辑
3. 添加一个新的路由分支
4. 测试不同的路由场景

### 预期输出
```bash
python examples/05_edge_routing.py
```

应该看到：
- 路由函数正确选择下一个节点
- 循环在满足条件时结束
- 所有路由路径都正确执行

---

## 常见错误

### 错误 1：路由函数返回无效值
```python
# 错误：返回了映射中不存在的值
def bad_route(state):
    return 'invalid_route'  # 不在映射中！

# 正确：返回映射中定义的值
def good_route(state):
    return 'valid_route'  # 在映射中

graph.add_conditional_edges(
    'node',
    good_route,
    {
        'valid_route': 'next_node'  # 必须包含
    }
)
```

### 错误 2：忘记处理所有情况
```python
# 错误：没有处理所有可能的情况
def incomplete_route(state):
    if state['status'] == 'success':
        return 'success'
    # 忘记处理其他情况！

# 正确：处理所有情况
def complete_route(state):
    if state['status'] == 'success':
        return 'success'
    else:
        return 'default'  # 默认情况
```

### 错误 3：无限循环
```python
# 错误：可能造成无限循环
def infinite_loop_route(state):
    return 'continue'  # 总是返回 continue！

# 正确：有终止条件
def safe_loop_route(state):
    if state['count'] >= 3:
        return 'end'
    return 'continue'
```

---

## 下一步

- 📖 `notes/04_tool_calling_contracts.md` - 工具调用契约
- 🧪 `examples/05_edge_routing.py` - 边路由示例

---

**记住：边就像道路的岔路口，根据目的地选择不同的路线！** 🛣️
