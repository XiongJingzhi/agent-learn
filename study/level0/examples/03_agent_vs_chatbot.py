"""
示例 03: Agent vs Chatbot 对比

对比 Agent 和 Chatbot 的实现差异，理解两种模式的不同。

作者：Senior Developer
日期：2026-02-19
"""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

print("=" * 70)
print("Agent vs Chatbot 对比示例")
print("=" * 70)
print()

# ============================================================================
# Part 1: 基于规则的 Chatbot
# ============================================================================

print("【Part 1: 基于规则的 Chatbot】")
print("-" * 70)
print()

class RuleBasedChatbot:
    """基于规则的 Chatbot"""

    def __init__(self):
        """初始化 Chatbot"""
        self.rules = {
            "你好": "你好！有什么我可以帮你的？",
            "再见": "再见！祝你有美好的一天！",
            "谢谢": "不客气！",
            "什么是 LangChain": "LangChain 是一个 LLM 应用开发框架。",
            "什么是 LangGraph": "LangGraph 是一个状态管理框架。",
        }

    def get_response(self, user_input: str) -> str:
        """获取回复（基于规则匹配）"""
        # 规则匹配
        for key, value in self.rules.items():
            if key in user_input:
                return value

        # 默认回复
        return "抱歉，我还没有学会如何回答这个问题。"

# 创建 Chatbot
chatbot = RuleBasedChatbot()

# 测试 Chatbot
test_inputs = [
    "你好",
    "什么是 LangChain",
    "LangGraph 能做什么",
    "再见"
]

print("Chatbot 测试结果：")
print()
for test_input in test_inputs:
    response = chatbot.get_response(test_input)
    print(f"用户: {test_input}")
    print(f"Chatbot: {response}")
    print()

print()
print("Chatbot 特点：")
print("- ✅ 规则明确，回复可控")
print("- ✅ 实现简单，易于维护")
print("- ❌ 只能回答预设的问题")
print("- ❌ 没有理解和推理能力")
print()

# ============================================================================
# Part 2: 简单的 Agent
# ============================================================================

print("【Part 2: 简单的 Agent】")
print("-" * 70)
print()

# 创建 LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# 创建工具
def search_knowledge(query: str) -> str:
    """搜索知识库"""
    knowledge = {
        "LangChain": "LangChain 是一个 LLM 应用开发框架，提供了丰富的工具和组件。",
        "LangGraph": "LangGraph 是一个状态管理框架，用于构建有状态的 Agent 应用。",
        "Agent": "Agent 是一个自主的智能体，能够感知、推理、执行和学习。",
        "Chatbot": "Chatbot 是一个基于规则的对话系统，只能回答预设的问题。"
    }

    for key, value in knowledge.items():
        if key.lower() in query.lower():
            return value

    return f"知识库中没有找到关于 '{query}' 的信息。"

# 创建 Tool
knowledge_tool = Tool(
    name="search_knowledge",
    func=search_knowledge,
    description="搜索知识库，查找相关信息"
)

# 创建 Agent
agent = create_react_agent(
    llm=llm,
    tools=[knowledge_tool],
    verbose=True
)

# 创建 Agent 执行器
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[knowledge_tool],
    verbose=False,  # 关闭详细输出，使输出更清晰
    handle_parsing_errors=True,
    max_iterations=5
)

# 测试 Agent
print("Agent 测试结果：")
print()
for test_input in test_inputs:
    try:
        result = agent_executor.invoke({"input": test_input})
        print(f"用户: {test_input}")
        print(f"Agent: {result['output']}")
        print()
    except Exception as e:
        print(f"用户: {test_input}")
        print(f"Agent: [错误] {e}")
        print()

print()
print("Agent 特点：")
print("- ✅ 能够理解用户意图")
print("- ✅ 能够推理和决策")
print("- ✅ 能够调用工具完成任务")
print("- ✅ 能够生成灵活的回复")
print("- ❌ 实现复杂，成本较高")
print()

# ============================================================================
# Part 3: 对比总结
# ============================================================================

print("【Part 3: 对比总结】")
print("-" * 70)
print()

comparison_table = """
┌─────────────────┬──────────────────┬──────────────────┐
│     特性        │     Chatbot      │      Agent       │
├─────────────────┼──────────────────┼──────────────────┤
│ 工作原理        │ 规则匹配         │ 推理 + 行动      │
│ 能力范围        │ 预设问题         │ 自主决策         │
│ 灵活性          │ 固定回复         │ 灵活生成         │
│ 实现难度        │ 简单             │ 复杂             │
│ 适用场景        │ 规则明确         │ 复杂任务         │
│ 成本            │ 低               │ 高               │
│ 可控性          │ 高               │ 中               │
└─────────────────┴──────────────────┴──────────────────┘
"""

print(comparison_table)

print()
print("使用建议：")
print()
print("1. 使用 Chatbot 的场景：")
print("   - 规则明确，不需要推理")
print("   - 问题范围有限且可控")
print("   - 需要快速实现和低成本")
print("   - 客户服务常见问题解答（FAQ）")
print()

print("2. 使用 Agent 的场景：")
print("   - 需要理解和推理")
print("   - 需要调用外部工具")
print("   - 问题复杂且多变")
print("   - 需要自主决策和适应")
print("   - 智能客服、自动化助理")
print()

print("=" * 70)
print("Agent vs Chatbot 对比示例完成！")
print("=" * 70)
