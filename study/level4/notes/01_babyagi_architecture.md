# 01. BabyAGI 架构详解

> **目标**: 理解 BabyAGI 的核心架构和工作原理
> **预计时间**: 50 分钟
> **难度**: ⭐⭐⭐ 中高级
> **前置**: 已阅读 00_autonomous_agent_intro.md

---

## 什么是 BabyAGI？

### 定义

**BabyAGI** 是一个由 [Yohei Nakajima](https://twitter.com/yoheinakajima) 创建的**任务驱动的自主 Agent**，通过不断生成新任务、执行任务、存储结果的循环，来实现自主目标达成。

> **类比**：BabyAGI 就像一个"**专注的实习生**"，它会：
> 1. 接收一个目标
> 2. 列出需要做的事情（任务列表）
> 3. 按优先级逐个完成
> 4. 根据完成情况调整后续任务
> 5. 循环直到目标达成

---

## 核心架构

### 四大组件

```
┌─────────────────────────────────────────────────────────┐
│                    BabyAGI 架构                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │ 1. 任务   │ -> │ 2. 优先级 │ -> │ 3. 执行   │         │
│  │   生成   │    │   排序   │    │   任务   │         │
│  └──────────┘    └──────────┘    └──────────┘         │
│       │                                │               │
│       │                               ┌┴┐              │
│       └──────────────────────────────┤存储│◄────┐     │
│                                      └───┘     │     │
│                                                │     │
│  ┌────────────────────────────────────────────┘     │
│  │                                                 │
│  ▼                                                 │
│┌──────────┐                                        │
││ 4. 结果  │ ──────────────────────────────────────┘
││  存储   │
│└──────────┘
│                                                      │
│              循环执行直到目标达成                     │
└──────────────────────────────────────────────────────┘
```

---

## 组件详解

### 组件 1：任务生成（Task Creation）

**职责**：根据目标和已有结果，生成新的任务

**输入**：
- 用户目标（objective）
- 已完成的结果（result）
- 任务描述（task_description）
- 当前任务列表（task_list）

**输出**：
- 新的任务列表

**实现逻辑**：
```python
def task_creation(
    objective: str,
    result: Dict,
    task_description: str,
    task_list: List[Task]
) -> List[Task]:
    """创建新任务"""

    # 1. 构建提示词
    prompt = f"""
    你是一个任务创建专家。你的目标是：{objective}

    已完成的任务：
    {result['description']}

    当前任务列表：
    {[task.name for task in task_list]}

    请根据以下标准创建新任务：
    1. 任务应该能够帮助我们接近目标
    2. 任务应该具体且可执行
    3. 任务应该不重复已有任务
    4. 最多创建 3 个新任务

    返回格式：JSON 列表
    """

    # 2. 调用 LLM 生成任务
    response = llm.invoke(prompt)
    new_tasks = parse_tasks(response)

    return new_tasks
```

**示例**：
```python
# 目标："学习 LangGraph 并构建一个应用"

# 第 1 轮：初始任务
tasks = [
    Task("搜索 LangGraph 基础概念"),
    Task("搜索 LangGraph 快速入门教程"),
    Task("搜索 LangGraph 示例代码")
]

# 执行 "搜索 LangGraph 基础概念" 后
result = "LangGraph 是一个用于构建有状态、多参与者应用器的框架..."

# 第 2 轮：生成新任务
new_tasks = task_creation(objective, result, "...", tasks)
# 可能生成：
# [
#     Task("深入理解 LangGraph 的状态管理"),
#     Task("学习 LangGraph 的节点和边概念"),
#     Task("搜索 LangGraph 实战项目案例")
# ]
```

---

### 组件 2：优先级排序（Prioritization）

**职责**：根据任务的重要性和紧迫性排序

**输入**：
- 当前任务列表
- 最近完成的任务
- 目标描述

**输出**：
- 排序后的任务列表

**实现逻辑**：
```python
def prioritization_agent(
    task_list: List[Task],
    current_task: Task,
    objective: str
) -> List[Task]:
    """任务优先级排序"""

    # 1. 构建提示词
    prompt = f"""
    你是一个任务优先级管理专家。目标：{objective}

    当前任务列表：
    {format_tasks(task_list)}

    最近完成的任务：
    {current_task.name}

    请重新排序这些任务，考虑以下因素：
    1. 任务对目标的重要性
    2. 任务之间的依赖关系
    3. 任务的紧迫性

    返回排序后的任务列表（编号 1-N）
    """

    # 2. 调用 LLM 排序
    response = llm.invoke(prompt)
    prioritized_tasks = parse_prioritized_tasks(response)

    return prioritized_tasks
```

**排序策略**：
- **依赖性优先**：被其他任务依赖的任务优先
- **重要性优先**：对目标贡献大的任务优先
- **紧迫性优先**：时效性强的任务优先

---

### 组件 3：任务执行（Execution）

**职责**：执行排序后的第一个任务

**输入**：
- 待执行的任务
- 可用的工具列表

**输出**：
- 执行结果

**实现逻辑**：
```python
def execution_agent(
    task: Task,
    tools: List[Tool]
) -> Dict:
    """执行任务"""

    # 1. 构建执行提示
    prompt = f"""
    你是一个任务执行专家。请执行以下任务：

    任务：{task.name}
    描述：{task.description}

    可用工具：
    {format_tools(tools)}

    请使用工具完成这个任务，并返回结果。
    """

    # 2. 创建带工具的 Agent
    agent = create_react_agent(llm, tools)

    # 3. 执行任务
    result = agent.invoke({"input": prompt})

    return {
        "task": task.name,
        "result": result["output"],
        "status": "completed"
    }
```

**执行流程**：
1. 理解任务要求
2. 选择合适的工具
3. 调用工具执行
4. 处理工具返回
5. 生成执行结果

---

### 组件 4：结果存储（Result Storage）

**职责**：存储执行结果，供后续任务参考

**存储内容**：
- 任务描述
- 执行结果
- 执行时间
- 相关元数据

**实现逻辑**：
```python
class ResultStorage:
    """结果存储"""

    def __init__(self):
        # 短期记忆：当前会话的结果
        self.short_term = []

        # 长期记忆：向量数据库
        self.long_term = VectorStore()

    def store(self, result: Dict):
        """存储结果"""

        # 1. 存储到短期记忆
        self.short_term.append(result)

        # 2. 存储到长期记忆（向量化）
        embedding = embed(result["task"] + result["result"])
        self.long_term.add(embedding, result)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """检索相关结果"""

        # 1. 向量化查询
        query_embedding = embed(query)

        # 2. 相似度搜索
        results = self.long_term.similarity_search(
            query_embedding,
            k=top_k
        )

        return results
```

---

## 完整工作流程

### 流程图

```
开始
  │
  ▼
┌─────────────────┐
│  1. 初始化目标    │
│  "学习 LangGraph"│
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  2. 创建初始任务  │
│  - 搜索基础概念   │
│  - 查看文档      │
│  - 找示例代码    │
└─────────────────┘
  │
  ▼
┌─────────────────┐       ┌──────────────┐
│  3. 优先级排序    │ ───> │ Task 1 (最高) │
│  Task 1, 2, 3   │       │ Task 2       │
│                 │       │ Task 3       │
└─────────────────┘       └──────────────┘
  │
  ▼
┌─────────────────┐
│  4. 执行 Task 1 │ ───> 结果1
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  5. 存储结果1    │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  6. 基于结果1    │
│  生成新任务      │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  7. 重新排序所有  │
│  任务（Task 2-5) │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  8. 执行 Task 2 │ ───> 结果2
└─────────────────┘
  │
  ▼
   ...（循环直到目标达成）
```

---

### 伪代码实现

```python
class BabyAGI:
    """BabyAGI 核心逻辑"""

    def __init__(self, objective: str, llm, tools):
        self.objective = objective
        self.llm = llm
        self.tools = tools

        # 初始化组件
        self.task_creator = TaskCreationAgent(llm)
        self.prioritizer = PrioritizationAgent(llm)
        self.executor = ExecutionAgent(llm, tools)
        self.storage = ResultStorage()

        # 初始任务列表
        self.task_list = []

    def run(self, max_iterations: int = 10):
        """运行 BabyAGI"""

        # 1. 创建初始任务
        self.task_list = self.task_creator.create_initial_tasks(
            self.objective
        )

        # 2. 循环执行
        for iteration in range(max_iterations):
            print(f"\n=== 迭代 {iteration + 1} ===")

            # 2.1 优先级排序
            print(f"[1] 排序 {len(self.task_list)} 个任务")
            self.task_list = self.prioritizer.sort_tasks(
                self.task_list,
                self.objective
            )

            # 2.2 执行第一个任务
            print(f"[2] 执行任务: {self.task_list[0].name}")
            result = self.executor.execute(
                self.task_list[0],
                self.storage
            )

            # 2.3 存储结果
            print(f"[3] 存储结果")
            self.storage.store(result)

            # 2.4 生成新任务
            print(f"[4] 生成新任务")
            new_tasks = self.task_creator.create_tasks(
                self.objective,
                result,
                self.task_list
            )
            self.task_list.extend(new_tasks)

            # 2.5 移除已完成的任务
            self.task_list = self.task_list[1:]

            # 2.6 检查是否完成
            if self.is_objective_met():
                print("\n=== 目标达成 ===")
                break

        return self.storage.get_all_results()

    def is_objective_met(self) -> bool:
        """检查目标是否达成"""
        # 简单检查：如果没有任务了，说明完成
        return len(self.task_list) == 0
```

---

## 关键设计决策

### 决策 1：任务生成策略

**问题**：如何避免生成重复或无用的任务？

**解决方案**：
1. **上下文感知**：基于已有结果生成新任务
2. **去重机制**：检查任务是否已存在
3. **质量过滤**：过滤掉不相关的任务

**示例**：
```python
def create_tasks(self, objective, result, existing_tasks):
    """创建新任务（带去重和过滤）"""

    # 1. 生成候选任务
    candidate_tasks = self.llm_generate(objective, result)

    # 2. 去重
    unique_tasks = []
    for task in candidate_tasks:
        if not any(is_similar(task, t) for t in existing_tasks):
            unique_tasks.append(task)

    # 3. 相关性过滤
    relevant_tasks = []
    for task in unique_tasks:
        if is_relevant(task, objective):
            relevant_tasks.append(task)

    return relevant_tasks[:3]  # 最多返回 3 个
```

---

### 决策 2：循环终止条件

**问题**：如何知道目标已经达成？

**方法**：
1. **任务耗尽**：没有新任务生成
2. **用户确认**：询问用户是否满意
3. **质量评估**：评估结果的完整性

**示例**：
```python
def should_stop(self, objective, results):
    """判断是否应该停止"""

    # 方法 1：任务耗尽
    if len(self.task_list) == 0:
        return True, "任务列表为空"

    # 方法 2：用户确认（交互式）
    if self.interactive:
        user_input = input(f"目标「{objective}」是否已完成？(y/n): ")
        if user_input.lower() == 'y':
            return True, "用户确认完成"

    # 方法 3：质量评估
    completeness = self.assess_completeness(objective, results)
    if completeness >= 0.9:
        return True, f"完整度 {completeness:.2f} >= 0.9"

    return False, "继续执行"
```

---

### 决策 3：记忆管理

**问题**：如何高效存储和检索历史结果？

**策略**：
- **向量存储**：用于语义检索
- **近期缓存**：快速访问最近的结果
- **定期清理**：避免存储无限增长

**示例**：
```python
class SmartStorage:
    """智能存储"""

    def __init__(self):
        self.vector_store = ChromaDB()  # 长期记忆
        self.cache = []  # 近期缓存（最多 100 条）

    def store(self, result):
        """存储结果"""

        # 1. 存储到向量数据库
        self.vector_store.add(
            documents=[result["content"]],
            metadatas=[{"task": result["task"]}]
        )

        # 2. 添加到缓存
        self.cache.append(result)

        # 3. 清理旧缓存
        if len(self.cache) > 100:
            self.cache = self.cache[-100:]

    def retrieve(self, query, top_k=3):
        """检索相关结果"""

        # 1. 先查缓存
        cached_results = [
            r for r in self.cache
            if query.lower() in r["task"].lower()
        ]

        if len(cached_results) >= top_k:
            return cached_results[:top_k]

        # 2. 缓存不足，查向量数据库
        return self.vector_store.similarity_search(query, k=top_k)
```

---

## 最小验证

### 验证目标
- ✅ 理解 BabyAGI 的四大组件
- ✅ 能够描述 BabyAGI 的循环流程
- ✅ 理解任务生成和优先级排序的逻辑

### 验证步骤
1. 阅读本笔记，理解 BabyAGI 的架构
2. 画出 BabyAGI 的流程图
3. 思考如何改进 BabyAGI 的某个组件

### 预期输出
能够回答以下问题：
1. BabyAGI 的四大组件是什么？
2. BabyAGI 的工作流程是怎样的？
3. 如何避免生成重复任务？
4. 如何判断目标是否达成？

---

## 常见错误

### 错误 1：任务生成过多

**问题**：每次生成太多任务，导致执行时间过长

**解决**：限制每次生成的任务数量（1-3 个）

---

### 错误 2：优先级排序不合理

**问题**：任务排序没有考虑依赖关系

**解决**：在排序提示词中明确要求考虑依赖关系

---

### 错误 3：结果检索不准确

**问题**：向量检索返回的结果不相关

**解决**：
1. 优化 embedding 模型
2. 改进查询语句
3. 使用混合检索（稠密 + 稀疏）

---

## 下一步

- 📖 `notes/02_autogpt_pattern.md` - AutoGPT 模式详解
- 🧪 `examples/01_babyagi_agent.py` - BabyAGI 示例代码
- ✏ `exercises/01_basic_exercises.md` - 基础练习题

---

**记住：BabyAGI 就像一个专注的实习生，通过不断生成、排序、执行任务，逐步达成目标！** 👶🤖
