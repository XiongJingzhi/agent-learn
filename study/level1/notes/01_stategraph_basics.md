# StateGraph 基础

> **目标**: 理解 StateGraph 的核心概念、状态定义和图结构构建
> **预计时间**: 45 分钟
> **前置**: 已完成 Level 0 学习

---

## 为什么需要 StateGraph？

LangGraph 的核心是 **StateGraph（状态图）**，它定义了：
- **状态（State）**：Agent 在执行过程中的数据
- **节点（Node）**：处理状态的函数
- **边（Edge）**：连接节点，定义执行流程

**类比**：StateGraph 就像一个**工作流程图**，定义了从一个状态到另一个状态的转换规则。

---

## StateGraph 核心概念

### 1. State（状态）

状态是 Agent 在执行过程中的数据容器。

**示例**：
```python
from typing import TypedDict, Annotated, Sequence
from operator import add
from langgraph.graph import StateGraph

# 定义状态类型
class AgentState(TypedDict):
    # 用户输入
    input: str
    # Agent 输出
    output: str
    # 中间步骤
    steps: Annotated[Sequence[str], add]
    # 当前循环次数
    loop_count: int
```

**要点**：
- 使用 `TypedDict` 定义状态类型
- 使用 `Annotated` 定义状态的更新方式（如 `add` 表示追加）
- 状态是不可变的，每次更新都会创建新的状态

---

### 2. Node（节点）

节点是处理状态的函数，接收状态并返回状态更新。

**示例**：
```python
from langgraph.graph import StateGraph, END

def reasoning_node(state: AgentState) -> dict:
    """推理节点：分析当前情况，决定下一步行动"""
    print(f"推理中...循环次数: {state['loop_count']}")

    # 简单的推理逻辑
    if state['loop_count'] < 3:
        next_action = "continue"
    else:
        next_action = "finish"

    return {
        "steps": ["推理完成"],
        "loop_count": state['loop_count'] + 1,
        "output": f"决定: {next_action}"
    }

def action_node(state: AgentState) -> dict:
    """行动节点：执行具体的行动"""
    print(f"执行行动...")

    return {
        "steps": ["行动执行完成"],
        "output": "行动已执行"
    }
```

**要点**：
- 节点函数接收完整的状态作为参数
- 返回一个字典，包含要更新的状态字段
- 节点可以访问和修改状态

---

### 3. Edge（边）

边连接节点，定义执行流程。

**边类型**：

| 类型 | 说明 | 示例 |
|------|------|------|
| **普通边** | 从一个节点到另一个节点 | `graph.add_edge("node_a", "node_b")` |
| **条件边** | 根据状态决定下一个节点 | `graph.add_conditional_edges(...)` |
| **终止边** | 结束执行 | `graph.add_edge("node", END)` |

**示例**：
```python
# 普通边：从 reasoning_node 到 action_node
graph.add_edge("reasoning", "action")

# 条件边：根据输出决定下一步
def should_continue(state: AgentState) -> str:
    """判断是否继续循环"""
    if state['loop_count'] >= 3:
        return "end"
    return "continue"

graph.add_conditional_edges(
    "reasoning",
    should_continue,
    {
        "continue": "action",  # 继续 -> action 节点
        "end": END             # 结束 -> 终止
    }
)
```

---

## 完整示例：构建一个简单的 ReAct 循环

```python
from typing import TypedDict, Annotated, Sequence
from operator import add
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# 1. 定义状态
class ReActState(TypedDict):
    input: str
    thoughts: Annotated[Sequence[str], add]
    actions: Annotated[Sequence[str], add]
    observations: Annotated[Sequence[str], add]
    loop_count: int
    final_answer: str

# 2. 定义节点
llm = ChatOpenAI(temperature=0)

def thought_node(state: ReActState) -> dict:
    """思考节点：分析当前情况"""
    print(f"\n=== 思考 (循环 {state['loop_count']}) ===")

    # 使用 LLM 生成思考
    prompt = f"输入: {state['input']}\n" \
             f"历史思考: {state['thoughts']}\n" \
             f"历史行动: {state['actions']}\n" \
             f"历史观察: {state['observations']}\n" \
             "下一步应该做什么？"

    thought = llm.invoke(prompt).content

    return {
        "thoughts": [thought],
        "loop_count": state['loop_count'] + 1
    }

def action_node(state: ReActState) -> dict:
    """行动节点：执行工具调用"""
    print("=== 行动 ===")

    # 简单的模拟工具调用
    action = "搜索信息"
    observation = "找到相关信息"

    print(f"行动: {action}")
    print(f"观察: {observation}")

    return {
        "actions": [action],
        "observations": [observation]
    }

def answer_node(state: ReActState) -> dict:
    """答案节点：生成最终答案"""
    print("\n=== 生成答案 ===")

    answer = f"基于 {state['loop_count']} 次循环，我找到了答案。"

    return {
        "final_answer": answer
    }

# 3. 定义路由函数
def should_continue(state: ReActState) -> str:
    """判断是否继续"""
    if state['loop_count'] >= 3:
        return "answer"
    return "continue"

# 4. 构建图
def build_react_graph():
    """构建 ReAct 循环图"""
    graph = StateGraph(ReActState)

    # 添加节点
    graph.add_node("thought", thought_node)
    graph.add_node("action", action_node)
    graph.add_node("answer", answer_node)

    # 设置入口
    graph.set_entry_point("thought")

    # 添加边
    graph.add_conditional_edges(
        "thought",
        should_continue,
        {
            "continue": "action",
            "answer": "answer"
        }
    )
    graph.add_edge("action", "thought")
    graph.add_edge("answer", END)

    # 编译图
    return graph.compile()

# 5. 运行
if __name__ == "__main__":
    # 构建图
    graph = build_react_graph()

    # 初始状态
    initial_state = {
        "input": "什么是 LangGraph？",
        "thoughts": [],
        "actions": [],
        "observations": [],
        "loop_count": 0,
        "final_answer": ""
    }

    # 执行
    result = graph.invoke(initial_state)

    # 输出结果
    print("\n=== 最终结果 ===")
    print(f"思考过程: {result['thoughts']}")
    print(f"执行行动: {result['actions']}")
    print(f"观察结果: {result['observations']}")
    print(f"最终答案: {result['final_answer']}")
```

**输出示例**：
```
=== 思考 (循环 0) ===
=== 行动 ===
行动: 搜索信息
观察: 找到相关信息

=== 思考 (循环 1) ===
=== 行动 ===
行动: 搜索信息
观察: 找到相关信息

=== 思考 (循环 2) ===
=== 行动 ===
行动: 搜索信息
观察: 找到相关信息

=== 思考 (循环 3) ===
=== 生成答案 ===

=== 最终结果 ===
思考过程: [...]
执行行动: [...]
观察结果: [...]
最终答案: 基于 3 次循环，我找到了答案。
```

---

## 关键设计决策

### 决策 1：状态类型的选择

**选项**：
- **TypedDict**：简单、静态类型检查
- **dataclass**：更灵活、支持方法
- **pydantic BaseModel**：强验证、序列化支持

**推荐**：Level 1 使用 `TypedDict`，简单直接

---

### 决策 2：状态更新方式

**选项**：
- **替换**：完全替换状态字段
- **追加**：追加到列表（使用 `Annotated[..., add]`）

**示例**：
```python
# 替换
return {"output": "新值"}

# 追加
return {"steps": ["新步骤"]}  # 会追加到现有列表
```

---

### 决策 3：错误处理

```python
def safe_node(state: AgentState) -> dict:
    """带错误处理的节点"""
    try:
        # 执行逻辑
        result = do_something()
        return {"output": result}
    except Exception as e:
        # 返回错误状态
        return {"output": f"错误: {str(e)}"}
```

---

## 最小验证

### 验证目标
- ✅ 理解 State、Node、Edge 的概念
- ✅ 能够构建简单的 StateGraph
- ✅ 能够运行和调试 StateGraph

### 验证步骤
1. 运行上面的完整示例
2. 修改 `should_continue` 函数，改变循环次数
3. 添加一个新的节点，连接到图中
4. 记录输入、输出和结论

### 预期输出
```bash
python examples/03_stategraph_basics.py
```

应该看到：
- ReAct 循环执行了 3 次
- 每次循环包含思考和行动
- 最后生成最终答案

---

## 常见错误

### 错误 1：状态类型不匹配
```python
# 错误：返回了不存在的字段
return {"non_existent_field": "value"}

# 正确：只返回定义过的字段
return {"output": "value"}
```

### 错误 2：忘记设置入口
```python
# 错误：忘记设置入口
graph = StateGraph(AgentState)
graph.add_node("node1", node1)
# graph.set_entry_point("node1")  # 忘记了
compiled = graph.compile()  # 报错

# 正确：设置入口
graph.set_entry_point("node1")
```

### 错误 3：条件边返回无效值
```python
# 错误：返回了条件边中不定义的值
def should_continue(state):
    if condition:
        return "yes"  # "yes" 不在条件边的映射中
    return "no"

# 正确：返回映射中定义的值
def should_continue(state):
    if condition:
        return "continue"
    return "end"
```

---

## 下一步

- 📖 `notes/02_node_design_and_boundaries.md` - 节点设计与边界
- 📖 `notes/03_edge_routing_patterns.md` - 边路由模式
- 🧪 `examples/03_stategraph_basics.py` - StateGraph 基础示例

---

**记住：StateGraph 就像一个工作流程图，定义了从一个状态到另一个状态的转换规则！** 📊
