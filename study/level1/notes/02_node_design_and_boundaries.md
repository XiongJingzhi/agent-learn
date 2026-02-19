# 节点设计与边界

> **目标**: 理解节点设计原则、单一职责、输入输出契约
> **预计时间**: 40 分钟
> **前置**: 已完成 StateGraph 基础学习

---

## 为什么节点设计很重要？

节点是 StateGraph 的核心执行单元，良好的节点设计能够：
- **提高可维护性**：每个节点职责清晰，易于理解和修改
- **提高可测试性**：节点可以独立测试
- **提高复用性**：节点可以在不同的图中复用

**类比**：节点就像**工厂里的工人**，每个工人负责一个明确的任务，配合完成整个生产流程。

---

## 节点设计原则

### 原则 1：单一职责（Single Responsibility）

每个节点应该只做一件事，并做好这件事。

**反例**：
```python
def bad_node(state: AgentState) -> dict:
    """不好的节点：做了太多事情"""
    # 1. 搜索信息
    search_result = search(state['input'])

    # 2. 处理数据
    processed = process(search_result)

    # 3. 格式化输出
    formatted = format(processed)

    # 4. 发送通知
    send_notification(formatted)

    # 5. 记录日志
    log(formatted)

    return {"output": formatted}
```

**正例**：
```python
def search_node(state: AgentState) -> dict:
    """搜索节点：只负责搜索"""
    search_result = search(state['input'])
    return {"search_result": search_result}

def process_node(state: AgentState) -> dict:
    """处理节点：只负责处理"""
    processed = process(state['search_result'])
    return {"processed_data": processed}

def format_node(state: AgentState) -> dict:
    """格式化节点：只负责格式化"""
    formatted = format(state['processed_data'])
    return {"output": formatted}
```

---

### 原则 2：明确的输入输出契约

节点应该明确定义：
- **需要什么状态字段**（输入）
- **返回什么状态字段**（输出）
- **可能的错误情况**

**示例**：
```python
def calculator_node(state: AgentState) -> dict:
    """
    计算器节点

    输入:
    - state['expression']: str - 数学表达式

    输出:
    - state['result']: float - 计算结果
    - state['error']: str | None - 错误信息（如果有）

    错误处理:
    - 表达式无效时返回错误信息
    """
    expression = state.get('expression', '')

    try:
        # 安全计算
        allowed = set('0123456789+-*/(). ')
        if not all(c in allowed for c in expression):
            raise ValueError("表达式包含非法字符")

        result = eval(expression)

        return {
            "result": result,
            "error": None
        }

    except Exception as e:
        return {
            "result": None,
            "error": str(e)
        }
```

---

### 原则 3：幂等性（Idempotence）

如果可能，节点应该是幂等的，即多次执行产生相同结果。

**示例**：
```python
def non_idempotent_node(state: AgentState) -> dict:
    """非幂等节点：每次执行都会累加"""
    count = state.get('count', 0)
    return {"count": count + 1}

def idempotent_node(state: AgentState) -> dict:
    """幂等节点：多次执行结果相同"""
    return {"timestamp": time.time()}
```

---

### 原则 4：可测试性

节点应该容易测试，避免复杂的依赖。

**示例**：
```python
# 容易测试的节点
def add_node(state: AgentState) -> dict:
    """容易测试：纯函数，无副作用"""
    a = state.get('a', 0)
    b = state.get('b', 0)
    return {"sum": a + b}

# 测试
def test_add_node():
    state = {"a": 1, "b": 2}
    result = add_node(state)
    assert result["sum"] == 3
```

---

## 节点类型

### 类型 1：LLM 节点

使用 LLM 进行推理和生成。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)

def llm_node(state: AgentState) -> dict:
    """LLM 节点：使用 LLM 生成内容"""
    prompt = f"""
    输入: {state['input']}
    上下文: {state.get('context', '')}

    请分析并给出建议。
    """

    response = llm.invoke(prompt)

    return {
        "llm_output": response.content,
        "llm_tokens_used": response.usage_metadata
    }
```

---

### 类型 2：工具调用节点

调用外部工具或 API。

```python
def search_tool_node(state: AgentState) -> dict:
    """搜索工具节点"""
    query = state.get('query', '')

    # 调用搜索 API
    results = search_api(query)

    return {
        "search_results": results,
        "search_query": query
    }
```

---

### 类型 3：数据处理节点

处理和转换数据。

```python
def data_cleaning_node(state: AgentState) -> dict:
    """数据清洗节点"""
    raw_data = state.get('raw_data', '')

    # 清洗数据
    cleaned = raw_data.strip().lower()

    return {"cleaned_data": cleaned}

def data_validation_node(state: AgentState) -> dict:
    """数据验证节点"""
    data = state.get('cleaned_data', '')

    # 验证数据
    is_valid = len(data) > 0 and data.isalnum()

    return {
        "is_valid": is_valid,
        "validation_error": None if is_valid else "数据无效"
    }
```

---

### 类型 4：路由节点

根据状态决定下一步。

```python
def routing_node(state: AgentState) -> dict:
    """路由节点：根据数据类型决定路由"""
    data_type = state.get('data_type', '')

    # 返回路由信息
    if data_type == 'text':
        return {"next_node": "text_processor"}
    elif data_type == 'image':
        return {"next_node": "image_processor"}
    else:
        return {"next_node": "default_processor"}
```

---

### 类型 5：聚合节点

聚合多个来源的数据。

```python
def aggregation_node(state: AgentState) -> dict:
    """聚合节点：合并多个数据源"""
    source1 = state.get('source1', [])
    source2 = state.get('source2', [])
    source3 = state.get('source3', [])

    # 合并数据
    aggregated = source1 + source2 + source3

    # 去重
    unique = list(set(aggregated))

    return {"aggregated_data": unique}
```

---

## 节点边界设计

### 边界 1：输入边界

节点应该检查和验证输入。

```python
def safe_node(state: AgentState) -> dict:
    """安全的节点：检查输入"""
    # 检查必需字段
    if 'input' not in state:
        raise ValueError("缺少必需字段: input")

    # 检查字段类型
    if not isinstance(state['input'], str):
        raise TypeError("input 必须是字符串")

    # 检查字段值
    if len(state['input']) == 0:
        raise ValueError("input 不能为空")

    # 处理逻辑
    result = process(state['input'])

    return {"output": result}
```

---

### 边界 2：输出边界

节点应该确保输出的有效性。

```python
def validated_output_node(state: AgentState) -> dict:
    """验证输出的节点"""
    # 处理逻辑
    result = process(state['input'])

    # 验证输出
    if result is None:
        result = "默认值"

    if not isinstance(result, str):
        result = str(result)

    return {"output": result}
```

---

### 边界 3：错误边界

节点应该优雅地处理错误。

```python
def error_handling_node(state: AgentState) -> dict:
    """带错误处理的节点"""
    try:
        # 尝试处理
        result = risky_operation(state['input'])

        return {
            "output": result,
            "error": None,
            "status": "success"
        }

    except ValueError as e:
        # 处理特定错误
        return {
            "output": None,
            "error": f"值错误: {str(e)}",
            "status": "error"
        }

    except Exception as e:
        # 处理其他错误
        return {
            "output": None,
            "error": f"未知错误: {str(e)}",
            "status": "error"
        }
```

---

## 节点组合模式

### 模式 1：顺序组合

多个节点按顺序执行。

```python
# 构建顺序执行的图
graph = StateGraph(AgentState)
graph.add_node("step1", step1_node)
graph.add_node("step2", step2_node)
graph.add_node("step3", step3_node)

graph.set_entry_point("step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", "step3")
graph.add_edge("step3", END)
```

---

### 模式 2：条件分支

根据条件选择不同的节点。

```python
def route_condition(state: AgentState) -> str:
    """路由条件"""
    if state['type'] == 'A':
        return 'process_a'
    elif state['type'] == 'B':
        return 'process_b'
    else:
        return 'process_default'

graph.add_conditional_edges(
    "router",
    route_condition,
    {
        'process_a': 'node_a',
        'process_b': 'node_b',
        'process_default': 'node_default'
    }
)
```

---

### 模式 3：循环组合

节点循环执行直到满足条件。

```python
def loop_condition(state: AgentState) -> str:
    """循环条件"""
    if state['count'] >= 3:
        return 'end'
    return 'continue'

graph.add_conditional_edges(
    "process",
    loop_condition,
    {
        'continue': 'process',  # 循环回自己
        'end': END
    }
)
```

---

## 完整示例：构建一个多节点处理流程

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

class ProcessingState(TypedDict):
    input: str
    validated: bool
    processed: str
    formatted: str
    error: str

def validate_node(state: ProcessingState) -> dict:
    """验证节点"""
    print("1. 验证输入...")

    if not state['input']:
        return {"error": "输入为空"}

    return {"validated": True}

def process_node(state: ProcessingState) -> dict:
    """处理节点"""
    print("2. 处理数据...")

    if not state.get('validated'):
        return {"error": "数据未验证"}

    processed = state['input'].upper()

    return {"processed": processed}

def format_node(state: ProcessingState) -> dict:
    """格式化节点"""
    print("3. 格式化输出...")

    if not state.get('processed'):
        return {"error": "数据处理失败"}

    formatted = f"结果: {state['processed']}"

    return {"formatted": formatted}

def error_node(state: ProcessingState) -> dict:
    """错误处理节点"""
    print(f"错误: {state.get('error', '未知错误')}")

    return {"formatted": f"错误: {state.get('error')}"}

def should_continue(state: ProcessingState) -> str:
    """判断是否有错误"""
    if state.get('error'):
        return "error"
    return "continue"

# 构建图
graph = StateGraph(ProcessingState)

# 添加节点
graph.add_node("validate", validate_node)
graph.add_node("process", process_node)
graph.add_node("format", format_node)
graph.add_node("error", error_node)

# 设置入口
graph.set_entry_point("validate")

# 添加边
graph.add_conditional_edges(
    "validate",
    should_continue,
    {
        "continue": "process",
        "error": "error"
    }
)

graph.add_conditional_edges(
    "process",
    should_continue,
    {
        "continue": "format",
        "error": "error"
    }
)

graph.add_edge("format", END)
graph.add_edge("error", END)

# 编译并运行
app = graph.compile()

result = app.invoke({"input": "hello"})
print(f"\n最终结果: {result['formatted']}")
```

---

## 最小验证

### 验证目标
- ✅ 理解节点设计原则
- ✅ 能够设计单一职责的节点
- ✅ 能够处理节点边界和错误

### 验证步骤
1. 运行上面的完整示例
2. 修改一个节点，添加错误处理
3. 创建一个新的节点，连接到图中
4. 测试不同的输入场景（正常、错误）

### 预期输出
```bash
python examples/04_node_design.py
```

应该看到：
- 节点按顺序执行
- 错误被正确处理
- 最终输出符合预期

---

## 常见错误

### 错误 1：节点职责不清晰
```python
# 错误：一个节点做了太多事情
def do_everything_node(state):
    # 搜索、处理、格式化都在一起
    pass

# 正确：拆分成多个节点
def search_node(state):
    pass

def process_node(state):
    pass

def format_node(state):
    pass
```

### 错误 2：忘记检查输入
```python
# 错误：直接使用可能不存在的字段
def bad_node(state):
    value = state['missing_field']  # 可能报错

# 正确：检查字段是否存在
def good_node(state):
    value = state.get('missing_field', 'default')
```

### 错误 3：没有处理错误
```python
# 错误：没有错误处理
def risky_node(state):
    result = risky_operation()  # 可能抛出异常
    return {"output": result}

# 正确：添加错误处理
def safe_node(state):
    try:
        result = risky_operation()
        return {"output": result}
    except Exception as e:
        return {"error": str(e)}
```

---

## 下一步

- 📖 `notes/03_edge_routing_patterns.md` - 边路由模式
- 🧪 `examples/04_node_design.py` - 节点设计示例

---

**记住：节点就像工厂里的工人，每个工人负责一个明确的任务！** 👷
