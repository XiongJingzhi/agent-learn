"""
示例 02: 带工具的 Agent

实现一个带工具调用的 Agent，理解工具集成的概念。

作者：Senior Developer
日期：2026-02-19
"""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

# 创建 LLM
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo"
)

# 创建工具
def search_tool(query: str) -> str:
    """搜索工具（模拟）"""
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架",
        "langgraph": "LangGraph 是一个状态管理框架",
        "openai": "OpenAI 是一个 AI 研究实验室"
    }
    
    for key, value in results.items():
        if query.lower() in key.lower():
            return value
    
    return f"未找到与 '{query}' 相关的结果"

def calculator_tool(expression: str) -> str:
    """计算器工具（模拟）"""
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except:
        return f"无法计算：{expression}"

# 创建 LangChain 工具
tools = [
    Tool(
        name="search",
        func=search_tool,
        description="搜索关键词，返回相关信息"
    ),
    Tool(
        name="calculator",
        func=calculator_tool,
        description="计算数学表达式，支持加减乘除"
    )
]

# 创建 Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    verbose=True
)

# 创建 Agent 执行器
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

# 测试
print("=" * 60)
print("带工具的 Agent 示例")
print("=" * 60)
print()

# 测试 1: 搜索
print("测试 1: 搜索")
print("-" * 60)
try:
    result = agent_executor.invoke({
        "input": "搜索 LangChain 的文档"
    })
    print(f"用户: 搜索 LangChain 的文档")
    print(f"Agent: {result['output']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 2: 计算
print("测试 2: 计算")
print("-" * 60)
try:
    result = agent_executor.invoke({
        "input": "计算 1 + 1"
    })
    print(f"用户: 计算 1 + 1")
    print(f"Agent: {result['output']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 3: 复杂查询
print("测试 3: 复杂查询")
print("-" * 60)
try:
    result = agent_executor.invoke({
        "input": "请先搜索 LangChain，然后计算 1 + 1"
    })
    print(f"用户: 请先搜索 LangChain，然后计算 1 + 1")
    print(f"Agent: {result['output']}")
except Exception as e:
    print(f"错误: {e}")
print()

print("=" * 60)
print("带工具的 Agent 示例完成！")
print("=" * 60)
