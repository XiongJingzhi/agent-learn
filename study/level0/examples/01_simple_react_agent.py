"""
示例 01: 简单的 ReAct Agent

实现一个简单的 ReAct Agent，理解 ReAct 循环的四个阶段。

作者：Senior Developer
日期：2026-02-19
"""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

# 创建 LLM
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

# 创建工具
def get_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date() -> str:
    """获取当前日期"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

time_tool = Tool(
    name="get_time",
    func=get_time,
    description="获取当前时间，格式：YYYY-MM-DD HH:MM:SS"
)

date_tool = Tool(
    name="get_date",
    func=get_date,
    description="获取当前日期，格式：YYYY-MM-DD"
)

# 创建 ReAct Agent
agent = create_react_agent(
    llm=llm,
    tools=[time_tool, date_tool],
    verbose=True
)

# 创建 Agent 执行器
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[time_tool, date_tool],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

# 测试
print("=" * 60)
print("ReAct Agent 示例")
print("=" * 60)
print()

# 测试 1: 获取时间
print("测试 1: 获取时间")
print("-" * 60)
try:
    result = agent_executor.invoke({"input": "现在几点了？"})
    print(f"用户: 现在几点了？")
    print(f"Agent: {result['output']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 2: 获取日期
print("测试 2: 获取日期")
print("-" * 60)
try:
    result = agent_executor.invoke({"input": "今天是几号？"})
    print(f"用户: 今天是几号？")
    print(f"Agent: {result['output']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 3: 复杂查询
print("测试 3: 复杂查询")
print("-" * 60)
try:
    result = agent_executor.invoke({"input": "请告诉我现在的日期和时间"})
    print(f"用户: 请告诉我现在的日期和时间")
    print(f"Agent: {result['output']}")
except Exception as e:
    print(f"错误: {e}")
print()

print("=" * 60)
print("ReAct Agent 示例完成！")
print("=" * 60)
