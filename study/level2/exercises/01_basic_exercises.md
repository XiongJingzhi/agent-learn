# 基础练习

> **目标**: 巩固 Level 2 核心概念
> **预计时间**: 2 小时
> **难度**: ⭐⭐

---

## 练习 1：PER 架构理解

### 问题 1.1
Planner、Executor、Reflector 三个组件的职责分别是什么？

<details>
<summary>查看答案</summary>

- **Planner（规划器）**：分解任务、制定计划（DAG）、确定执行顺序
- **Executor（执行器）**：执行具体任务、维护状态、处理错误
- **Reflector（反思器）**：评估结果、分析完成度、决定下一步行动
</details>

---

### 问题 1.2
在什么情况下 Reflector 会决定重新规划？

<details>
<summary>查看答案</summary>

Reflector 决定重新规划的情况：
- 完成度 < 50%
- 存在失败任务
- 发现新的关键信息
- 用户修改目标
</details>

---

## 练习 2：DAG 设计

### 问题 2.1
设计一个任务 DAG 来完成以下任务：
"搜索 LangGraph 文档，提取关键特性，并与竞品对比，生成报告"

<details>
<summary>查看答案</summary>

```python
tasks = [
    Task(id="search_langgraph", type="search",
         description="搜索 LangGraph 文档", dependencies=[]),

    Task(id="search_competitor", type="search",
         description="搜索竞品信息", dependencies=[]),

    Task(id="extract_features", type="extract",
         description="提取 LangGraph 特性", dependencies=["search_langgraph"]),

    Task(id="extract_competitor", type="extract",
         description="提取竞品特性", dependencies=["search_competitor"]),

    Task(id="compare", type="compare",
         description="对比分析", dependencies=["extract_features", "extract_competitor"]),

    Task(id="generate_report", type="generate",
         description="生成报告", dependencies=["compare"])
]
```
</details>

---

### 问题 2.2
如何检测 DAG 中是否存在循环依赖？

<details>
<summary>查看答案</summary>

使用深度优先搜索（DFS）检测环：

```python
def has_cycle(graph):
    visited = set()
    rec_stack = set()

    def visit(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if visit(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if visit(node):
                return True

    return False
```
</details>

---

## 练习 3：状态机设计

### 问题 3.1
列出任务可能的状态，并说明哪些状态之间可以转换。

<details>
<summary>查看答案</summary>

任务状态：
- `PENDING`：待执行
- `READY`：准备执行（依赖满足）
- `IN_PROGRESS`：执行中
- `COMPLETED`：已完成
- `FAILED`：失败
- `BLOCKED`：被阻塞
- `RETRYING`：重试中

合法转换：
- `PENDING` → `READY`（依赖满足）
- `READY` → `IN_PROGRESS`（开始执行）
- `IN_PROGRESS` → `COMPLETED`（成功）
- `IN_PROGRESS` → `FAILED`（失败）
- `FAILED` → `RETRYING`（重试）
- `RETRYING` → `IN_PROGRESS`（再次尝试）
</details>

---

### 问题 3.2
为什么需要状态持久化？

<details>
<summary>查看答案</summary>

状态持久化的作用：
1. **恢复执行**：系统崩溃后可以恢复状态
2. **审计追踪**：查看任务历史
3. **调试分析**：分析执行问题
4. **监控展示**：可视化执行进度
</details>

---

## 练习 4：记忆系统

### 问题 4.1
短期记忆、中期记忆、长期记忆的区别是什么？

<details>
<summary>查看答案</summary>

| 特性 | 短期记忆 | 中期记忆 | 长期记忆 |
|------|----------|----------|----------|
| **内容** | 当前对话 | 对话摘要 | 用户偏好、知识库 |
| **容量** | ~10-20 条消息 | ~50-100 条摘要 | 几乎无限 |
| **速度** | 极快 | 快 | 中等 |
| **持久化** | 否 | 会话级别 | 持久 |
</details>

---

### 问题 4.2
如何实现高效的记忆检索？

<details>
<summary>查看答案</summary>

检索策略：
1. **精确匹配**：根据 ID 或关键词
2. **向量搜索**：使用语义相似度
3. **混合检索**：结合精确和向量搜索
4. **时间衰减**：考虑信息新鲜度
5. **上下文感知**：根据当前上下文调整
</details>

---

## 练习 5：推理机制

### 问题 5.1
比较 ReAct、CoT、ToT 三种推理机制的特点和适用场景。

<details>
<summary>查看答案</summary>

| 机制 | 特点 | 适用场景 | 复杂度 |
|------|------|----------|--------|
| **ReAct** | 推理-行动-观察循环 | 工具调用、简单任务 | 低 |
| **CoT** | 显式推理链 | 数学、逻辑推理 | 中 |
| **ToT** | 多路径探索 | 创意、规划任务 | 高 |
</details>

---

### 问题 5.2
何时应该使用 Reflection 推理？

<details>
<summary>查看答案</summary>

Reflection 推理适用于：
- **写作任务**：需要反复修改和精炼
- **分析任务**：需要自我纠正和改进
- **代码生成**：需要审查和优化
- **长文档生成**：需要逐步完善
</details>

---

## 练习 6：测试策略

### 问题 6.1
在测试 Agent 时，为什么需要 Mock LLM 和工具？

<details>
<summary>查看答案</summary>

使用 Mock 的原因：
1. **成本**：避免每次测试都调用真实 API
2. **速度**：测试运行更快
3. **确定性**：控制输出，便于断言
4. **隔离**：不依赖外部服务
</details>

---

### 问题 6.2
单元测试、集成测试、端到端测试的区别是什么？

<details>
<summary>查看答案</summary>

- **单元测试**：测试单个组件（节点、工具）
- **集成测试**：测试多个组件协同工作
- **端到端测试**：测试完整的用户场景

测试金字塔：
```
        /\
       /E2E\        少量
      /------\
     /集成测试 \     适量
    /----------\
   /  单元测试  \    大量
  /--------------\
```
</details>

---

## 代码练习

### 练习 7：实现简单的规划器

实现一个简单的 `Planner` 类，能够将"搜索并总结"类的任务分解为 DAG。

```python
class SimplePlanner:
    def plan(self, input: str) -> TaskDAG:
        # TODO: 实现任务分解逻辑
        pass
```

<details>
<summary>提示</summary>

1. 检查输入是否包含"搜索"和"总结"
2. 创建相应的任务
3. 建立依赖关系
4. 返回 TaskDAG
</details>

---

### 练习 8：实现状态转换验证

实现一个 `StateMachine` 类，能够验证状态转换的合法性。

```python
class StateMachine:
    def can_transition(self, from_state: str, to_state: str) -> bool:
        # TODO: 检查状态转换是否合法
        pass
```

<details>
<summary>提示</summary>

1. 定义合法的状态转换映射
2. 检查 `from_state` → `to_state` 是否在映射中
3. 处理终态（不能再转换）
</details>

---

## 完成标准

完成本练习后，你应该能够：
- ✅ 解释 PER 架构的三个组件
- ✅ 设计简单的任务 DAG
- ✅ 理解状态机的工作原理
- ✅ 区分不同类型的记忆
- ✅ 选择合适的推理机制
- ✅ 编写基础的测试

---

## 下一步

- 📖 `exercises/02_intermediate_exercises.md` - 进阶练习
- 🧪 开始实践 Capstone 项目
- `projects/01_capstone_project.md`

---

**记住：基础练习是巩固概念的关键！** 💪
