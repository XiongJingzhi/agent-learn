"""
示例 04: 节点设计与边界

演示节点设计原则和边界处理：
- 单一职责原则
- 输入输出契约
- 错误处理
- 节点组合模式

作者：Senior Developer
日期：2026-02-19
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
import time

# ===== 1. 定义状态 =====

class ProcessingState(TypedDict):
    """处理状态"""
    input: str
    validated: bool
    processed: str
    formatted: str
    error: str

# ===== 2. 单一职责节点 =====

def validate_input_node(state: ProcessingState) -> dict:
    """
    验证节点：只负责验证输入

    单一职责：只验证，不做其他事情
    """
    print("[1/3] 验证输入...")
    time.sleep(0.2)

    # 输入边界检查
    if not state.get('input'):
        return {"error": "输入为空"}

    if not isinstance(state['input'], str):
        return {"error": "输入必须是字符串"}

    if len(state['input']) == 0:
        return {"error": "输入长度不能为 0"}

    print("✓ 输入验证通过")

    return {"validated": True, "error": ""}

def process_data_node(state: ProcessingState) -> dict:
    """
    处理节点：只负责处理数据

    单一职责：只处理，不做验证
    """
    print("[2/3] 处理数据...")
    time.sleep(0.2)

    # 检查前置条件
    if not state.get('validated'):
        return {"error": "数据未验证"}

    # 处理逻辑
    processed = state['input'].upper().strip()

    print(f"✓ 数据已处理: {processed}")

    return {"processed": processed}

def format_output_node(state: ProcessingState) -> dict:
    """
    格式化节点：只负责格式化输出

    单一职责：只格式化，不做处理
    """
    print("[3/3] 格式化输出...")
    time.sleep(0.2)

    # 检查前置条件
    if not state.get('processed'):
        return {"error": "数据处理失败"}

    # 格式化逻辑
    formatted = f"结果: {state['processed']}"

    print(f"✓ 输出已格式化")

    return {"formatted": formatted}

# ===== 3. 错误处理节点 =====

def error_handling_node(state: ProcessingState) -> dict:
    """
    错误处理节点：处理所有错误

    边界：优雅地处理错误，提供有意义的错误信息
    """
    error = state.get('error', '未知错误')

    print(f"[错误] {error}")

    return {
        "formatted": f"处理失败: {error}",
        "error": error
    }

# ===== 4. 路由函数 =====

def check_error(state: ProcessingState) -> str:
    """
    检查是否有错误

    Returns:
        "error" 或 "continue"
    """
    if state.get('error'):
        return "error"
    return "continue"

def check_validation(state: ProcessingState) -> str:
    """
    检查是否验证通过

    Returns:
        "process" 或 "error"
    """
    if not state.get('validated'):
        return "error"
    return "process"

# ===== 5. 构建图 =====

def build_processing_graph():
    """
    构建处理流程图

    图结构：
    validate -> (process -> format -> END)
             -> (error -> END)
    """
    graph = StateGraph(ProcessingState)

    # 添加节点
    graph.add_node("validate", validate_input_node)
    graph.add_node("process", process_data_node)
    graph.add_node("format", format_output_node)
    graph.add_node("error", error_handling_node)

    # 设置入口
    graph.set_entry_point("validate")

    # 添加条件边：validate -> (process, error)
    graph.add_conditional_edges(
        "validate",
        check_validation,
        {
            "process": "process",
            "error": "error"
        }
    )

    # 添加条件边：process -> (format, error)
    graph.add_conditional_edges(
        "process",
        check_error,
        {
            "continue": "format",
            "error": "error"
        }
    )

    # 添加边：format -> END
    graph.add_edge("format", END)
    graph.add_edge("error", END)

    return graph.compile()

# ===== 6. 运行示例 =====

def main():
    """主函数"""
    print("=" * 70)
    print("节点设计示例 - 单一职责与边界处理")
    print("=" * 70)

    graph = build_processing_graph()

    # 测试用例
    test_cases = [
        {"input": "hello world"},      # 正常情况
        {"input": ""},                 # 错误：空输入
        {"input": "LANGGRAPH"},        # 正常情况
    ]

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"测试用例 {i}: {test_input}")
        print('=' * 70)

        result = graph.invoke(test_input)

        print(f"\n结果:")
        print(f"  输入: {test_input.get('input', '')}")
        print(f"  输出: {result.get('formatted', '')}")
        print(f"  错误: {result.get('error', '无')}")
        print(f"  验证: {result.get('validated', False)}")

    # 设计原则总结
    print("\n" + "=" * 70)
    print("节点设计原则总结:")
    print("=" * 70)
    print("""
1. 单一职责原则
   - 每个节点只做一件事
   - validate: 只验证输入
   - process: 只处理数据
   - format: 只格式化输出

2. 输入输出契约
   - 明确定义输入参数
   - 明确定义输出字段
   - 检查前置条件

3. 边界处理
   - 验证输入参数
   - 处理错误情况
   - 提供有意义的错误信息

4. 节点组合
   - 通过边连接节点
   - 使用条件边实现分支
   - 形成完整的处理流程
    """)

if __name__ == "__main__":
    main()
