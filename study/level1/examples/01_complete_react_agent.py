"""
示例 01: 完整的 ReAct Agent

完整的 ReAct Agent 实现，包括：
- 多个工具的集成
- 记忆系统
- 错误处理
- 日志记录

作者：Senior Developer
日期：2026-02-19
"""

from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def search_tool(query: str) -> str:
    """搜索工具（模拟）"""
    logger.info(f"执行搜索工具，查询：{query}")
    
    # 模拟搜索结果
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架，提供工具、记忆、链等组件",
        "langgraph": "LangGraph 是一个状态管理框架，用于构建有状态的 Agent",
        "openai": "OpenAI 是一个 AI 研究实验室，开发了 GPT 系列模型",
        "anthropic": "Anthropic 是一个 AI 安全研究公司，开发了 Claude 系列 LLM"
    }
    
    for key, value in results.items():
        if query.lower() in key.lower():
            logger.info(f"搜索成功：{value}")
            return value
    
    logger.warning(f"未找到与 '{query}' 相关的结果")
    return f"未找到与 '{query}' 相关的结果"


def calculator_tool(expression: str) -> str:
    """计算工具"""
    logger.info(f"执行计算工具，表达式：{expression}")
    
    try:
        result = eval(expression)
        logger.info(f"计算成功：{expression} = {result}")
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        logger.error(f"计算失败：{e}")
        return f"计算失败：无法计算 '{expression}'，错误：{str(e)}"


def weather_tool(city: str) -> str:
    """天气工具（模拟）"""
    logger.info(f"执行天气工具，城市：{city}")
    
    # 模拟天气数据
    weather_map = {
        "北京": "北京今天天气晴，气温 25℃",
        "上海": "上海今天天气多云，气温 28℃",
        "广州": "广州今天天气雨，气温 26℃",
        "深圳": "深圳今天天气晴，气温 29℃"
    }
    
    if city in weather_map:
        logger.info(f"查询成功：{weather_map[city]}")
        return weather_map[city]
    
    logger.warning(f"未找到 '{city}' 的天气信息")
    return f"抱歉，我们还没有 '{city}' 的天气信息。"


def create_tools() -> List[Tool]:
    """创建工具列表"""
    tools = [
        Tool(
            name="search",
            func=search_tool,
            description="搜索关键词，返回相关信息（支持：langchain, langgraph, openai, anthropic）"
        ),
        Tool(
            name="calculator",
            func=calculator_tool,
            description="计算数学表达式，支持加减乘除等基本运算（如：1 + 1, 2 * 3, 10 / 2）"
        ),
        Tool(
            name="weather",
            func=weather_tool,
            description="查询指定城市的天气信息（支持：北京, 上海, 广州, 深圳）"
        )
    ]
    
    logger.info(f"创建了 {len(tools)} 个工具")
    return tools


def create_memory() -> ConversationBufferMemory:
    """创建记忆系统"""
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        k=10  # 保留最近 10 条消息
    )
    
    logger.info("创建了记忆系统（保留最近 10 条消息）")
    return memory


def create_agent(tools: List[Tool], memory: ConversationBufferMemory) -> AgentExecutor:
    """创建完整的 ReAct Agent"""
    # 创建 LLM
    llm = ChatOpenAI(
        temperature=0.7,
        model="gpt-3.5-turbo"
    )
    
    # 创建 Agent Prompt
    template = """你是一个有用的助手。你有以下工具可以使用：

{tools}

使用以下格式回答问题：

Question: 我需要回答的问题
Thought: 我应该思考一下
Action: 我应该采取的行动（使用工具之一）
Action Input: 行动的输入
Observation: 行动的结果
... (这个 Thought/Action/Action Input/Observation 可以重复多次)
Thought: 我现在知道最终答案了
Final Answer: 最终答案

开始！

{chat_history}
Question: {input}
Thought: {agent_scratchpad}
"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "agent_scratchpad", "chat_history", "tools"]
    )
    
    # 创建 Agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # 创建 Agent 执行器
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        return_intermediate_steps=True
    )
    
    logger.info("创建了完整的 ReAct Agent")
    return agent_executor


def main():
    """主函数"""
    print("=" * 80)
    print("完整的 ReAct Agent 示例")
    print("=" * 80)
    print()
    
    # 创建工具
    tools = create_tools()
    
    # 创建记忆系统
    memory = create_memory()
    
    # 创建 Agent
    agent = create_agent(tools, memory)
    
    # 测试用例
    test_cases = [
        "搜索 LangChain 的信息",
        "计算 1 + 1",
        "查询北京的天气",
        "计算 2 * 3 + 4",
        "搜索 OpenAI 的信息，然后查询上海的天气",
        "计算 (10 + 20) / 2"
    ]
    
    # 执行测试
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"测试 {i}: {test_case}")
        print(f"{'=' * 80}")
        
        try:
            result = agent.invoke({"input": test_case})
            
            print("\n结果：")
            print(result["output"])
            print()
            
            # 显示中间步骤
            if "intermediate_steps" in result:
                print("中间步骤：")
                for step in result["intermediate_steps"]:
                    print(f"  - {step}")
                print()
            
        except Exception as e:
            logger.error(f"测试失败：{e}")
            print(f"错误：{e}")
            continue
    
    print("=" * 80)
    print("所有测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
