# 03. 目标分解技术

> **目标**: 掌握自主 Agent 中的目标分解方法
> **预计时间**: 45 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 什么是目标分解？

### 定义

**目标分解（Goal Decomposition）** 是将复杂目标分解为可执行的子目标的过程。

> **类比**：就像"**把大象装进冰箱**"这个目标，分解为三步：
> 1. 打开冰箱门
> 2. 把大象放进去
> 3. 关上冰箱门

虽然这是个笑话，但它说明了目标分解的核心：**把复杂问题简单化**。

---

## 分解策略

### 策略 1：层次分解（Hierarchical Decomposition）

**原理**：从顶层目标开始，逐层分解直到可执行

**示例**：
```
目标：构建一个 AI 写作助手

L1: 主目标
├─ L2: 子目标
│   ├─ 研究现有产品
│   ├─ 设计核心功能
│   └─ 开发原型
│       ├─ L3: 任务
│       │   ├─ 实现文本生成
│       │   ├─ 实现文本优化
│       │   └─ 实现风格迁移
```

**代码实现**：
```python
def hierarchical_decompose(goal: str, max_depth: int = 3):
    """层次分解"""

    class Node:
        def __init__(self, name, children=None):
            self.name = name
            self.children = children or []

    # 构建层次树
    def build_tree(goal, depth):
        if depth >= max_depth:
            return Node(goal)

        # 分解为子目标
        sub_goals = llm_decompose(goal)

        children = [build_tree(sg, depth + 1) for sg in sub_goals]

        return Node(goal, children)

    return build_tree(goal, 0)
```

---

### 策略 2：依赖分析（Dependency Analysis）

**原理**：识别目标之间的依赖关系，确定执行顺序

**依赖类型**：
- **顺序依赖**：A 必须在 B 之前完成
- **并行独立**：A 和 B 可以同时进行
- **资源冲突**：A 和 B 共享资源，需要协调

**示例**：
```python
class TaskDependency:
    """任务依赖分析"""

    def analyze(self, tasks: List[Task]) -> Dict:
        """分析依赖关系"""

        dependencies = {}

        for i, task_a in enumerate(tasks):
            for j, task_b in enumerate(tasks):
                if i == j:
                    continue

                # 判断依赖关系
                if self.depends_on(task_a, task_b):
                    if task_a.name not in dependencies:
                        dependencies[task_a.name] = []
                    dependencies[task_a.name].append(task_b.name)

        return dependencies

    def depends_on(self, task_a, task_b):
        """判断 task_a 是否依赖 task_b"""

        prompt = f"""
        任务 A：{task_a.description}
        任务 B：{task_b.description}

        任务 A 是否依赖任务 B？（是/否）
        如果是，说明原因。
        """

        response = self.llm.invoke(prompt)
        return "是" in response
```

---

### 策略 3：原子化分解（Atomic Decomposition）

**原理**：将目标分解为最小的、不可再分的原子任务

**原子任务特征**：
- 单一职责：只做一件事
- 可独立执行：不依赖其他任务
- 可验证：有明确的完成标准

**示例**：
```python
# 非原子任务
task = "实现用户注册功能，包括验证码、邮件通知"

# 原子化分解
atomic_tasks = [
    "设计用户注册表单",
    "实现验证码生成",
    "实现表单验证",
    "实现用户存储",
    "实现邮件通知",
    "集成所有组件"
]
```

---

## LLM 驱动的目标分解

### 方法 1：直接分解

**提示词设计**：
```python
DECOMPOSITION_PROMPT = """
你是一个任务分解专家。

目标：{objective}

请将这个目标分解为 3-5 个子目标。
要求：
1. 每个子目标应该具体且可执行
2. 子目标之间有逻辑关系
3. 子目标的完成能够推动主目标的达成

返回格式：JSON 数组
[
  {{"name": "子目标1", "description": "..."}},
  {{"name": "子目标2", "description": "..."}},
  ...
]
"""

def decompose(objective: str) -> List[SubGoal]:
    """使用 LLM 分解目标"""

    prompt = DECOMPOSITION_PROMPT.format(objective=objective)
    response = llm.invoke(prompt)

    return parse_subgoals(response)
```

---

### 方法 2：逐步细化（Progressive Refinement）

**原理**：先粗粒度分解，再逐步细化

**示例**：
```python
def progressive_decompose(goal: str):
    """逐步细化分解"""

    # 第 1 轮：粗粒度分解
    print("[1] 粗粒度分解")
    sub_goals = decompose(goal, granularity="coarse")
    # 输出：["研究产品", "设计功能", "开发原型"]

    # 第 2 轮：细化每个子目标
    refined_goals = []
    for sg in sub_goals:
        print(f"[2] 细化：{sg}")
        tasks = decompose(sg, granularity="fine")
        refined_goals.extend(tasks)

    return refined_goals

# 输出：
# ["研究竞品产品", "研究用户需求", "设计核心功能", "设计界面",
#  "实现后端", "实现前端", "集成测试"]
```

---

### 方法 3：基于约束的分解

**原理**：在分解时考虑资源和时间约束

**示例**：
```python
def constrained_decompose(
    goal: str,
    time_limit: int,  # 小时
    budget: float     # 美元
):
    """基于约束分解"""

    prompt = f"""
    目标：{goal}
    时间限制：{time_limit} 小时
    预算限制：${budget}

    请在这些约束下分解目标。
    估算每个子目标的：
    1. 预计时间
    2. 预计成本
    3. 优先级（高/中/低）

    确保总时间和成本在限制内。
    """

    response = llm.invoke(prompt)
    return parse_constrained_decomposition(response)
```

---

## 动态目标分解

### 场景：执行过程中调整目标

**问题**：初始分解可能不合理，需要根据执行情况动态调整

**解决方案**：
```python
class DynamicDecomposer:
    """动态分解器"""

    def __init__(self):
        self.execution_history = []

    def decompose_and_refine(self, goal: str):
        """分解并持续优化"""

        # 初始分解
        sub_goals = self.initial_decompose(goal)

        for sub_goal in sub_goals:
            # 执行子目标
            result = self.execute(sub_goal)

            # 记录历史
            self.execution_history.append({
                "goal": sub_goal,
                "result": result
            })

            # 基于结果调整剩余目标
            if self.need_adjustment(result):
                remaining = sub_goals[sub_goals.index(sub_goal) + 1:]
                adjusted = self.adjust_goals(remaining, result)
                sub_goals = sub_goals[:sub_goals.index(sub_goal) + 1] + adjusted

        return sub_goals

    def need_adjustment(self, result):
        """判断是否需要调整"""

        # 检查失败率
        if result["status"] == "failed":
            return True

        # 检查是否发现新信息
        if result.get("new_information"):
            return True

        return False
```

---

## 目标分解的评估

### 评估指标

| 指标 | 说明 | 良好标准 |
|------|------|---------|
| **完整性** | 是否覆盖所有方面 | 所有子目标的并集 = 主目标 |
| **独立性** | 子目标是否独立 | 低耦合，可独立执行 |
| **可执行性** | 是否可执行 | 每个子目标有明确的行动 |
| **可验证性** | 是否可验证 | 有明确的完成标准 |

**评估方法**：
```python
def evaluate_decomposition(goal, sub_goals):
    """评估分解质量"""

    scores = {}

    # 1. 完整性
    completeness = llm_evaluate(
        f"这些子目标的并集是否等于「{goal}」？"
    )
    scores["completeness"] = completeness

    # 2. 独立性
    independence = check_independence(sub_goals)
    scores["independence"] = independence

    # 3. 可执行性
    executability = check_executability(sub_goals)
    scores["executability"] = executability

    # 4. 可验证性
    verifiability = check_verifiability(sub_goals)
    scores["verifiability"] = verifiability

    # 综合评分
    scores["overall"] = mean(scores.values())

    return scores
```

---

## 最小验证

### 验证目标
- ✅ 理解目标分解的三种策略
- ✅ 能够使用 LLM 进行目标分解
- ✅ 理解动态目标分解的必要性

### 验证步骤
1. 选择一个复杂目标（如"学习 LangGraph"）
2. 使用层次分解策略分解它
3. 评估分解质量

### 预期输出
能够将复杂目标分解为 3-5 个可执行的子目标。

---

## 常见错误

### 错误 1：分解过细

**问题**：分解得太细，导致任务数量爆炸

**解决**：控制分解深度（最多 3 层）

---

### 错误 2：忽略依赖关系

**问题**：不考虑依赖关系，导致执行顺序混乱

**解决**：在分解时分析依赖关系

---

### 错误 3：静态分解

**问题**：分解后不再调整，无法适应变化

**解决**：采用动态分解，根据执行情况调整

---

## 下一步

- 📖 `notes/04_long_term_planning.md` - 长期规划
- 📖 `notes/05_self_reflection.md` - 自我反思

---

**记住：目标分解就像把大象装进冰箱，一步一步来！** 🐘🚪
