# 01. 架构练习题 - Level 1

> **练习类型**: 架构设计题  
> **题数**: 30 个  
> **预计时间**: 45 分钟  
> **目标**: 测试你对单一 Agent 架构的理解

---

## 📊 练习统计

- **总题数**: 30 题
- **选择题**: 15 题
- **设计题**: 15 题
- **预计时间**: 45 分钟

---

## 🎯 单选题（1-15）

### 第 1 部分：单一 Agent 架构（1-8）

**Q1. 单一 Agent 架构的组件不包括：**

A. LLM（大语言模型）
B. Tools（工具）
C. Memory（记忆）
D. Database（数据库）

**答案**: D

**Q2. ReAct 循环的四个阶段不包括：**

A. 思考
B. 行动
C. 观察
D. 编译

**答案**: D

**Q3. 工具（Tool）的作用不包括：**

A. 扩展能力
B. 提高效率
C. 提高准确性
D. 替代 LLM

**答案**: D

**Q4. 记忆（Memory）的作用不包括：**

A. 存储历史
B. 支持推理
C. 提供个性化服务
D. 自动生成代码

**答案**: D

**Q5. 错误处理和重试机制不包括：**

A. 异常捕获
B. 错误分类
C. 重试机制
D. 自动修复

**答案**: D

**Q6. 状态管理的类型不包括：**

A. 短期状态
B. 中期状态
C. 长期状态
D. 永久状态

**答案**: D

**Q7. 工具开发的最佳实践不包括：**

A. 明确的输入和输出
B. 清晰的描述
C. 错误处理
D. 尽可能多的功能

**答案**: D

**Q8. 代码直觉的培养方法不包括：**

A. 多读代码
B. 多写代码
C. 多思考代码
D. 记忆代码

**答案**: D

---

### 第 2 部分：单元测试与 Mock（9-15）

**Q9. 单元测试的作用不包括：**

A. 验证功能
B. 发现缺陷
C. 提高信心
D. 替代集成测试

**答案**: D

**Q10. pytest 的特点不包括：**

A. 简单易用
B. 插件丰富
C. 支持并行执行
D. 自动生成代码

**答案**: D

**Q11. Mock 的作用不包括：**

A. 隔离测试
B. 控制行为
C. 验证调用
D. 替代真实对象

**答案**: D

**Q12. Stub 的作用不包括：**

A. 简化依赖
B. 快速返回
C. 验证调用
D. 控制输出

**答案**: C

**Q13. Mock 和 Stub 的主要区别是：**

A. Mock 可以验证调用，Stub 不能
B. Stub 可以验证调用，Mock 不能
C. Mock 和 Stub 没有区别
D. Mock 和 Stub 都不能验证调用

**答案**: A

**Q14. 测试覆盖率的目标是：**

A. 50%
B. 70%
C. 90%
D. 100%

**答案**: B

**Q15. 测试驱动开发（TDD）的步骤是：**

A. 编码 → 测试 → 重构
B. 测试 → 编码 → 重构
C. 重构 → 编码 → 测试
D. 编码 → 重构 → 测试

**答案**: B

---

## 🎯 设计题（16-30）

### 第 1 部分：架构设计（16-23）

**Q16. 设计一个搜索 Agent 的架构**

**要求**：
- 有一个搜索工具
- 有一个记忆系统
- 能够记录用户的搜索历史
- 能够根据历史记录推荐相关内容

**答案**:
```python
# 架构设计
class SearchAgent:
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI()
        
        # 工具
        self.search_tool = Tool(
            name="search",
            func=self.search,
            description="搜索关键词"
        )
        
        # 记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[self.search_tool]
        )
    
    def search(self, query: str) -> str:
        """搜索"""
        # 实现搜索逻辑
        pass
    
    def get_recommendations(self) -> List[str]:
        """根据历史记录推荐相关内容"""
        history = self.memory.load_memory_variables({})
        # 实现推荐逻辑
        pass
```

---

**Q17. 设计一个计算 Agent 的架构**

**要求**：
- 有一个计算工具
- 有一个历史记录
- 能够记录计算历史
- 能够重复执行之前的计算

**答案**:
```python
# 架构设计
class CalculatorAgent:
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI()
        
        # 工具
        self.calculator_tool = Tool(
            name="calculator",
            func=self.calculate,
            description="计算数学表达式"
        )
        
        # 历史记录
        self.history = []
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[self.calculator_tool]
        )
    
    def calculate(self, expression: str) -> str:
        """计算"""
        result = eval(expression)
        self.history.append({
            "expression": expression,
            "result": result,
            "timestamp": datetime.now()
        })
        return str(result)
    
    def replay_calculation(self, index: int) -> str:
        """重复执行之前的计算"""
        if index < len(self.history):
            calculation = self.history[index]
            return self.calculate(calculation["expression"])
        return "索引超出范围"
```

---

**Q18. 设计一个天气查询 Agent 的架构**

**要求**：
- 有一个天气工具
- 有一个缓存系统
- 能够缓存天气查询结果
- 能够设置缓存过期时间

**答案**:
```python
# 架构设计
class WeatherAgent:
    def __init__(self, cache_ttl: int = 3600):
        # LLM
        self.llm = ChatOpenAI()
        
        # 工具
        self.weather_tool = Tool(
            name="weather",
            func=self.get_weather,
            description="查询天气"
        )
        
        # 缓存
        self.cache = {}
        self.cache_ttl = cache_ttl
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[self.weather_tool]
        )
    
    def get_weather(self, city: str) -> str:
        """查询天气（带缓存）"""
        # 检查缓存
        if city in self.cache:
            cached_data = self.cache[city]
            if time.time() - cached_data["timestamp"] < self.cache_ttl:
                return cached_data["data"]
        
        # 查询天气
        result = self._query_weather_api(city)
        
        # 更新缓存
        self.cache[city] = {
            "data": result,
            "timestamp": time.time()
        }
        
        return result
    
    def _query_weather_api(self, city: str) -> str:
        """查询天气 API"""
        # 实现 API 调用
        pass
```

---

**Q19. 设计一个带错误处理的 Agent**

**要求**：
- 能够捕获所有异常
- 能够记录错误日志
- 能够提供友好的错误提示
- 能够自动重试失败的任务

**答案**:
```python
# 架构设计
class ErrorHandlingAgent:
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI()
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[]
        )
        
        # 错误处理器
        self.error_handler = ErrorHandler()
    
    def execute_with_retry(self, task: str, max_retries: int = 3):
        """执行任务，带重试机制"""
        retry_count = 0
        delay = 1
        
        while retry_count < max_retries:
            try:
                result = self.agent.invoke({"input": task})
                return result["output"]
            except Exception as e:
                self.error_handler.log_error(e)
                retry_count += 1
                
                if retry_count < max_retries:
                    time.sleep(delay)
                    delay *= 2  # 指数退避
        
        return f"任务失败，已重试 {max_retries} 次"


class ErrorHandler:
    """错误处理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_error(self, error: Exception):
        """记录错误"""
        self.logger.error(f"发生错误：{str(error)}")
    
    def get_friendly_message(self, error: Exception) -> str:
        """获取友好的错误提示"""
        if isinstance(error, ConnectionError):
            return "网络连接错误，请检查网络连接"
        elif isinstance(error, TimeoutError):
            return "请求超时，请稍后重试"
        else:
            return "发生未知错误，请稍后重试"
```

---

**Q20. 设计一个带日志的 Agent**

**要求**：
- 能够记录所有工具调用
- 能够记录所有中间步骤
- 能够生成详细的执行日志
- 能够导出日志到文件

**答案**:
```python
# 架构设计
class LoggingAgent:
    def __init__(self, log_file: str = "agent.log"):
        # LLM
        self.llm = ChatOpenAI()
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[]
        )
        
        # 日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.FileHandler(log_file))
        self.logger.setLevel(logging.INFO)
    
    def invoke(self, input: str):
        """调用 Agent（带日志记录）"""
        self.logger.info(f"输入：{input}")
        
        result = self.agent.invoke({"input": input})
        
        # 记录中间步骤
        if "intermediate_steps" in result:
            self.logger.info(f"中间步骤：{result['intermediate_steps']}")
        
        # 记录输出
        self.logger.info(f"输出：{result['output']}")
        
        return result
```

---

**Q21. 设计一个多工具 Agent 的架构**

**要求**：
- 有至少 3 个工具
- 有工具路由策略
- 能够根据任务选择合适的工具
- 能够记录工具使用统计

**答案**:
```python
# 架构设计
class MultiToolAgent:
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI()
        
        # 工具
        self.tools = [
            Tool(name="search", func=self.search, description="搜索"),
            Tool(name="calculator", func=self.calculate, description="计算"),
            Tool(name="weather", func=self.get_weather, description="天气")
        ]
        
        # 工具路由器
        self.router = ToolRouter(self.tools)
        
        # 工具使用统计
        self.usage_stats = {tool.name: 0 for tool in self.tools}
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools
        )
    
    def route(self, query: str) -> str:
        """路由到合适的工具"""
        tool_name = self.router.route(query)
        if tool_name:
            self.usage_stats[tool_name] += 1
        return tool_name
    
    def get_usage_stats(self) -> Dict[str, int]:
        """获取工具使用统计"""
        return self.usage_stats.copy()


class ToolRouter:
    """工具路由器"""
    
    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}
    
    def route(self, query: str) -> Optional[str]:
        """路由到合适的工具"""
        query_lower = query.lower()
        
        if "搜索" in query_lower or "search" in query_lower:
            return "search"
        elif "计算" in query_lower or "calculate" in query_lower:
            return "calculator"
        elif "天气" in query_lower or "weather" in query_lower:
            return "weather"
        
        return None
```

---

**Q22. 设计一个带记忆的对话 Agent**

**要求**：
- 有一个对话历史
- 有一个用户上下文
- 能够记住用户的偏好
- 能够提供个性化服务

**答案**:
```python
# 架构设计
class ConversationalAgent:
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI()
        
        # 记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 用户上下文
        self.user_context = {
            "preferences": {},
            "history": [],
            "intentions": []
        }
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[]
        )
    
    def remember_preference(self, key: str, value: str):
        """记住用户偏好"""
        self.user_context["preferences"][key] = value
    
    def get_preference(self, key: str) -> Optional[str]:
        """获取用户偏好"""
        return self.user_context["preferences"].get(key)
    
    def invoke(self, input: str):
        """调用 Agent（带记忆）"""
        result = self.agent.invoke({
            "input": input,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        })
        
        # 保存上下文
        self.memory.save_context(
            {"input": input},
            {"output": result["output"]}
        )
        
        return result
```

---

**Q23. 设计一个带状态管理的 Agent**

**要求**：
- 有一个状态机
- 有状态转换逻辑
- 能够记录状态变化
- 能够根据状态执行不同的行为

**答案**:
```python
# 架构设计
class StatefulAgent:
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI()
        
        # 状态机
        self.state = "idle"
        self.state_history = []
        
        # Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[]
        )
    
    def transition(self, new_state: str):
        """状态转换"""
        old_state = self.state
        self.state = new_state
        self.state_history.append({
            "old_state": old_state,
            "new_state": new_state,
            "timestamp": datetime.now()
        })
    
    def execute_based_on_state(self, input: str):
        """根据状态执行不同的行为"""
        if self.state == "idle":
            return self._execute_idle(input)
        elif self.state == "processing":
            return self._execute_processing(input)
        elif self.state == "error":
            return self._execute_error(input)
    
    def _execute_idle(self, input: str):
        """idle 状态的行为"""
        self.transition("processing")
        return self.agent.invoke({"input": input})
    
    def _execute_processing(self, input: str):
        """processing 状态的行为"""
        result = self.agent.invoke({"input": input})
        self.transition("idle")
        return result
    
    def _execute_error(self, input: str):
        """error 状态的行为"""
        self.transition("idle")
        return "发生错误，已恢复"
```

---

### 第 2 部分：测试设计（24-30）

**Q24. 设计一个搜索工具的单元测试**

**要求**：
- 测试正常情况
- 测试边界条件
- 测试异常情况

**答案**:
```python
def test_search_tool():
    """测试搜索工具"""
    # 测试正常情况
    result = search_tool("langchain")
    assert "LangChain" in result
    
    # 测试边界条件
    result = search_tool("")
    assert "未找到" in result
    
    # 测试异常情况
    result = search_tool("nonexistent")
    assert "未找到" in result
```

---

**Q25. 设计一个计算工具的单元测试**

**要求**：
- 测试基本运算
- 测试复杂表达式
- 测试异常表达式

**答案**:
```python
def test_calculator_tool():
    """测试计算工具"""
    # 测试基本运算
    result = calculator_tool("1 + 1")
    assert "2" in result
    
    # 测试复杂表达式
    result = calculator_tool("(1 + 2) * 3")
    assert "9" in result
    
    # 测试异常表达式
    result = calculator_tool("1 / 0")
    assert "失败" in result
```

---

**Q26. 设计一个 Agent 的集成测试**

**要求**：
- 测试 Agent 的完整流程
- 测试工具调用
- 测试记忆系统

**答案**:
```python
def test_agent_integration():
    """测试 Agent 集成"""
    # 创建 Agent
    agent = create_agent()
    
    # 测试完整流程
    result = agent.invoke({"input": "搜索 LangChain"})
    assert result["output"] is not None
    
    # 测试工具调用
    assert "intermediate_steps" in result
    
    # 测试记忆系统
    history = agent.memory.load_memory_variables({})
    assert len(history["chat_history"]) > 0
```

---

**Q27. 设计一个 Mock 对象用于测试**

**要求**：
- 模拟搜索工具
- 模拟错误情况
- 验证调用次数

**答案**:
```python
def test_search_tool_with_mock():
    """测试搜索工具（使用 Mock）"""
    from unittest.mock import Mock
    
    # 创建 Mock 对象
    mock_search = Mock(return_value="Mock 搜索结果")
    
    # 替换真实工具
    original_search_tool = search_tool
    search_tool = mock_search
    
    # 调用工具
    result = search_tool("test")
    
    # 验证结果
    assert result == "Mock 搜索结果"
    
    # 验证调用
    mock_search.assert_called_once_with("test")
    
    # 恢复真实工具
    search_tool = original_search_tool
```

---

**Q28. 设计一个测试用例测试错误处理**

**要求**：
- 模拟错误
- 验证错误日志
- 验证重试机制

**答案**:
```python
def test_error_handling():
    """测试错误处理"""
    from unittest.mock import Mock, patch
    
    # 创建 Mock 对象（模拟错误）
    mock_tool = Mock(side_effect=Exception("模拟错误"))
    
    # 创建带错误处理的 Agent
    agent = ErrorHandlingAgent()
    
    # 测试错误处理
    result = agent.execute_with_retry("test", max_retries=3)
    
    # 验证结果
    assert "失败" in result
    
    # 验证重试次数
    assert mock_tool.call_count == 3
```

---

**Q29. 设计一个测试用例测试工具路由**

**要求**：
- 测试路由逻辑
- 测试所有工具
- 测试边界条件

**答案**:
```python
def test_tool_routing():
    """测试工具路由"""
    # 创建工具路由器
    tools = [
        Tool(name="search", func=lambda x: x, description="搜索"),
        Tool(name="calculator", func=lambda x: x, description="计算"),
        Tool(name="weather", func=lambda x: x, description="天气")
    ]
    router = ToolRouter(tools)
    
    # 测试路由逻辑
    assert router.route("搜索 LangChain") == "search"
    assert router.route("计算 1 + 1") == "calculator"
    assert router.route("查询天气") == "weather"
    
    # 测试边界条件
    assert router.route("未知查询") is None
```

---

**Q30. 设计一个测试用例测试记忆系统**

**要求**：
- 测试记忆保存
- 测试记忆加载
- 测试记忆清理

**答案**:
```python
def test_memory_system():
    """测试记忆系统"""
    # 创建记忆系统
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # 测试记忆保存
    memory.save_context(
        {"input": "test"},
        {"output": "result"}
    )
    
    # 测试记忆加载
    vars = memory.load_memory_variables({})
    assert len(vars["chat_history"]) == 2
    
    # 测试记忆清理
    memory.clear()
    vars = memory.load_memory_variables({})
    assert len(vars["chat_history"]) == 0
```

---

## 🎯 核心要点总结

### 单一 Agent 架构

| 组件 | 作用 | 类比 |
|------|------|------|
| **LLM** | 提供推理和生成能力 | 大脑 |
| **Tools** | 提供执行特定任务的能力 | 技能 |
| **Memory** | 提供存储和检索历史信息的能力 | 记忆 |
| **State** | 提供状态管理的能力 | 工作笔记 |
| **Error Handler** | 提供错误处理和重试的能力 | 容错能力 |
| **Logger** | 提供日志记录的能力 | 日记 |

### 工具开发

| 步骤 | 说明 |
|------|------|
| **定义函数** | 定义工具的函数（输入、输出、描述）|
| **创建 Tool** | 使用 Tool 类创建工具对象 |
| **注册到 Agent** | 将工具注册到 Agent 中 |

### 单元测试

| 技术 | 说明 |
|------|------|
| **pytest** | 自动化测试工具 |
| **Mock** | 模拟对象，用于隔离测试 |
| **Stub** | 简化的实现，用于快速返回 |

---

## 📊 练习总结

### 统计信息

- **选择题**: 15 题
- **设计题**: 15 题
- **总计**: 30 题

### 难度分布

- ⭐ 简单: 10 题 (1-10)
- ⭐⭐ 中等: 10 题 (11-20)
- ⭐⭐⭐ 困难: 10 题 (21-30)

### 预计时间

- 快速完成: 30 分钟
- 仔细完成: 45 分钟
- 深入思考: 60 分钟

---

## 🎯 完成标准

当你完成以下所有项，就说明架构练习达标了：

- [ ] 完成 15 道选择题
- [ ] 完成 15 道设计题
- [ ] 正确率 >= 80%
- [ ] 能够设计单一 Agent 架构
- [ ] 能够设计工具开发方案
- [ ] 能够设计测试用例

---

**继续学习**: `exercises/02_practice_exercises.md` - 实践练习题 🚀
