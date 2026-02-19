"""
示例 05: 失败模式与错误处理

演示 Agent 的常见失败模式和错误处理策略。

作者：Senior Developer
日期：2026-02-19
"""

import time
from typing import Callable, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

print("=" * 70)
print("失败模式与错误处理示例")
print("=" * 70)
print()

# ============================================================================
# Part 1: 常见失败模式演示
# ============================================================================

print("【Part 1: 常见失败模式】")
print("-" * 70)
print()

# 失败模式 1: 无限循环
print("失败模式 1: 无限循环")
print("-" * 70)
print()

class InfiniteLoopAgent:
    """无限循环 Agent（错误示例）"""

    def __init__(self):
        """初始化"""
        self.count = 0
        self.max_iterations = 10  # 安全限制

    def run_without_limit(self):
        """没有循环限制（会导致无限循环）"""
        print("⚠️  错误示例：没有循环限制")
        print()

        count = 0
        while True:
            count += 1
            print(f"循环第 {count} 次...")
            if count >= 3:  # 演示时限制为 3 次
                print("⚠️  警告：检测到无限循环，强制退出！")
                break

    def run_with_limit(self):
        """有循环限制（正确做法）"""
        print("✅ 正确示例：有循环限制")
        print()

        for i in range(3):
            print(f"循环第 {i + 1} 次...")

        print("✅ 循环正常结束")

# 演示
agent = InfiniteLoopAgent()
agent.run_without_limit()
print()
agent.run_with_limit()
print()

# 失败模式 2: 资源耗尽
print("失败模式 2: 资源耗尽")
print("-" * 70)
print()

class ResourceExhaustionAgent:
    """资源耗尽 Agent（错误示例）"""

    def __init__(self):
        """初始化"""
        self.memory_limit = 1000  # 内存限制

    def allocate_memory_unlimited(self):
        """无限制分配内存（错误示例）"""
        print("⚠️  错误示例：无限制分配内存")
        print()

        data = []
        try:
            for i in range(10000):
                data.append([0] * 100)  # 每次分配 100 个元素
                if i >= 3:  # 演示时限制
                    print(f"⚠️  警告：已分配 {len(data)} 块内存，可能耗尽资源！")
                    break
        except MemoryError:
            print("❌ 内存耗尽！")

    def allocate_memory_limited(self):
        """有限制分配内存（正确做法）"""
        print("✅ 正确示例：有限制分配内存")
        print()

        data = []
        for i in range(3):
            data.append([0] * 100)
            print(f"✅ 已分配 {i + 1} 块内存，在限制范围内")

        print(f"✅ 总共分配 {len(data)} 块内存，安全")

# 演示
agent = ResourceExhaustionAgent()
agent.allocate_memory_unlimited()
print()
agent.allocate_memory_limited()
print()

# ============================================================================
# Part 2: 错误处理策略
# ============================================================================

print("【Part 2: 错误处理策略】")
print("-" * 70)
print()

# 策略 1: 超时检测
print("策略 1: 超时检测")
print("-" * 70)
print()

def execute_with_timeout(func: Callable, timeout: int = 2) -> Optional[Any]:
    """带超时的执行"""
    print(f"执行函数，超时时间：{timeout} 秒")

    start_time = time.time()

    try:
        result = func()
        elapsed = time.time() - start_time

        if elapsed > timeout:
            print(f"⚠️  警告：执行时间 {elapsed:.2f} 秒，超过超时时间 {timeout} 秒")
            return None

        print(f"✅ 执行成功，耗时 {elapsed:.2f} 秒")
        return result

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ 执行失败，耗时 {elapsed:.2f} 秒，错误：{e}")
        return None

# 测试
def quick_task():
    """快速任务"""
    time.sleep(0.5)
    return "快速任务完成"

def slow_task():
    """慢速任务"""
    time.sleep(3)
    return "慢速任务完成"

print("测试 1: 快速任务")
execute_with_timeout(quick_task, timeout=2)
print()

print("测试 2: 慢速任务")
execute_with_timeout(slow_task, timeout=2)
print()

# 策略 2: 重试机制
print("策略 2: 重试机制（指数退避）")
print("-" * 70)
print()

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    backoff_factor: int = 2
) -> Optional[Any]:
    """重试机制（指数退避）"""

    retry_count = 0
    delay = 1

    while retry_count < max_retries:
        try:
            print(f"尝试 {retry_count + 1}/{max_retries}...")
            result = func()
            print(f"✅ 成功！")
            return result

        except Exception as e:
            retry_count += 1
            print(f"❌ 失败：{e}")

            if retry_count < max_retries:
                print(f"等待 {delay} 秒后重试...")
                time.sleep(delay)
                delay *= backoff_factor  # 指数退避

    print(f"❌ 重试 {max_retries} 次后仍然失败")
    return None

# 测试
class UnstableAPI:
    """不稳定的 API（模拟）"""

    def __init__(self):
        """初始化"""
        self.attempt = 0

    def call(self):
        """调用 API"""
        self.attempt += 1
        if self.attempt < 3:
            raise ConnectionError("连接失败")
        return "成功"

api = UnstableAPI()

print("测试重试机制：")
result = retry_with_backoff(api.call, max_retries=3)
print(f"结果：{result}")
print()

# 策略 3: 降级策略
print("策略 3: 降级策略")
print("-" * 70)
print()

def execute_with_fallback(
    main_func: Callable,
    fallback_func: Callable,
    func_name: str = "操作"
) -> Any:
    """降级策略"""

    try:
        print(f"尝试主方案：{func_name}")
        result = main_func()
        print(f"✅ 主方案成功")
        return result

    except Exception as e:
        print(f"⚠️  主方案失败：{e}")
        print(f"使用降级方案：{func_name}")

        try:
            result = fallback_func()
            print(f"✅ 降级方案成功")
            return result

        except Exception as e2:
            print(f"❌ 降级方案也失败：{e2}")
            return None

# 测试
def main_search(query: str):
    """主搜索（可能失败）"""
    raise ConnectionError("主搜索引擎连接失败")

def fallback_search(query: str):
    """备用搜索"""
    return f"备用搜索结果：{query}"

print("测试降级策略：")
result = execute_with_fallback(
    lambda: main_search("LangChain"),
    lambda: fallback_search("LangChain"),
    func_name="搜索"
)
print(f"结果：{result}")
print()

# ============================================================================
# Part 3: 带错误处理的 Agent
# ============================================================================

print("【Part 3: 带错误处理的 Agent】")
print("-" * 70)
print()

# 创建一个可能失败的工具
def unreliable_tool(input: str) -> str:
    """不可靠的工具（模拟）"""
    import random
    if random.random() < 0.3:  # 30% 失败率
        raise Exception("工具调用失败")
    return f"工具处理结果：{input}"

# 创建 LLM 和工具
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

tools = [
    Tool(
        name="reliable_tool",
        func=lambda x: f"可靠工具结果：{x}",
        description="一个可靠的工具"
    ),
    Tool(
        name="unreliable_tool",
        func=unreliable_tool,
        description="一个不可靠的工具（可能失败）"
    )
]

# 创建 Agent
agent = create_react_agent(llm=llm, tools=tools)

# 创建带错误处理的 Agent 执行器
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,  # 处理解析错误
    max_iterations=5,             # 防止无限循环
    return_intermediate_steps=True  # 返回中间步骤
)

print("测试带错误处理的 Agent：")
print()

# 测试 1: 使用可靠工具
print("测试 1: 使用可靠工具")
try:
    result = agent_executor.invoke({"input": "使用可靠工具处理 hello"})
    print(f"✅ 成功：{result['output']}")
except Exception as e:
    print(f"❌ 失败：{e}")
print()

# 测试 2: 使用不可靠工具（多次尝试）
print("测试 2: 使用不可靠工具（可能失败）")
success_count = 0
for i in range(5):
    try:
        result = agent_executor.invoke({"input": "使用不可靠工具处理 test"})
        print(f"✅ 尝试 {i + 1} 成功：{result['output'][:50]}...")
        success_count += 1
    except Exception as e:
        print(f"⚠️  尝试 {i + 1} 失败：{str(e)[:50]}...")

print()
print(f"成功率：{success_count}/5 = {success_count * 20}%")
print()

# ============================================================================
# Part 4: 自定义异常
# ============================================================================

print("【Part 4: 自定义异常】")
print("-" * 70)
print()

# 定义自定义异常
class AgentTimeoutError(Exception):
    """Agent 超时错误"""
    pass

class ToolExecutionError(Exception):
    """工具执行错误"""
    pass

class DecisionLogicError(Exception):
    """决策逻辑错误"""
    pass

class ResourceExhaustionError(Exception):
    """资源耗尽错误"""
    pass

# 演示自定义异常的使用
print("自定义异常类型：")
print()
print("1. AgentTimeoutError - Agent 执行超时")
print("2. ToolExecutionError - 工具执行失败")
print("3. DecisionLogicError - 决策逻辑错误")
print("4. ResourceExhaustionError - 资源耗尽")
print()

# 使用自定义异常
def safe_execute(func: Callable) -> Any:
    """安全执行，捕获自定义异常"""

    try:
        return func()

    except AgentTimeoutError as e:
        print(f"❌ Agent 超时：{e}")
        return None

    except ToolExecutionError as e:
        print(f"❌ 工具执行失败：{e}")
        return None

    except DecisionLogicError as e:
        print(f"❌ 决策逻辑错误：{e}")
        return None

    except ResourceExhaustionError as e:
        print(f"❌ 资源耗尽：{e}")
        return None

    except Exception as e:
        print(f"❌ 未知错误：{e}")
        return None

# 测试
def risky_operation():
    """有风险的操作"""
    raise ToolExecutionError("搜索服务不可用")

print("测试自定义异常处理：")
result = safe_execute(risky_operation)
print(f"结果：{result}")
print()

# ============================================================================
# 总结
# ============================================================================

print("【总结】")
print("-" * 70)
print()

print("常见失败模式：")
print()
print("1. 无限循环（Infinite Loop）")
print("   - 原因：循环条件错误、状态不变")
print("   - 解决：设置循环最大次数、更新状态")
print()

print("2. 资源耗尽（Resource Exhaustion）")
print("   - 原因：内存泄漏、API 限制")
print("   - 解决：资源限制、内存管理")
print()

print("3. 工具失败（Tool Failure）")
print("   - 原因：网络问题、服务不可用")
print("   - 解决：重试机制、降级策略")
print()

print("错误处理策略：")
print()
print("1. 超时检测（Timeout Detection）")
print("   - 为每个任务设置超时时间")
print("   - 超时后终止执行")
print()

print("2. 重试机制（Retry Mechanism）")
print("   - 自动重试失败的任务")
print("   - 使用指数退避策略")
print()

print("3. 降级策略（Fallback Strategy）")
print("   - 主方案失败时使用备选方案")
print("   - 保证基本功能的可用性")
print()

print("4. 自定义异常（Custom Exceptions）")
print("   - 为每种错误定义明确的异常类型")
print("   - 便于调试和错误处理")
print()

print("=" * 70)
print("失败模式与错误处理示例完成！")
print("=" * 70)
