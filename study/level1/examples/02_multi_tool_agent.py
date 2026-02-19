"""
示例 02: 多工具 Agent

多工具 Agent 实现，包括：
- 多个工具的路由策略
- 工具的并行调用
- 工具的错误处理
- 工具调用的日志

作者：Senior Developer
日期：2026-02-19
"""

from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ToolRouter:
    """工具路由器，根据任务选择合适的工具"""
    
    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}
        self.tool_descriptions = {tool.name: tool.description for tool in tools}
        self.tool_usage_count = {tool.name: 0 for tool in tools}
    
    def route(self, query: str) -> Optional[str]:
        """根据查询内容路由到合适的工具"""
        query_lower = query.lower()
        
        # 简单的关键词路由策略
        if any(keyword in query_lower for keyword in ["搜索", "search", "查找", "find"]):
            return "search"
        elif any(keyword in query_lower for keyword in ["计算", "calculate", "算", "compute"]):
            return "calculator"
        elif any(keyword in query_lower for keyword in ["天气", "weather", "气温"]):
            return "weather"
        elif any(keyword in query_lower for keyword in ["时间", "time", "日期", "date"]):
            return "time"
        elif any(keyword in query_lower for keyword in ["翻译", "translate", "译"]):
            return "translate"
        
        return None
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """获取指定的工具"""
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> List[Tool]:
        """获取所有工具"""
        return list(self.tools.values())
    
    def record_usage(self, tool_name: str):
        """记录工具使用"""
        if tool_name in self.tool_usage_count:
            self.tool_usage_count[tool_name] += 1
    
    def get_usage_stats(self) -> Dict[str, int]:
        """获取工具使用统计"""
        return self.tool_usage_count.copy()


def search_tool(query: str) -> str:
    """搜索工具（模拟）"""
    logger.info(f"[搜索工具] 查询：{query}")
    
    # 模拟搜索结果
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架，提供工具、记忆、链等组件",
        "langgraph": "LangGraph 是一个状态管理框架，用于构建有状态的 Agent",
        "openai": "OpenAI 是一个 AI 研究实验室，开发了 GPT 系列模型",
        "anthropic": "Anthropic 是一个 AI 安全研究公司，开发了 Claude 系列 LLM",
        "python": "Python 是一种流行的编程语言，以其简洁和易读著称"
    }
    
    for key, value in results.items():
        if query.lower() in key.lower():
            logger.info(f"[搜索工具] 成功：{value}")
            return value
    
    logger.warning(f"[搜索工具] 未找到与 '{query}' 相关的结果")
    return f"未找到与 '{query}' 相关的结果"


def calculator_tool(expression: str) -> str:
    """计算工具"""
    logger.info(f"[计算工具] 表达式：{expression}")
    
    try:
        # 安全计算（只允许数字和基本运算符）
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("表达式包含非法字符")
        
        result = eval(expression)
        logger.info(f"[计算工具] 成功：{expression} = {result}")
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        logger.error(f"[计算工具] 失败：{e}")
        return f"计算失败：无法计算 '{expression}'，错误：{str(e)}"


def weather_tool(city: str) -> str:
    """天气工具（模拟）"""
    logger.info(f"[天气工具] 城市：{city}")
    
    weather_map = {
        "北京": "北京今天天气晴，气温 25℃",
        "上海": "上海今天天气多云，气温 28℃",
        "广州": "广州今天天气雨，气温 26℃",
        "深圳": "深圳今天天气晴，气温 29℃",
        "杭州": "杭州今天天气多云，气温 27℃"
    }
    
    if city in weather_map:
        logger.info(f"[天气工具] 成功：{weather_map[city]}")
        return weather_map[city]
    
    logger.warning(f"[天气工具] 未找到 '{city}' 的天气信息")
    return f"抱歉，我们还没有 '{city}' 的天气信息。"


def time_tool(query: str) -> str:
    """时间工具"""
    logger.info(f"[时间工具] 查询：{query}")
    
    now = datetime.now()
    result = f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    logger.info(f"[时间工具] 成功：{result}")
    return result


def translate_tool(text: str) -> str:
    """翻译工具（模拟）"""
    logger.info(f"[翻译工具] 文本：{text}")
    
    # 模拟翻译结果
    # 在实际应用中，这里会调用翻译 API
    return f"（翻译）{text}"


def create_tools() -> List[Tool]:
    """创建工具列表"""
    tools = [
        Tool(
            name="search",
            func=search_tool,
            description="搜索关键词，返回相关信息"
        ),
        Tool(
            name="calculator",
            func=calculator_tool,
            description="计算数学表达式，支持加减乘除等基本运算"
        ),
        Tool(
            name="weather",
            func=weather_tool,
            description="查询指定城市的天气信息"
        ),
        Tool(
            name="time",
            func=time_tool,
            description="查询当前时间和日期"
        ),
        Tool(
            name="translate",
            func=translate_tool,
            description="翻译文本（模拟）"
        )
    ]
    
    logger.info(f"创建了 {len(tools)} 个工具")
    return tools


def create_multi_tool_agent(tools: List[Tool]) -> Dict[str, Any]:
    """创建多工具 Agent"""
    # 创建工具路由器
    router = ToolRouter(tools)
    
    # 创建 LLM
    llm = ChatOpenAI(
        temperature=0.7,
        model="gpt-3.5-turbo"
    )
    
    # 创建 Agent Prompt
    template = """你是一个多功能的助手。你有以下工具可以使用：

{tools}

工具路由策略：
- 搜索相关问题 → search 工具
- 计算问题 → calculator 工具
- 天气问题 → weather 工具
- 时间/日期问题 → time 工具
- 翻译问题 → translate 工具

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

Question: {input}
Thought: {agent_scratchpad}
"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "agent_scratchpad", "tools"]
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
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        return_intermediate_steps=True
    )
    
    logger.info("创建了多工具 Agent")
    return {
        "agent": agent_executor,
        "router": router
    }


def main():
    """主函数"""
    print("=" * 80)
    print("多工具 Agent 示例")
    print("=" * 80)
    print()
    
    # 创建工具
    tools = create_tools()
    
    # 创建工具路由器
    router = ToolRouter(tools)
    
    # 显示所有工具
    print("可用工具：")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    print()
    
    # 创建多工具 Agent
    agent_result = create_multi_tool_agent(tools)
    agent = agent_result["agent"]
    
    # 测试用例
    test_cases = [
        "搜索 LangChain 的信息",
        "计算 1 + 1",
        "查询北京的天气",
        "计算 2 * 3 + 4",
        "查询当前时间",
        "搜索 Python 的信息",
        "计算 (10 + 20) / 2",
        "查询上海的天气"
    ]
    
    # 执行测试
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"测试 {i}: {test_case}")
        print(f"{'=' * 80}")
        
        try:
            # 路由到合适的工具
            tool_name = router.route(test_case)
            if tool_name:
                print(f"工具路由：{tool_name}")
                router.record_usage(tool_name)
            
            # 执行 Agent
            result = agent.invoke({"input": test_case})
            
            print("\n结果：")
            print(result["output"])
            print()
            
        except Exception as e:
            logger.error(f"测试失败：{e}")
            print(f"错误：{e}")
            continue
    
    # 显示工具使用统计
    print("\n" + "=" * 80)
    print("工具使用统计")
    print("=" * 80)
    usage_stats = router.get_usage_stats()
    for tool_name, count in usage_stats.items():
        print(f"  {tool_name}: {count} 次")
    print()
    
    print("=" * 80)
    print("所有测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
