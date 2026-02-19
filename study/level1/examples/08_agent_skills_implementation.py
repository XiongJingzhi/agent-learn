"""
示例：Agent Skills/Tools 完整实现

本示例展示如何从零实现 Agent 的工具/技能，包括：
1. OpenAI Function Calling
2. LangChain Tools
3. 自定义 Tool 类
4. 工具集成到 Agent

Author: Claude (Sonnet 4.5)
Date: 2025-01-19
"""

# ============================================================================
# 第一部分：OpenAI Function Calling 基础实现
# ============================================================================

import openai
import json
from typing import List, Dict, Any, Callable, Optional

# ===== 1.1 定义工具 Schema =====

def get_tool_schemas() -> List[Dict]:
    """定义工具 Schema"""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的当前天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，例如：北京、上海、广州"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "温度单位（默认：celsius）"
                        }
                    },
                    "required": ["city"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "计算数学表达式",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "数学表达式，例如：2 + 2 或 (10 * 5) / 2"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search",
                "description": "搜索关键词并返回相关信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "最大返回结果数（默认：5）",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]


# ===== 1.2 实现工具函数 =====

class ToolFunctions:
    """工具函数集合"""

    @staticmethod
    def get_weather(city: str, unit: str = "celsius") -> Dict[str, Any]:
        """获取天气（模拟实现）"""
        # 模拟天气数据
        weather_db = {
            "北京": {"temp": 25, "condition": "晴天", "humidity": 45},
            "上海": {"temp": 28, "condition": "多云", "humidity": 65},
            "广州": {"temp": 26, "condition": "小雨", "humidity": 80},
            "深圳": {"temp": 27, "condition": "阴天", "humidity": 70},
            "杭州": {"temp": 24, "condition": "晴转多云", "humidity": 55}
        }

        data = weather_db.get(city)
        if not data:
            return {
                "success": False,
                "error": f"未找到城市: {city}"
            }

        result = {
            "city": city,
            "temperature": data["temp"],
            "unit": unit,
            "condition": data["condition"],
            "humidity": data["humidity"]
        }

        # 温度单位转换
        if unit == "fahrenheit":
            result["temperature"] = data["temp"] * 9/5 + 32

        return {
            "success": True,
            "data": result
        }

    @staticmethod
    def calculator(expression: str) -> Dict[str, Any]:
        """计算器（带安全校验）"""
        try:
            # 安全校验：只允许数学字符
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expression):
                return {
                    "success": False,
                    "error": "表达式包含非法字符"
                }

            # 计算结果
            result = eval(expression)

            return {
                "success": True,
                "expression": expression,
                "result": result
            }

        except ZeroDivisionError:
            return {
                "success": False,
                "error": "除零错误"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def search(query: str, max_results: int = 5) -> Dict[str, Any]:
        """搜索工具（模拟实现）"""
        # 模拟知识库
        knowledge_base = {
            "langchain": "LangChain 是一个用于开发由语言模型驱动的应用程序的框架",
            "langgraph": "LangGraph 是 LangChain 的扩展，用于构建有状态的多参与者应用",
            "openai": "OpenAI 是一个人工智能研究实验室，创建了 GPT 系列",
            "anthropic": "Anthropic 是一家 AI 安全公司，创建了 Claude 系列",
            "google": "Google 是一家科技公司，开发了 Gemini 系列模型",
            "python": "Python 是一种高级编程语言，广泛用于 AI 开发",
            "javascript": "JavaScript 是一种脚本语言，主要用于 Web 开发"
        }

        # 搜索匹配
        results = []
        query_lower = query.lower()

        for key, value in knowledge_base.items():
            if query_lower in key.lower() or query_lower in value.lower():
                results.append({
                    "title": key,
                    "content": value
                })

            if len(results) >= max_results:
                break

        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }


# ===== 1.3 Function Calling Agent =====

class FunctionCallingAgent:
    """支持 Function Calling 的 Agent"""

    def __init__(self, api_key: str = None):
        """初始化 Agent"""
        if api_key:
            openai.api_key = api_key

        self.tools = get_tool_schemas()
        self.tool_functions = ToolFunctions()
        self.conversation_history = []

    def add_tool(self, tool_schema: Dict, func: Callable):
        """添加工具"""
        self.tools.append(tool_schema)
        tool_name = tool_schema["function"]["name"]
        setattr(self.tool_functions, tool_name, func)

    def run(self, user_message: str, model: str = "gpt-4") -> str:
        """运行 Agent"""
        messages = [{"role": "user", "content": user_message}]
        self.conversation_history = messages.copy()

        max_iterations = 5  # 防止无限循环
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # 调用 LLM
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            self.conversation_history.append(assistant_message)

            # 检查是否需要调用工具
            tool_calls = assistant_message.tool_calls

            if not tool_calls:
                # 没有工具调用，返回最终回答
                return assistant_message.content

            # 执行所有工具调用
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"\n[工具调用] {function_name}({function_args})")

                # 执行工具函数
                try:
                    func = getattr(self.tool_functions, function_name)
                    result = func(**function_args)

                    print(f"[工具返回] {json.dumps(result, ensure_ascii=False, indent=2)}")

                    # 判断是否成功
                    if isinstance(result, dict) and result.get("success"):
                        tool_result = result.get("data", result)
                    else:
                        tool_result = str(result)

                except AttributeError:
                    tool_result = f"错误：未知工具 {function_name}"
                    print(f"[错误] {tool_result}")

                except Exception as e:
                    tool_result = f"工具执行错误: {str(e)}"
                    print(f"[错误] {tool_result}")

                # 将工具结果添加到消息
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result, ensure_ascii=False)
                })

        return "超过最大迭代次数"


# ===== 1.4 使用示例 =====

def demo_openai_function_calling():
    """演示 OpenAI Function Calling"""
    print("="*60)
    print("演示 1: OpenAI Function Calling")
    print("="*60)

    # 注意：需要设置 OPENAI_API_KEY 环境变量
    # agent = FunctionCallingAgent()

    # 示例 1：天气查询
    print("\n[示例 1] 天气查询")
    print("-" * 40)
    # answer = agent.run("北京现在天气怎么样？")
    # print(f"回答: {answer}")

    # 示例 2：计算
    print("\n[示例 2] 数学计算")
    print("-" * 40)
    # answer = agent.run("帮我计算 (100 + 50) * 2")
    # print(f"回答: {answer}")

    # 示例 3：搜索
    print("\n[示例 3] 知识搜索")
    print("-" * 40)
    # answer = agent.run("搜索 LangChain 的相关信息")
    # print(f"回答: {answer}")

    print("\n[提示] 需要设置 OPENAI_API_KEY 环境变量才能运行")


# ============================================================================
# 第二部分：LangChain Tools 实现
# ============================================================================

from langchain.tools import Tool, StructuredTool, BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any


# ===== 2.1 基础 Tool =====

def basic_search_function(query: str) -> str:
    """基础搜索函数"""
    knowledge = {
        "python": "Python 是一种编程语言",
        "javascript": "JavaScript 是一种脚本语言",
        "java": "Java 是一种面向对象的语言"
    }

    query_lower = query.lower()
    results = []

    for key, value in knowledge.items():
        if query_lower in key.lower() or query_lower in value.lower():
            results.append(f"{key}: {value}")

    if results:
        return "\n".join(results)
    else:
        return f"未找到关于 '{query}' 的信息"


# 创建基础 Tool
basic_search_tool = Tool(
    name="basic_search",
    func=basic_search_function,
    description="搜索关键词，返回相关信息（简单版本）"
)


# ===== 2.2 StructuredTool（带参数验证）=====

class CalculatorInput(BaseModel):
    """计算器输入"""
    expression: str = Field(
        description="数学表达式，例如：2 + 2 或 (10 * 5) / 2"
    )
    precision: int = Field(
        default=2,
        ge=0,
        le=10,
        description="小数位数（0-10）"
    )


def calculator_function(expression: str, precision: int = 2) -> str:
    """计算器函数"""
    try:
        # 安全校验
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return f"错误：表达式包含非法字符"

        result = eval(expression)
        return f"{result:.{precision}f}"
    except ZeroDivisionError:
        return "错误：除零错误"
    except Exception as e:
        return f"错误：{str(e)}"


calculator_tool = StructuredTool.from_function(
    func=calculator_function,
    name="calculator",
    description="计算数学表达式，支持加减乘除和括号",
    args_schema=CalculatorInput
)


# ===== 2.3 自定义 BaseTool 类 =====

class WeatherInput(BaseModel):
    """天气查询输入"""
    city: str = Field(description="城市名称")
    unit: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="温度单位"
    )


class WeatherTool(BaseTool):
    """天气工具（自定义 BaseTool）"""

    name = "get_weather"
    description = "获取指定城市的当前天气"
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, city: str, unit: str = "celsius") -> str:
        """同步执行"""
        weather_db = {
            "北京": {"temp": 25, "condition": "晴天"},
            "上海": {"temp": 28, "condition": "多云"},
            "广州": {"temp": 26, "condition": "小雨"}
        }

        data = weather_db.get(city)
        if not data:
            return f"未找到城市: {city}"

        temp = data["temp"]
        condition = data["condition"]

        if unit == "fahrenheit":
            temp = temp * 9/5 + 32
            return f"{city}现在{condition}，温度 {temp:.1f}°F"
        else:
            return f"{city}现在{condition}，温度 {temp}°C"

    async def _arun(self, city: str, unit: str = "celsius") -> str:
        """异步执行"""
        # 模拟异步操作
        import asyncio
        await asyncio.sleep(0.1)
        return self._run(city, unit)


# ===== 2.4 高级工具：带状态的工具 =====

class ConversationMemoryTool(BaseTool):
    """对话记忆工具"""

    name = "conversation_memory"
    description = "记住并检索对话历史"

    def __init__(self):
        super().__init__()
        self.history = []

    class ConversationInput(BaseModel):
        action: Literal["save", "recall", "clear"] = Field(
            description="操作类型：save（保存）、recall（回忆）、clear（清空）"
        )
        message: str = Field(
            default="",
            description="要保存的消息（save 时需要）"
        )

    args_schema = Type[BaseModel] = ConversationInput

    def _run(self, action: str, message: str = "") -> str:
        """执行"""
        if action == "save":
            if not message:
                return "错误：save 操作需要提供 message"
            self.history.append({
                "message": message,
                "timestamp": self.__get_timestamp()
            })
            return f"已保存消息：{message[:50]}..."

        elif action == "recall":
            if not self.history:
                return "对话历史为空"
            recent = self.history[-3:]  # 最近 3 条
            return "\n".join([h["message"] for h in recent])

        elif action == "clear":
            count = len(self.history)
            self.history.clear()
            return f"已清空 {count} 条历史记录"

        else:
            return f"未知操作：{action}"

    def __get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")


# ===== 2.5 工具集成示例 =====

def demo_langchain_tools():
    """演示 LangChain Tools"""
    print("\n" + "="*60)
    print("演示 2: LangChain Tools")
    print("="*60)

    # 创建工具列表
    tools = [
        basic_search_tool,
        calculator_tool,
        WeatherTool(),
        ConversationMemoryTool()
    ]

    # 测试每个工具
    print("\n[测试 1] 基础搜索工具")
    print("-" * 40)
    result = basic_search_tool.run("python")
    print(result)

    print("\n[测试 2] 计算器工具")
    print("-" * 40)
    result = calculator_tool.run({"expression": "2 * (3 + 4)", "precision": 1})
    print(result)

    print("\n[测试 3] 天气工具")
    print("-" * 40)
    weather_tool = WeatherTool()
    result = weather_tool.run({"city": "北京", "unit": "celsius"})
    print(result)

    print("\n[测试 4] 记忆工具")
    print("-" * 40)
    memory_tool = ConversationMemoryTool()

    memory_tool.run({"action": "save", "message": "我叫张三"})
    memory_tool.run({"action": "save", "message": "我喜欢编程"})
    result = memory_tool.run({"action": "recall", "message": ""})
    print(result)


# ============================================================================
# 第三部分：完整的 Agent with Tools
# ============================================================================

from langchain.agents import initialize_agent, Tool as LangChainTool
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

class ToolEnhancedAgent:
    """工具增强的 Agent"""

    def __init__(self, tools: List, model: str = "gpt-3.5-turbo"):
        """初始化"""
        self.llm = ChatOpenAI(temperature=0, model=model)
        self.tools = tools

        # 系统提示
        self.system_prompt = """你是一个有帮助的 AI 助手。

你可以使用以下工具来完成任务：
- {tools}

使用工具时，请确保：
1. 仔细理解用户的请求
2. 选择最合适的工具
3. 使用正确的参数调用工具
4. 基于工具返回的结果给用户清晰的回答

如果没有合适的工具，请诚实地告诉用户。"""

    def query(self, user_input: str) -> str:
        """查询"""
        # 创建工具描述
        tool_descriptions = "\n- ".join([
            f"{tool.name}: {tool.description}"
            for tool in self.tools
        ])

        # 构建消息
        messages = [
            SystemMessage(content=self.system_prompt.format(tools=tool_descriptions)),
            SystemMessage(content=f"用户问题：{user_input}")
        ]

        # 简化实现：直接检查是否需要工具
        for tool in self.tools:
            if self._should_use_tool(user_input, tool):
                result = tool.run(user_input)
                return f"使用工具 {tool.name} 的结果：\n{result}"

        # 如果没有工具匹配，让 LLM 直接回答
        response = self.llm.predict(messages)
        return response

    def _should_use_tool(self, query: str, tool) -> bool:
        """判断是否应该使用工具"""
        # 简化的判断逻辑
        keywords = {
            "basic_search": ["搜索", "查找", "什么是"],
            "calculator": ["计算", "加减乘除", "等于多少"],
            "get_weather": ["天气", "温度", "下雨"],
            "conversation_memory": ["记住", "回忆", "历史"]
        }

        tool_keywords = keywords.get(tool.name, [])
        query_lower = query.lower()

        return any(kw in query_lower for kw in tool_keywords)


def demo_complete_agent():
    """演示完整的 Agent with Tools"""
    print("\n" + "="*60)
    print("演示 3: 完整的 Agent with Tools")
    print("="*60)

    # 创建工具
    tools = [
        basic_search_tool,
        calculator_tool,
        WeatherTool()
    ]

    # 创建 Agent
    agent = ToolEnhancedAgent(tools)

    # 测试查询
    queries = [
        "搜索 Python 的信息",
        "计算 123 * 456",
        "北京天气怎么样"
    ]

    for query in queries:
        print(f"\n[用户] {query}")
        print("-" * 40)
        response = agent.query(query)
        print(f"[助手] {response}")


# ============================================================================
# 第四部分：工具测试
# ============================================================================

import pytest

def test_basic_search_tool():
    """测试基础搜索工具"""
    result = basic_search_tool.run("python")
    assert "python" in result.lower()
    print("✓ 基础搜索工具测试通过")


def test_calculator_tool():
    """测试计算器工具"""
    result = calculator_tool.run({"expression": "2 + 2"})
    assert "4.00" in result
    print("✓ 计算器工具测试通过")


def test_weather_tool():
    """测试天气工具"""
    tool = WeatherTool()
    result = tool.run({"city": "北京"})
    assert "北京" in result
    assert "°C" in result
    print("✓ 天气工具测试通过")


def test_conversation_memory_tool():
    """测试对话记忆工具"""
    tool = ConversationMemoryTool()

    # 保存
    save_result = tool.run({"action": "save", "message": "测试消息"})
    assert "已保存" in save_result

    # 回忆
    recall_result = tool.run({"action": "recall"})
    assert "测试消息" in recall_result

    # 清空
    clear_result = tool.run({"action": "clear"})
    assert "已清空" in clear_result

    print("✓ 对话记忆工具测试通过")


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序"""
    print("="*60)
    print("Agent Skills/Tools 完整示例")
    print("="*60)

    # 演示 1: OpenAI Function Calling（需要 API key）
    demo_openai_function_calling()

    # 演示 2: LangChain Tools
    demo_langchain_tools()

    # 演示 3: 完整的 Agent with Tools
    demo_complete_agent()

    # 运行测试
    print("\n" + "="*60)
    print("运行测试")
    print("="*60)
    test_basic_search_tool()
    test_calculator_tool()
    test_weather_tool()
    test_conversation_memory_tool()

    print("\n" + "="*60)
    print("所有示例和测试完成！")
    print("="*60)


if __name__ == "__main__":
    main()
