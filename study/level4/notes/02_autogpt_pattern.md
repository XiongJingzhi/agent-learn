# 02. AutoGPT 模式详解

> **目标**: 理解 AutoGPT 的核心模式和架构设计
> **预计时间**: 50 分钟
> **难度**: ⭐⭐⭐ 中高级
> **前置**: 已阅读 01_babyagi_architecture.md

---

## 什么是 AutoGPT？

### 定义

**AutoGPT** 是一个开源的**自主 AI Agent**，能够通过自主规划、执行、反思的循环，实现复杂目标的达成。

> **类比**：如果说 BabyAGI 是"**专注的实习生**"（逐个完成任务），那么 AutoGPT 就是"**经验丰富的项目经理**"（能够全局规划、动态调整、深度反思）。

---

## BabyAGI vs AutoGPT

### 对比表格

| 特征 | BabyAGI | AutoGPT |
|------|---------|---------|
| **核心模式** | 任务驱动 | 规划-执行-反思 |
| **目标分解** | 生成任务列表 | 分层规划（目标→子目标→任务）|
| **反思机制** | 简单完成度评估 | 深度反思和策略调整 |
| **记忆系统** | 简单向量存储 | 分层记忆（短期/长期）|
| **执行方式** | 顺序执行任务 | 动态调整执行策略 |
| **复杂度** | 中等 | 高 |

---

## AutoGPT 核心架构

### 五大组件

```
┌────────────────────────────────────────────────────────┐
│                     AutoGPT 架构                       │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │ 1. 规划  │ -> │ 2. 执行  │ -> │ 3. 反思  │        │
│  │  Planner │    │ Executor │    │ Reflector│        │
│  └──────────┘    └──────────┘    └──────────┘        │
│       │               │               │               │
│       │               │               │               │
│       ▼               ▼               ▼               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │ 4. 记忆  │◄───┤ 5. 工具  │◄───┤ 6. 调整  │        │
│  │  Memory  │    │  Tools   │    │ Adjust   │        │
│  └──────────┘    └──────────┘    └──────────┘        │
│                                                         │
│              持续循环直到目标达成                        │
└─────────────────────────────────────────────────────────┘
```

---

## 组件详解

### 组件 1：规划器（Planner）

**职责**：将目标分解为可执行的子目标

**输入**：
- 主目标（objective）
- 当前状态（current_state）
- 可用资源（resources）

**输出**：
- 子目标列表（sub_goals）
- 执行计划（plan）

**实现逻辑**：
```python
class Planner:
    """规划器"""

    def plan(self, objective: str, context: Dict) -> Plan:
        """制定执行计划"""

        # 1. 分析目标
        goal_analysis = self._analyze_goal(objective)

        # 2. 分解子目标
        sub_goals = self._decompose_goals(objective, goal_analysis)

        # 3. 确定依赖关系
        dependencies = self._identify_dependencies(sub_goals)

        # 4. 生成执行计划
        plan = {
            "objective": objective,
            "sub_goals": sub_goals,
            "dependencies": dependencies,
            "estimated_steps": len(sub_goals)
        }

        return plan

    def _decompose_goals(self, objective, analysis):
        """分解子目标"""

        prompt = f"""
        目标：{objective}
        复杂度：{analysis['complexity']}
        领域：{analysis['domain']}

        请将这个目标分解为 3-5 个子目标。
        要求：
        1. 每个子目标都应该可独立验证
        2. 子目标之间有逻辑关系
        3. 子目标的完成能够推动主目标的达成

        返回格式：JSON 列表
        """

        response = self.llm.invoke(prompt)
        return parse_sub_goals(response)
```

**规划示例**：
```python
# 目标："构建一个 LangGraph 应用"

# 规划器生成：
plan = {
    "sub_goals": [
        "学习 LangGraph 基础概念",
        "理解状态管理机制",
        "设计应用架构",
        "实现核心功能",
        "测试和优化"
    ],
    "dependencies": {
        "理解状态管理机制": ["学习 LangGraph 基础概念"],
        "设计应用架构": ["理解状态管理机制"],
        "实现核心功能": ["设计应用架构"]
    }
}
```

---

### 组件 2：执行器（Executor）

**职责**：执行具体的子目标

**输入**：
- 当前子目标
- 可用工具
- 历史上下文

**输出**：
- 执行结果
- 新的状态

**实现逻辑**：
```python
class Executor:
    """执行器"""

    def execute(self, sub_goal: str, tools: List[Tool], context: Dict) -> Result:
        """执行子目标"""

        # 1. 理解子目标
        understanding = self._understand_goal(sub_goal, context)

        # 2. 选择工具
        selected_tools = self._select_tools(understanding, tools)

        # 3. 执行任务
        if len(selected_tools) == 1:
            # 单工具直接执行
            result = self._execute_with_tool(sub_goal, selected_tools[0])
        else:
            # 多工具使用 Agent
            result = self._execute_with_agent(sub_goal, selected_tools)

        # 4. 验证结果
        if self._validate_result(result, sub_goal):
            return Result(success=True, data=result)
        else:
            # 执行失败，尝试其他方法
            return self._retry_with_alternative(sub_goal, tools)

    def _execute_with_agent(self, goal, tools):
        """使用 Agent 执行"""

        # 创建 ReAct Agent
        agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            verbose=True
        )

        # 执行
        response = agent.invoke({"input": goal})

        return response["output"]
```

---

### 组件 3：反思器（Reflector）

**职责**：评估执行结果，反思并调整策略

**输入**：
- 原始目标
- 执行结果
- 执行历史

**输出**：
- 反思报告
- 调整建议

**实现逻辑**：
```python
class Reflector:
    """反思器"""

    def reflect(self, objective: str, execution: Dict) -> Reflection:
        """反思执行结果"""

        # 1. 评估完成度
        completeness = self._assess_completeness(
            objective,
            execution["result"]
        )

        # 2. 识别问题
        issues = self._identify_issues(execution)

        # 3. 分析原因
        root_causes = self._analyze_root_causes(issues)

        # 4. 生成建议
        suggestions = self._generate_suggestions(root_causes)

        # 5. 决定下一步
        if completeness >= 0.9:
            next_action = "finish"
        elif issues and completeness < 0.5:
            next_action = "replan"
        else:
            next_action = "continue"

        return Reflection(
            completeness=completeness,
            issues=issues,
            suggestions=suggestions,
            next_action=next_action
        )

    def _assess_completeness(self, objective, result):
        """评估完成度"""

        prompt = f"""
        目标：{objective}
        结果：{result}

        请评估结果的完成度（0.0-1.0）。
        考虑因素：
        1. 是否回答了目标的问题
        2. 信息是否完整
        3. 质量是否满足要求

        只返回一个数字（如 0.85）
        """

        response = self.llm.invoke(prompt)
        return float(response.strip())
```

---

### 组件 4：记忆系统（Memory System）

**职责**：存储和检索历史经验

**分层结构**：
```
┌──────────────────────────────────────┐
│      工作记忆（Working Memory）       │
│  - 当前任务上下文                      │
│  - 最近的几轮思考                      │
│  - 临时变量                           │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│      短期记忆（Short-term）           │
│  - 当前会话的所有任务                  │
│  - 执行结果                           │
│  - 反思记录                           │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│      长期记忆（Long-term）            │
│  - 向量数据库存储                     │
│  - 历史经验                           │
│  - 成功和失败的模式                    │
└──────────────────────────────────────┘
```

**实现逻辑**：
```python
class MemorySystem:
    """记忆系统"""

    def __init__(self):
        self.working_memory = {}  # 工作记忆
        self.short_term = []  # 短期记忆
        self.long_term = VectorStore()  # 长期记忆

    def store(self, key, value, memory_type="short_term"):
        """存储信息"""

        if memory_type == "working":
            self.working_memory[key] = value
        elif memory_type == "short_term":
            self.short_term.append({"key": key, "value": value})
        elif memory_type == "long_term":
            # 向量化存储
            embedding = self.embed(value)
            self.long_term.add(embedding, {"key": key, "value": value})

    def retrieve(self, query, top_k=5):
        """检索信息"""

        # 1. 先查工作记忆
        if query in self.working_memory:
            return [self.working_memory[query]]

        # 2. 查短期记忆
        short_term_results = [
            item for item in self.short_term
            if query.lower() in str(item["value"]).lower()
        ]

        # 3. 查长期记忆
        long_term_results = self.long_term.similarity_search(
            self.embed(query),
            k=top_k
        )

        # 4. 合并结果
        return short_term_results + long_term_results
```

---

### 组件 5：工具集（Tools）

**常用工具类型**：

| 类型 | 示例 | 用途 |
|------|------|------|
| **搜索** | Google Search, Wikipedia | 搜索信息 |
| **文件** | Read File, Write File | 文件操作 |
| **代码** | Execute Python, Review Code | 代码执行和审查 |
| **网页** | Browse Website, Scrape Web | 网页浏览和抓取 |
| **数据处理** | Analyze Data, Visualize | 数据分析 |

**工具定义示例**：
```python
from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """搜索网络信息"""
    # 实现搜索逻辑
    pass

@tool
def read_file(file_path: str) -> str:
    """读取文件内容"""
    with open(file_path, 'r') as f:
        return f.read()

@tool
def execute_python(code: str) -> str:
    """执行 Python 代码"""
    try:
        result = eval(code)
        return f"执行结果：{result}"
    except Exception as e:
        return f"错误：{str(e)}"
```

---

## 完整工作流程

### 循环流程

```
开始
  │
  ▼
┌─────────────────┐
│  1. 接收目标     │
│  "构建 LangGraph │
│   应用"         │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  2. 规划         │
│  - 分解子目标    │
│  - 确定依赖      │
│  - 生成计划      │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  3. 执行子目标1  │
│  "学习基础概念"  │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  4. 反思         │
│  - 评估完成度    │
│  - 识别问题      │
│  - 生成建议      │
└─────────────────┘
  │
  ├─ 完成度高 ──> 下一个子目标
  │
  └─ 完成度低 ──> 调整策略 ──> 重新规划
                          │
                          ▼
                    ┌─────────────────┐
                    │  5. 调整后执行   │
                    │  "换种方式学习"  │
                    └─────────────────┘
                          │
                          ▼
                    ...（循环直到目标达成）
```

---

## 关键设计决策

### 决策 1：何时重新规划

**触发条件**：
1. 执行失败率 > 50%
2. 发现与目标冲突的新信息
3. 完成度长期停滞
4. 用户要求调整

**重新规划策略**：
```python
def should_replan(reflection, execution_history):
    """判断是否需要重新规划"""

    # 条件 1：失败率高
    recent_failures = [
        e for e in execution_history[-5:]
        if e["status"] == "failed"
    ]
    if len(recent_failures) / 5 > 0.5:
        return True, "失败率过高"

    # 条件 2：完成度停滞
    if is_stagnant(execution_history):
        return True, "完成度停滞"

    # 条件 3：反思建议重新规划
    if reflection.next_action == "replan":
        return True, reflection.reason

    return False, "继续执行"
```

---

### 决策 2：如何平衡自主性与可控性

**自主性风险**：
- 可能偏离用户目标
- 可能产生不可控行为
- 可能浪费资源

**可控性措施**：
1. **目标边界**：明确设定可执行范围
2. **审批机制**：关键决策需要用户确认
3. **资源限制**：设置最大步数和成本上限
4. **安全检查**：验证操作的安全性

**示例**：
```python
class SafeExecutor:
    """安全的执行器"""

    def __init__(self):
        self.max_steps = 20
        self.budget_limit = 10.0  # 美元
        self.approval_required = True

    def execute(self, task, tools):
        """安全执行"""

        # 检查步数
        if self.step_count >= self.max_steps:
            raise Exception("已达到最大步数限制")

        # 检查预算
        if self.estimated_cost(task) > self.budget_limit:
            raise Exception(f"超出预算限制：${self.budget_limit}")

        # 关键操作需要审批
        if self.is_critical_operation(task):
            if not self.get_user_approval(task):
                raise Exception("用户未批准")

        # 执行任务
        return self._do_execute(task, tools)
```

---

## 最小验证

### 验证目标
- ✅ 理解 AutoGPT 的五大组件
- ✅ 能够对比 BabyAGI 和 AutoGPT
- ✅ 理解规划-执行-反思循环

### 验证步骤
1. 阅读本笔记，理解 AutoGPT 的架构
2. 对比 BabyAGI 和 AutoGPT 的异同
3. 思考在什么场景下应该使用 AutoGPT

### 预期输出
能够回答以下问题：
1. AutoGPT 的五大组件是什么？
2. AutoGPT 与 BabyAGI 的主要区别是什么？
3. 什么时候需要重新规划？
4. 如何平衡自主性与可控性？

---

## 常见错误

### 错误 1：过度规划

**问题**：规划过于详细，缺乏灵活性

**解决**：采用渐进式规划，先粗后细

---

### 错误 2：反思流于形式

**问题**：反思只是简单判断，没有深入分析

**解决**：设计详细的反思维度和标准

---

### 错误 3：忽略成本

**问题**：频繁的规划和反思导致成本过高

**解决**：设置循环上限，优化提示词

---

## 下一步

- 📖 `notes/03_goal_decomposition.md` - 目标分解详解
- 🧪 `examples/02_autogpt_agent.py` - AutoGPT 示例代码
- ✏ `exercises/01_basic_exercises.md` - 基础练习题

---

**记住：AutoGPT 就像一个经验丰富的项目经理，能够规划全局、动态调整、深度反思！** 🎯🤖
