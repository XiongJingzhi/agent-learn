# Agent 测试学习计划（调整版 v2.0）
## 从零到精通的测试策略演进路径

> **作者**: Testing Expert (测试专家)
> **版本**: v2.0 (2025-02-19 调整)
> **视角**: 质量保证、TDD实践、Mock策略、多框架测试
> **核心理念**: "没有测试的代码是不可靠的，Agent更需要全面的测试来保证其行为的可控性。"

---

## 🔄 本次调整说明

### 主要变更

1. **对齐架构师的学习路径**
   - 原Level 3（OpenClaw）→ 调整并扩展为"框架对比测试"
   - 原Level 4（OpenCode + 多Agent）→ 拆分为Level 4和Level 5
   - 多Agent测试独立为Level 5
   - 生产级测试提升为Level 6

2. **新增框架对比测试（Level 3）**
   - LangGraph vs 其他框架的功能等价性测试
   - 跨框架的性能对比测试
   - 学习曲线和开发效率评估

3. **整合实际框架特性**
   - OpenClaw：多渠道、Gateway、语音交互
   - OpenCode：TUI、LSP集成、客户端/服务器架构
   - 真实的测试场景和策略

---

## 学习目标

从质量保证和TDD实践角度，掌握Agent系统的测试方法，能够：
1. 设计全面的测试策略（单元测试、集成测试、端到端测试）
2. 实施TDD开发流程
3. 构建Mock和Stub体系，避免依赖真实LLM
4. 测试单Agent的深入功能（LangGraph → 框架对比 → OpenClaw → OpenCode）
5. 测试多Agent系统的协作
6. 建立持续集成和回归测试体系
7. 掌握跨框架的测试策略

---

## 学习路径概览（对齐架构师计划）

```
Level 0: 测试基础（1-2周）
  └─ 环境搭建 + 测试工具链
       ↓
Level 1: 单元测试与Mock基础（2-3周）
  └─ LangGraph基础测试 + TDD实践
       ↓
Level 2: LangGraph集成测试（3-4周）
  └─ Fixture体系 + 状态管理 + 记忆系统测试
       ↓
Level 3: 框架对比测试（3-4周）⭐ 新增
  ├─ 功能等价性测试
  ├─ 性能对比测试
  └─ Level 3.5: OpenClaw + OpenCode专项测试
       ↓
Level 4: 高级单Agent测试（4-5周）
  └─ LSP集成 + MCP协议 + 客户端/服务器测试
       ↓
Level 5: 多Agent协作测试（5-6周）
  └─ 通信测试 + 同步机制 + 冲突解决
       ↓
Level 6: 生产级测试体系（5-6周）
  └─ CI/CD + A/B测试 + 多框架监控
       ↓
Level 7: 前沿测试技术（持续学习）
  └─ 新工具、新方法、最佳实践
```

---

## Level 0: 测试基础与环境搭建（1-2周）

### 学习目标
- 理解Agent测试的重要性和挑战
- 搭建完整的测试环境
- 掌握基本测试工具的使用

### 关键知识点

#### 1. Agent测试的特殊性
```python
# 为什么Agent测试比传统测试更难？
- 依赖外部LLM API（成本高、速度慢、不确定性）
- 输出非确定性（同一输入可能产生不同输出）
- 需要测试推理链（Chain of Thought）
- 需要测试工具调用逻辑
- 需要评估输出质量（主观性强）
```

#### 2. 测试工具链
```bash
# 已安装的测试工具
pytest              # 测试框架
pytest-asyncio      # 异步测试支持
pytest-mock         # Mock工具
pytest-cov          # 覆盖率报告
pytest-benchmark    # 性能测试（推荐安装）
```

#### 3. 测试金字塔
```
        E2E测试         ← 少量、真实环境
       /        \
    集成测试           ← 适量、部分Mock
   /          \
单元测试              ← 大量、完全Mock
```

### 实践任务

#### Task 0.1: 环境验证
```python
# tests/test_level0_env.py

def test_pytest_works():
    """验证测试环境正常"""
    assert True

def test_import_langchain():
    """验证可以导入核心库"""
    try:
        import langchain
        import langgraph
        assert True
    except ImportError as e:
        raise AssertionError(f"导入失败: {e}")
```

运行测试：
```bash
pytest tests/test_level0_env.py -v
```

#### Task 0.2: 安装额外测试工具
```bash
pip install pytest-cov pytest-benchmark pytest-xdist

# 验证工具
pytest tests/test_level0_env.py --cov=app
```

#### Task 0.3: 创建测试配置
```python
# tests/conftest.py - pytest共享配置

import pytest
from typing import AsyncGenerator
from unittest.mock import Mock
from langchain_core.messages import AIMessage

@pytest.fixture
def sample_llm_response():
    """示例LLM响应fixture"""
    return {
        "content": "Hello, world!",
        "tool_calls": [],
        "usage": {"total_tokens": 10}
    }

@pytest.fixture
def mock_ai_message():
    """Mock AI消息fixture"""
    return AIMessage(content="Test response")

@pytest.fixture
async def async_fixture():
    """异步fixture示例"""
    yield "async_value"

@pytest.fixture
def test_config():
    """测试配置fixture"""
    return {
        "timeout": 30,
        "max_retries": 3,
        "use_cache": True
    }
```

### 推荐资源
- 📖 [Pytest官方文档](https://docs.pytest.org/)
- 📖 [pytest-asyncio文档](https://pytest-asyncio.readthedocs.io/)
- 🎥 视频：Python测试最佳实践

### 验收标准
- [ ] 能运行简单的pytest测试
- [ ] 理解fixture、parametrize等概念
- [ ] 能生成覆盖率报告
- [ ] 安装所有推荐测试工具

---

## Level 1: 单元测试与Mock基础（2-3周）

### 学习目标
- 掌握单元测试的编写方法
- 学会Mock LLM响应和工具调用
- 理解TDD的基本流程
- 测试LangGraph的基础功能

### 关键知识点

#### 1. Mock LLM响应
```python
# tests/level1/test_mock_llm.py

from unittest.mock import Mock
from langchain_core.messages import AIMessage

def test_mock_llm_response():
    """Mock LLM响应的基本示例"""
    # 创建Mock对象
    mock_llm = Mock()
    mock_llm.invoke.return_value = AIMessage(content="Mocked response")

    # 使用Mock
    response = mock_llm.invoke("Hello")
    assert response.content == "Mocked response"
    mock_llm.invoke.assert_called_once_with("Hello")

def test_mock_llm_with_side_effect():
    """Mock多次调用返回不同值"""
    mock_llm = Mock()
    mock_llm.invoke.side_effect = [
        AIMessage(content="First response"),
        AIMessage(content="Second response"),
        AIMessage(content="Third response")
    ]

    # 测试多次调用
    assert mock_llm.invoke("Q1").content == "First response"
    assert mock_llm.invoke("Q2").content == "Second response"
    assert mock_llm.invoke("Q3").content == "Third response"
```

#### 2. Mock工具调用
```python
def test_mock_tool_call():
    """Mock Agent工具调用"""
    mock_tool = Mock()
    mock_tool.name = "search"
    mock_tool.invoke.return_value = "Search result: Paris"

    result = mock_tool.invoke({"query": "capital of France"})
    assert "Paris" in result
    mock_tool.invoke.assert_called_once()

def test_mock_tool_with_exception():
    """测试工具调用异常处理"""
    mock_tool = Mock()
    mock_tool.invoke.side_effect = Exception("API Error")

    try:
        mock_tool.invoke({"query": "test"})
        assert False, "Should have raised exception"
    except Exception as e:
        assert str(e) == "API Error"
```

#### 3. 测试LangGraph节点
```python
# tests/level1/test_langgraph_node.py

from langgraph.graph import StateGraph
from typing import TypedDict

class TestState(TypedDict):
    message: str
    count: int

def test_agent_node():
    """测试LangGraph节点函数"""
    # 定义节点函数
    def agent_node(state: TestState) -> TestState:
        state["count"] += 1
        state["message"] = f"Processed {state['count']} times"
        return state

    # 测试节点
    initial_state = {"message": "", "count": 0}
    result = agent_node(initial_state)

    assert result["count"] == 1
    assert "Processed 1 times" in result["message"]
```

### TDD实践

#### TDD循环示例
```python
# 场景：测试Agent的token计数功能

# Step 1: 写测试（Red）
def test_count_tokens():
    """测试token计数"""
    from app.utils import count_tokens
    assert count_tokens("Hello world") == 2

# Step 2: 运行测试（失败）- NameError

# Step 3: 实现功能（Green）
def count_tokens(text: str) -> int:
    """简单的token计数（实际应用中应该用tiktoken）"""
    return len(text.split())

# Step 4: 重构（改进）
import tiktoken

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """使用tiktoken准确计数"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
```

### 实践任务

#### Task 1.1: 测试简单Agent
```python
# tests/level1/test_simple_agent.py

def test_simple_agent_with_mock_llm(mocker):
    """测试简单Agent使用Mock LLM"""
    from app.agents import SimpleAgent
    from langchain_openai import ChatOpenAI

    # Mock LLM
    mock_llm = mocker.Mock(spec=ChatOpenAI)
    mock_llm.invoke.return_value = AIMessage(
        content="The capital of France is Paris."
    )

    # 创建Agent
    agent = SimpleAgent(llm=mock_llm)

    # 测试
    result = agent.invoke("What is the capital of France?")
    assert "Paris" in result
    mock_llm.invoke.assert_called_once()

def test_agent_with_tool(mocker):
    """测试Agent使用工具"""
    from app.agents import ToolAgent
    from langchain.tools import tool

    # Mock工具
    @tool
    def calculator(expression: str) -> str:
        """计算数学表达式"""
        return str(eval(expression))

    mock_calculator = mocker.Mock(wraps=calculator)

    # Mock LLM返回工具调用
    mock_llm = mocker.Mock()
    mock_llm.invoke.return_value = AIMessage(
        content="",
        tool_calls=[{
            "name": "calculator",
            "args": {"expression": "2+2"},
            "id": "call_1"
        }]
    )

    agent = ToolAgent(llm=mock_llm, tools=[mock_calculator])
    result = agent.invoke("What is 2 plus 2?")

    assert "4" in result
```

#### Task 1.2: 参数化测试
```python
@pytest.mark.parametrize("input_msg,expected_keyword", [
    ("capital of France", "Paris"),
    ("capital of Japan", "Tokyo"),
    ("capital of UK", "London"),
])
def test_agent_knowledge(mocker, input_msg, expected_keyword):
    """参数化测试Agent知识"""
    from app.agents import SimpleAgent

    mock_llm = mocker.Mock()
    mock_llm.invoke.return_value = AIMessage(
        content=f"The answer involves {expected_keyword}"
    )

    agent = SimpleAgent(llm=mock_llm)
    result = agent.invoke(input_msg)

    assert expected_keyword in result
```

#### Task 1.3: 测试异常处理
```python
def test_agent_handles_llm_error(mocker):
    """测试Agent处理LLM错误"""
    from app.agents import ResilientAgent

    mock_llm = mocker.Mock()
    mock_llm.invoke.side_effect = Exception("API timeout")

    agent = ResilientAgent(llm=mock_llm, max_retries=2)

    # 应该有降级策略
    result = agent.invoke("Test")
    assert result is not None  # 不应该抛出异常
```

### 推荐资源
- 📖 [unittest.mock文档](https://docs.python.org/3/library/unittest.mock.html)
- 📖 [pytest-mock文档](https://pytest-mock.readthedocs.io/)
- 📖 [TDD实战教程](https://testdriven.io/blog/tdd-python/)

### 验收标准
- [ ] 能编写单元测试覆盖Agent核心逻辑
- [ ] 能熟练Mock LLM和工具调用
- [ ] 完成一个完整的TDD循环
- [ ] 测试覆盖率达到60%+

---

## Level 2: LangGraph深入测试（3-4周）

### 学习目标
- 设计可复用的测试Fixture
- 测试LangGraph的状态管理
- 测试Agent记忆系统
- 测试复杂的工具编排

### 关键知识点

#### 1. Fixture设计模式
```python
# tests/conftest.py - 集中管理fixture

@pytest.fixture
def mock_openai_client(mocker):
    """Mock OpenAI客户端 - 全局可复用"""
    from langchain_openai import ChatOpenAI

    mock_client = mocker.patch.object(ChatOpenAI, '__init__', return_value=None)
    mock_llm = mocker.patch.object(ChatOpenAI, 'invoke')
    mock_llm.return_value = AIMessage(content="Test response")

    return mock_llm

@pytest.fixture
def sample_langgraph_state():
    """标准LangGraph状态fixture"""
    return {
        "messages": [],
        "next": "",
        "thought": "",
        "tool_calls": []
    }

@pytest.fixture
def tool_registry():
    """工具注册表fixture"""
    from langchain.tools import tool

    @tool
    def search(query: str) -> str:
        return f"Search results for: {query}"

    @tool
    def calculator(expression: str) -> str:
        return str(eval(expression))

    return [search, calculator]
```

#### 2. 测试状态流转
```python
# tests/level2/test_state_management.py

def test_state_flow():
    """测试LangGraph状态流转"""
    from langgraph.graph import StateGraph, END
    from typing import Annotated
    from operator import add

    class State(TypedDict):
        messages: Annotated[list, add]
        count: int

    def node_a(state: State) -> State:
        state["count"] += 1
        return {"messages": ["Node A executed"], "count": state["count"]}

    def node_b(state: State) -> State:
        state["count"] += 1
        return {"messages": ["Node B executed"], "count": state["count"]}

    # 构建图
    graph = StateGraph(State)
    graph.add_node("a", node_a)
    graph.add_node("b", node_b)
    graph.add_edge("a", "b")
    graph.add_edge("b", END)
    graph.set_entry_point("a")

    app = graph.compile()

    # 测试执行
    result = app.invoke({"messages": [], "count": 0})

    assert result["count"] == 2
    assert len(result["messages"]) == 2
```

#### 3. 测试条件边
```python
def test_conditional_edges(mocker):
    """测试条件边路由"""
    from langgraph.graph import StateGraph, END

    class State(TypedDict):
        score: int

    def router(state: State) -> str:
        """路由函数"""
        if state["score"] >= 80:
            return "excellent"
        elif state["score"] >= 60:
            return "good"
        else:
            return "fail"

    # 测试路由逻辑
    assert router({"score": 90}) == "excellent"
    assert router({"score": 70}) == "good"
    assert router({"score": 50}) == "fail"
```

#### 4. 测试记忆系统
```python
# tests/level2/test_memory.py

def test_conversation_buffer_memory(mocker):
    """测试对话缓冲记忆"""
    from langchain.memory import ConversationBufferMemory

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # 添加对话
    memory.save_context(
        {"input": "My name is Alice"},
        {"output": "Nice to meet you, Alice!"}
    )

    memory.save_context(
        {"input": "What's my name?"},
        {"output": "Your name is Alice."}
    )

    # 验证记忆
    history = memory.load_memory_variables({})
    assert len(history["chat_history"]) == 4  # 2轮对话，每轮2条

def test_vector_store_memory(mocker):
    """测试向量存储记忆"""
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OpenAIEmbeddings

    # Mock embedding
    mock_embeddings = mocker.Mock()
    mock_embeddings.embed_documents.return_value = [[0.1, 0.2, 0.3]]

    # 测试向量存储
    vectorstore = Chroma(
        collection_name="test_memory",
        embedding_function=mock_embeddings
    )

    # 添加记忆
    vectorstore.add_texts(
        texts=["User prefers Python over JavaScript"],
        metadatas [{"user": "alice", "timestamp": "2025-01-01"}]
    )

    # 验证检索
    results = vectorstore.similarity_search("What language does Alice prefer?")
    assert len(results) > 0
```

### 实践任务

#### Task 2.1: 测试ReAct Agent
```python
# tests/level2/test_react_agent.py

def test_react_reasoning_loop(mocker):
    """测试ReAct推理循环"""
    from app.agents import ReActAgent

    thoughts = []

    def capture_thought(prompt):
        thoughts.append(prompt)
        return AIMessage(content="I should search for information")

    mock_llm = mocker.Mock()
    mock_llm.invoke.side_effect = [
        # Thought 1
        capture_thought("Question"),
        # Action 1
        AIMessage(
            content="",
            tool_calls=[{"name": "search", "args": {"query": "test"}}]
        ),
        # Thought 2
        AIMessage(content="Based on the search results..."),
        # Final Answer
        AIMessage(content="The answer is 42")
    ]

    mock_search = mocker.Mock()
    mock_search.run.return_value = "Search result"

    agent = ReActAgent(llm=mock_llm, tools=[mock_search])
    result = agent.invoke("What is the meaning of life?")

    # 验证推理过程
    assert len(thoughts) > 0
    assert "42" in result
```

#### Task 2.2: 测试工具编排
```python
def test_parallel_tool_execution(mocker):
    """测试并行工具执行"""
    import asyncio

    async def mock_async_tool(name: str, delay: float):
        await asyncio.sleep(delay)
        return f"Result from {name}"

    # 测试并行执行
    start = time.time()
    results = asyncio.gather(
        mock_async_tool("tool1", 1.0),
        mock_async_tool("tool2", 1.0),
        mock_async_tool("tool3", 1.0)
    )
    elapsed = time.time() - start

    # 并行执行应该快于串行
    assert elapsed < 2.0  # 3个工具并行，应该约1秒
```

#### Task 2.3: 测试状态持久化
```python
def test_state_checkpointing():
    """测试状态检查点"""
    from langgraph.checkpoint import MemorySaver

    # 创建检查点保存器
    checkpointer = MemorySaver()

    # 在实际应用中，可以保存状态到文件或数据库
    state = {
        "messages": ["Hello"],
        "count": 5
    }

    config = {"configurable": {"thread_id": "test-thread"}}
    checkpointer.put(config, state, None)

    # 验证恢复
    restored = checkpointer.get(config)
    assert restored is not None
    assert restored["count"] == 5
```

### 推荐资源
- 📖 [Pytest Fixture详解](https://docs.pytest.org/en/stable/fixture.html)
- 📖 [LangGraph状态管理](https://langchain-ai.github.io/langgraph/concepts/low_level/#state)
- 📖 [测试数据管理模式](https://martinfowler.com/bliki/ObjectMother.html)

### 验收标准
- [ ] 设计可复用的Fixture体系
- [ ] 编写状态管理测试
- [ ] 测试记忆系统的准确性
- [ ] 测试覆盖率达到75%+

---

## Level 3: 框架对比测试（3-4周）

### 学习目标
- 掌握跨框架的功能等价性测试方法
- 测试不同框架的性能和资源消耗
- 评估框架的学习曲线和开发效率
- 测试OpenClaw框架（多渠道个人AI助手）
- 比较LangGraph与OpenClaw的测试差异

### 关键知识点

#### 1. 框架对比测试概述
```python
"""
为什么需要框架对比测试？
- 不同框架可能有相同的功能
- 但实现方式、性能、易用性不同
- 测试需要验证：功能等价性、性能差异、学习曲线

对比维度：
1. 功能等价性：相同输入是否产生语义相似的输出？
2. 性能指标：延迟、内存消耗、Token使用、吞吐量
3. 开发效率：代码行数、配置复杂度、Mock难度
4. 生态成熟度：文档质量、社区活跃度、扩展性
"""
```

#### 2. 功能等价性测试
```python
# tests/level3/test_framework_equivalence.py

def test_functional_equivalence_across_frameworks():
    """测试相同功能在不同框架中的实现"""
    from langgraph import create_langgraph_agent
    from openclaw import create_openclaw_agent

    # 相同的测试用例
    test_cases = [
        {"input": "What is 2+2?", "expected_keywords": ["4", "four"]},
        {"input": "Capital of France", "expected_keywords": ["Paris"]},
        {"input": "Summarize this text", "type": "summary"}
    ]

    frameworks = {
        "langgraph": create_langgraph_agent(),
        "openclaw": create_openclaw_agent()
    }

    for test_case in test_cases:
        results = {}
        for name, agent in frameworks.items():
            result = agent.invoke(test_case["input"])
            results[name] = result

        # 验证语义相似性
        if "expected_keywords" in test_case:
            for name, result in results.items():
                assert any(kw in result.lower() for kw in test_case["expected_keywords"]), \
                    f"{name} failed for: {test_case['input']}"

        # 验证跨框架一致性
        assert semantic_similarity(results["langgraph"], results["openclaw"]) > 0.7

def test_semantic_similarity(text1: str, text2: str) -> float:
    """计算两个文本的语义相似度"""
    # 使用嵌入模型或简单的词向量
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]

    return similarity
```

#### 3. 性能对比测试
```python
# tests/level3/test_framework_performance.py

import pytest
import time
import tracemalloc

@pytest.mark.benchmark(group="framework_comparison", min_rounds=5)
def test_latency_comparison(benchmark):
    """对比不同框架的响应延迟"""
    frameworks = [create_langgraph_agent(), create_openclaw_agent()]
    test_query = "What is the capital of France?"

    for agent in frameworks:
        result = benchmark(agent.invoke, test_query)
        assert "Paris" in result or "paris" in result

def test_memory_usage():
    """对比不同框架的内存消耗"""
    frameworks = {
        "langgraph": create_langgraph_agent(),
        "openclaw": create_openclaw_agent()
    }

    memory_usage = {}

    for name, agent in frameworks.items():
        tracemalloc.start()
        agent.invoke("Test query")
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memory_usage[name] = {
            "current": current,
            "peak": peak
        }

    # OpenClaw应该更轻量（如果优化得当）
    print(f"Memory usage: {memory_usage}")

def test_token_efficiency(mocker):
    """对比Token使用效率"""
    frameworks = {
        "langgraph": create_langgraph_agent(),
        "openclaw": create_openclaw_agent()
    }

    token_usage = {}

    for name, agent in frameworks.items():
        # Mock LLM来追踪Token
        mock_llm = mocker.Mock()
        mock_llm.invoke.return_value = AIMessage(content="Test response")

        agent.invoke("Test query")

        # 假设Agent记录了Token使用
        token_usage[name] = agent.get_token_usage()

    # 验证Token使用在合理范围内
    for name, usage in token_usage.items():
        assert usage < 1000, f"{name} used too many tokens: {usage}"
```

#### 4. 学习曲线评估
```python
# tests/level3/test_learning_curve.py

def test_code_complexity():
    """评估代码复杂度"""
    import ast
    import os

    frameworks = {
        "langgraph": "examples/langgraph_agent.py",
        "openclaw": "examples/openclaw_agent.py"
    }

    complexity_metrics = {}

    for name, file_path in frameworks.items():
        with open(file_path, 'r') as f:
            code = f.read()

        tree = ast.parse(code)

        metrics = {
            "lines_of_code": len(code.splitlines()),
            "functions": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
            "classes": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
            "imports": len([node for node in ast.walk(tree) if isinstance(node, ast.Import)])
        }

        complexity_metrics[name] = metrics

    print(f"Code complexity: {complexity_metrics}")

def test_mock_difficulty():
    """评估Mock难度"""
    # 测试：为每个框架编写Mock需要多少代码？
    frameworks = {
        "langgraph": mock_langgraph_setup,
        "openclaw": mock_openclaw_setup
    }

    for name, mock_fn in frameworks.items():
        lines_of_code = len(mock_fn.__code__.co_code)
        print(f"{name} mock setup: {lines_of_code} bytes")
```

---

### Level 3.1: OpenClaw框架专项测试（2周）

#### OpenClaw框架概述
```python
"""
OpenClaw框架特点（实际）：
- 个人AI助手，运行在自有设备上
- 多渠道支持：WhatsApp, Telegram, Slack, Discord, Google Chat,
  Signal, iMessage, Microsoft Teams, BlueBubbles, Matrix, Zalo等
- Gateway控制平面（WebSocket://127.0.0.1:18789）
- 多Agent路由（工作空间 + 会话隔离）
- Voice Wake + Talk Mode（macOS/iOS/Android）
- Live Canvas + A2UI（Agent驱动的视觉工作空间）
- Companion Apps（macOS菜单栏 + iOS/Android节点）
- Pi agent runtime（RPC模式，工具流式传输）
- Session模型（main直接聊天，群组隔离）
- 安全默认（DM配对，allowlist）
"""

#### 2. 测试多渠道消息路由
```python
# tests/level3/test_openclaw_channels.py

def test_channel_routing(mocker):
    """测试渠道消息路由"""
    from openclaw import Gateway, ChannelRegistry

    # Mock Gateway
    mock_gateway = mocker.Mock()
    mock_gateway.ws_port = 18789

    # 测试渠道注册
    channels = ["whatsapp", "telegram", "slack", "discord", "googlechat"]
    for channel in channels:
        assert ChannelRegistry.is_registered(channel)

def test_group_message_routing(mocker):
    """测试群组消息路由和Mention Gating"""
    # Mock群组消息
    group_message = {
        "channel": "telegram",
        "chat_type": "group",
        "from": "user123",
        "text": "@openclaw help"
    }

    # 测试路由逻辑
    router = GroupMessageRouter()
    route_decision = router.route(group_message)

    assert route_decision["should_respond"] == True
    assert route_decision["reason"] == "mention_detected"

def test_dm_pairing_security(mocker):
    """测试DM配对安全机制"""
    from openclaw.security import DMPolicy

    # 未知发送者应该收到配对码
    policy = DMPolicy(mode="pairing")
    unknown_sender = "+1234567890"

    result = policy.handle_inbound_dm(unknown_sender)
    assert result["action"] == "request_pairing"
    assert "pairing_code" in result

    # 配对后应该允许
    policy.approve_sender(unknown_sender, result["pairing_code"])
    result2 = policy.handle_inbound_dm(unknown_sender)
    assert result2["action"] == "allow"
```

#### 3. 测试Gateway和WebSocket连接
```python
# tests/level3/test_openclaw_gateway.py

def test_gateway_websocket_connection(mocker):
    """测试Gateway WebSocket连接"""
    import asyncio
    from openclaw import Gateway

    async def test_connection():
        # Mock WebSocket连接
        mock_ws = mocker.patch('websockets.serve')

        gateway = Gateway(port=18789)
        await gateway.start()

        # 验证WebSocket服务器启动
        mock_ws.assert_called_once()
        assert gateway.is_running()

    asyncio.run(test_connection())

def test_session_management(mocker):
    """测试Session模型"""
    from openclaw import SessionManager

    manager = SessionManager()

    # 创建main会话
    main_session = manager.get_or_create("main")
    assert main_session.type == "direct"

    # 创建群组隔离会话
    group_session = manager.get_or_create(
        f"group:telegram:chat123",
        isolate=True
    )
    assert group_session.isolated == True
    assert group_session.activation_mode == "auto"

def test_presence_and_typing(mocker):
    """测试在线状态和打字指示器"""
    from openclaw import PresenceManager

    presence = PresenceManager()

    # 模拟用户在线
    presence.set_online("user123", "telegram")
    assert presence.is_online("user123")

    # 模拟打字指示器
    presence.set_typing("user123", True)
    assert presence.is_typing("user123")
```

#### 4. 测试语音和Canvas功能
```python
# tests/level3/test_openclaw_voice_canvas.py

def test_voice_wake(mocker):
    """测试Voice Wake功能"""
    from openclaw.nodes import VoiceWake

    # Mock语音检测
    mock_detector = mocker.patch('openclaw.nodes.speech.WakeWordDetector')

    wake = VoiceWake(wake_phrase="Hey OpenClaw")
    mock_detector.return_value = True

    # 模拟唤醒词检测
    detected = wake.listen()
    assert detected == True
    mock_detector.assert_called_once()

def test_talk_mode(mocker):
    """测试Talk Mode（macOS/iOS/Android）"""
    from openclaw.nodes import TalkMode

    # Mock ElevenLabs TTS
    mock_tts = mocker.patch('openclaw.nodes.tts.elevenlabs')

    talk = TalkMode()
    talk.speak("Hello, this is OpenClaw")

    # 验证TTS调用
    mock_tts.generate.assert_called_once_with("Hello, this is OpenClaw")

def test_canvas_a2ui(mocker):
    """测试Canvas和A2UI（Agent-to-UI）"""
    from openclaw.canvas import CanvasHost, A2UI

    # Mock Canvas渲染
    mock_canvas = mocker.patch('openclaw.canvas.host.render')

    canvas = CanvasHost()
    a2ui = A2UI(canvas)

    # Agent推送UI更新
    a2ui.push({
        "type": "text",
        "content": "Task completed",
        "position": {"x": 100, "y": 200}
    })

    # 验证Canvas更新
    mock_canvas.assert_called_once()
```

### 实践任务

#### Task 3.1: 测试Companion Apps集成
```python
# tests/level3/test_openclaw_apps.py

def test_macos_menu_bar_app(mocker):
    """测试macOS菜单栏应用"""
    from openclaw.platforms.macos import MenuBarApp

    # Mock菜单栏
    mock_menu = mocker.patch('openclaw.platforms.macos.menu')

    app = MenuBarApp()
    app.show_status("Gateway: Connected")

    # 验证状态显示
    mock_menu.set_status.assert_called_once_with("Gateway: Connected")

def test_ios_node_camera(mocker):
    """测试iOS节点相机功能"""
    from openclaw.platforms.ios import IOSNode

    # Mock相机
    mock_camera = mocker.patch('openclaw.platforms.ios.camera')

    node = IOSNode()
    photo = node.take_photo()

    # 验证相机调用
    mock_camera.capture.assert_called_once()
    assert photo is not None

def test_android_node_screen_recording(mocker):
    """测试Android节点屏幕录制"""
    from openclaw.platforms.android import AndroidNode

    # Mock屏幕录制
    mock_recorder = mocker.patch('openclaw.platforms.android.screen')

    node = AndroidNode()
    recording = node.start_screen_recording()

    # 验证录制启动
    mock_recorder.start.assert_called_once()
```

#### Task 3.2: 性能对比测试
```python
def test_performance_comparison():
    """对比LangGraph和OpenClaw的性能"""
    import pytest

    @pytest.mark.benchmark(group="agent_frameworks")
    def test_langgraph_performance(benchmark, langgraph_agent):
        """测试LangGraph性能"""
        result = benchmark(langgraph_agent.invoke, "Test query")

    @pytest.mark.benchmark(group="agent_frameworks")
    def test_openclaw_performance(benchmark, openclaw_agent):
        """测试OpenClaw性能"""
        result = benchmark(openclaw_agent.process, "Test query")

    # 运行后比较benchmark结果
    # OpenClaw应该更快或更省内存
```

#### Task 3.3: OpenClaw集成测试
```python
def test_openclaw_with_external_apis(mocker):
    """测试OpenClaw与外部API集成"""
    from openclaw import Agent, APITool

    # Mock外部API
    mock_api = mocker.patch('requests.get')
    mock_api.return_value.json.return_value = {
        "data": "External data"
    }

    agent = Agent(name="api_agent", llm=mocker.Mock())
    agent.register_tool(APITool(
        name="external_api",
        endpoint="https://api.example.com"
    ))

    result = agent.use_tool("external_api", {})
    assert "External data" in result
```

### 推荐资源
- 📖 [OpenClaw文档](https://docs.openclaw.ai)
- 📖 [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- 📖 [OpenClaw Gateway架构](https://docs.openclaw.ai/gateway)
- 📖 [OpenClaw多渠道路由](https://docs.openclaw.ai/concepts/group-messages)
- 📖 [OpenClaw Canvas/A2UI](https://docs.openclaw.ai/platforms/mac/canvas)
- 📖 [多Agent系统论文](https://arxiv.org/abs/2308.03262)

### 验收标准
- [ ] 理解OpenClaw的架构特点
- [ ] 编写OpenClaw Agent的测试
- [ ] 完成LangGraph到OpenClaw的迁移测试
- [ ] 测试覆盖率达到80%+

---

## Level 4: OpenCode框架专项测试（4-5周）

### 学习目标
- 掌握OpenCode框架的测试方法
- 测试TUI（Terminal UI）交互
- 测试LSP集成和代码智能
- 测试Agent切换（build vs plan）
- 测试客户端/服务器架构
- 测试MCP（Model Context Protocol）集成
- 测试远程Agent执行
- 测试多客户端同步

### 关键知识点

#### 1. OpenCode框架概述
```python
"""
OpenCode框架特点（实际）：
- 开源AI编程助手（100% open source）
- Provider-agnostic（支持Claude, OpenAI, Google, 本地模型）
- TUI-focused（Terminal UI，由neovim用户开发）
- 客户端/服务器架构（可在本地运行Agent，远程从移动端控制）
- 内置LSP支持（开箱即用的Language Server Protocol）
- 两个内置Agent：
  - build：完全访问权限的默认Agent
  - plan：只读Agent，用于分析和代码探索
- general子agent：复杂搜索和多步任务
- TUI、Desktop、Web、Mobile多前端支持
- MCP协议全面支持
"""
```

#### 2. 测试TUI和Agent切换
```python
# tests/level4/test_opencode_tui.py

def test_tui_interaction(mocker):
    """测试TUI交互"""
    from opencode import TUI, TerminalInput

    # Mock终端输入
    mock_input = mocker.patch('opencode.tui.read_input')
    mock_input.return_value = "Fix the bug in app.py"

    tui = TUI()
    user_command = tui.get_user_input()

    assert user_command == "Fix the bug in app.py"
    mock_input.assert_called_once()

def test_agent_switching(mocker):
    """测试Agent切换（build vs plan）"""
    from opencode import AgentSwitcher

    # Mock Agent
    mock_build_agent = mocker.Mock()
    mock_plan_agent = mocker.Mock()

    switcher = AgentSwitcher(
        build_agent=mock_build_agent,
        plan_agent=mock_plan_agent
    )

    # 默认使用build agent
    assert switcher.current_agent == "build"

    # 切换到plan agent
    switcher.switch_to("plan")
    assert switcher.current_agent == "plan"

    # Plan agent应该拒绝文件编辑
    mock_plan_agent.can_edit_files.return_value = False
    assert not switcher.current_agent_can_edit()

def test_plan_agent_read_only(mocker):
    """测试Plan Agent的只读行为"""
    from opencode import PlanAgent

    mock_llm = mocker.Mock()
    mock_llm.complete.return_value = "I can analyze this code"

    agent = PlanAgent(llm=mock_llm)
    agent.set_read_only_mode(True)

    # 尝试编辑文件
    result = agent.edit_file("app.py", {"change": "fix bug"})

    # 应该拒绝编辑
    assert result["allowed"] == False
    assert result["reason"] == "plan_agent_read_only"
```

#### 3. 测试LSP集成
```python
# tests/level4/test_opencode_lsp.py

def test_lsp_server_lifecycle(mocker):
    """测试LSP服务器生命周期"""
    from opencode.lsp import LSPClientManager

    # Mock LSP服务器
    mock_lsp_server = mocker.patch('opencode.lsp.start_server')

    manager = LSPClientManager()

    # 启动Python LSP服务器
    server = manager.get_or_create("test.py", project_root="/project")
    assert server is not None
    mock_lsp_server.assert_called_once()

def test_lsp_code_intelligence(mocker):
    """测试LSP代码智能功能"""
    from opencode.lsp import LSPClient

    # Mock LSP客户端
    mock_client = mocker.Mock()
    mock_client.request_definition.return_value = {
        "uri": "file:///project/app.py",
        "range": {"start": {"line": 10, "character": 0}, "end": {"line": 10, "character": 20}}
    }

    client = LSPClient(mock_client)

    # 测试定义跳转
    result = client.go_to_definition("app.py", 5, 10)
    assert result["uri"].endswith("app.py")
    assert result["range"]["start"]["line"] == 10

def test_lsp_diagnostics_integration(mocker):
    """测试LSP诊断集成（150ms防抖）"""
    from opencode.lsp import LSPClientManager
    import time

    manager = LSPClientManager()

    # Mock诊断
    mock_diagnostics = mocker.patch('opencode.lsp.publish_diagnostics')

    # 模拟快速多次更改
    for i in range(5):
        manager.on_file_change("test.py")
        time.sleep(0.01)  # 10ms间隔

    # 应该防抖，只发布一次
    time.sleep(0.2)  # 等待防抖期结束
    assert mock_diagnostics.call_count == 1
```

#### 4. 测试MCP集成
```python
# tests/level4/test_opencode_mcp.py

def test_mcp_server_connection(mocker):
    """测试MCP服务器连接"""
    from opencode.mcp import MCPClient

    # Mock MCP服务器（stdio）
    mock_process = mocker.patch('subprocess.Popen')

    client = MCPClient(
        transport="stdio",
        command="npx",
        args=["@modelcontextprotocol/server-git"]
    )

    client.connect()

    # 验证进程启动
    mock_process.assert_called_once()

def test_mcp_tool_discovery(mocker):
    """测试MCP工具动态发现"""
    from opencode.mcp import MCPClient

    # Mock工具列表
    mock_tools = mocker.patch('opencode.mcp.list_tools')
    mock_tools.return_value = [
        {"name": "git_diff", "description": "Show git diff"},
        {"name": "git_log", "description": "Show git log"}
    ]

    client = MCPClient()
    tools = client.discover_tools()

    # 验证工具发现
    assert len(tools) == 2
    assert tools[0]["name"] == "git_diff"

def test_mcp_oauth_authentication(mocker):
    """测试MCP OAuth 2.0认证"""
    from opencode.mcp.auth import OAuthAuthenticator

    # Mock OAuth流程
    mock_oauth = mocker.patch('opencode.mcp.auth.authenticate')

    authenticator = OAuthAuthenticator(
        client_id="test_client",
        auth_url="https://example.com/oauth"
    )

    token = authenticator.get_token()

    # 验证OAuth调用
    mock_oauth.assert_called_once()
    assert token is not None
```

### 实践任务

#### Task 4.1: 测试客户端/服务器架构
```python
# tests/level4/test_opencode_client_server.py

def test_remote_agent_execution(mocker):
    """测试远程Agent执行（移动端控制）"""
    from opencode import Server, RemoteClient

    # Mock服务器
    mock_server = mocker.Mock()
    mock_server.run_agent.return_value = {"result": "Task completed"}

    server = Server(port=3000)
    server.start()

    # Mock客户端（移动端）
    client = RemoteClient(server_url="http://localhost:3000")
    result = client.execute_agent("Fix bug in app.py")

    # 验证远程执行
    mock_server.run_agent.assert_called_once()
    assert result["result"] == "Task completed"

def test_multi_client_sync(mocker):
    """测试多客户端同步（TUI + Desktop + Mobile）"""
    from opencode import SessionManager

    manager = SessionManager()

    # Mock多个客户端连接
    clients = ["tui", "desktop", "mobile"]
    for client_id in clients:
        manager.connect_client(client_id)

    # 测试状态同步
    manager.update_state("current_file", "app.py")

    # 所有客户端应该收到更新
    for client_id in clients:
        state = manager.get_client_state(client_id)
        assert state["current_file"] == "app.py"
```

#### Task 4.2: 测试Agent同步和冲突解决
```python
# tests/level4/test_agent_sync.py

def test_agent_synchronization(mocker):
    """测试Agent同步机制"""
    from opencode import SharedState

    # 创建共享状态
    shared_state = SharedState()

    agent1 = Agent(name="agent1", llm=mocker.Mock())
    agent2 = Agent(name="agent2", llm=mocker.Mock())

    agent1.bind_state(shared_state)
    agent2.bind_state(shared_state)

    # Agent1修改状态
    agent1.update_state("progress", 50)

    # Agent2应该能看到
    assert agent2.read_state("progress") == 50

def test_agent_conflict_resolution(mocker):
    """测试Agent冲突解决"""
    from opencode import ConflictResolver

    agent1 = Agent(name="agent1", llm=mocker.Mock())
    agent2 = Agent(name="agent2", llm=mocker.Mock())

    # 两个Agent给出不同建议
    suggestion1 = "Use Python for this project"
    suggestion2 = "Use JavaScript for this project"

    resolver = ConflictResolver()

    # 测试冲突解决策略
    resolution = resolver.resolve(
        agents=[agent1, agent2],
        suggestions=[suggestion1, suggestion2],
        strategy="vote"  # 或 "merge", "prioritize"
    )

    assert resolution is not None
    assert isinstance(resolution, str)
```

### 推荐资源
- 📖 [OpenCode文档](https://opencode.ai/docs)
- 📖 [OpenCode GitHub](https://github.com/anomalyco/opencode)
- 📖 [OpenCode LSP集成](https://opencode.ai/docs/lsp-integration-for-code-intelligence)
- 📖 [OpenCode Agent系统](https://opencode.ai/docs/agent-system-architecture-and-design)
- 📖 [OpenCode MCP支持](https://opencode.ai/docs/mcp-model-context-protocol-support)
- 📖 [多Agent系统论文](https://arxiv.org/abs/2308.03262)

### 验收标准
- [ ] 掌握OpenCode框架的测试方法
- [ ] 能测试复杂的多Agent协作
- [ ] 能测试Agent间的通信和同步
- [ ] 测试覆盖率达到85%+

---

## Level 5: 生产级测试体系（4-6周）

### 学习目标
- 建立完整的CI/CD测试流程
- 实现金丝雀发布和A/B测试
- 监控生产环境Agent质量
- 持续优化测试策略

### 关键知识点

#### 1. 分层测试策略
```python
"""
测试分层（针对多框架系统）：

单元测试 (Unit Tests)
  ├─ LangGraph组件测试
  ├─ OpenClaw组件测试
  └─ OpenCode组件测试
  ├─ 快速 (<0.1s each)
  └─ 完全Mock

集成测试 (Integration Tests)
  ├─ 框架间集成测试
  ├─ 工具集成测试
  └─ 中速 (<1s each)

E2E测试 (End-to-End Tests)
  ├─ 完整工作流测试
  ├─ 多Agent协作测试
  └─ 较慢 (<10s each)

回归测试 (Regression Tests)
  ├─ 历史bug场景
  └─ 性能回归检测
"""
```

#### 2. 多框架测试配置
```python
# tests/conftest.py

@pytest.fixture
def framework_test_env():
    """多框架测试环境"""
    return {
        "langgraph": {
            "enabled": True,
            "version": "0.2.0"
        },
        "openclaw": {
            "enabled": True,
            "version": "1.0.0"
        },
        "opencode": {
            "enabled": True,
            "version": "0.5.0"
        }
    }

@pytest.fixture
def agent_factory():
    """Agent工厂，支持多框架"""
    class AgentFactory:
        def create_langgraph_agent(self, name):
            from app.agents.langgraph_agent import LangGraphAgent
            return LangGraphAgent(name=name)

        def create_openclaw_agent(self, name):
            from app.agents.openclaw_agent import OpenClawAgent
            return OpenClawAgent(name=name)

        def create_opencode_agent(self, name):
            from app.agents.opencode_agent import OpenCodeAgent
            return OpenCodeAgent(name=name)

    return AgentFactory()
```

#### 3. 框架兼容性测试
```python
# tests/level5/test_framework_compatibility.py

def test_cross_framework_compatibility(agent_factory):
    """测试跨框架兼容性"""
    # 创建不同框架的Agent
    lg_agent = agent_factory.create_langgraph_agent("lg")
    oc_agent = agent_factory.create_openclaw_agent("oc")
    od_agent = agent_factory.create_opencode_agent("od")

    # 使用相同的测试用例
    test_case = {
        "input": "What is 2+2?",
        "expected_keywords": ["4", "four"]
    }

    # 验证所有框架都能处理
    for agent in [lg_agent, oc_agent, od_agent]:
        result = agent.process(test_case["input"])
        assert any(kw in result.lower() for kw in test_case["expected_keywords"])
```

### 实践任务

#### Task 5.1: 完整的CI/CD配置
```yaml
# .github/workflows/test_all_frameworks.yml

name: Multi-Framework CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    strategy:
      matrix:
        framework: [langgraph, openclaw, opencode]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run unit tests for ${{ matrix.framework }}
        run: |
          pytest tests/unit/${{ matrix.framework }}/ \
            --cov=app.${{ matrix.framework }} \
            --cov-report=xml

      - name: Check coverage
        run: |
          coverage report --fail-under=85

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4

      - name: Install all frameworks
        run: |
          pip install langgraph openclaw opencode

      - name: Run cross-framework integration tests
        run: |
          pytest tests/integration/cross_framework/ \
            --cov=app \
            --cov-report=xml

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4

      - name: Run E2E tests
        run: |
          pytest tests/e2e/ --timeout=600

      - name: Upload test results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: tests/e2e/results/
```

#### Task 5.2: A/B测试不同框架
```python
# tests/level5/test_ab_frameworks.py

class FrameworkABTest:
    """框架A/B测试"""

    def __init__(self):
        self.frameworks = {}
        self.metrics = {}

    def add_framework(self, name: str, agent):
        """添加测试框架"""
        self.frameworks[name] = agent

    def run_comparison_test(self, test_cases: list) -> dict:
        """运行对比测试"""
        results = {}

        for framework_name, agent in self.frameworks.items():
            framework_results = {
                "success": 0,
                "failed": 0,
                "total_time": 0,
                "avg_tokens": 0
            }

            for test_case in test_cases:
                try:
                    start = time.time()
                    response = agent.process(test_case["input"])
                    elapsed = time.time() - start

                    # 验证结果
                    if self.verify_response(response, test_case):
                        framework_results["success"] += 1
                    else:
                        framework_results["failed"] += 1

                    framework_results["total_time"] += elapsed

                except Exception as e:
                    framework_results["failed"] += 1

            # 计算平均值
            framework_results["avg_time"] = (
                framework_results["total_time"] / len(test_cases)
            )
            framework_results["success_rate"] = (
                framework_results["success"] / len(test_cases)
            )

            results[framework_name] = framework_results

        return results

    def recommend_framework(self, results: dict) -> str:
        """推荐最佳框架"""
        best_framework = None
        best_score = 0

        for name, metrics in results.items():
            # 综合评分
            score = (
                metrics["success_rate"] * 0.6 +
                (1 / metrics["avg_time"]) * 0.4
            )

            if score > best_score:
                best_score = score
                best_framework = name

        return best_framework

# 使用示例
def test_framework_selection():
    """测试框架选择"""
    # 创建测试实例
    ab_test = FrameworkABTest()

    # 添加不同框架的Agent
    ab_test.add_framework("langgraph", create_langgraph_agent())
    ab_test.add_framework("openclaw", create_openclaw_agent())
    ab_test.add_framework("opencode", create_opencode_agent())

    # 运行对比测试
    test_cases = [
        {"input": "Calculate fibonacci(10)", "expected": "55"},
        {"input": "Summarize this text", "type": "summary"},
        {"input": "Generate code for sorting", "type": "code"}
    ]

    results = ab_test.run_comparison_test(test_cases)

    # 输出结果
    print("Framework Comparison Results:")
    for framework, metrics in results.items():
        print(f"{framework}:")
        print(f"  Success Rate: {metrics['success_rate']:.2%}")
        print(f"  Avg Time: {metrics['avg_time']:.2f}s")

    # 获取推荐
    recommended = ab_test.recommend_framework(results)
    print(f"\nRecommended Framework: {recommended}")
```

#### Task 5.3: 生产监控
```python
# app/monitoring/agent_monitor.py

class MultiFrameworkMonitor:
    """多框架生产监控"""

    def __init__(self):
        self.metrics = {
            "langgraph": {},
            "openclaw": {},
            "opencode": {}
        }

    def record_invocation(
        self,
        framework: str,
        agent_name: str,
        success: bool,
        response_time: float,
        tokens_used: int,
        error: str = None
    ):
        """记录Agent调用"""
        if framework not in self.metrics:
            self.metrics[framework] = {
                "total_calls": 0,
                "successful": 0,
                "failed": 0,
                "total_time": 0,
                "total_tokens": 0,
                "errors": {}
            }

        metrics = self.metrics[framework]
        metrics["total_calls"] += 1

        if success:
            metrics["successful"] += 1
            metrics["total_time"] += response_time
            metrics["total_tokens"] += tokens_used
        else:
            metrics["failed"] += 1
            if error:
                metrics["errors"][error] = metrics["errors"].get(error, 0) + 1

    def get_framework_stats(self, framework: str) -> dict:
        """获取框架统计"""
        if framework not in self.metrics:
            return None

        metrics = self.metrics[framework]
        total = metrics["total_calls"]

        if total == 0:
            return {"avg_time": 0, "success_rate": 0, "avg_tokens": 0}

        return {
            "total_calls": total,
            "success_rate": metrics["successful"] / total,
            "avg_time": metrics["total_time"] / total,
            "avg_tokens": metrics["total_tokens"] / total,
            "error_distribution": metrics["errors"]
        }

    def get_best_framework(self, metric: str = "success_rate") -> str:
        """获取最佳表现的框架"""
        best = None
        best_value = 0

        for framework, data in self.metrics.items():
            stats = self.get_framework_stats(framework)
            if stats and stats.get(metric, 0) > best_value:
                best_value = stats[metric]
                best = framework

        return best

    def generate_report(self) -> str:
        """生成监控报告"""
        report = ["=" * 60]
        report.append("Multi-Framework Performance Report")
        report.append("=" * 60)

        for framework in self.metrics:
            stats = self.get_framework_stats(framework)
            if stats:
                report.append(f"\n{framework.upper()}:")
                report.append(f"  Total Calls: {stats['total_calls']}")
                report.append(f"  Success Rate: {stats['success_rate']:.2%}")
                report.append(f"  Avg Response Time: {stats['avg_time']:.2f}s")
                report.append(f"  Avg Tokens: {stats['avg_tokens']:.0f}")

        best = self.get_best_framework()
        report.append(f"\n🏆 Best Performing Framework: {best}")

        return "\n".join(report)
```

### 持续改进检查清单

#### 每周检查
- [ ] 所有框架的测试覆盖率是否达标？
- [ ] 是否有失败的测试？
- [ ] 是否有新增的边界情况需要测试？

#### 每月检查
- [ ] 框架版本更新是否需要调整测试？
- [ ] 测试运行时间是否过长？
- [ ] 是否有过时的测试用例？

#### 每季度检查
- [ ] 是否需要添加新框架的测试？
- [ ] 测试策略是否需要调整？
- [ ] 团队是否需要测试培训？

### 推荐资源
- 📖 [多框架测试最佳实践](https://testing.googleblog.com/)
- 📖 [持续集成与持续部署](https://www.continuousdelivery20.com/)
- 📖 [A/B测试统计学原理](https://www.amazon.com/Trustworthy-Online-Controlled-Experiments-A/B/dp/1108724262)

### 验收标准
- [ ] CI/CD流程覆盖所有框架
- [ ] 所有测试自动化运行
- [ ] 生产环境有完整监控
- [ ] 测试覆盖率>90%
- [ ] 有框架对比和选择机制
- [ ] 团队遵循TDD流程

---

## 总结：测试能力进阶路径

```
Level 0: 环境搭建 → 能运行测试
Level 1: 单元测试  → 能Mock、写单元测试、TDD实践
Level 2: LangGraph深入 → 集成测试、Fixture体系
Level 3: OpenClaw多渠道 → Gateway测试、渠道路由、语音/Canvas测试
Level 4: OpenCode + 多Agent → LSP测试、TUI测试、MCP集成、协作测试
Level 5: 生产体系 → CI/CD、多框架监控、持续改进
```

## 框架对比总结

### LangGraph
- **定位**: 底层Agent编排框架
- **测试重点**: 状态管理、图流转、工具调用
- **适用场景**: 构建自定义Agent工作流

### OpenClaw
- **定位**: 个人AI助手（多渠道）
- **测试重点**:
  - 多渠道消息路由（WhatsApp/Telegram/Slack等10+平台）
  - Gateway WebSocket连接
  - Session管理（群组隔离、DM配对）
  - Voice Wake + Talk Mode
  - Canvas + A2UI
  - Companion Apps（macOS/iOS/Android）
- **适用场景**: 个人助理、跨平台消息处理

### OpenCode
- **定位**: 开源AI编程助手（100%开源、Provider-agnostic）
- **测试重点**:
  - TUI交互
  - LSP集成（代码智能）
  - Agent切换（build vs plan）
  - 客户端/服务器架构
  - MCP协议集成
  - 多前端（TUI/Desktop/Web/Mobile）
- **适用场景**: 代码开发、IDE集成、远程编程

## 核心原则

1. **测试先行**：TDD是保证质量的基础
2. **快速反馈**：单元测试应该秒级完成
3. **真实模拟**：Mock要尽可能接近真实行为
4. **全面覆盖**：单元、集成、E2E三层测试
5. **持续监控**：生产环境质量不容忽视
6. **框架中立**：测试方法适用于不同框架

## 推荐学习顺序

1. **打好基础**：完成 Level 0-1，建立TDD习惯
2. **深入第一框架**：Level 2 专注LangGraph测试
3. **扩展到新框架**：Level 3-4 学习OpenClaw和OpenCode
4. **掌握多Agent**：Level 4 后半部分专注协作测试
5. **达到生产级**：Level 5 建立完整测试体系

## 测试工具总结

### 基础工具
- `pytest` - 测试框架
- `pytest-asyncio` - 异步测试
- `pytest-mock` - Mock支持
- `pytest-cov` - 覆盖率
- `pytest-benchmark` - 性能测试
- `pytest-xdist` - 并行测试

### 高级工具
- `moto` - AWS服务Mock
- `responses` - HTTP请求Mock
- `freezegun` - 时间Mock
- `faker` - 测试数据生成
- `hypothesis` - 属性测试

### 框架特定
- LangGraph测试工具
- OpenClaw测试套件
- OpenCode验证工具

---

**记住**：优秀的测试体系是Agent生产环境的基石。从第一行代码开始就建立测试保障，让每个Agent都可靠、可控、可信任！🧪
