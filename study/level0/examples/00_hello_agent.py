"""
示例 00: Hello Agent

运行第一个 Agent，理解 Agent 的基本概念。

作者：Senior Developer
日期：2026-02-19
"""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

# 创建 LLM
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo"
)

# 创建简单的 Agent
class SimpleAgent:
    """简单的 Agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def invoke(self, user_input: str) -> str:
        """执行 Agent"""
        # 创建消息
        messages = [HumanMessage(content=user_input)]
        
        # 调用 LLM
        response = self.llm.invoke(messages)
        
        # 返回回复
        return response.content

# 创建 Agent
agent = SimpleAgent(llm)

# 执行
print("=" * 60)
print("Hello Agent 示例")
print("=" * 60)
print()

# 测试 1: 问候
print("测试 1: 问候")
result = agent.invoke("你好！")
print(f"用户: 你好！")
print(f"Agent: {result}")
print()

# 测试 2: 询问
print("测试 2: 询问")
result = agent.invoke("什么是 Agent？")
print(f"用户: 什么是 Agent？")
print(f"Agent: {result}")
print()

# 测试 3: 复杂查询
print("测试 3: 复杂查询")
result = agent.invoke("请用简单的语言解释 ReAct 循环的四个阶段。")
print(f"用户: 请用简单的语言解释 ReAct 循环的四个阶段。")
print(f"Agent: {result}")
print()

print("=" * 60)
print("Hello Agent 示例完成！")
print("=" * 60)
