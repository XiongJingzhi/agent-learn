"""
08_first_agent.py
第一个完整的 Agent 示例

构建一个能够搜索信息、计算、回答问题的简单 Agent
"""

import os
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

# ==================== 定义工具 ====================

@tool
def search_database(query: str) -> str:
    """在数据库中搜索信息

    Args:
        query: 搜索关键词

    Returns:
        搜索结果
    """
    # 模拟数据库
    database = {
        "LangChain": "LangChain 是一个用于构建 LLM 应用的框架",
        "Python": "Python 是一种高级编程语言",
        "AI": "AI（人工智能）是计算机科学的一个分支",
        "Agent": "Agent 是能够自主感知和行动的智能体"
    }

    # 搜索
    results = []
    for key, value in database.items():
        if query.lower() in key.lower() or query.lower() in value.lower():
            results.append(f"{key}: {value}")

    if results:
        return "\n".join(results)
    else:
        return f"未找到关于 '{query}' 的信息"


@tool
def calculator(expression: str) -> str:
    """计算数学表达式

    Args:
        expression: 数学表达式，如 '2 + 2' 或 '10 * 5'

    Returns:
        计算结果
    """
    try:
        # 安全计算：只允许数字和基本运算符
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含非法字符"

        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


@tool
def text_analyzer(text: str) -> str:
    """分析文本的统计信息

    Args:
        text: 要分析的文本

    Returns:
        文本统计信息
    """
    word_count = len(text.split())
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))

    return f"""文本分析结果：
- 字数（单词）：{word_count}
- 字符数（含空格）：{char_count}
- 字符数（不含空格）：{char_count_no_spaces}
"""


# ==================== 创建 Agent ====================

print("\n" + "="*70)
print("创建你的第一个 Agent")
print("="*70 + "\n")

# 1. 创建 LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 2. 准备工具列表
tools = [search_database, calculator, text_analyzer]

# 3. 加载 ReAct 提示模板
try:
    prompt = hub.pull("hwchase17/react")

    # 4. 创建 Agent
    agent = create_react_agent(llm, tools, prompt)

    # 5. 创建执行器
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    # ==================== 使用 Agent ====================

    print("✓ Agent 创建成功！\n")

    # 示例 1：搜索信息
    print("\n" + "-"*70)
    print("任务 1：搜索 LangChain 的信息")
    print("-"*70 + "\n")

    result1 = agent_executor.invoke({
        "input": "什么是 LangChain？"
    })

    print(f"\n回答: {result1['output']}\n")


    # 示例 2：计算
    print("\n" + "-"*70)
    print("任务 2：计算 15 * 8 + 32")
    print("-"*70 + "\n")

    result2 = agent_executor.invoke({
        "input": "请帮我计算 15 * 8 + 32"
    })

    print(f"\n回答: {result2['output']}\n")


    # 示例 3：文本分析
    print("\n" + "-"*70)
    print("任务 3：分析文本")
    print("-"*70 + "\n")

    result3 = agent_executor.invoke({
        "input": "请分析这段文本的统计信息：LangChain is a framework for building LLM applications"
    })

    print(f"\n回答: {result3['output']}\n")


    # 示例 4：复杂任务
    print("\n" + "-"*70)
    print("任务 4：复杂任务（搜索 + 计算）")
    print("-"*70 + "\n")

    result4 = agent_executor.invoke({
        "input": "先搜索 AI 的信息，然后计算 100 除以 4"
    })

    print(f"\n回答: {result4['output']}\n")


    # ==================== 交互模式 ====================

    print("\n" + "="*70)
    print("交互模式（输入 'quit' 退出）")
    print("="*70 + "\n")

    while True:
        user_input = input("\n你: ")

        if user_input.lower() in ['quit', 'exit', '退出']:
            print("\n再见！👋\n")
            break

        try:
            result = agent_executor.invoke({"input": user_input})
            print(f"\nAgent: {result['output']}")
        except Exception as e:
            print(f"\nAgent: 抱歉，我遇到了一些问题：{str(e)}")


except Exception as e:
    print(f"\n❌ 创建 Agent 失败: {e}")
    print("\n提示：")
    print("  1. 确保已安装所有依赖：")
    print("     pip install langchain langchain-openai langchainhub")
    print("\n  2. 确保已设置 OpenAI API Key：")
    print("     export OPENAI_API_KEY='your-api-key'")
    print("\n  3. 检查网络连接\n")


# ==================== 学习指南 ====================

print("\n" + "="*70)
print("学习指南")
print("="*70 + "\n")

guide = """
恭喜你创建了第一个 Agent！下面是一些学习建议：

📚 接下来的学习步骤：

1. 📖 理解 Agent 的核心概念
   - 阅读 Level 0 的其他笔记
   - 重点理解 ReAct 循环

2. 🛠️ 修改和扩展这个 Agent
   - 添加新的工具
   - 修改提示词
   - 观察行为变化

3. 🎯 尝试构建自己的 Agent
   - 定义具体的应用场景
   - 选择合适的工具
   - 测试和优化

💡 关键概念回顾：

- Tool（工具）：Agent 能执行的操作
- ReAct 循环：思考（Thought）→ 行动（Action）→ 观察（Observation）
- Agent Executor：管理 Agent 的执行过程

🚀 下一步：

- 学习 Level 1：LangGraph 单 Agent 基础
- 实践更复杂的 Agent 应用
- 探索 LangChain 的其他功能
"""

print(guide)
