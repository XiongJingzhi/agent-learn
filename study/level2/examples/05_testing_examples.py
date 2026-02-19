"""
示例 05: Agent 测试完整示例

演示单元测试、集成测试、Mock 和 Fixture 的使用

作者：Senior Developer
日期：2026-02-19
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from typing import List, Dict, Any
from dataclasses import dataclass
import time


# ===== 被测试的组件 =====

@dataclass
class Task:
    """任务"""
    id: str
    type: str
    description: str
    status: str = "pending"
    result: Any = None


class SimpleTool:
    """简单工具"""

    def __init__(self, name: str, result: Any = None):
        self.name = name
        self.result = result
        self.call_count = 0

    def execute(self, input_data: Any) -> Any:
        """执行工具"""
        self.call_count += 1
        if self.result is not None:
            return self.result
        return f"{self.name} 的结果"


class SimpleAgent:
    """简单的 Agent（用于测试）"""

    def __init__(self, tools: List[SimpleTool] = None):
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.history = []

    def run(self, query: str) -> str:
        """运行 Agent"""
        if not query or not query.strip():
            raise ValueError("查询不能为空")

        self.history.append({"type": "query", "content": query})

        # 简化：直接返回结果
        result = f"处理: {query}"
        self.history.append({"type": "result", "content": result})

        return result

    def use_tool(self, tool_name: str, input_data: Any) -> Any:
        """使用工具"""
        if tool_name not in self.tools:
            raise ValueError(f"工具不存在: {tool_name}")

        tool = self.tools[tool_name]
        return tool.execute(input_data)

    def get_history(self) -> List[Dict]:
        """获取历史记录"""
        return self.history


# ===== 单元测试 =====

class TestSimpleTool(unittest.TestCase):
    """SimpleTool 的单元测试"""

    def setUp(self):
        """测试前准备"""
        self.tool = SimpleTool(name="test_tool", result="test_result")

    def test_tool_execution(self):
        """测试工具执行"""
        result = self.tool.execute("input")

        self.assertEqual(result, "test_result")
        self.assertEqual(self.tool.call_count, 1)

    def test_tool_call_count(self):
        """测试调用计数"""
        self.tool.execute("input1")
        self.tool.execute("input2")

        self.assertEqual(self.tool.call_count, 2)

    def test_tool_with_none_result(self):
        """测试无预设结果"""
        tool = SimpleTool(name="no_result_tool")
        result = tool.execute("input")

        self.assertEqual(result, "no_result_tool 的结果")


class TestSimpleAgent(unittest.TestCase):
    """SimpleAgent 的单元测试"""

    def setUp(self):
        """测试前准备"""
        self.agent = SimpleAgent()

    def test_run_with_valid_query(self):
        """测试有效查询"""
        result = self.agent.run("测试查询")

        self.assertEqual(result, "处理: 测试查询")
        self.assertEqual(len(self.agent.history), 2)

    def test_run_with_empty_query_raises_error(self):
        """测试空查询抛出错误"""
        with self.assertRaises(ValueError) as context:
            self.agent.run("")

        self.assertIn("查询不能为空", str(context.exception))

    def test_run_with_whitespace_query_raises_error(self):
        """测试空白查询抛出错误"""
        with self.assertRaises(ValueError):
            self.agent.run("   ")

    def test_history_tracking(self):
        """测试历史记录"""
        self.agent.run("查询1")
        self.agent.run("查询2")

        history = self.agent.get_history()

        self.assertEqual(len(history), 4)  # 每次查询添加 2 条记录
        self.assertEqual(history[0]["content"], "查询1")
        self.assertEqual(history[2]["content"], "查询2")


# ===== Mock 测试 =====

class TestWithMock(unittest.TestCase):
    """使用 Mock 的测试"""

    def test_mock_tool(self):
        """测试 Mock 工具"""
        # 创建 Mock 工具
        mock_tool = Mock()
        mock_tool.execute.return_value = "mocked_result"

        # 使用 Mock 工具
        result = mock_tool.execute("input")

        # 验证结果
        self.assertEqual(result, "mocked_result")

        # 验证调用
        mock_tool.execute.assert_called_once_with("input")

    def test_mock_with_side_effect(self):
        """测试 Mock 副作用"""
        mock_tool = Mock()

        # 设置副作用：每次调用返回不同的值
        mock_tool.execute.side_effect = ["result1", "result2", "result3"]

        result1 = mock_tool.execute("input")
        result2 = mock_tool.execute("input")
        result3 = mock_tool.execute("input")

        self.assertEqual(result1, "result1")
        self.assertEqual(result2, "result2")
        self.assertEqual(result3, "result3")

    def test_mock_with_exception(self):
        """测试 Mock 异常"""
        mock_tool = Mock()
        mock_tool.execute.side_effect = Exception("工具失败")

        with self.assertRaises(Exception) as context:
            mock_tool.execute("input")

        self.assertEqual(str(context.exception), "工具失败")

    def test_agent_with_mock_tools(self):
        """测试使用 Mock 工具的 Agent"""
        # 创建 Mock 工具
        mock_search = Mock()
        mock_search.execute.return_value = "搜索结果"

        mock_calculate = Mock()
        mock_calculate.execute.return_value = 42

        # 创建 Agent
        agent = SimpleAgent(tools=[
            SimpleTool("search"),
            SimpleTool("calculate")
        ])

        # 替换为 Mock
        agent.tools["search"] = mock_search
        agent.tools["calculate"] = mock_calculate

        # 使用工具
        result1 = agent.use_tool("search", "query")
        result2 = agent.use_tool("calculate", [1, 2, 3])

        # 验证
        self.assertEqual(result1, "搜索结果")
        self.assertEqual(result2, 42)

        mock_search.execute.assert_called_once_with("query")
        mock_calculate.execute.assert_called_once_with([1, 2, 3])


# ===== Patch 测试 =====

class TestWithPatch(unittest.TestCase):
    """使用 Patch 的测试"""

    @patch('__main__.SimpleTool.execute')
    def test_patch_tool_method(self, mock_execute):
        """测试 Patch 工具方法"""
        mock_execute.return_value = "patched_result"

        tool = SimpleTool(name="test")
        result = tool.execute("input")

        self.assertEqual(result, "patched_result")
        mock_execute.assert_called_once_with("input")

    @patch('time.sleep')
    def test_patch_sleep(self, mock_sleep):
        """测试 Patch sleep（加速测试）"""
        # 正常会等待 2 秒，但 Patch 后立即返回
        time.sleep(2)

        # 验证被调用
        mock_sleep.assert_called_once_with(2)


# ===== 集成测试 =====

class TestAgentIntegration(unittest.TestCase):
    """Agent 集成测试"""

    def setUp(self):
        """测试前准备"""
        # 使用 Mock 工具
        self.mock_tools = [
            SimpleTool(name="search", result="搜索结果"),
            SimpleTool(name="calculate", result=42)
        ]
        self.agent = SimpleAgent(tools=self.mock_tools)

    def test_agent_completes_task(self):
        """测试 Agent 完成任务"""
        result = self.agent.run("搜索并计算")

        self.assertIsNotNone(result)
        self.assertIn("搜索并计算", result)

    def test_agent_uses_multiple_tools(self):
        """测试 Agent 使用多个工具"""
        result1 = self.agent.use_tool("search", "query")
        result2 = self.agent.use_tool("calculate", [1, 2, 3])

        self.assertEqual(result1, "搜索结果")
        self.assertEqual(result2, 42)

    def test_agent_handles_tool_failure(self):
        """测试 Agent 处理工具失败"""
        # 设置工具失败
        self.mock_tools[0].result = None
        self.mock_tools[0].execute = Mock(side_effect=Exception("搜索失败"))

        # Agent 应该能够处理失败
        with self.assertRaises(Exception):
            self.agent.use_tool("search", "query")


# ===== Fixture 测试 =====

class TestWithFixtures(unittest.TestCase):
    """使用 Fixture 的测试"""

    @classmethod
    def setUpClass(cls):
        """所有测试前运行一次"""
        cls.shared_resource = "共享资源"

    @classmethod
    def tearDownClass(cls):
        """所有测试后运行一次"""
        cls.shared_resource = None

    def setUp(self):
        """每个测试前运行"""
        self.test_data = {"key": "value"}

    def tearDown(self):
        """每个测试后运行"""
        self.test_data = None

    def test_with_class_fixture(self):
        """测试使用类级别 Fixture"""
        self.assertEqual(self.shared_resource, "共享资源")

    def test_with_test_fixture(self):
        """测试使用测试级别 Fixture"""
        self.assertIn("key", self.test_data)
        self.assertEqual(self.test_data["key"], "value")


# ===== 参数化测试 =====

class TestParameterized(unittest.TestCase):
    """参数化测试"""

    def test_valid_queries(self):
        """测试多个有效查询"""
        valid_queries = [
            ("简单查询", "处理: 简单查询"),
            ("复杂查询", "处理: 复杂查询"),
            ("123", "处理: 123")
        ]

        for query, expected in valid_queries:
            with self.subTest(query=query):
                agent = SimpleAgent()
                result = agent.run(query)
                self.assertEqual(result, expected)

    def test_invalid_queries(self):
        """测试多个无效查询"""
        invalid_queries = ["", "   ", "\t\n"]

        for query in invalid_queries:
            with self.subTest(query=repr(query)):
                agent = SimpleAgent()
                with self.assertRaises(ValueError):
                    agent.run(query)


# ===== 性能测试 =====

class TestPerformance(unittest.TestCase):
    """性能测试"""

    def test_execution_time(self):
        """测试执行时间"""
        agent = SimpleAgent()

        start = time.time()
        for _ in range(100):
            agent.run("测试查询")
        end = time.time()

        # 应该在合理时间内完成（< 1 秒）
        self.assertLess(end - start, 1.0)

    def test_memory_usage(self):
        """测试内存使用（简化）"""
        agent = SimpleAgent()

        # 执行大量操作
        for i in range(1000):
            agent.run(f"查询 {i}")

        # 历史记录应该被管理
        # （实际应用中可能需要限制历史大小）
        self.assertLessEqual(len(agent.history), 2000)  # 每次查询添加 2 条记录


# ===== 测试套件 =====

def create_test_suite():
    """创建测试套件"""
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(unittest.makeSuite(TestSimpleTool))
    suite.addTests(unittest.makeSuite(TestSimpleAgent))
    suite.addTests(unittest.makeSuite(TestWithMock))
    suite.addTests(unittest.makeSuite(TestWithPatch))
    suite.addTests(unittest.makeSuite(TestAgentIntegration))
    suite.addTests(unittest.makeSuite(TestWithFixtures))
    suite.addTests(unittest.makeSuite(TestParameterized))
    suite.addTests(unittest.makeSuite(TestPerformance))

    return suite


# ===== 运行测试 =====

if __name__ == "__main__":
    print("=" * 70)
    print("Agent 测试示例")
    print("=" * 70)

    # 运行所有测试
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    result = runner.run(suite)

    # 打印总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 存在测试失败")
