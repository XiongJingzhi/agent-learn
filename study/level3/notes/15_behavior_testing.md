# 15. 行为测试策略

> **主题**: 测试多智能体系统的行为正确性
> **时间**: 60 分钟
> **难度**: ⭐⭐⭐⭐

---

## 🎯 学习目标

1. ✅ 理解为什么多智能体系统需要特殊的测试策略
2. ✅ 掌握行为测试的设计方法
3. ✅ 理解如何测试 Agent 之间的协作
4. ✅ 能够设计全面的多智能体测试用例

---

## 📚 核心概念

### 什么是行为测试？

**行为测试** = 验证系统的行为是否符合预期

**区别**:
- **单元测试** = 测试组件是否正确
- **行为测试** = 测试系统行为是否符合预期

**类比**:
- 单元测试 = 检查车零件是否合格
- 行为测试 = 检查车是否能安全驾驶

---

## 🔍 为什么多智能体系统需要行为测试？

### 挑战 1: 不可预测性

多智能体系统的行为可能因为以下因素而变化：
- Agent 的决策顺序
- 通信延迟
- 并发冲突

**解决方案**: 设计能够覆盖各种场景的测试用例。

---

### 挑战 2: 协作复杂性

Agent 之间的协作可能产生意外行为。

**示例**:
```
Agent A 和 Agent B 同时尝试修改同一个资源
→ 可能产生竞态条件
→ 需要测试并发场景
```

**解决方案**: 测试各种协作场景，包括冲突场景。

---

### 挑战 3: 状态空间爆炸

多个 Agent 的状态组合非常多。

**示例**:
- 3 个 Agent，每个有 5 种状态
→ 5³ = 125 种状态组合

**解决方案**: 使用等价类划分和边界值分析。

---

## 🧩 行为测试设计

### 测试维度

#### 1. 功能性测试

**目标**: 验证系统是否正确完成功能

**示例**:
```python
def test_research_write_pipeline():
    """测试研究-写作流水线"""
    # 创建 Agent
    researcher = Agent(name="researcher", role="研究")
    writer = Agent(name="writer", role="写作")

    # 执行任务
    result = pipeline.execute(
        agents=[researcher, writer],
        input="写一篇关于 LangGraph 的文章"
    )

    # 验证功能
    assert result.status == "success"
    assert "LangGraph" in result.content
    assert len(result.content) > 100  # 有实际内容
```

---

#### 2. 协作测试

**目标**: 验证 Agent 之间的协作是否正确

**示例**:
```python
def test_agent_collaboration():
    """测试 Agent 协作"""
    # 创建 Agent
    manager = Agent(name="manager", role="协调")
    worker1 = Agent(name="worker1", role="执行1")
    worker2 = Agent(name="worker2", role="执行2")

    # 执行任务
    result = manager.delegate(
        agents=[worker1, worker2],
        task="分析数据并生成报告"
    )

    # 验证协作
    assert worker1.received_tasks > 0  # worker1 收到任务
    assert worker2.received_tasks > 0  # worker2 收到任务
    assert result.worker_results  # 有工作结果
    assert result.final_output  # 有最终输出
```

---

#### 3. 冲突测试

**目标**: 验证系统能否正确处理冲突

**示例**:
```python
def test_conflict_resolution():
    """测试冲突解决"""
    # 创建 Agent
    agent1 = Agent(name="agent1", role="专家1")
    agent2 = Agent(name="agent2", role="专家2")

    # 创建冲突场景（两个 Agent 需要同一个资源）
    resource = LimitedResource(capacity=1)

    # 并发访问
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(agent1.use_resource, resource)
        future2 = executor.submit(agent2.use_resource, resource)

        # 验证只有一个 Agent 成功
        results = [future1.result(), future2.result()]
        success_count = sum(1 for r in results if r.success)
        assert success_count == 1  # 只有一个成功

        # 验证另一个 Agent 得到了正确的错误处理
        failed = next(r for r in results if not r.success)
        assert failed.error_type == "resource_busy"
```

---

#### 4. 性能测试

**目标**: 验证系统的性能是否满足要求

**示例**:
```python
def test_performance():
    """测试性能"""
    # 创建多个 Agent
    agents = [Agent(f"agent{i}") for i in range(10)]

    # 测量执行时间
    start_time = time.time()
    results = run_parallel_tasks(agents, tasks)
    end_time = time.time()

    # 验证性能
    execution_time = end_time - start_time
    assert execution_time < 10  # 10 秒内完成
    assert all(r.success for r in results)  # 所有任务成功
```

---

## 🎯 测试用例设计

### 等价类划分

将输入空间划分为若干等价类，每类中选择代表性测试用例。

**示例**:
```
Agent 数量:
- 小规模: 1-3 个
- 中规模: 4-10 个
- 大规模: >10 个

选择测试: 1, 5, 15 个 Agent
```

---

### 边界值分析

测试边界情况。

**示例**:
```
Agent 数量边界:
- 0 个 Agent（无效输入）
- 1 个 Agent（最小有效）
- 最大支持数（上限）
```

---

### 场景测试

测试真实场景。

**示例**:
```python
def test_real_world_scenario():
    """测试真实场景：客服系统"""
    # 创建 Agent
    receptionist = Agent(name="接待员", role="初步接待")
    technician = Agent(name="技术员", role="技术支持")
    supervisor = Agent(name="主管", role="疑难处理")

    # 模拟用户咨询
    user_query = "我的账户无法登录"

    # 执行流程
    step1 = receptionist.handle(user_query)
    assert step1.status == "escalated"  # 需要升级

    step2 = technician.handle(step1.escalated_query)
    assert step2.need_supervisor  # 需要主管

    step3 = supervisor.handle(step2.escalated_query)
    assert step3.resolved  # 问题解决
```

---

## 📊 测试覆盖率

### 覆盖率维度

#### 1. Agent 覆盖率

每个 Agent 是否都被测试？

```python
# 测试所有 Agent
agents = get_all_agents()
for agent in agents:
    test_agent_behavior(agent)
```

---

#### 2. 交互覆盖率

Agent 之间的所有交互是否都被测试？

```python
# 测试所有 Agent 对
agent_pairs = get_all_agent_pairs()
for agent1, agent2 in agent_pairs:
    test_agent_interaction(agent1, agent2)
```

---

#### 3. 场景覆盖率

所有重要场景是否都被测试？

```python
# 测试所有场景
scenarios = [
    "正常流程",
    "冲突处理",
    "错误恢复",
    "性能压力"
]
for scenario in scenarios:
    test_scenario(scenario)
```

---

## 💡 实践建议

### 测试设计原则

1. **从简单到复杂**
   - 先测试单个 Agent
   - 再测试两个 Agent 的协作
   - 最后测试多个 Agent 的复杂协作

2. **覆盖边界情况**
   - 测试 0 个 Agent、1 个 Agent、最大 Agent 数
   - 测试资源耗尽、网络中断等极端情况

3. **使用 Mock 隔离**
   - Mock 外部依赖
   - 专注于测试协作逻辑

4. **记录测试结果**
   - 保存测试日志
   - 分析失败原因
   - 持续改进测试

---

## 🧪 测试工具

### 1. pytest

```python
import pytest

@pytest.mark.parametrize("num_agents", [1, 2, 5, 10])
def test_multi_agent_system(num_agents):
    """参数化测试"""
    agents = create_agents(num_agents)
    result = run_system(agents)
    assert result.success
```

---

### 2. hypothesis（基于属性的测试）

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=100))
def test_with_various_agent_counts(num_agents):
    """基于属性的测试"""
    agents = create_agents(num_agents)
    result = run_system(agents)

    # 验证属性
    assert result.execution_time < num_agents * 2  # 线性时间
    assert result.success_rate > 0.9  # 高成功率
```

---

### 3. pytest-asyncio（异步测试）

```python
import pytest

@pytest.mark.asyncio
async def test_async_agent_communication():
    """测试异步通信"""
    agent1 = AsyncAgent("agent1")
    agent2 = AsyncAgent("agent2")

    # 异步发送消息
    task1 = agent1.send_message(agent2, "Hello")
    task2 = agent2.send_message(agent1, "Hi")

    # 等待完成
    await asyncio.gather(task1, task2)

    # 验证
    assert agent1.received_messages > 0
    assert agent2.received_messages > 0
```

---

## 🎓 费曼解释

### 给 5 岁孩子的解释

**多智能体系统的行为测试就像检查团队合作**：

1. **功能性测试** = 检查团队是否完成了任务
2. **协作测试** = 检查队员之间是否配合良好
3. **冲突测试** = 检查队员吵架时能否解决问题
4. **性能测试** = 检查团队工作是否够快

### 关键要点

1. **多智能体系统的测试比单 Agent 更复杂**
2. **需要测试 Agent 之间的协作和冲突**
3. **设计全面的测试用例很重要**

---

## 🔗 相关资源

- [Behavior-Driven Development](https://en.wikipedia.org/wiki/Behavior-driven_development)
- [Property-Based Testing](https://hypothesis.works/)
- [Multi-Agent Testing Patterns](https://martinfowler.com/articles/multi-agent-testing.html)

---

## ✅ 最小验证

### 任务

1. 为一个简单的多智能体系统设计测试用例（20 分钟）
2. 实现功能性测试（15 分钟）
3. 实现协作测试（15 分钟）
4. 运行测试并分析结果（10 分钟）

### 期望输出

- [ ] 测试用例设计文档
- [ ] 可运行的测试代码
- [ ] 测试结果分析报告

---

## 🚀 下一步

学习完本笔记后，继续学习：
- `notes/16_property_based_testing.md` - 深入了解基于属性的测试
- `examples/11_behavior_tests.py` - 实现行为测试套件

---

**记住：行为测试确保多智能体系统的正确性和可靠性！** 🧪
