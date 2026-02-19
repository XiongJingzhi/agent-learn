# Level 2 快速开始指南

> **目标**: 快速了解 Level 2 的学习路径和核心内容
> **适合**: 刚开始学习 Level 2 的学习者

---

## 🎯 Level 2 学习目标

完成 Level 2 后，你将能够：

1. **理解和实现 PER 架构**（Planner-Executor-Reflector）
2. **设计和实现任务分解 DAG**
3. **实现状态机和执行流程控制**
4. **构建分层记忆系统**
5. **选择和实现合适的推理机制**
6. **编写全面的测试**

---

## 📚 学习路径概览

```
Level 2 学习路径
│
├─ 第一阶段：任务规划架构 (8-10 小时)
│  ├─ PER 架构 (00-07)
│  ├─ 代码示例：01_planner_agent.py
│  └─ 练习：基础练习 1-3
│
├─ 第二阶段：记忆系统 (6-8 小时)
│  ├─ 三层记忆设计 (08-09)
│  ├─ 代码示例：03_memory_system.py
│  └─ 练习：基础练习 4
│
├─ 第三阶段：推理机制 (6-8 小时)
│  ├─ 推理机制对比 (12-15)
│  ├─ 代码示例：04_reasoning_comparison.py
│  └─ 练习：基础练习 5
│
├─ 第四阶段：测试策略 (6-8 小时)
│  ├─ 测试策略 (16)
│  ├─ 代码示例：05_testing_examples.py
│  └─ 练习：基础练习 6
│
└─ 第五阶段：Capstone 项目 (10-12 小时)
   └─ 完整的 Planning Agent
```

---

## 🚀 快速开始

### 第 1 步：理解 PER 架构 (45 分钟)

**阅读**: `notes/00_planner_executor_reflector_architecture.md`

**核心概念**:
- **Planner**: 分解任务、制定计划
- **Executor**: 执行任务、管理状态
- **Reflector**: 评估结果、决定下一步

**实践**: 运行 `examples/01_planner_agent.py`

```bash
cd study/level2/examples
python 01_planner_agent.py
```

**预期输出**:
```
PER Agent 示例
输入: 搜索并总结 LangGraph 的核心特性

[规划器] 分析输入
[执行器] 开始执行
[反思器] 评估执行结果
任务完成！
```

---

### 第 2 步：学习任务分解 (50 分钟)

**阅读**: `notes/01_task_decomposition_dag.md`

**核心概念**:
- DAG（有向无环图）
- 任务依赖
- 拓扑排序

**实践**: 运行 `examples/02_task_decomposition.py`

```bash
python 02_task_decomposition.py
```

---

### 第 3 步：完成基础练习 (2 小时)

**文件**: `exercises/01_basic_exercises.md`

**包含**:
- 练习 1: PER 架构理解
- 练习 2: DAG 设计
- 练习 3: 状态机设计
- 练习 4: 记忆系统
- 练习 5: 推理机制
- 练习 6: 测试策略

**建议**: 先尝试自己回答，再查看答案（点击展开）。

---

### 第 4 步：实现记忆系统 (2 小时)

**阅读**:
- `notes/08_memory_hierarchy_design.md`
- `notes/09_memory_retrieval_strategy.md`

**实践**: 运行 `examples/03_memory_system.py`

```bash
python 03_memory_system.py
```

**理解**: 三层记忆如何协同工作

---

### 第 5 步：对比推理机制 (2 小时)

**阅读**: `notes/12_reasoning_mechanisms_comparison.md`

**实践**: 运行 `examples/04_reasoning_comparison.py`

```bash
python 04_reasoning_comparison.py
```

**理解**: 何时使用哪种推理机制

---

### 第 6 步：学习测试 (2 小时)

**阅读**: `notes/16_testing_strategy.md`

**实践**: 运行 `examples/05_testing_examples.py`

```bash
python 05_testing_examples.py
```

**理解**: 如何测试 Agent 系统

---

### 第 7 步：Capstone 项目 (10-12 小时)

**文件**: `projects/01_capstone_project.md`

**目标**: 构建完整的 Planning Agent

**阶段**:
1. 基础框架 (2-3 小时)
2. 核心功能 (3-4 小时)
3. 记忆系统 (2 小时)
4. 测试优化 (2-3 小时)

---

## 📊 学习检查点

### 检查点 1：第一周结束

**应该完成**:
- [ ] 阅读 PER 架构相关笔记 (00-07)
- [ ] 运行所有示例代码 (01-02)
- [ ] 完成基础练习 1-3

**验收**:
- 能够解释 PER 三个组件的职责
- 能够设计简单的任务 DAG
- 理解状态机的基本概念

---

### 检查点 2：第二周结束

**应该完成**:
- [ ] 阅读记忆系统笔记 (08-09)
- [ ] 运行记忆系统示例 (03)
- [ ] 完成基础练习 4

**验收**:
- 理解三层记忆架构
- 能够实现简单的检索
- 知道如何优化记忆性能

---

### 检查点 3：第三周结束

**应该完成**:
- [ ] 阅读推理机制笔记 (12-15)
- [ ] 运行推理对比示例 (04)
- [ ] 完成基础练习 5

**验收**:
- 能够对比 ReAct、CoT、ToT、Reflection
- 知道何时使用哪种推理机制
- 能够实现简单的推理器

---

### 检查点 4：第四周结束

**应该完成**:
- [ ] 阅读测试策略笔记 (16)
- [ ] 运行测试示例 (05)
- [ ] 完成基础练习 6
- [ ] 开始 Capstone 项目

**验收**:
- 能够编写单元测试
- 理解 Mock 的使用
- 知道如何测试 Agent 系统

---

## 💡 学习建议

### 建议 1：理论和实践结合

不要只读笔记，要运行代码，修改代码，观察结果。

**示例**:
```python
# 修改 01_planner_agent.py 中的任务
# 观察执行顺序的变化
```

---

### 建议 2：记录学习过程

建议为每个笔记创建学习记录：

```markdown
## 学习笔记：PER 架构

### 核心概念
- Planner: ...
- Executor: ...
- Reflector: ...

### 疑问
- Q: 何时触发重规划？
- A: ...

### 实践
- 运行了示例代码
- 修改了 XXX
- 观察到了 YYY
```

---

### 建议 3：完成练习

不要跳过练习。练习是巩固知识的关键。

- 基础练习：理解概念
- 进阶练习：深入理解
- 挑战项目：综合应用

---

### 建议 4：循序渐进

不要试图一次性完成所有内容。

- 每天 2-3 小时
- 每周完成一个阶段
- 4 周完成 Level 2

---

## 🆘 常见问题

### Q1: 如果我不理解某个概念怎么办？

**A**:
1. 重新阅读笔记
2. 运行示例代码
3. 修改代码观察变化
4. 完成相关练习
5. 查看参考资料

---

### Q2: 如果代码运行出错怎么办？

**A**:
1. 检查 Python 版本（需要 3.8+）
2. 检查依赖是否安装
3. 查看错误信息
4. 使用 `try-except` 调试
5. 参考示例代码

---

### Q3: 如何知道我是否掌握了内容？

**A**: 使用"费曼技巧"：
- 能否用简单的语言解释？
- 能否教会别人？
- 能否应用到实际问题？

---

### Q4: Capstone 项目太难了怎么办？

**A**:
1. 从 MVP 开始（最小可行产品）
2. 参考示例代码
3. 逐步增加功能
4. 寻求帮助和反馈

---

## 📖 资源清单

### 必读笔记

- `00_planner_executor_reflector_architecture.md` - PER 架构
- `01_task_decomposition_dag.md` - 任务分解
- `08_memory_hierarchy_design.md` - 记忆系统
- `12_reasoning_mechanisms_comparison.md` - 推理机制
- `16_testing_strategy.md` - 测试策略

### 必运行示例

- `examples/01_planner_agent.py` - PER Agent
- `examples/03_memory_system.py` - 记忆系统
- `examples/04_reasoning_comparison.py` - 推理对比
- `examples/05_testing_examples.py` - 测试示例

### 必完成练习

- `exercises/01_basic_exercises.md` - 基础练习
- `projects/01_capstone_project.md` - Capstone 项目

---

## ✅ 完成标准

完成 Level 2 的标准：

### 知识理解

- [ ] 能解释 PER 架构
- [ ] 能设计任务 DAG
- [ ] 能实现状态机
- [ ] 能对比推理机制
- [ ] 能设计测试策略

### 实践能力

- [ ] 能实现 Planning Agent
- [ ] 能实现三层记忆
- [ ] 能实现至少两种推理机制
- [ ] 能编写测试（>= 70% 覆盖率）

### 项目产出

- [ ] 完成 Capstone 项目
- [ ] 代码有类型提示和文档
- [ ] 测试覆盖率 >= 70%

---

## 🎉 开始学习

准备好了吗？让我们开始 Level 2 的学习之旅！

**第一步**: 阅读 `notes/00_planner_executor_reflector_architecture.md`

**第二步**: 运行 `examples/01_planner_agent.py`

**第三步**: 完成 `exercises/01_basic_exercises.md` 的练习 1

祝学习顺利！🚀

---

**记住：学习是一个循序渐进的过程，不要急于求成。每天进步一点点，4 周后你将掌握 Level 2 的所有核心内容！** 💪
