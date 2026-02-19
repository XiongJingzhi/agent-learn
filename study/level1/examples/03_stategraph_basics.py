"""
示例 03: StateGraph 基础示例

演示 StateGraph 的核心概念：
- State（状态）定义
- Node（节点）实现
- Edge（边）路由
- 完整的 ReAct 循环

作者：Senior Developer
日期：2026-02-19
"""

from typing import TypedDict, Annotated, Sequence
from operator import add
from langgraph.graph import StateGraph, END

# ===== 1. 定义状态 =====

class AgentState(TypedDict):
    """Agent 状态定义"""
    # 用户输入
    input: str
    # Agent 输出
    output: str
    # 中间步骤（使用 Annotated 实现追加）
    steps: Annotated[Sequence[str], add]
    # 当前循环次数
    loop_count: int
    # 最大循环次数
    max_loops: int

# ===== 2. 定义节点 =====

def reasoning_node(state: AgentState) -> dict:
    """
    推理节点：分析当前情况，决定下一步行动

    这个节点演示了：
    - 读取状态
    - 执行逻辑
    - 返回状态更新
    """
    print(f"\n[推理 {state['loop_count']}]")

    # 简单的推理逻辑
    if state['loop_count'] < state['max_loops']:
        next_action = "继续执行行动"
        should_continue = True
    else:
        next_action = "生成最终答案"
        should_continue = False

    thought = f"第 {state['loop_count']} 次推理: {next_action}"

    print(f"思考: {thought}")

    return {
        "steps": [thought],
        "loop_count": state['loop_count'] + 1
    }

def action_node(state: AgentState) -> dict:
    """
    行动节点：执行具体的行动

    这个节点演示了：
    - 模拟工具调用
    - 生成观察结果
    """
    print("[行动] 执行搜索")

    # 模拟搜索工具
    action = "搜索信息"
    observation = "找到相关信息: LangGraph 是一个状态管理框架"

    print(f"行动: {action}")
    print(f"观察: {observation}")

    return {
        "steps": [f"行动: {action}", f"观察: {observation}"]
    }

def answer_node(state: AgentState) -> dict:
    """
    答案节点：生成最终答案

    这个节点演示了：
    - 总结执行过程
    - 生成最终输出
    """
    print("\n[答案] 生成最终答案")

    answer = f"基于 {state['loop_count']} 次循环的推理和行动，我找到了答案。"

    return {
        "output": answer,
        "steps": [f"最终答案: {answer}"]
    }

# ===== 3. 定义路由函数 =====

def should_continue(state: AgentState) -> str:
    """
    路由函数：决定是继续还是结束

    Args:
        state: 当前状态

    Returns:
        str: "continue" 或 "end"
    """
    # 检查是否达到最大循环次数
    if state['loop_count'] >= state['max_loops']:
        return "end"

    # 继续循环
    return "continue"

# ===== 4. 构建图 =====

def build_react_graph():
    """
    构建 ReAct 循环图

    图结构：
    reasoning -> (continue -> action -> reasoning)
             -> (end -> answer -> END)
    """
    graph = StateGraph(AgentState)

    # 添加节点
    graph.add_node("reasoning", reasoning_node)
    graph.add_node("action", action_node)
    graph.add_node("answer", answer_node)

    # 设置入口点
    graph.set_entry_point("reasoning")

    # 添加条件边：reasoning -> (continue -> action, end -> answer)
    graph.add_conditional_edges(
        "reasoning",
        should_continue,
        {
            "continue": "action",  # 继续 -> 行动节点
            "end": "answer"        # 结束 -> 答案节点
        }
    )

    # 添加边：action -> reasoning（形成循环）
    graph.add_edge("action", "reasoning")

    # 添加边：answer -> END
    graph.add_edge("answer", END)

    # 编译图
    return graph.compile()

# ===== 5. 运行示例 =====

def main():
    """主函数"""
    print("=" * 70)
    print("StateGraph 基础示例 - ReAct 循环")
    print("=" * 70)

    # 构建图
    graph = build_react_graph()

    # 初始状态
    initial_state = {
        "input": "什么是 LangGraph？",
        "output": "",
        "steps": [],
        "loop_count": 0,
        "max_loops": 3
    }

    print(f"\n输入: {initial_state['input']}")
    print(f"最大循环次数: {initial_state['max_loops']}")
    print("\n开始执行...")

    # 执行图
    result = graph.invoke(initial_state)

    # 输出结果
    print("\n" + "=" * 70)
    print("执行完成")
    print("=" * 70)

    print(f"\n最终循环次数: {result['loop_count']}")
    print(f"\n执行步骤:")
    for i, step in enumerate(result['steps'], 1):
        print(f"  {i}. {step}")

    print(f"\n最终答案:\n  {result['output']}")

    # 可视化图结构
    print("\n" + "=" * 70)
    print("图结构:")
    print("=" * 70)
    print("""
    reasoning ───(continue)──> action ──┐
       │                           │
       └──────(end)──> answer ────> END
             ↑                     │
             └─────────────────────┘
    """)

if __name__ == "__main__":
    main()
