# 测试策略

> **目标**: 掌握 Agent 系统的测试策略和最佳实践
> **预计时间**: 30 分钟
> **难度**: ⭐⭐⭐

---

## 为什么需要测试策略？

Agent 系统的测试比传统软件更具挑战性：

**挑战 1：非确定性输出**
- LLM 的输出每次可能不同
- 难以断言确切的结果

**挑战 2：外部依赖**
- 依赖外部 API（LLM、工具）
- 测试环境和生产环境不同

**挑战 3：复杂行为**
- Agent 的行为取决于多个因素
- 难以覆盖所有场景

---

## 测试层次

### 层次 1：单元测试

测试单个组件（节点、工具、函数）。

```python
import unittest
from unittest.mock import Mock, patch

class TestSearchTool(unittest.TestCase):
    """搜索工具的单元测试"""

    def setUp(self):
        """测试前准备"""
        self.search_tool = SearchTool()

    def test_search_with_valid_query(self):
        """测试有效查询"""
        result = self.search_tool.search("LangGraph")

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_search_with_empty_query(self):
        """测试空查询"""
        with self.assertRaises(ValueError):
            self.search_tool.search("")

    def test_search_returns_expected_structure(self):
        """测试返回结构"""
        result = self.search_tool.search("test")

        # 检查结果的结构
        for item in result:
            self.assertIn("title", item)
            self.assertIn("url", item)
            self.assertIn("snippet", item)


class TestLLMNode(unittest.TestCase):
    """LLM 节点的单元测试"""

    def setUp(self):
        """测试前准备"""
        self.node = LLMNode(model_name="gpt-3.5-turbo")

    @patch('node.openai.ChatCompletion.create')
    def test_node_calls_llm(self, mock_create):
        """测试节点调用 LLM"""
        # Mock LLM 响应
        mock_create.return_value = {
            "choices": [{"message": {"content": "测试响应"}}]
        }

        result = self.node.process({"input": "测试输入"})

        # 验证 LLM 被调用
        mock_create.assert_called_once()

        # 验证结果
        self.assertEqual(result["output"], "测试响应")

    def test_node_handles_errors(self):
        """测试错误处理"""
        # 模拟 LLM 错误
        with patch('node.openai.ChatCompletion.create', side_effect=Exception("API 错误")):
            with self.assertRaises(Exception):
                self.node.process({"input": "测试"})
```

---

### 层次 2：集成测试

测试多个组件协同工作。

```python
class TestAgentIntegration(unittest.TestCase):
    """Agent 集成测试"""

    def setUp(self):
        """测试前准备"""
        # 使用 Mock 工具
        self.mock_tools = [
            MockTool(name="search", result="搜索结果"),
            MockTool(name="calculate", result="42")
        ]

        self.agent = ReActAgent(tools=self.mock_tools)

    def test_agent_completes_simple_task(self):
        """测试 Agent 完成简单任务"""
        result = self.agent.run("搜索并计算")

        self.assertIsNotNone(result)
        self.assertIn("42", result)

    def test_agent_handles_tool_failure(self):
        """测试 Agent 处理工具失败"""
        # 设置一个工具失败
        self.mock_tools[0].should_fail = True

        # Agent 应该能够处理失败
        result = self.agent.run("搜索")

        # 验证 Agent 没有崩溃
        self.assertIsNotNone(result)

    def test_agent_follows_expected_flow(self):
        """测试 Agent 遵循预期流程"""
        with patch.object(self.agent, '_execute_action', wraps=self.agent._execute_action) as mock_execute:
            self.agent.run("多步骤任务")

            # 验证调用次数
            self.assertGreater(mock_execute.call_count, 1)
```

---

### 层次 3：端到端测试

测试完整的用户场景。

```python
class TestAgentE2E(unittest.TestCase):
    """端到端测试"""

    def setUp(self):
        """测试前准备"""
        self.agent = ProductionAgent()

    def test_complete_user_journey(self):
        """测试完整的用户旅程"""
        # 模拟用户对话
        conversation = [
            "你好，我想了解 LangGraph",
            "它有什么特点？",
            "能给我一个例子吗？"
        ]

        for user_message in conversation:
            response = self.agent.chat(user_message)

            # 验证响应
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)

    def test_agent_handles_edge_cases(self):
        """测试边界情况"""
        edge_cases = [
            "",  # 空输入
            "a" * 10000,  # 超长输入
            "🎉🎊🎈",  # 只有表情符号
        ]

        for edge_case in edge_cases:
            with self.subTest(input=edge_case):
                response = self.agent.chat(edge_case)
                self.assertIsNotNone(response)
```

---

## Mock 策略

### 策略 1：Mock LLM 响应

```python
from unittest.mock import patch, MagicMock

def mock_llm_response(content: str):
    """创建 Mock LLM 响应"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = content
    return mock_response


class TestWithMockLLM(unittest.TestCase):
    """使用 Mock LLM 的测试"""

    @patch('agent.openai.ChatCompletion.create')
    def test_with_mocked_llm(self, mock_create):
        """测试使用 Mock 的 LLM"""
        # 设置 Mock 响应
        mock_create.return_value = mock_llm_response("测试响应")

        # 运行测试
        agent = Agent()
        result = agent.run("测试输入")

        # 验证结果
        self.assertEqual(result, "测试响应")

        # 验证 LLM 被正确调用
        mock_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "测试输入"}]
        )
```

---

### 策略 2：Mock 工具调用

```python
class MockTool:
    """Mock 工具"""

    def __init__(self, name: str, result: any = None):
        self.name = name
        self.result = result
        self.call_count = 0
        self.should_fail = False

    def __call__(self, *args, **kwargs):
        self.call_count += 1

        if self.should_fail:
            raise Exception(f"Mock tool {self.name} failed")

        return self.result


def test_agent_with_mock_tools():
    """测试使用 Mock 工具的 Agent"""
    # 创建 Mock 工具
    mock_search = MockTool(name="search", result=["结果1", "结果2"])
    mock_calculate = MockTool(name="calculate", result=42)

    # 创建 Agent
    agent = Agent(tools=[mock_search, mock_calculate])

    # 运行
    result = agent.run("搜索并计算")

    # 验证工具被调用
    assert mock_search.call_count > 0
    assert mock_calculate.call_count > 0
```

---

### 策略 3：Fixture 设计

```python
import pytest

@pytest.fixture
def sample_agent():
    """提供测试用的 Agent 实例"""
    tools = [
        MockTool(name="search", result=["结果1"]),
        MockTool(name="calculate", result=42)
    ]
    return Agent(tools=tools)


@pytest.fixture
def sample_conversation():
    """提供测试用的对话历史"""
    return [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！"},
        {"role": "user", "content": "帮我搜索"}
    ]


def test_agent_with_fixture(sample_agent, sample_conversation):
    """使用 Fixture 的测试"""
    # 使用提供的 Agent 和对话
    for message in sample_conversation:
        if message["role"] == "user":
            response = sample_agent.chat(message["content"])
            assert response is not None
```

---

## 测试覆盖率

### 目标

- **单元测试**：>= 80%
- **集成测试**：>= 60%
- **整体覆盖率**：>= 70%

### 测量工具

```bash
# 使用 pytest-cov
pytest --cov=src --cov-report=html

# 或使用 coverage.py
coverage run -m pytest
coverage report
coverage html
```

---

## 完整示例：测试套件

```python
import unittest
from unittest.mock import Mock, patch, MagicMock

# 被测试的组件
class SimpleAgent:
    """简单的 Agent 实现"""

    def __init__(self, tools=None):
        self.tools = tools or []

    def run(self, query: str) -> str:
        """运行 Agent"""
        if not query:
            raise ValueError("查询不能为空")

        # 简化：直接返回结果
        return f"处理: {query}"


# 测试套件
class TestSimpleAgent(unittest.TestCase):
    """SimpleAgent 测试套件"""

    def setUp(self):
        """测试前准备"""
        self.agent = SimpleAgent()

    # === 单元测试 ===

    def test_run_with_valid_query(self):
        """测试有效查询"""
        result = self.agent.run("测试查询")

        self.assertEqual(result, "处理: 测试查询")

    def test_run_with_empty_query_raises_error(self):
        """测试空查询抛出错误"""
        with self.assertRaises(ValueError):
            self.agent.run("")

    def test_run_returns_string(self):
        """测试返回字符串"""
        result = self.agent.run("测试")

        self.assertIsInstance(result, str)

    # === 集成测试 ===

    def test_agent_with_tools(self):
        """测试带工具的 Agent"""
        mock_tool = Mock(return_value="工具结果")
        agent = SimpleAgent(tools=[mock_tool])

        # 如果 Agent 使用工具
        # agent.run("使用工具")

        # mock_tool.assert_called_once()

    # === 边界测试 ===

    def test_run_with_very_long_query(self):
        """测试超长查询"""
        long_query = "a" * 10000
        result = self.agent.run(long_query)

        self.assertIsInstance(result, str)

    def test_run_with_special_characters(self):
        """测试特殊字符"""
        special_query = "🎉 @#$%^&*()"
        result = self.agent.run(special_query)

        self.assertIn("🎉", result)


# 运行测试
if __name__ == "__main__":
    unittest.main()
```

---

## 测试最佳实践

### 实践 1：使用描述性的测试名称

```python
# 好
def test_agent_fails_gracefully_when_llm_api_times_out(self):
    ...

# 不好
def test_agent_timeout(self):
    ...
```

---

### 实践 2：每个测试只验证一件事

```python
# 好
def test_agent_returns_result(self):
    result = self.agent.run("测试")
    self.assertIsNotNone(result)

def test_agent_result_format(self):
    result = self.agent.run("测试")
    self.assertIn("答案", result)

# 不好
def test_agent(self):
    result = self.agent.run("测试")
    self.assertIsNotNone(result)
    self.assertIn("答案", result)
    self.assertGreater(len(result), 10)
```

---

### 实践 3：使用 Setup 和 Teardown

```python
class TestWithSetup(unittest.TestCase):

    def setUp(self):
        """每个测试前运行"""
        self.agent = Agent()
        self.test_data = load_test_data()

    def tearDown(self):
        """每个测试后运行"""
        cleanup_test_data()

    @classmethod
    def setUpClass(cls):
        """所有测试前运行一次"""
        initialize_test_environment()

    @classmethod
    def tearDownClass(cls):
        """所有测试后运行一次"""
        cleanup_test_environment()
```

---

## 最小验证

- [ ] 能够编写单元测试
- [ ] 能够使用 Mock
- [ ] 能够编写集成测试
- [ ] 能够测量测试覆盖率

---

## 下一步

- 📖 回顾所有笔记，准备进入实践阶段
- 🧪 `exercises/01_basic_exercises.md` - 基础练习
- `projects/01_capstone_project.md` - Capstone 项目

---

**记住：测试是保证 Agent 质量的关键，就像建筑的质量检测！** 🏗️
