"""
示例 04: 状态管理与反馈机制

演示 Agent 的状态管理和反馈机制，包括短期、中期、长期状态。

作者：Senior Developer
日期：2026-02-19
"""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory
)
from typing import TypedDict, Dict, Any
from datetime import datetime

print("=" * 70)
print("状态管理与反馈机制示例")
print("=" * 70)
print()

# ============================================================================
# Part 1: 定义 Agent 状态
# ============================================================================

print("【Part 1: 定义 Agent 状态】")
print("-" * 70)
print()

class AgentState(TypedDict):
    """Agent 状态定义"""
    # 当前信息
    user_input: str                    # 用户输入
    current_task: str                  # 当前任务
    tool_result: str                   # 工具执行结果

    # 历史信息
    conversation_history: list         # 对话历史
    action_history: list               # 操作历史

    # 元信息
    timestamp: str                     # 时间戳
    state_version: int                 # 状态版本号

print("Agent 状态结构：")
print("┌─────────────────────────────────────────────────────────┐")
print("│ AgentState                                                │")
print("│ ├── 当前信息                                              │")
print("│ │   ├── user_input: 用户输入                              │")
print("│ │   ├── current_task: 当前任务                            │")
print("│ │   └── tool_result: 工具执行结果                         │")
print("│ ├── 历史信息                                              │")
print("│ │   ├── conversation_history: 对话历史                    │")
print("│ │   └── action_history: 操作历史                          │")
print("│ └── 元信息                                                │")
print("│     ├── timestamp: 时间戳                                 │")
print("│     └── state_version: 状态版本号                         │")
print("└─────────────────────────────────────────────────────────┘")
print()

# 初始化状态
initial_state: AgentState = {
    "user_input": "",
    "current_task": "",
    "tool_result": "",
    "conversation_history": [],
    "action_history": [],
    "timestamp": datetime.now().isoformat(),
    "state_version": 1
}

print("初始状态：")
print(f"- 时间戳: {initial_state['timestamp']}")
print(f"- 版本号: {initial_state['state_version']}")
print(f"- 对话历史: {initial_state['conversation_history']}")
print()

# ============================================================================
# Part 2: 短期状态管理
# ============================================================================

print("【Part 2: 短期状态管理】")
print("-" * 70)
print()

# 创建短期状态（ConversationBufferMemory）
short_term_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)

print("短期状态特点：")
print("- ✅ 容量小：保存最近的消息")
print("- ✅ 速度快：读写速度快")
print("- ❌ 遗忘快：信息会快速遗忘")
print()

# 模拟对话
print("模拟对话（短期状态）：")
print()

conversations = [
    ("我叫张三", "你好，张三！很高兴认识你。"),
    ("我喜欢的语言是 Python", "了解了，你喜欢 Python！"),
    ("我有个问题", "请说，我来帮你解答。")
]

for user_input, bot_response in conversations:
    print(f"用户: {user_input}")
    print(f"Bot: {bot_response}")

    # 保存到短期状态
    short_term_memory.save_context(
        {"input": user_input},
        {"output": bot_response}
    )
    print()

# 加载短期状态
print("短期状态内容：")
state_vars = short_term_memory.load_memory_variables({})
print(f"- 对话轮数: {len(state_vars['chat_history']) // 2}")
for msg in state_vars['chat_history']:
    print(f"  - {msg.type}: {msg.content[:50]}...")
print()

# ============================================================================
# Part 3: 中期状态管理
# ============================================================================

print("【Part 3: 中期状态管理】")
print("-" * 70)
print()

# 创建中期状态（ConversationBufferWindowMemory）
medium_term_memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=10,  # 保留最近 10 条消息
    return_messages=True,
    output_key="output"
)

print("中期状态特点：")
print("- ✅ 容量中：保存较多消息（如：最近 10 条）")
print("- ✅ 时间中：信息会保留一段时间")
print("- ✅ 适合：记住对话上下文")
print()

# 模拟更多对话
print("模拟对话（中期状态）：")
print()

more_conversations = [
    ("什么是 LangChain", "LangChain 是一个 LLM 应用开发框架。"),
    ("什么是 LangGraph", "LangGraph 是一个状态管理框架。"),
    ("什么是 Agent", "Agent 是一个自主的智能体。"),
    ("谢谢你的解答", "不客气！"),
    ("再见", "再见！祝你有美好的一天！")
]

for user_input, bot_response in conversations + more_conversations:
    medium_term_memory.save_context(
        {"input": user_input},
        {"output": bot_response}
    )

# 加载中期状态
print("中期状态内容：")
state_vars = medium_term_memory.load_memory_variables({})
print(f"- 对话轮数: {len(state_vars['chat_history']) // 2}")
print(f"- 总消息数: {len(state_vars['chat_history'])}")
print()

# ============================================================================
# Part 4: 状态更新策略
# ============================================================================

print("【Part 4: 状态更新策略】")
print("-" * 70)
print()

class StateManager:
    """状态管理器"""

    def __init__(self):
        """初始化状态管理器"""
        self.state: AgentState = {
            "user_input": "",
            "current_task": "",
            "tool_result": "",
            "conversation_history": [],
            "action_history": [],
            "timestamp": datetime.now().isoformat(),
            "state_version": 1
        }

    def direct_update(self, key: str, value: Any) -> None:
        """直接更新状态（覆盖旧值）"""
        print(f"[直接更新] {key}: {self.state.get(key, 'None')} → {value}")
        self.state[key] = value
        self.state["timestamp"] = datetime.now().isoformat()
        self.state["state_version"] += 1

    def append_update(self, key: str, value: Any) -> None:
        """追加更新状态（保留旧值）"""
        if isinstance(self.state.get(key), list):
            print(f"[追加更新] {key}: 添加 {value}")
            self.state[key].append(value)
        else:
            print(f"[追加更新] {key}: {self.state.get(key, 'None')} → [{value}]")
            self.state[key] = [value]
        self.state["timestamp"] = datetime.now().isoformat()
        self.state["state_version"] += 1

    def get_state(self) -> AgentState:
        """获取当前状态"""
        return self.state

    def print_state(self) -> None:
        """打印当前状态"""
        print()
        print("当前状态：")
        print(f"├─ 版本: {self.state['state_version']}")
        print(f"├─ 时间: {self.state['timestamp']}")
        print(f"├─ 用户输入: {self.state['user_input']}")
        print(f"├─ 当前任务: {self.state['current_task']}")
        print(f"├─ 工具结果: {self.state['tool_result']}")
        print(f"├─ 对话历史: {len(self.state['conversation_history'])} 条")
        print(f"└─ 操作历史: {len(self.state['action_history'])} 条")
        print()

# 创建状态管理器
state_manager = StateManager()

# 演示直接更新
print("演示 1: 直接更新策略")
state_manager.direct_update("user_input", "你好")
state_manager.direct_update("current_task", "问候")
state_manager.print_state()

# 演示追加更新
print("演示 2: 追加更新策略")
state_manager.append_update("conversation_history", "用户: 你好")
state_manager.append_update("conversation_history", "Bot: 你好！")
state_manager.append_update("action_history", "执行: 问候")
state_manager.print_state()

# ============================================================================
# Part 5: 反馈机制
# ============================================================================

print("【Part 5: 反馈机制】")
print("-" * 70)
print()

class FeedbackAgent:
    """带反馈机制的 Agent"""

    def __init__(self):
        """初始化 Agent"""
        self.state = {}
        self.feedback_history = []

    def process(self, user_input: str) -> str:
        """处理用户输入"""
        print(f"[输入] {user_input}")

        # 推理
        if "你好" in user_input:
            action = "问候"
            response = "你好！很高兴见到你。"
        elif "再见" in user_input:
            action = "告别"
            response = "再见！祝你有美好的一天！"
        else:
            action = "对话"
            response = f"我收到了你的消息：{user_input}"

        print(f"[行动] {action}")
        print(f"[输出] {response}")

        # 收集反馈
        feedback = {
            "user_input": user_input,
            "action": action,
            "response": response,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }

        self.feedback_history.append(feedback)

        # 更新状态
        self.state["last_action"] = action
        self.state["last_response"] = response

        return response

    def get_feedback(self) -> list:
        """获取反馈历史"""
        return self.feedback_history

    def analyze_feedback(self) -> dict:
        """分析反馈"""
        if not self.feedback_history:
            return {"total": 0, "success_rate": 0}

        total = len(self.feedback_history)
        success = sum(1 for f in self.feedback_history if f["success"])

        return {
            "total": total,
            "success": success,
            "success_rate": success / total * 100,
            "actions": [f["action"] for f in self.feedback_history]
        }

# 创建反馈 Agent
feedback_agent = FeedbackAgent()

print("演示反馈机制：")
print()

# 模拟对话
test_inputs = ["你好", "今天天气怎么样", "再见"]
for test_input in test_inputs:
    feedback_agent.process(test_input)
    print()

# 分析反馈
print("反馈分析：")
analysis = feedback_agent.analyze_feedback()
print(f"- 总交互次数: {analysis['total']}")
print(f"- 成功次数: {analysis['success']}")
print(f"- 成功率: {analysis['success_rate']:.1f}%")
print(f"- 执行的操作: {', '.join(analysis['actions'])}")
print()

# ============================================================================
# 总结
# ============================================================================

print("【总结】")
print("-" * 70)
print()

print("状态管理类型：")
print()
print("1. 短期状态（Short-Term State）")
print("   - 容量小，速度快")
print("   - 适合：最近对话、当前任务")
print("   - 实现：ConversationBufferMemory")
print()

print("2. 中期状态（Medium-Term State）")
print("   - 容量中，时间中")
print("   - 适合：对话上下文、任务进度")
print("   - 实现：ConversationBufferWindowMemory")
print()

print("3. 长期状态（Long-Term State）")
print("   - 容量大，时间长")
print("   - 适合：用户偏好、重要历史")
print("   - 实现：数据库、向量存储")
print()

print("状态更新策略：")
print()
print("1. 直接更新（Direct Update）")
print("   - 新值覆盖旧值")
print("   - 适合：当前任务、临时状态")
print()

print("2. 追加更新（Append Update）")
print("   - 保留旧值，追加新值")
print("   - 适合：对话历史、操作记录")
print()

print("3. 分层更新（Hierarchical Update）")
print("   - 短期、中期、长期分开管理")
print("   - 适合：复杂 Agent 系统")
print()

print("=" * 70)
print("状态管理与反馈机制示例完成！")
print("=" * 70)
