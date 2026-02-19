# 04. 工具箱最小集 - Feynman Technique

> **费曼技巧**：如果不能简单解释，说明没有真正理解。  
> **目标**：用简单的语言和类比，解释 Agent 的工具箱最小集。

---

## 🎯 学习目标

通过本章学习，你将能够：

1. ✅ 理解 **Agent 工具箱最小集是什么**
2. ✅ 掌握 **核心工具的定义和使用**
3. ✅ 理解 **工具的分类和选择原则**
4. ✅ 掌握 **工具集成的最佳实践**
5. ✅ 能够用简单的语言向"资深开发"解释工具箱

---

## 📚 核心概念

### 概念 1：Agent 工具箱最小集是什么？

> **类比**：Agent 工具箱最小集就像一个**瑞士军刀**，它包含了最常用的工具，可以解决大部分常见问题。

**Agent 工具箱最小集的定义**：

Agent 工具箱最小集是一个**包含最常用、最重要工具的集合**，它能够：

1. ✅ **完成核心任务**：解决大部分常见的 Agent 任务
2. ✅ **保持简单**：工具数量少，易于理解和维护
3. ✅ **易于集成**：工具之间的接口统一，易于集成
4. ✅ **可扩展**：可以轻松添加新的工具

**核心思想**：从最小可用的工具集开始，逐步扩展，而不是一开始就追求大而全。

---

### 概念 2：核心工具的定义和使用

#### 1. 文本处理工具（Text Processing Tool）

> **类比**：文本处理工具就像一个人的**阅读和理解能力**，它可以阅读文本、提取信息、总结内容。

**文本处理工具的作用**：

- ✅ **文本清洗**：去除多余的空格、标点、特殊字符
- ✅ **文本分词**：将文本分割成单词或短语
- ✅ **文本总结**：总结长文本的关键内容
- ✅ **文本提取**：从文本中提取关键信息（如：日期、人名、地点）

**示例**：
```python
from langchain.tools import Tool

def clean_text(text: str) -> str:
    """清洗文本"""
    # 去除多余的空格
    cleaned = " ".join(text.split())
    
    # 去除多余的标点
    cleaned = cleaned.strip(".,!?:;")
    
    return cleaned

# 创建工具
clean_text_tool = Tool(
    name="clean_text",
    func=clean_text,
    description="清洗文本，去除多余的空格和标点"
)

# 使用工具
result = clean_text_tool.run("  Hello, World!  ")
print(result)  # 输出：Hello, World
```

---

#### 2. 数据查询工具（Data Query Tool）

> **类比**：数据查询工具就像一个人的**查询能力**，它可以从数据库、API 或文件中查询数据。

**数据查询工具的作用**：

- ✅ **数据库查询**：从数据库中查询数据
- ✅ **API 调用**：调用外部 API 获取数据
- ✅ **文件读取**：从文件中读取数据
- ✅ **数据过滤**：根据条件过滤数据

**示例**：
```python
from langchain.tools import Tool
import requests

def query_api(query: str) -> str:
    """查询 API（模拟）"""
    # 模拟 API 调用
    results = {
        "LangChain": "LangChain 是一个 LLM 应用开发框架",
        "LangGraph": "LangGraph 是一个状态管理框架",
        "OpenAI": "OpenAI 是一个 AI 研究实验室"
    }
    
    return results.get(query, "未找到相关结果")

# 创建工具
query_tool = Tool(
    name="query_api",
    func=query_api,
    description="查询 API，返回相关信息"
)

# 使用工具
result = query_tool.run("LangChain")
print(result)  # 输出：LangChain 是一个 LLM 应用开发框架
```

---

#### 3. 计算工具（Calculator Tool）

> **类比**：计算工具就像一个人的**计算能力**，它可以进行数学计算、数据转换、统计分析。

**计算工具的作用**：

- ✅ **数学计算**：进行加减乘除等数学计算
- ✅ **数据转换**：将数据从一种格式转换为另一种格式
- ✅ **统计分析**：计算数据的统计信息（如：平均值、中位数、标准差）
- ✅ **数据验证**：验证数据是否符合预期的格式

**示例**：
```python
from langchain.tools import Tool

def calculator(expression: str) -> str:
    """计算器（简化版）"""
    try:
        # 计算表达式（简化：只支持加减乘除）
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except:
        return f"无法计算：{expression}"

# 创建工具
calculator_tool = Tool(
    name="calculator",
    func=calculator,
    description="计算数学表达式（支持加减乘除）"
)

# 使用工具
result = calculator_tool.run("1 + 1")
print(result)  # 输出：计算结果：1 + 1 = 2
```

---

#### 4. 搜索工具（Search Tool）

> **类比**：搜索工具就像一个人的**搜索能力**，它可以从搜索引擎、文档、知识库中搜索信息。

**搜索工具的作用**：

- ✅ **网络搜索**：从搜索引擎（如：Google、Bing）中搜索信息
- ✅ **文档搜索**：从文档中搜索信息
- ✅ **知识库搜索**：从知识库中搜索信息
- ✅ **向量搜索**：基于向量相似度的语义搜索

**示例**：
```python
from langchain.tools import Tool

def search_web(query: str) -> str:
    """网络搜索（模拟）"""
    # 模拟网络搜索
    results = {
        "LangChain": "https://python.langchain.com/",
        "LangGraph": "https://langchain-ai.github.io/langgraph/",
        "OpenAI": "https://platform.openai.com/docs"
    }
    
    return results.get(query, "未找到相关结果")

# 创建工具
search_tool = Tool(
    name="search_web",
    func=search_web,
    description="网络搜索，返回相关信息"
)

# 使用工具
result = search_tool.run("LangChain")
print(result)  # 输出：https://python.langchain.com/
```

---

#### 5. 时间工具（Time Tool）

> **类比**：时间工具就像一个人的**时间感知能力**，它可以获取当前时间、计算时间差、设置定时任务。

**时间工具的作用**：

- ✅ **获取时间**：获取当前时间和日期
- ✅ **时间计算**：计算时间差、时间间隔
- ✅ **时间格式化**：将时间格式化为不同的格式
- ✅ **定时任务**：设置定时任务，在指定时间执行

**示例**：
```python
from langchain.tools import Tool
from datetime import datetime

def get_current_time() -> str:
    """获取当前时间"""
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

# 创建工具
time_tool = Tool(
    name="get_current_time",
    func=get_current_time,
    description="获取当前时间和日期"
)

# 使用工具
result = time_tool.run("")
print(result)  # 输出：2026-02-19 11:27:00
```

---

### 概念 3：工具的分类和选择原则

#### 工具的分类

| 工具类型 | 作用 | 示例 |
|----------|------|------|
| **文本处理工具** | 阅读和理解文本 | 清洗文本、分词、总结、提取 |
| **数据查询工具** | 查询和获取数据 | 数据库查询、API 调用、文件读取 |
| **计算工具** | 计算和分析数据 | 数学计算、数据转换、统计分析 |
| **搜索工具** | 搜索和检索信息 | 网络搜索、文档搜索、向量搜索 |
| **时间工具** | 处理时间和日期 | 获取时间、时间计算、定时任务 |

#### 工具的选择原则

| 原则 | 说明 |
|------|------|
| **最小化原则** | 从最小可用的工具集开始，只添加必需的工具 |
| **实用性原则** | 选择最实用、最常用的工具，避免过度设计 |
| **易用性原则** | 选择简单易用的工具，避免复杂的接口 |
| **可维护性原则** | 选择易于维护的工具，避免复杂的依赖 |
| **可扩展性原则** | 选择易于扩展的工具，便于后续添加新功能 |

---

### 概念 4：工具集成的最佳实践

#### 1. 工具注册表

> **类比**：工具注册表就像一个**工具清单**，它记录了所有可用的工具及其说明。

**工具注册表的作用**：

- ✅ **集中管理**：集中管理所有工具
- ✅ **易于查找**：可以快速找到需要的工具
- ✅ **易于扩展**：可以轻松添加新的工具
- ✅ **易于维护**：可以轻松删除或修改工具

**示例**：
```python
# 工具注册表
tool_registry = {
    "text_processing": {
        "clean_text": clean_text_tool,
        "split_text": split_text_tool,
        "summarize_text": summarize_text_tool
    },
    "data_query": {
        "query_api": query_tool,
        "read_file": read_file_tool,
        "query_database": query_database_tool
    },
    "calculator": {
        "calculator": calculator_tool,
        "statistics": statistics_tool,
        "data_conversion": data_conversion_tool
    },
    "search": {
        "search_web": search_web_tool,
        "search_documents": search_documents_tool,
        "vector_search": vector_search_tool
    },
    "time": {
        "get_current_time": time_tool,
        "calculate_time_diff": calculate_time_diff_tool,
        "schedule_task": schedule_task_tool
    }
}

# 使用工具
tool = tool_registry["text_processing"]["clean_text"]
result = tool.run("  Hello, World!  ")
print(result)  # 输出：Hello, World
```

---

#### 2. 工具路由

> **类比**：工具路由就像一个**工具调度员**，它根据任务的需求，选择最合适的工具。

**工具路由的作用**：

- ✅ **智能选择**：根据任务的需求，智能选择最合适的工具
- ✅ **负载均衡**：在多个相同功能的工具之间负载均衡
- ✅ **容错处理**：如果一个工具失败，自动切换到另一个工具
- ✅ **性能优化**：根据工具的性能，选择最优的工具

**示例**：
```python
def route_tool(task: str, tool_registry: dict) -> Tool:
    """工具路由"""
    # 解析任务
    task_type = parse_task_type(task)
    
    # 根据任务类型选择工具
    if task_type == "clean_text":
        category = "text_processing"
        tool_name = "clean_text"
    elif task_type == "query_api":
        category = "data_query"
        tool_name = "query_api"
    elif task_type == "calculate":
        category = "calculator"
        tool_name = "calculator"
    elif task_type == "search":
        category = "search"
        tool_name = "search_web"
    elif task_type == "get_time":
        category = "time"
        tool_name = "get_current_time"
    else:
        raise ValueError(f"Unknown task type: {task_type}")
    
    # 获取工具
    tool = tool_registry[category][tool_name]
    
    return tool

# 使用工具路由
task = "清理文本：  Hello, World!  "
tool = route_tool(task, tool_registry)
result = tool.run("  Hello, World!  ")
print(result)  # 输出：Hello, World
```

---

#### 3. 工具组合

> **类比**：工具组合就像**搭积木**，可以将多个工具组合成更复杂的工具。

**工具组合的作用**：

- ✅ **功能增强**：组合多个工具，实现更复杂的功能
- ✅ **流程优化**：优化工具的执行流程，提高效率
- ✅ **错误处理**：组合多个工具的错误处理逻辑
- ✅ **可重用性**：将工具组合封装成可重用的组件

**示例**：
```python
def clean_and_summarize(text: str) -> str:
    """清理并总结文本"""
    # 步骤 1：清理文本
    cleaned = clean_text_tool.run(text)
    
    # 步骤 2：总结文本
    summarized = summarize_text_tool.run(cleaned)
    
    return summarized

# 创建组合工具
clean_and_summarize_tool = Tool(
    name="clean_and_summarize",
    func=clean_and_summarize,
    description="清理文本并总结关键内容"
)

# 使用组合工具
text = "  Hello, World! This is a test.  "
result = clean_and_summarize_tool.run(text)
print(result)  # 输出：Hello World This is a test
```

---

## 🔍 费曼学习检查

### 向"资深开发"解释

**假设你正在向资深开发解释 Agent 的工具箱最小集，你能这样说吗？**

1. **Agent 工具箱最小集是什么？**
   > "Agent 工具箱最小集就像一个瑞士军刀，它包含了最常用的工具，可以解决大部分常见的 Agent 任务。工具包括：文本处理工具、数据查询工具、计算工具、搜索工具、时间工具。"

2. **核心工具有哪些？**
   > "核心工具有：文本处理工具（阅读和理解文本）、数据查询工具（查询和获取数据）、计算工具（计算和分析数据）、搜索工具（搜索和检索信息）、时间工具（处理时间和日期）。"

3. **如何选择工具？**
   > "工具的选择原则有：最小化原则（只添加必需的工具）、实用性原则（选择最实用的工具）、易用性原则（选择简单易用的工具）、可维护性原则（选择易于维护的工具）、可扩展性原则（选择易于扩展的工具）。"

4. **如何集成工具？**
   > "工具集成的方法有：工具注册表（集中管理所有工具）、工具路由（智能选择最合适的工具）、工具组合（组合多个工具实现更复杂的功能）。"

---

## 🎯 核心要点总结

### 核心工具

| 工具 | 作用 | 示例 |
|------|------|------|
| **文本处理工具** | 阅读和理解文本 | 清洗文本、分词、总结、提取 |
| **数据查询工具** | 查询和获取数据 | 数据库查询、API 调用、文件读取 |
| **计算工具** | 计算和分析数据 | 数学计算、数据转换、统计分析 |
| **搜索工具** | 搜索和检索信息 | 网络搜索、文档搜索、向量搜索 |
| **时间工具** | 处理时间和日期 | 获取时间、时间计算、定时任务 |

### 工具选择原则

| 原则 | 说明 |
|------|------|
| **最小化** | 从最小可用的工具集开始 |
| **实用性** | 选择最实用的工具 |
| **易用性** | 选择简单易用的工具 |
| **可维护性** | 选择易于维护的工具 |
| **可扩展性** | 选择易于扩展的工具 |

### 工具集成方法

| 方法 | 说明 | 示例 |
|------|------|------|
| **工具注册表** | 集中管理所有工具 | `tool_registry` |
| **工具路由** | 智能选择最合适的工具 | `route_tool` |
| **工具组合** | 组合多个工具 | `clean_and_summarize` |

---

## 🚀 下一步

现在你已经理解了 Agent 的工具箱最小集，让我们继续学习：

- 📖 `notes/05_failure_modes_basics.md` - 失败模式基础
- 📖 `notes/06_environment_check_guide.md` - 环境检查指南
- 🧪 `examples/01_simple_react_agent.py` - 简单的 ReAct Agent 示例
- ✏ `exercises/00_concept_check.md` - 概念检查练习题

---

**记住：Agent 工具箱最小集就像瑞士军刀，包含了最常用的工具，可以解决大部分常见任务！** 🛠
