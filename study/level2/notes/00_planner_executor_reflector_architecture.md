# PER 架构总览

> **目标**: 理解 Planner-Executor-Reflector 架构模式
> **预计时间**: 45 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 为什么需要 PER 架构？

传统的 ReAct Agent 在面对复杂任务时存在局限：
- **缺乏规划**：没有全局规划，走一步看一步
- **无法反思**：执行完成后无法评估和改进
- **难以分解**：无法将大任务分解为小任务

PER 架构通过引入三个专门的组件解决这些问题：
- **Planner（规划器）**: 分解任务、制定计划
- **Executor（执行器）**: 执行具体任务
- **Reflector（反思器）**: 评估结果、调整策略

**类比**：PER 就像一个**项目管理团队**，项目经理制定计划，开发工程师执行任务，质量保证团队评估结果。

---

## PER 架构组成

### 组件 1：Planner（规划器）

**职责**：
- 接收用户输入
- 分析任务要求
- 分解任务为子任务
- 制定执行计划（DAG）
- 确定任务优先级

**输入**：
- 用户查询或任务描述
- 可用的工具列表
- 之前的执行历史

**输出**：
- 任务列表（DAG 结构）
- 任务依赖关系
- 执行顺序

**示例**：
```python
from typing import List, Dict

class Planner:
    def plan(self, input: str, tools: List[str]) -> Dict:
        """制定执行计划"""
        # 分析任务
        task_type = self._analyze_task(input)

        # 分解为子任务
        subtasks = self._decompose_task(input, task_type)

        # 构建依赖图
        dag = self._build_dag(subtasks)

        # 确定优先级
        prioritized = self._prioritize(dag)

        return {
            "tasks": prioritized,
            "dag": dag,
            "estimated_steps": len(prioritized)
        }
```

---

### 组件 2：Executor（执行器）

**职责**：
- 接收计划中的任务
- 执行具体任务（调用工具、LLM 等）
- 维护执行状态
- 处理执行错误
- 返回执行结果

**输入**：
- 当前任务
- 可用的工具
- 之前任务的结果（上下文）

**输出**：
- 任务结果
- 执行状态
- 错误信息（如果有）

**示例**：
```python
class Executor:
    def execute(self, task: Dict, context: Dict) -> Dict:
        """执行任务"""
        task_id = task["id"]
        task_type = task["type"]

        try:
            if task_type == "tool_call":
                result = self._execute_tool(task, context)
            elif task_type == "llm_query":
                result = self._execute_llm(task, context)
            else:
                result = self._execute_default(task, context)

            return {
                "task_id": task_id,
                "status": "completed",
                "result": result
            }

        except Exception as e:
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }
```

---

### 组件 3：Reflector（反思器）

**职责**：
- 评估执行结果
- 分析是否完成目标
- 判断是否需要重新规划
- 提供改进建议

**输入**：
- 原始用户查询
- 执行结果汇总
- 执行过程日志

**输出**：
- 评估结果（成功/失败/部分成功）
- 改进建议
- 是否需要重新规划

**示例**：
```python
class Reflector:
    def reflect(self, input: str, execution_result: Dict) -> Dict:
        """反思执行结果"""
        # 提取关键信息
        final_answer = execution_result.get("final_answer")
        steps = execution_result.get("execution_steps", [])

        # 评估完成度
        completeness = self._assess_completeness(input, final_answer)

        # 分析问题
        issues = self._identify_issues(steps)

        # 判断下一步
        if completeness >= 0.9:
            next_action = "finish"
        elif issues:
            next_action = "replan"
        else:
            next_action = "continue"

        return {
            "completeness": completeness,
            "issues": issues,
            "next_action": next_action,
            "suggestions": self._generate_suggestions(issues)
        }
```

---

## 完整 PER 流程

### 流程图

```
用户输入
    │
    ▼
[Planner] ──────> 任务计划（DAG）
    │                 │
    │                 ▼
    │            [Executor] ──> 任务1 ──> 结果1
    │            [Executor] ──> 任务2 ──> 结果2
    │            [Executor] ──> 任务3 ──> 结果3
    │                 │
    │                 ▼
    └────────> [Reflector] ──> 评估结果
                          │
                    ┌─────┴─────┐
                    ▼             ▼
                [完成]        [重规划]
                    │             │
                    ▼             │
                返回答案      新一轮循环
```

---

## 关键设计决策

### 决策 1：任务分解粒度

**问题**：任务应该分解到多细？

**选项**：
- **细粒度**：每个步骤都是一个任务
  - 优点：执行灵活，易于并行
  - 缺点：计划复杂，调度开销大

- **粗粒度**：每个子任务都是一个任务
  - 优点：计划简单，调度快
  - 缺点：执行不灵活，难以并行

**推荐**：中等粒度（2-5 个步骤/任务）

---

### 决策 2：何时重新规划

**问题**：什么情况下需要重新规划？

**触发条件**：
- 执行失败率 > 50%
- 发现新的关键信息
- 用户修改目标
- 超过最大执行步数

**重新规划策略**：
- 保留已完成的有效结果
- 调整剩余任务的顺序
- 重新评估任务优先级

---

### 决策 3：如何评估完成度

**评估方法**：
1. **关键词匹配**：结果是否包含关键信息
2. **用户确认**：询问用户是否满意
3. **质量评分**：对答案进行质量评分

**阈值**：
- 完全匹配：>= 0.9
- 部分匹配：0.5 - 0.9
- 不匹配：< 0.5

---

## 简化示例

```python
from typing import Dict, List

class SimplePERAgent:
    """简化的 PER Agent"""

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.reflector = Reflector()

    def run(self, input: str) -> str:
        """运行 PER 流程"""
        max_iterations = 3

        for iteration in range(max_iterations):
            print(f"\n=== 迭代 {iteration + 1} ===")

            # 1. 规划
            print("[1] 规划阶段")
            plan = self.planner.plan(input, ["search", "calculate"])
            print(f"计划: {len(plan['tasks'])} 个任务")

            # 2. 执行
            print("[2] 执行阶段")
            results = []
            for task in plan['tasks']:
                result = self.executor.execute(task, {})
                results.append(result)
                print(f"  任务 {task['id']}: {result['status']}")

            # 3. 反思
            print("[3] 反思阶段")
            reflection = self.reflector.reflect(input, {
                "results": results,
                "execution_steps": len(results)
            })

            print(f"  完成度: {reflection['completeness']:.2f}")
            print(f"  下一步: {reflection['next_action']}")

            # 4. 判断是否继续
            if reflection['next_action'] == "finish":
                print("\n=== 任务完成 ===")
                return self._generate_final_answer(results)

            elif reflection['next_action'] == "replan":
                print("\n=== 重新规划 ===")
                input = self._update_input(input, reflection['suggestions'])

        return "达到最大迭代次数，返回部分结果"

    def _generate_final_answer(self, results: List[Dict]) -> str:
        """生成最终答案"""
        return "基于执行结果，答案是：42"

# 使用示例
agent = SimplePERAgent()
result = agent.run("计算 1+1，然后搜索 LangGraph 的信息")
print(f"\n最终结果: {result}")
```

---

## 最小验证

### 验证目标
- ✅ 理解 PER 三个组件的职责
- ✅ 能够设计简单的规划流程
- ✅ 能够实现执行器
- ✅ 能够设计反思逻辑

### 验证步骤
1. 运行上面的简化示例
2. 修改规划器的任务分解逻辑
3. 添加新的任务类型到执行器
4. 改进反思器的评估逻辑

---

## 常见错误

### 错误 1：规划过度

**问题**：规划太详细，无法执行

**解决**：从粗粒度开始，逐步细化

---

### 错误 2：忽略错误处理

**问题**：执行器没有错误处理

**解决**：每个任务都要有 try-catch

---

### 错误 3：没有真正的反思

**问题**：反思器只是形式主义

**解决**：基于实际结果给出具体建议

---

## 下一步

- 📖 `notes/01_task_decomposition_dag.md` - 任务分解 DAG
- 🧪 `examples/01_planner_agent.py` - 规划 Agent 示例
- ✏ `exercises/01_basic_exercises.md` - 基础练习题

---

**记住：PER 就像一个项目管理团队，项目经理制定计划，开发工程师执行任务，质量保证团队评估结果！** 👥
