# 02. 实践练习题 - Level 1

> **练习类型**: 代码实现题、代码重构题、代码优化题  
> **题数**: 30 个  
> **预计时间**: 60 分钟  
> **目标**: 提升你的代码实现、重构和优化能力

---

## 📊 练习统计

- **总题数**: 30 题
- **代码实现题**: 15 题
- **代码重构题**: 10 题
- **代码优化题**: 5 题
- **预计时间**: 60 分钟

---

## 🎯 代码实现题（1-15）

### 第 1 部分：基础实现（1-8）

**Q1. 实现一个简单的搜索工具**

**要求**:
- 输入：查询字符串
- 输出：搜索结果
- 处理异常情况

**答案**:
```python
def search_tool(query: str) -> str:
    """搜索工具"""
    if not query:
        return "查询不能为空"
    
    # 模拟搜索
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架",
        "langgraph": "LangGraph 是一个状态管理框架",
        "openai": "OpenAI 是一个 AI 研究实验室"
    }
    
    for key, value in results.items():
        if query.lower() in key.lower():
            return value
    
    return f"未找到与 '{query}' 相关的结果"
```

---

**Q2. 实现一个计算工具**

**要求**:
- 输入：数学表达式
- 输出：计算结果
- 处理异常情况

**答案**:
```python
def calculator_tool(expression: str) -> str:
    """计算工具"""
    try:
        # 安全计算
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("表达式包含非法字符")
        
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算失败：{str(e)}"
```

---

**Q3. 实现一个天气工具**

**要求**:
- 输入：城市名
- 输出：天气信息
- 使用缓存

**答案**:
```python
def weather_tool(city: str) -> str:
    """天气工具（带缓存）"""
    # 模拟天气数据
    weather_map = {
        "北京": "北京今天天气晴，气温 25℃",
        "上海": "上海今天天气多云，气温 28℃",
        "广州": "广州今天天气雨，气温 26℃"
    }
    
    if city in weather_map:
        return weather_map[city]
    
    return f"抱歉，我们还没有 '{city}' 的天气信息。"
```

---

**Q4. 实现一个时间工具**

**要求**:
- 无输入
- 输出：当前时间
- 格式化输出

**答案**:
```python
from datetime import datetime

def time_tool(query: str = "") -> str:
    """时间工具"""
    now = datetime.now()
    return f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"
```

---

**Q5. 实现一个简单的 Agent**

**要求**:
- 使用 ChatOpenAI
- 集成一个工具
- 实现基本对话

**答案**:
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# 创建 LLM
llm = ChatOpenAI(temperature=0.7)

# 创建工具
def hello_tool(query: str) -> str:
    """打招呼工具"""
    return f"你好，{query}！"

tools = [Tool(name="hello", func=hello_tool, description="打招呼")]

# 创建 Agent
agent = create_react_agent(llm=llm, tools=tools)

# 创建执行器
executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)

# 执行
result = executor.invoke({"input": "你好，世界！"})
print(result["output"])
```

---

**Q6. 实现一个带记忆的 Agent**

**要求**:
- 使用 ConversationBufferMemory
- 保存对话历史
- 加载对话历史

**答案**:
```python
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 保存对话
memory.save_context(
    {"input": "我叫张三"},
    {"output": "你好，张三！"}
)

# 加载对话
vars = memory.load_memory_variables({})
print(vars["chat_history"])
```

---

**Q7. 实现一个带错误处理的 Agent**

**要求**:
- 捕获所有异常
- 记录错误日志
- 提供友好提示

**答案**:
```python
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_with_error_handling(agent, input: str) -> str:
    """执行 Agent，带错误处理"""
    try:
        result = agent.invoke({"input": input})
        return result["output"]
    except Exception as e:
        logger.error(f"发生错误：{e}")
        return f"抱歉，发生错误：{str(e)}"
```

---

**Q8. 实现一个带日志的 Agent**

**要求**:
- 记录所有工具调用
- 记录中间步骤
- 导出日志到文件

**答案**:
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='agent.log'
)
logger = logging.getLogger(__name__)

def execute_with_logging(agent, input: str):
    """执行 Agent，带日志记录"""
    logger.info(f"输入：{input}")
    
    result = agent.invoke({"input": input})
    
    # 记录中间步骤
    if "intermediate_steps" in result:
        logger.info(f"中间步骤：{result['intermediate_steps']}")
    
    logger.info(f"输出：{result['output']}")
    
    return result
```

---

### 第 2 部分：高级实现（9-15）

**Q9. 实现一个工具路由器**

**要求**:
- 根据查询内容路由到合适的工具
- 支持至少 3 个工具
- 记录路由统计

**答案**:
```python
from typing import Dict, Optional

class ToolRouter:
    """工具路由器"""
    
    def __init__(self, tools: Dict[str, callable]):
        self.tools = tools
        self.usage_stats = {name: 0 for name in tools.keys()}
    
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
    
    def execute(self, query: str) -> str:
        """执行路由和工具调用"""
        tool_name = self.route(query)
        if tool_name and tool_name in self.tools:
            self.usage_stats[tool_name] += 1
            return self.tools[tool_name](query)
        
        return "未找到合适的工具"
    
    def get_usage_stats(self) -> Dict[str, int]:
        """获取使用统计"""
        return self.usage_stats.copy()
```

---

**Q10. 实现一个带缓存的工具**

**要求**:
- 缓存工具结果
- 设置缓存过期时间
- 自动清理过期缓存

**答案**:
```python
import time
from typing import Dict, Optional

class CachedTool:
    """带缓存的工具"""
    
    def __init__(self, tool_func, ttl: int = 3600):
        self.tool_func = tool_func
        self.cache = {}
        self.ttl = ttl
    
    def execute(self, input: str) -> str:
        """执行工具（带缓存）"""
        # 检查缓存
        if input in self.cache:
            cached_data = self.cache[input]
            if time.time() - cached_data["timestamp"] < self.ttl:
                return cached_data["data"]
        
        # 执行工具
        result = self.tool_func(input)
        
        # 更新缓存
        self.cache[input] = {
            "data": result,
            "timestamp": time.time()
        }
        
        return result
    
    def clear_cache(self):
        """清理缓存"""
        self.cache.clear()
```

---

**Q11. 实现一个带重试机制的执行器**

**要求**:
- 自动重试失败的任务
- 使用指数退避
- 设置最大重试次数

**答案**:
```python
import time

def execute_with_retry(func, max_retries: int = 3, backoff_factor: int = 2):
    """执行函数，带重试机制"""
    retry_count = 0
    delay = 1
    
    while retry_count < max_retries:
        try:
            return func()
        except Exception as e:
            retry_count += 1
            
            if retry_count < max_retries:
                time.sleep(delay)
                delay *= backoff_factor
            else:
                raise e
```

---

**Q12. 实现一个多工具 Agent**

**要求**:
- 集成至少 3 个工具
- 实现工具路由
- 记录工具使用统计

**答案**:
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# 创建工具
tools = [
    Tool(name="search", func=search_tool, description="搜索"),
    Tool(name="calculator", func=calculator_tool, description="计算"),
    Tool(name="weather", func=weather_tool, description="天气")
]

# 创建 LLM
llm = ChatOpenAI(temperature=0.7)

# 创建 Agent
agent = create_react_agent(llm=llm, tools=tools)

# 创建执行器
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10
)

# 执行
result = executor.invoke({"input": "搜索 LangChain，然后计算 1 + 1"})
print(result["output"])
```

---

**Q13. 实现一个状态机**

**要求**:
- 定义状态
- 定义状态转换
- 根据状态执行不同的行为

**答案**:
```python
from typing import Dict, List
from datetime import datetime

class StateMachine:
    """状态机"""
    
    def __init__(self):
        self.state = "idle"
        self.state_history = []
        self.transitions = {
            "idle": ["processing"],
            "processing": ["idle", "error"],
            "error": ["idle"]
        }
    
    def transition(self, new_state: str) -> bool:
        """状态转换"""
        if new_state in self.transitions[self.state]:
            old_state = self.state
            self.state = new_state
            self.state_history.append({
                "old_state": old_state,
                "new_state": new_state,
                "timestamp": datetime.now()
            })
            return True
        return False
    
    def execute(self, action: str):
        """根据状态执行行为"""
        if self.state == "idle":
            print(f"Idle 状态：{action}")
        elif self.state == "processing":
            print(f"Processing 状态：{action}")
        elif self.state == "error":
            print(f"Error 状态：{action}")
```

---

**Q14. 实现一个对话历史管理器**

**要求**:
- 保存对话历史
- 查询对话历史
- 清理对话历史

**答案**:
```python
from typing import List, Dict
from datetime import datetime

class ConversationHistory:
    """对话历史管理器"""
    
    def __init__(self, max_history: int = 100):
        self.history: List[Dict] = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        }
        self.history.append(message)
        
        # 限制历史记录数量
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_history(self, count: int = 10) -> List[Dict]:
        """获取历史记录"""
        return self.history[-count:]
    
    def clear_history(self):
        """清理历史记录"""
        self.history.clear()
```

---

**Q15. 实现一个完整的 Agent 框架**

**要求**:
- 集成 LLM、工具、记忆、日志
- 支持错误处理和重试
- 支持状态管理

**答案**:
```python
class AgentFramework:
    """完整的 Agent 框架"""
    
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI(temperature=0.7)
        
        # 工具
        self.tools = []
        
        # 记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 日志
        self.logger = logging.getLogger(__name__)
        
        # 状态
        self.state = "idle"
    
    def add_tool(self, tool: Tool):
        """添加工具"""
        self.tools.append(tool)
    
    def execute(self, input: str) -> str:
        """执行 Agent"""
        try:
            # 创建 Agent
            agent = create_react_agent(
                llm=self.llm,
                tools=self.tools
            )
            
            # 创建执行器
            executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                memory=self.memory,
                verbose=False
            )
            
            # 执行
            result = executor.invoke({"input": input})
            
            # 保存对话
            self.memory.save_context(
                {"input": input},
                {"output": result["output"]}
            )
            
            return result["output"]
        
        except Exception as e:
            self.logger.error(f"执行失败：{e}")
            return f"执行失败：{str(e)}"
```

---

## 🎯 代码重构题（16-25）

### 重构原则

- ✅ 提高可读性
- ✅ 提高可维护性
- ✅ 消除重复代码
- ✅ 提高代码复用性

---

**Q16. 重构重复代码**

**原始代码**:
```python
def search_tool(query: str) -> str:
    if not query:
        return "查询不能为空"
    # 搜索逻辑
    pass

def calculator_tool(expression: str) -> str:
    if not expression:
        return "表达式不能为空"
    # 计算逻辑
    pass

def weather_tool(city: str) -> str:
    if not city:
        return "城市不能为空"
    # 天气逻辑
    pass
```

**重构后的代码**:
```python
def validate_input(input: str, error_msg: str) -> bool:
    """验证输入"""
    if not input:
        raise ValueError(error_msg)
    return True

def search_tool(query: str) -> str:
    """搜索工具"""
    validate_input(query, "查询不能为空")
    # 搜索逻辑
    pass

def calculator_tool(expression: str) -> str:
    """计算工具"""
    validate_input(expression, "表达式不能为空")
    # 计算逻辑
    pass

def weather_tool(city: str) -> str:
    """天气工具"""
    validate_input(city, "城市不能为空")
    # 天气逻辑
    pass
```

---

**Q17. 重构长函数**

**原始代码**:
```python
def process_data(data: str) -> str:
    # 清洗数据
    cleaned = data.strip()
    # 转换数据
    converted = cleaned.lower()
    # 验证数据
    if not converted:
        raise ValueError("数据不能为空")
    # 处理数据
    processed = converted.replace(" ", "_")
    # 返回数据
    return processed
```

**重构后的代码**:
```python
def clean_data(data: str) -> str:
    """清洗数据"""
    return data.strip()

def convert_data(data: str) -> str:
    """转换数据"""
    return data.lower()

def validate_data(data: str):
    """验证数据"""
    if not data:
        raise ValueError("数据不能为空")

def process_data(data: str) -> str:
    """处理数据"""
    cleaned = clean_data(data)
    converted = convert_data(cleaned)
    validate_data(converted)
    return converted.replace(" ", "_")
```

---

**Q18. 重构条件语句**

**原始代码**:
```python
def get_tool_name(query: str) -> str:
    if "search" in query.lower():
        return "search"
    elif "calculate" in query.lower():
        return "calculator"
    elif "weather" in query.lower():
        return "weather"
    else:
        return "unknown"
```

**重构后的代码**:
```python
TOOL_KEYWORDS = {
    "search": ["search", "搜索"],
    "calculator": ["calculate", "计算"],
    "weather": ["weather", "天气"]
}

def get_tool_name(query: str) -> str:
    """获取工具名称"""
    query_lower = query.lower()
    for tool_name, keywords in TOOL_KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            return tool_name
    return "unknown"
```

---

**Q19. 重构重复的异常处理**

**原始代码**:
```python
def tool1(input: str) -> str:
    try:
        # 工具逻辑
        return result
    except Exception as e:
        logger.error(f"Tool1 错误：{e}")
        return f"Tool1 失败：{str(e)}"

def tool2(input: str) -> str:
    try:
        # 工具逻辑
        return result
    except Exception as e:
        logger.error(f"Tool2 错误：{e}")
        return f"Tool2 失败：{str(e)}"
```

**重构后的代码**:
```python
def execute_with_error_handling(tool_func, tool_name: str, *args, **kwargs):
    """执行工具，带错误处理"""
    try:
        return tool_func(*args, **kwargs)
    except Exception as e:
        logger.error(f"{tool_name} 错误：{e}")
        return f"{tool_name} 失败：{str(e)}"

def tool1(input: str) -> str:
    """工具 1"""
    return execute_with_error_handling(_tool1_logic, "Tool1", input)

def tool2(input: str) -> str:
    """工具 2"""
    return execute_with_error_handling(_tool2_logic, "Tool2", input)
```

---

**Q20. 重构硬编码的值**

**原始代码**:
```python
def search_tool(query: str) -> str:
    results = {
        "langchain": "LangChain 是一个 LLM 应用开发框架",
        "langgraph": "LangGraph 是一个状态管理框架"
    }
    # 搜索逻辑
    pass
```

**重构后的代码**:
```python
SEARCH_RESULTS = {
    "langchain": "LangChain 是一个 LLM 应用开发框架",
    "langgraph": "LangGraph 是一个状态管理框架"
}

def search_tool(query: str) -> str:
    """搜索工具"""
    for key, value in SEARCH_RESULTS.items():
        if query.lower() in key.lower():
            return value
    return "未找到结果"
```

---

**Q21. 重构重复的日志记录**

**原始代码**:
```python
def tool1(input: str) -> str:
    logger.info(f"Tool1 输入：{input}")
    result = process(input)
    logger.info(f"Tool1 输出：{result}")
    return result

def tool2(input: str) -> str:
    logger.info(f"Tool2 输入：{input}")
    result = process(input)
    logger.info(f"Tool2 输出：{result}")
    return result
```

**重构后的代码**:
```python
def log_execution(tool_name: str, input: str, output: str):
    """记录执行日志"""
    logger.info(f"{tool_name} 输入：{input}")
    logger.info(f"{tool_name} 输出：{output}")

def tool1(input: str) -> str:
    """工具 1"""
    result = process(input)
    log_execution("Tool1", input, result)
    return result

def tool2(input: str) -> str:
    """工具 2"""
    result = process(input)
    log_execution("Tool2", input, result)
    return result
```

---

**Q22. 重构复杂的类**

**原始代码**:
```python
class Agent:
    def __init__(self):
        self.llm = ChatOpenAI()
        self.tools = []
        self.memory = ConversationBufferMemory()
        self.logger = logging.getLogger()
        self.state = "idle"
    
    def execute(self, input: str):
        # 所有逻辑都在这里
        pass
```

**重构后的代码**:
```python
class AgentConfig:
    """Agent 配置"""
    def __init__(self):
        self.llm = ChatOpenAI()
        self.tools = []
        self.memory = ConversationBufferMemory()
        self.logger = logging.getLogger()

class AgentState:
    """Agent 状态"""
    def __init__(self):
        self.state = "idle"
        self.history = []

class Agent:
    """Agent"""
    def __init__(self):
        self.config = AgentConfig()
        self.state = AgentState()
    
    def execute(self, input: str) -> str:
        """执行 Agent"""
        return self._execute_logic(input)
```

---

**Q23. 重构全局变量**

**原始代码**:
```python
counter = 0

def increment():
    global counter
    counter += 1
    return counter

def decrement():
    global counter
    counter -= 1
    return counter
```

**重构后的代码**:
```python
class Counter:
    """计数器"""
    def __init__(self, initial: int = 0):
        self._count = initial
    
    def increment(self) -> int:
        """递增"""
        self._count += 1
        return self._count
    
    def decrement(self) -> int:
        """递减"""
        self._count -= 1
        return self._count

counter = Counter()
```

---

**Q24. 重构重复的类型检查**

**原始代码**:
```python
def process_string(value):
    if not isinstance(value, str):
        raise TypeError("必须是字符串")
    # 处理逻辑
    pass

def process_int(value):
    if not isinstance(value, int):
        raise TypeError("必须是整数")
    # 处理逻辑
    pass
```

**重构后的代码**:
```python
def validate_type(value, expected_type, type_name: str):
    """验证类型"""
    if not isinstance(value, expected_type):
        raise TypeError(f"必须是{type_name}")

def process_string(value: str):
    """处理字符串"""
    validate_type(value, str, "字符串")
    # 处理逻辑
    pass

def process_int(value: int):
    """处理整数"""
    validate_type(value, int, "整数")
    # 处理逻辑
    pass
```

---

**Q25. 重构深度嵌套**

**原始代码**:
```python
def process(data):
    if data:
        if "value" in data:
            if isinstance(data["value"], str):
                if data["value"].strip():
                    return data["value"].strip().lower()
    return None
```

**重构后的代码**:
```python
def process(data) -> Optional[str]:
    """处理数据"""
    if not data:
        return None
    
    value = data.get("value")
    if not isinstance(value, str):
        return None
    
    value = value.strip()
    if not value:
        return None
    
    return value.lower()
```

---

## 🎯 代码优化题（26-30）

### 优化原则

- ✅ 提高性能
- ✅ 减少内存使用
- ✅ 提高响应速度
- ✅ 优化算法

---

**Q26. 优化循环**

**原始代码**:
```python
def find_duplicate(items: list) -> Optional[str]:
    """查找重复项"""
    for i, item1 in enumerate(items):
        for j, item2 in enumerate(items):
            if i != j and item1 == item2:
                return item1
    return None
```

**优化后的代码**:
```python
def find_duplicate(items: list) -> Optional[str]:
    """查找重复项（优化版）"""
    seen = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None
```

**性能提升**: O(n²) → O(n)

---

**Q27. 优化字符串拼接**

**原始代码**:
```python
def build_string(parts: List[str]) -> str:
    """构建字符串"""
    result = ""
    for part in parts:
        result += part
    return result
```

**优化后的代码**:
```python
def build_string(parts: List[str]) -> str:
    """构建字符串（优化版）"""
    return "".join(parts)
```

**性能提升**: 减少内存分配

---

**Q28. 优化列表操作**

**原始代码**:
```python
def get_unique_items(items: list) -> list:
    """获取唯一项"""
    unique = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique
```

**优化后的代码**:
```python
def get_unique_items(items: list) -> list:
    """获取唯一项（优化版）"""
    return list(set(items))
```

**性能提升**: O(n²) → O(n)

---

**Q29. 优化缓存使用**

**原始代码**:
```python
def expensive_calculation(x: int) -> int:
    """昂贵的计算"""
    # 每次都重新计算
    return x * x * x

def process(data: List[int]) -> List[int]:
    """处理数据"""
    return [expensive_calculation(x) for x in data]
```

**优化后的代码**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_calculation(x: int) -> int:
    """昂贵的计算（带缓存）"""
    return x * x * x

def process(data: List[int]) -> List[int]:
    """处理数据"""
    return [expensive_calculation(x) for x in data]
```

**性能提升**: 避免重复计算

---

**Q30. 优化数据库查询**

**原始代码**:
```python
def get_user_orders(user_id: int) -> List[Dict]:
    """获取用户订单"""
    orders = []
    # N+1 查询问题
    for order in db.query("SELECT * FROM orders WHERE user_id = ?", user_id):
        order_items = db.query(
            "SELECT * FROM order_items WHERE order_id = ?",
            order["id"]
        )
        order["items"] = order_items
        orders.append(order)
    return orders
```

**优化后的代码**:
```python
def get_user_orders(user_id: int) -> List[Dict]:
    """获取用户订单（优化版）"""
    # 一次查询获取所有订单和订单项
    results = db.query("""
        SELECT o.*, oi.* 
        FROM orders o 
        LEFT JOIN order_items oi ON o.id = oi.order_id 
        WHERE o.user_id = ?
    """, user_id)
    
    # 整理结果
    orders = {}
    for row in results:
        order_id = row["id"]
        if order_id not in orders:
            orders[order_id] = {
                "id": order_id,
                "user_id": row["user_id"],
                "items": []
            }
        if row["item_id"]:
            orders[order_id]["items"].append({
                "id": row["item_id"],
                "name": row["item_name"]
            })
    
    return list(orders.values())
```

**性能提升**: N+1 查询 → 1 次查询

---

## 🎯 核心要点总结

### 代码实现

| 类型 | 说明 |
|------|------|
| **基础实现** | 基本功能实现 |
| **高级实现** | 集成多个组件 |

### 代码重构

| 原则 | 说明 |
|------|------|
| **可读性** | 代码易于理解 |
| **可维护性** | 代码易于修改 |
| **复用性** | 代码可重复使用 |

### 代码优化

| 方向 | 说明 |
|------|------|
| **性能** | 提高执行速度 |
| **内存** | 减少内存使用 |
| **算法** | 选择更优算法 |

---

## 📊 练习总结

### 统计信息

- **代码实现题**: 15 题
- **代码重构题**: 10 题
- **代码优化题**: 5 题
- **总计**: 30 题

### 难度分布

- ⭐ 简单: 10 题 (1-10)
- ⭐⭐ 中等: 10 题 (11-20)
- ⭐⭐⭐ 困难: 10 题 (21-30)

### 预计时间

- 快速完成: 45 分钟
- 仔细完成: 60 分钟
- 深入思考: 90 分钟

---

## 🎯 完成标准

当你完成以下所有项，就说明实践练习达标了：

- [ ] 完成 15 道代码实现题
- [ ] 完成 10 道代码重构题
- [ ] 完成 5 道代码优化题
- [ ] 正确率 >= 80%
- [ ] 能够编写高质量的代码
- [ ] 能够重构和优化代码

---

**完成练习！** 🎉  
**继续学习**: `projects/01_single_agent_project.md` - 单一 Agent 项目 🚀
