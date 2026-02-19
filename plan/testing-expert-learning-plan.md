# Testing Expert 学习计划 - Agent 测试

> **角色**: Testing Expert (高级测试）  
> **目标**: 设计测试用例、验证功能正确性、评估代码质量

---

## 🎯 学习目标

通过 Testing Expert 角色的学习，你将能够：

1. ✅ **掌握 Agent 测试策略**
   - 单元测试（Unit Testing）
   - 集成测试（Integration Testing）
   - 端到端测试（End-to-End Testing）
   - 行为测试（Behavior Testing）

2. ✅ **掌握测试工具和框架**
   - pytest、unittest
   - unittest.mock
   - hypothesis（属性测试）
   - pytest-asyncio（异步测试）

3. ✅ **掌握 Mock 和 Stub**
   - Mock LLM 和工具
   - Mock 外部依赖（API、数据库）
   - 测试隔离和独立性

4. ✅ **掌握测试覆盖率**
   - 行覆盖率（Line Coverage）
   - 分支覆盖率（Branch Coverage）
   - 覆盖率工具（pytest-cov）

5. ✅ **掌握性能测试和基准测试**
   - 性能测试（Performance Testing）
   - 基准测试（Benchmark Testing）
   - 性能分析和优化建议

6. ✅ **掌握测试自动化和 CI/CD**
   - 自动化测试运行
   - 测试报告生成
   - CI/CD 集成

---

## 📚 学习路径（6 个 Levels）

### Level 0: 认知地图 (1-2 周)

**学习目标**: 理解 Agent 测试的基础概念和基本用法

**核心内容**:
- Agent 测试的重要性
- Agent 测试的类型
- 测试用例设计
- 环境搭建和配置

**实战项目**:
- 环境搭建（Python、pytest、pytest-cov）
- 第一个测试用例
- 测试报告生成

**时间投入**: 5-10 小时

---

### Level 1: 动手实践 (2-3 周)

**学习目标**: 掌握 Agent 的单元测试和 Mock

**核心内容**:
- 单元测试策略
- Mock LLM 和工具
- 测试隔离和独立性
- 测试覆盖率

**实战项目**:
- 测试 Agent 的工具调用
- 测试 Agent 的记忆管理
- 测试 Agent 的决策逻辑
- 测试覆盖率 >= 70%

**时间投入**: 15-25 小时

---

### Level 2: 深度理解 (3-4 周)

**学习目标**: 掌握 Agent 的集成测试和 Fixture

**核心内容**:
- 集成测试策略
- Fixture 设计和使用
- 测试数据准备和管理
- 测试环境的隔离

**实战项目**:
- 测试 Agent 的完整工作流
- 测试 Agent 与外部系统的集成
- 设计和使用 Fixture
- 集成测试覆盖率 >= 60%

**时间投入**: 20-30 小时

---

### Level 3: 设计思维 (4-5 周)

**学习目标**: 掌握 Agent 的行为测试和质量评估

**核心内容**:
- 行为测试策略
- 基于属性的测试（Property-Based Testing）
- Agent 行为的正确性验证
- Agent 行为的鲁棒性测试
- 质量评估和改进建议

**实战项目**:
- 测试 Agent 的行为正确性
- 测试 Agent 的边界条件
- 测试 Agent 的异常处理
- 评估 Agent 的输出质量
- 提供改进建议

**时间投入**: 25-35 小时

---

### Level 4: 优化进阶 (3-4 周)

**学习目标**: 掌握 Agent 的性能测试和基准测试

**核心内容**:
- 性能测试策略
- 基准测试（Benchmark Testing）
- 性能分析和优化建议
- 高级 Mock（模拟复杂场景）
- 并发测试和压力测试

**实战项目**:
- 测试 Agent 的执行速度
- 测试 Agent 的资源使用
- 对比不同实现的性能
- 提供性能优化建议
- 压力测试和极限测试

**时间投入**: 20-30 小时

---

### Level 5: 生产系统 (4-6 周)

**学习目标**: 掌握 Agent 的自动化测试和 CI/CD

**核心内容**:
- 自动化测试运行
- 测试报告生成和可视化
- CI/CD 集成
- 监控和告警
- 持续改进

**实战项目**:
- 配置自动化测试（GitHub Actions）
- 生成测试报告和覆盖率报告
- 集成到 CI/CD 流程
- 配置监控和告警
- 持续改进测试策略

**时间投入**: 30-40 小时

---

## 🧪 测试策略

### 1. 单元测试 (Unit Testing)

**目标**: 测试 Agent 的各个组件

**测试对象**:
- Agent 的工具（Tools）
- Agent 的记忆（Memory）
- Agent 的决策逻辑（Reasoning Logic）

**测试方法**:
- 隔离被测试的组件
- 使用 Mock 对象模拟依赖
- 验证组件的输入输出

**示例**:
```python
import pytest
from unittest.mock import Mock, patch

def test_search_tool():
    """测试搜索工具"""
    # 创建 Mock
    mock_search_api = Mock(return_value="搜索结果")
    
    # 测试工具
    tool = Tool(name="search", func=mock_search_api)
    result = tool.run("LangChain")
    
    # 验证结果
    assert result == "搜索结果"
    mock_search_api.assert_called_once_with("LangChain")
```

---

### 2. 集成测试 (Integration Testing)

**目标**: 测试 Agent 组件的交互

**测试对象**:
- Agent 的完整工作流
- Agent 与外部系统的集成（API、数据库）
- Agent 的多轮对话

**测试方法**:
- 测试真实的交互（而不是 Mock）
- 测试完整的工作流
- 验证组件之间的交互

**示例**:
```python
def test_agent_workflow():
    """测试 Agent 工作流"""
    # 创建真实的 Agent
    agent = create_agent(tools=[search_tool, calculator_tool])
    
    # 测试工作流
    result = agent.invoke({"input": "搜索 LangChain"})
    
    # 验证结果
    assert result["output"] is not None
    assert "LangChain" in result["output"]
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["tool"] == "search"
```

---

### 3. 端到端测试 (End-to-End Testing)

**目标**: 测试 Agent 在真实场景中的表现

**测试对象**:
- Agent 在真实场景中的表现
- Agent 的用户体验（UX）
- Agent 的业务价值

**测试方法**:
- 使用真实的数据和场景
- 测试完整的用户旅程
- 验证 Agent 的输出质量

**示例**:
```python
def test_e2e_conversation():
    """测试端到端对话"""
    # 创建真实的 Agent
    agent = create_agent(tools=[search_tool])
    
    # 模拟用户对话
    conversation = [
        {"role": "user", "content": "我叫张三"},
        {"role": "assistant", "content": "你好，张三！"},
        {"role": "user", "content": "我叫什么？"},
        {"role": "assistant", "content": "你的名字是张三。"}
    ]
    
    # 测试对话
    for turn in conversation:
        result = agent.invoke({"input": turn["content"]})
        assert result["output"] is not None
    
    # 验证 Agent 是否记住了用户姓名
    last_result = agent.invoke({"input": "我叫什么？"})
    assert "张三" in last_result["output"]
```

---

### 4. 行为测试 (Behavior Testing)

**目标**: 测试 Agent 的行为正确性和鲁棒性

**测试对象**:
- Agent 的决策是否正确
- Agent 是否能处理异常和错误
- Agent 的行为是否一致

**测试方法**:
- 设计测试场景覆盖各种边界条件
- 验证 Agent 的决策逻辑
- 测试 Agent 的错误处理

**示例**:
```python
import pytest

class TestAgentBehavior:
    """测试 Agent 行为"""
    
    def test_correct_decision(self):
        """测试正确决策"""
        agent = create_agent()
        
        # 测试 Agent 的决策
        result = agent.invoke({"input": "搜索 LangChain"})
        
        # 验证 Agent 是否调用了正确的工具
        assert result["tool_calls"][0]["tool"] == "search"
        assert "LangChain" in result["tool_calls"][0]["input"]
    
    def test_error_handling(self):
        """测试错误处理"""
        agent = create_agent()
        
        # 测试异常情况
        result = agent.invoke({"input": "无效的查询"})
        
        # 验证 Agent 是否优雅地处理了错误
        assert result["error_message"] is not None or result["output"] is not None
    
    def test_consistency(self):
        """测试行为一致性"""
        agent = create_agent()
        
        # 测试相同的输入是否得到相同的输出
        result_1 = agent.invoke({"input": "什么是 LangChain？"})
        result_2 = agent.invoke({"input": "什么是 LangChain？"})
        
        # 验证 Agent 的输出是否一致
        assert result_1["output"] == result_2["output"]
```

---

## 📊 测试工具和框架

### 1. pytest

**描述**: 最流行的 Python 测试框架

**特点**:
- 简单易用
- 丰富的插件生态
- 支持参数化测试
- 支持并行测试

**示例**:
```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("1 + 1", "2"),
    ("2 + 2", "4"),
    ("3 + 3", "6")
])
def test_calculator(input, expected):
    """参数化测试"""
    result = eval(input)
    assert result == int(expected)
```

---

### 2. unittest.mock

**描述**: Python 内置的 Mock 框架

**特点**:
- 内置在 Python 标准库中
- 简单易用
- 支持 Mock 和 Stub

**示例**:
```python
from unittest.mock import Mock, patch

def test_agent_with_mock():
    """使用 Mock 测试 Agent"""
    # 创建 Mock LLM
    mock_llm = Mock(return_value="Mock 回复")
    
    # 创建 Agent
    agent = create_agent(llm=mock_llm)
    
    # 执行 Agent
    result = agent.invoke({"input": "测试"})
    
    # 验证 Agent 是否调用了 LLM
    mock_llm.assert_called_once()
    assert result["output"] == "Mock 回复"
```

---

### 3. hypothesis

**描述**: 基于属性的测试库（Property-Based Testing）

**特点**:
- 基于属性生成测试用例
- 发现边界条件的 Bug
- 生成简洁的测试用例

**示例**:
```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=0, max_value=100))
def test_addition(x, y):
    """基于属性的测试"""
    result = x + y
    
    # 验证属性
    assert result >= x
    assert result >= y
    assert result == y + x
```

---

### 4. pytest-cov

**描述**: pytest 的覆盖率插件

**特点**:
- 测量代码覆盖率
- 生成覆盖率报告
- 支持多种覆盖率类型

**示例**:
```bash
# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

---

## 🎯 核心技能

### 1. 测试策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **单元测试** | 测试各个组件 | 测试工具、记忆、决策逻辑 |
| **集成测试** | 测试组件交互 | 测试工作流、外部系统集成 |
| **端到端测试** | 测试真实场景 | 测试用户体验、业务价值 |
| **行为测试** | 测试行为正确性 | 测试决策逻辑、错误处理、一致性 |

### 2. Mock 和 Stub

| 技术 | 说明 | 适用场景 |
|------|------|----------|
| **Mock** | 模拟依赖的行为 | 测试 LLM 调用、API 调用 |
| **Stub** | 模拟依赖的返回值 | 测试工具调用、数据库查询 |

### 3. 测试覆盖率

| 类型 | 说明 | 目标 |
|------|------|------|
| **行覆盖率** | 测试代码行是否被覆盖 | >= 80% |
| **分支覆盖率** | 测试条件分支是否被覆盖 | >= 70% |
| **函数覆盖率** | 测试函数是否被覆盖 | >= 90% |

---

## 🚀 下一步

### 1. 开始学习 Level 0

```bash
cd /Users/xiongfeng/SourceCode/agent-learn/study/level0

# 查看学习起点
cat START_HERE.md

# 开始学习
# 1. 阅读 notes 目录下的学习笔记
# 2. 运行 examples 目录下的示例代码
# 3. 完成 exercises 目录下的练习题
```

### 2. 查看测试学习计划

```bash
cd /Users/xiongfeng/SourceCode/agent-learn

# 查看测试学习计划
cat testing-expert-learning-plan.md
```

---

## 📝 学习产出

每个 Level，Testing Expert 应该产出：

1. ✅ **测试用例**: 清晰的测试用例，覆盖各种场景
2. ✅ **测试报告**: 覆盖率报告和测试结果报告
3. ✅ **质量评估**: Agent 行为的质量评估报告
4. ✅ **改进建议**: 代码质量改进和优化建议
5. ✅ **测试策略**: 测试策略和最佳实践文档

---

**记住：作为 Testing Expert，你的职责是设计测试用例、验证功能正确性、评估代码质量！** 🧪
