"""
示例 05: 边路由模式

演示条件边、循环边、终止边的使用：
- 普通边
- 条件边
- 循环边
- 复杂路由逻辑

作者：Senior Developer
日期：2026-02-19
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# ===== 1. 定义状态 =====

class RoutingState(TypedDict):
    """路由状态"""
    input: str
    status: str
    priority: str
    count: int
    output: str

# ===== 2. 定义节点 =====

def classify_node(state: RoutingState) -> dict:
    """分类节点：判断输入类型"""
    print("\n[分类] 分析输入...")
    input_str = state['input'].lower()

    # 简单分类逻辑
    if any(word in input_str for word in ['urgent', '紧急', '急']):
        status = 'urgent'
        priority = 'high'
    elif any(word in input_str for word in ['error', '错误', '失败']):
        status = 'error'
        priority = 'high'
    elif any(word in input_str for word in ['question', '问题', '？', '?']):
        status = 'question'
        priority = 'normal'
    else:
        status = 'normal'
        priority = 'normal'

    print(f"状态: {status}, 优先级: {priority}")

    return {"status": status, "priority": priority}

def urgent_handler_node(state: RoutingState) -> dict:
    """紧急处理节点"""
    print("[紧急处理] 高优先级处理")
    return {"output": f"紧急处理完成: {state['input']}"}

def error_handler_node(state: RoutingState) -> dict:
    """错误处理节点"""
    print("[错误处理] 处理错误情况")
    return {"output": f"错误已记录: {state['input']}"}

def question_handler_node(state: RoutingState) -> dict:
    """问题处理节点"""
    print("[问题处理] 回答问题")
    return {"output": f"问题答案: {state['input']}"}

def normal_handler_node(state: RoutingState) -> dict:
    """普通处理节点"""
    print("[普通处理] 标准处理流程")
    return {"output": f"已处理: {state['input']}"}

def retry_node(state: RoutingState) -> dict:
    """重试节点"""
    count = state.get('count', 0) + 1
    print(f"[重试] 第 {count} 次重试")
    return {"count": count}

# ===== 3. 路由函数 =====

def route_by_status(state: RoutingState) -> str:
    """
    状态路由：根据 status 字段决定路由

    Returns:
        路由目标节点名称
    """
    status = state.get('status', 'normal')
    priority = state.get('priority', 'normal')

    print(f"[路由] status={status}, priority={priority}")

    # 组合条件路由
    if status == 'urgent' and priority == 'high':
        return 'urgent_handler'
    elif status == 'error':
        return 'error_handler'
    elif status == 'question':
        return 'question_handler'
    else:
        return 'normal_handler'

def should_retry(state: RoutingState) -> str:
    """
    重试判断：决定是否重试

    Returns:
        "retry" 或 "end"
    """
    count = state.get('count', 0)
    max_retries = 2

    if count < max_retries and state.get('status') == 'error':
        print(f"[重试判断] 将进行第 {count + 1} 次重试")
        return 'retry'

    print("[重试判断] 达到最大重试次数或无需重试")
    return 'end'

# ===== 4. 构建图 =====

def build_routing_graph():
    """
    构建路由图

    图结构：
    classify -> urgent_handler -> END
             -> error_handler -> (retry -> classify) -> END
             -> question_handler -> END
             -> normal_handler -> END
    """
    graph = StateGraph(RoutingState)

    # 添加节点
    graph.add_node("classify", classify_node)
    graph.add_node("urgent_handler", urgent_handler_node)
    graph.add_node("error_handler", error_handler_node)
    graph.add_node("question_handler", question_handler_node)
    graph.add_node("normal_handler", normal_handler_node)
    graph.add_node("retry", retry_node)

    # 设置入口
    graph.set_entry_point("classify")

    # 添加条件边：classify -> 多个处理器
    graph.add_conditional_edges(
        "classify",
        route_by_status,
        {
            "urgent_handler": "urgent_handler",
            "error_handler": "error_handler",
            "question_handler": "question_handler",
            "normal_handler": "normal_handler"
        }
    )

    # 添加条件边：error_handler -> (retry -> classify 或 end)
    graph.add_conditional_edges(
        "error_handler",
        should_retry,
        {
            "retry": "retry",  # 循环边：回到 classify
            "end": END
        }
    )

    # 添加边：retry -> classify（形成循环）
    graph.add_edge("retry", "classify")

    # 添加其他终止边
    graph.add_edge("urgent_handler", END)
    graph.add_edge("question_handler", END)
    graph.add_edge("normal_handler", END)

    return graph.compile()

# ===== 5. 运行示例 =====

def main():
    """主函数"""
    print("=" * 70)
    print("边路由模式示例")
    print("=" * 70)

    graph = build_routing_graph()

    # 测试用例
    test_cases = [
        "紧急：服务器宕机了",           # urgent
        "出错了，无法连接数据库",       # error
        "LangGraph 是什么？",          # question
        "这是一个普通的消息",          # normal
    ]

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"测试 {i}: {test_input}")
        print('=' * 70)

        initial_state = {
            "input": test_input,
            "status": "",
            "priority": "",
            "count": 0,
            "output": ""
        }

        result = graph.invoke(initial_state)

        print(f"\n最终结果:")
        print(f"  输出: {result['output']}")
        print(f"  次数: {result['count']}")

    # 路由模式总结
    print("\n" + "=" * 70)
    print("路由模式总结:")
    print("=" * 70)
    print("""
1. 普通边（Normal Edge）
   - 从一个节点直接连接到另一个节点
   - 总是执行，无条件跳转

2. 条件边（Conditional Edge）
   - 根据状态动态选择下一个节点
   - 支持多个分支
   - 需要路由函数和映射

3. 循环边（Loop Edge）
   - 通过条件边形成循环
   - 需要终止条件
   - 避免无限循环

4. 路由函数设计
   - 纯函数：只根据状态做决策
   - 明确返回值：返回映射中定义的值
   - 处理边界情况：考虑所有可能的状态
    """)

if __name__ == "__main__":
    main()
