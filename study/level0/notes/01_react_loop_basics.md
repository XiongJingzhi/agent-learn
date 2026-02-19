# 01. ReAct 循环基础 - Feynman Technique

> **费曼技巧**：如果不能简单解释，说明没有真正理解。  
> **目标**：用简单的语言和类比，解释 ReAct 循环的核心概念。

---

## 🎯 学习目标

通过本章学习，你将能够：

1. ✅ 理解 **ReAct 模式是什么**
2. ✅ 掌握 **ReAct 循环的四个阶段**
3. ✅ 理解 **ReAct 与 Agent 的关系**
4. ✅ 掌握 **如何实现 ReAct 循环**
5. ✅ 能够用简单的语言向"资深开发"解释 ReAct 循环

---

## 📚 核心概念

### 概念 1：ReAct 模式是什么？

> **类比**：就像一个**医生**，他会先**问诊（Reasoning）**，然后根据诊断结果**开药（Action）**，最后观察病情变化（Observation）**，循环直到病愈。

**ReAct 模式的定义**：

ReAct (Reasoning + Acting) 是一个**结合推理和行动的循环模式**，Agent 会循环执行以下四个阶段：

1. **思考（Thought）**：分析当前情况，制定下一步计划
2. **行动（Action）**：执行计划，调用工具或生成回复
3. **观察（Observation）**：观察行动的结果，更新状态
4. **循环（Loop）**：根据观察结果决定是否继续下一轮循环

**核心思想**：推理（Reasoning）和行动（Acting）交替进行，形成循环。

---

### 概念 2：ReAct 循环的四个阶段

#### 阶段 1：思考

> **类比**：就像**思考**下一步该怎么做。

**思考的作用**：
- ✅ 分析当前的状态和信息
- ✅ 理解用户的意图和需求
- ✅ 制定下一步的行动计划

**示例**：
```
Thought: 用户想知道当前的时间，我需要调用获取时间的工具。
```

---

#### 阶段 2：行动

> **类比**：就像**行动**，执行思考中制定的计划。

**行动的作用**：
- ✅ 执行思考中制定的计划
- ✅ 调用工具或生成回复
- ✅ 采取实际行动影响环境

**示例**：
```
Action: GetTime()
Observation: 当前时间是 2026-02-19 02:00:00
```

---

#### 阶段 3：观察

> **类比**：就像**观察**行动的结果。

**观察的作用**：
- ✅ 观察行动的结果
- ✅ 评估行动是否成功
- ✅ 更新 Agent 的状态
- ✅ 决定是否继续循环

**示例**：
```
Observation: 获取时间成功，当前时间是 2026-02-19 02:00:00
```

---

#### 阶段 4：循环

> **类比**：就像**判断**是否需要继续下一步行动。

**循环的作用**：
- ✅ 根据观察结果判断是否完成目标
- ✅ 如果未完成，继续下一轮循环
- ✅ 如果已完成，结束循环

**示例**：
```
Thought: 我已经获取到时间，现在需要生成回复给用户。
Action: GenerateResponse("现在时间是 2026-02-19 02:00:00")
Observation: 回复生成成功。
Thought: 任务完成，结束循环。
```

---

### 概念 3：ReAct 与 Agent 的关系

> **类比**：ReAct 就像 Agent 的**大脑**，控制 Agent 的**思考**和**行动**。

**ReAct 与 Agent 的关系**：

- **ReAct 是 Agent 的大脑**：ReAct 模式是 Agent 的核心控制逻辑
- **ReAct 决定 Agent 的行为**：ReAct 循环决定了 Agent 何时思考、何时行动、何时结束
- **ReAct 控制循环**：ReAct 负责控制整个循环的执行流程
- **ReAct 管理状态**：ReAct 负责在循环中管理 Agent 的状态

**示意图**：
```
Agent
  └─ ReAct 循环 (大脑）
       ├─ Thought (思考）
       ├─ Action (行动)
       ├─ Observation (观察)
       └─ Loop (循环判断)
```

---

### 概念 4：ReAct 循环的实现

#### 伪代码

```python
def react_loop(agent, task):
    """ReAct 循环"""
    
    while not task.completed:
        # 阶段 1：思考
        thought = agent.think(task)
        task.log_thought(thought)
        
        # 阶段 2：行动
        action = agent.decide_action(thought)
        task.log_action(action)
        
        # 阶段 3：观察
        observation = agent.execute_action(action)
        task.log_observation(observation)
        
        # 阶段 4：循环判断
        if task.is_completed(observation):
            task.completed = True
            break
        else:
            # 更新状态
            task.update_state(observation)
    
    return task.result
```

#### 代码示例

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

# 创建工具
def get_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time_tool = Tool(
    name="get_time",
    func=get_time,
    description="获取当前时间"
)

# 创建 LLM
llm = OpenAI(temperature=0)

# 创建 Agent（使用 ReAct 模式）
agent = create_react_agent(
    llm=llm,
    tools=[time_tool],
    verbose=True
)

# 创建执行器（内置 ReAct 循环）
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[time_tool],
    verbose=True,
    max_iterations=10  # 最多循环 10 次
)

# 执行
result = agent_executor.invoke({
    "input": "现在几点了？"
})

# 输出：
# Thought: 用户想知道现在几点，我需要调用获取时间的工具。
# Action: get_time
# Observation: 2026-02-19 02:00:00
# Thought: 我已经获取到时间，现在需要生成回复给用户。
# Action: GenerateResponse("现在时间是 2026-02-19 02:00:00")
# Final Answer: 现在时间是 2026-02-19 02:00:00
```

---

## 🔍 费曼学习检查

### 向"资深开发"解释

**假设你正在向资深开发解释 ReAct 循环，你能这样说吗？**

1. **ReAct 模式是什么？**
   > "ReAct 模式就像一个医生，他会先问诊（Reasoning），然后根据诊断结果开药（Action），最后观察病情变化（Observation），循环直到病愈。"

2. **ReAct 循环的四个阶段是什么？**
   > "ReAct 循环的四个阶段是：思考（分析情况）、行动（执行计划）、观察（观察结果）、循环（判断是否继续）。"

3. **ReAct 与 Agent 的关系是什么？**
   > "ReAct 是 Agent 的大脑，控制 Agent 的思考和行动。ReAct 循环决定了 Agent 何时思考、何时行动、何时结束。"

---

## 🎯 核心要点总结

### ReAct 循环的四个阶段

| 阶段 | 作用 | 类比 |
|------|------|------|
| **思考** | 分析情况、制定计划 | 医生问诊 |
| **行动** | 执行计划、调用工具 | 医生开药 |
| **观察** | 观察结果、更新状态 | 医生观察病情 |
| **循环** | 判断是否继续、结束循环 | 医生判断是否康复 |

### ReAct 与 Agent 的关系

| 关系 | 说明 |
|------|------|
| **大脑** | ReAct 是 Agent 的大脑，控制 Agent 的思考和行为 |
| **控制逻辑** | ReAct 决定 Agent 的行为、循环流程和结束条件 |
| **状态管理** | ReAct 负责在循环中管理 Agent 的状态 |

---

## 🚀 下一步

现在你已经理解了 ReAct 循环的核心概念，让我们继续学习：

- 📖 `notes/02_agent_vs_chatbot.md` - Agent vs Chatbot
- 📖 `notes/03_state_and_feedback.md` - 状态与反馈
- 🧪 `examples/01_simple_react_agent.py` - 简单的 ReAct Agent 示例

---

**记住：ReAct 循环就像医生的问诊流程，思考、行动、观察、循环，直到任务完成！** 🏥
