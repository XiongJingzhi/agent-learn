# 04. 工具箱最小集练习题 - Level 0

> **对应 Note**: `notes/04_toolbox_minimum_set.md`
> **对应 Example**: `examples/02_agent_with_tools.py`
> **目标**: 测试你对 Agent 工具箱和工具调用的理解

---

## 📊 练习统计

- **总题数**: 25 题
- **选择题**: 10 题
- **填空题**: 5 题
- **简答题**: 5 题
- **代码题**: 5 题
- **预计时间**: 40 分钟

---

## 🎯 选择题（1-10）

### 第 1 部分：工具基础（1-5）

**Q1. Agent 工具箱最小集不包括以下哪种工具？**

A. 搜索工具
B. 计算工具
C. 网络攻击工具
D. 文本处理工具

**答案**: C

---

**Q2. Tool 的核心组成部分是：**

A. 名称、函数、描述
B. 名称、函数、参数
C. 函数、描述、返回值
D. 名称、参数、返回值

**答案**: A

---

**Q3. 工具描述（description）的作用是：**

A. 供开发者阅读
B. 供 LLM 理解工具功能
C. 供用户查看
D. 生成日志

**答案**: B

**解析**: 工具描述会被 LLM 读取，帮助它理解何时以及如何调用工具。

---

**Q4. 以下哪个是好的工具命名？**

A. do_something
B. search_database
C. tool1
D. function_a

**答案**: B

**解析**: 工具名应该清晰描述功能，使用动词+名词的形式。

---

**Q5. 工具函数的输入输出类型应该是：**

A. 字符串 → 字符串
B. 任意 → 任意
C. 字符串 → 任意
D. 任意 → 字符串

**答案**: A

**解析**: LangChain 的 Tool 通常要求输入输出都是字符串类型。

---

### 第 2 部分：工具使用（6-10）

**Q6. Agent 调用工具的时机是：**

A. 接收到用户输入时
B. 完成推理后，根据决策调用
C. 每次都调用所有工具
D. 随机调用

**答案**: B

---

**Q7. 如果工具调用失败，Agent 应该：**

A. 直接报错退出
B. 重试或使用降级方案
C. 忽略错误继续
D. 重复调用直到成功

**答案**: B

---

**Q8. 工具的幂等性是指：**

A. 工具可以被多次调用
B. 多次调用产生相同结果
C. 工具只能调用一次
D. 工具调用需要权限

**答案**: B

---

**Q9. 以下哪个场景适合使用搜索工具？**

A. 计算 1+1
B. 查找 LangChain 文档
C. 获取当前时间
D. 发送邮件

**答案**: B

---

**Q10. 工具箱最小集的设计原则是：**

A. 工具越多越好
B. 包含最常用、最核心的工具
C. 包含所有可能的工具
D. 只包含一个工具

**答案**: B

---

## 🔤 填空题（11-15）

**Q11. LangChain 中创建 Tool 使用的是 _______ 类。**

**答案**: Tool（或 langchain.tools.Tool）

---

**Q12. Tool 的三个必需参数是 name、func 和 _______。**

**答案**: description

---

**Q13. 在 ReAct Agent 中，工具通过 _______ 传递给 Agent。**

**答案**: tools 参数（或 tools 列表）

---

**Q14. 工具调用失败时，应该使用 _______ 或降级策略。**

**答案**: 重试机制（或 retry）

---

**Q15. Agent 通过推理决定调用哪个工具，这个过程叫做 _______。**

**答案**: 工具选择（或 tool selection）

---

## 📝 简答题（16-20）

**Q16. 什么是 Agent 工具箱最小集？**

**答案**: Agent 工具箱最小集是包含最常用、最重要工具的集合，能够解决大部分常见的 Agent 任务。它包括搜索、计算、文本处理、数据查询等核心工具。

---

**Q17. 列举工具箱最小集中的 5 种核心工具。**

**答案**:
1. 搜索工具 - 搜索信息
2. 计算工具 - 数学计算
3. 文本处理工具 - 文本分析
4. 数据查询工具 - 数据库查询
5. API 调用工具 - 调用外部服务

---

**Q18. 为什么工具的描述（description）很重要？**

**答案**:
工具描述会被 LLM 读取，帮助它理解：
1. 工具的功能和用途
2. 何时应该调用这个工具
3. 如何正确使用这个工具
4. 工具的输入输出格式

好的描述能显著提高 Agent 调用工具的准确性。

---

**Q19. 如何设计一个好的工具？**

**答案**:
1. **命名清晰**: 使用动词+名词的形式，如 search_database
2. **描述准确**: 详细说明工具的功能、参数、返回值
3. **单一职责**: 每个工具只做一件事
4. **幂等性**: 相同输入产生相同输出
5. **错误处理**: 处理异常情况并返回友好的错误信息
6. **文档完整**: 包含使用示例和注意事项

---

**Q20. 什么时候应该创建自定义工具？**

**答案**:
1. 需要调用特定的外部 API
2. 需要执行特定的业务逻辑
3. 需要访问特定的数据源
4. 现有工具无法满足需求
5. 需要组合多个操作

---

## 💻 代码题（21-25）

**Q21. 创建一个简单的搜索工具：**

```python
from langchain.tools import Tool

def search_knowledge(query: str) -> str:
    """搜索知识库"""
    knowledge = {
        "LangChain": "LLM 应用开发框架",
        "LangGraph": "状态管理框架"
    }

    # 实现搜索逻辑
    # 你的代码

search_tool = Tool(
    name="______",
    func=search_knowledge,
    description="______"
)
```

**答案**:
```python
from langchain.tools import Tool

def search_knowledge(query: str) -> str:
    """搜索知识库"""
    knowledge = {
        "LangChain": "LLM 应用开发框架",
        "LangGraph": "状态管理框架"
    }

    for key, value in knowledge.items():
        if key.lower() in query.lower():
            return value
    return "未找到相关信息"

search_tool = Tool(
    name="search_knowledge",
    func=search_knowledge,
    description="搜索知识库，查找相关信息。输入：查询关键词"
)
```

---

**Q22. 创建一个计算器工具：**

```python
from langchain.tools import Tool

def calculator(expression: str) -> str:
    """计算数学表达式"""
    # 实现计算逻辑，注意错误处理
    pass

calculator_tool = Tool(
    name="______",
    func=calculator,
    description="______"
)
```

**答案**:
```python
from langchain.tools import Tool

def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        # 注意：eval 有安全风险，生产环境应使用更安全的方法
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"

calculator_tool = Tool(
    name="calculator",
    func=calculator,
    description="计算数学表达式。支持加减乘除。输入：数学表达式，如 '1+1'"
)
```

---

**Q23. 创建一个获取当前时间的工具：**

```python
from langchain.tools import Tool
from datetime import datetime

def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间"""
    # 实现代码
    pass

time_tool = Tool(
    name="get_current_time",
    func=get_current_time,
    description="______"
)
```

**答案**:
```python
from langchain.tools import Tool
from datetime import datetime

def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间"""
    return datetime.now().strftime(format)

time_tool = Tool(
    name="get_current_time",
    func=get_current_time,
    description="获取当前时间。输入：时间格式（可选），默认为 'YYYY-MM-DD HH:MM:SS'"
)
```

---

**Q24. 创建一个带错误处理的工具：**

**要求**:
- 工具名称：send_email
- 功能：发送邮件
- 包含错误处理和重试

**答案**:
```python
from langchain.tools import Tool
import time

def send_email(to: str, subject: str, body: str, max_retries: int = 3) -> str:
    """发送邮件"""
    retry_count = 0

    while retry_count < max_retries:
        try:
            # 模拟发送邮件
            print(f"发送邮件到：{to}")
            print(f"主题：{subject}")
            print(f"正文：{body}")

            # 模拟成功率 70%
            import random
            if random.random() < 0.7:
                return f"邮件已成功发送到 {to}"
            else:
                raise Exception("发送失败")

        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"发送失败，{2**retry_count} 秒后重试...")
                time.sleep(2**retry_count)
            else:
                return f"发送失败：{e}"

email_tool = Tool(
    name="send_email",
    func=lambda x: send_email(**eval(x)),  # 简化示例，实际应更安全
    description="发送邮件。输入：JSON 格式 {to, subject, body}"
)
```

---

**Q25. 创建一个工具组合，包含多个工具：**

**要求**:
1. 搜索工具
2. 计算工具
3. 时间工具

**答案**:
```python
from langchain.tools import Tool
from datetime import datetime

# 搜索工具
def search(query: str) -> str:
    data = {
        "Python": "一种编程语言",
        "JavaScript": "Web 开发语言"
    }
    for key, value in data.items():
        if key.lower() in query.lower():
            return value
    return "未找到"

search_tool = Tool(
    name="search",
    func=search,
    description="搜索关键词，返回相关信息"
)

# 计算工具
def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return f"结果：{result}"
    except:
        return "计算失败"

calculator_tool = Tool(
    name="calculator",
    func=calculate,
    description="计算数学表达式"
)

# 时间工具
def get_time(dummy: str) -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time_tool = Tool(
    name="get_time",
    func=get_time,
    description="获取当前时间"
)

# 工具组合
tools = [search_tool, calculator_tool, time_tool]

# 创建 Agent
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
agent = create_react_agent(llm, tools)
```

---

## 🎯 学习建议

1. **先阅读 note**: `notes/04_toolbox_minimum_set.md`
2. **再运行 example**: `examples/02_agent_with_tools.py`
3. **最后完成练习**: 本练习题

---

## ✅ 完成标准

- [ ] 完成 10 道选择题
- [ ] 完成 5 道填空题
- [ ] 完成 5 道简答题
- [ ] 完成 5 道代码题
- [ ] 正确率 >= 80%
- [ ] 理解工具箱最小集的概念
- [ ] 掌握 Tool 的创建和使用
- [ ] 理解工具描述的重要性

---

**下一练习**: `exercises/05_failure_modes_exercise.md` 🚀
