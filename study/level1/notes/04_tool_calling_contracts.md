# 工具调用契约

> **目标**: 理解工具定义、参数校验、返回结构、错误编码
> **预计时间**: 30 分钟
> **前置**: 已完成节点设计学习

---

## 为什么需要工具调用契约？

工具（Tool）是 Agent 与外部世界交互的接口，良好的契约设计能够：
- **保证调用安全**：参数校验防止错误调用
- **提高可维护性**：统一的返回结构易于处理
- **简化错误处理**：明确的错误编码易于诊断

**类比**：工具调用契约就像**API 文档**，明确定义了输入、输出和错误。

---

## 工具定义契约

### 契约 1：函数签名

工具函数必须有明确的类型提示。

```python
from typing import Optional, List, Dict

# 好的工具定义：明确的类型
def good_search_tool(
    query: str,
    max_results: int = 10,
    filters: Optional[Dict] = None
) -> Dict[str, any]:
    """
    搜索工具

    Args:
        query: 搜索关键词（必需）
        max_results: 最大结果数（默认 10）
        filters: 过滤条件（可选）

    Returns:
        Dict: {
            'results': List[Dict],  # 搜索结果
            'count': int,           # 结果数量
            'query': str            # 搜索词
        }

    Raises:
        ValueError: 参数无效
    """
    pass

# 不好的工具定义：类型不明确
def bad_search_tool(query, max_results, filters):
    pass
```

---

### 契约 2：参数校验

工具必须校验输入参数。

```python
def validated_search_tool(query: str, max_results: int = 10) -> Dict:
    """带参数校验的搜索工具"""

    # 校验 1：必需参数
    if not query:
        raise ValueError("query 不能为空")

    # 校验 2：参数类型
    if not isinstance(query, str):
        raise TypeError("query 必须是字符串")

    if not isinstance(max_results, int):
        raise TypeError("max_results 必须是整数")

    # 校验 3：参数范围
    if max_results < 1 or max_results > 100:
        raise ValueError("max_results 必须在 1-100 之间")

    # 执行搜索
    results = search(query, max_results)

    return results
```

---

### 契约 3：返回结构

工具应该返回统一的结构。

```python
def standardized_tool(input: str) -> Dict:
    """标准化的返回结构"""
    try:
        result = process(input)

        # 成功返回
        return {
            "success": True,
            "data": result,
            "error": None,
            "metadata": {
                "timestamp": time.time(),
                "processing_time": 0.1
            }
        }
    except Exception as e:
        # 错误返回
        return {
            "success": False,
            "data": None,
            "error": str(e),
            "metadata": {
                "timestamp": time.time()
            }
        }
```

---

## 错误编码契约

### 编码方案

使用统一的错误编码格式。

```python
# 定义错误编码
class ErrorCode:
    INVALID_PARAM = "INVALID_PARAM"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    TIMEOUT = "TIMEOUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"

def tool_with_error_codes(input: str) -> Dict:
    """带错误编码的工具"""
    try:
        # 校验参数
        if not input:
            return {
                "success": False,
                "error_code": ErrorCode.INVALID_PARAM,
                "error_message": "input 不能为空"
            }

        # 执行逻辑
        result = process(input)

        return {
            "success": True,
            "data": result
        }

    except PermissionError:
        return {
            "success": False,
            "error_code": ErrorCode.PERMISSION_DENIED,
            "error_message": "权限不足"
        }

    except TimeoutError:
        return {
            "success": False,
            "error_code": ErrorCode.TIMEOUT,
            "error_message": "请求超时"
        }

    except Exception as e:
        return {
            "success": False,
            "error_code": ErrorCode.INTERNAL_ERROR,
            "error_message": str(e)
        }
```

---

## LangChain Tool 定义

### 基础 Tool 定义

```python
from langchain.tools import Tool

def search_function(query: str) -> str:
    """搜索函数"""
    # 实现
    return f"搜索结果: {query}"

# 创建 Tool
search_tool = Tool(
    name="search",                    # 工具名称
    func=search_function,             # 工具函数
    description="搜索关键词，返回相关信息"  # 工具描述
)
```

---

### 带 schema 的 Tool 定义

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """搜索输入"""
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=10, description="最大结果数")

def search_function(query: str, max_results: int = 10) -> str:
    """搜索函数"""
    return f"搜索 {query}，返回 {max_results} 个结果"

# 创建带 schema 的 Tool
search_tool = StructuredTool.from_function(
    func=search_function,
    name="search",
    description="搜索关键词",
    args_schema=SearchInput
)
```

---

## 完整示例：工具集合

```python
from typing import Dict, Optional
from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel, Field

# ===== 工具 1：搜索工具 =====

class SearchInput(BaseModel):
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=5, ge=1, le=20)

def search_tool_func(query: str, max_results: int = 5) -> Dict:
    """搜索工具"""
    results = {
        "langchain": "LangChain 是一个 LLM 应用框架",
        "langgraph": "LangGraph 是一个状态管理框架",
        "openai": "OpenAI 是一个 AI 研究实验室"
    }

    filtered = {k: v for k, v in results.items() if query.lower() in k.lower()}

    return {
        "success": True,
        "results": list(filtered.values())[:max_results],
        "count": len(filtered)
    }

search_tool = StructuredTool.from_function(
    func=search_tool_func,
    name="search",
    description="搜索关键词，返回相关信息",
    args_schema=SearchInput
)

# ===== 工具 2：计算工具 =====

class CalculatorInput(BaseModel):
    expression: str = Field(description="数学表达式")

def calculator_tool_func(expression: str) -> Dict:
    """计算工具"""
    try:
        # 安全校验
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            raise ValueError("表达式包含非法字符")

        result = eval(expression)

        return {
            "success": True,
            "result": result,
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }

calculator_tool = StructuredTool.from_function(
    func=calculator_tool_func,
    name="calculator",
    description="计算数学表达式",
    args_schema=CalculatorInput
)

# ===== 工具 3：天气工具 =====

class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")

def weather_tool_func(city: str) -> Dict:
    """天气工具"""
    weather_data = {
        "北京": "晴天，25℃",
        "上海": "多云，28℃",
        "广州": "雨天，26℃"
    }

    if city in weather_data:
        return {
            "success": True,
            "city": city,
            "weather": weather_data[city]
        }
    else:
        return {
            "success": False,
            "error": f"未找到城市: {city}"
        }

weather_tool = StructuredTool.from_function(
    func=weather_tool_func,
    name="weather",
    description="查询城市天气",
    args_schema=WeatherInput
)

# ===== 工具集合 =====
tools = [search_tool, calculator_tool, weather_tool]
```

---

## 工具调用最佳实践

### 实践 1：文档字符串

每个工具都应该有清晰的文档。

```python
def well_documented_tool(input: str) -> Dict:
    """
    工具简短描述

    详细的工具说明，包括：
    - 工具的功能
    - 使用场景
    - 注意事项

    Args:
        input: 参数说明

    Returns:
        Dict: 返回值说明
            - success: 是否成功
            - data: 数据
            - error: 错误信息

    Raises:
        ValueError: 参数无效时抛出

    Example:
        >>> well_documented_tool("test")
        {'success': True, 'data': 'result', 'error': None}
    """
    pass
```

---

### 实践 2：日志记录

记录工具调用的关键信息。

```python
import logging

logger = logging.getLogger(__name__)

def logged_tool(input: str) -> Dict:
    """带日志的工具"""
    logger.info(f"工具调用: input={input}")

    try:
        result = process(input)
        logger.info(f"工具成功: result={result}")
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"工具失败: error={str(e)}")
        return {"success": False, "error": str(e)}
```

---

### 实践 3：超时控制

为工具调用设置超时。

```python
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    """超时上下文"""
    def timeout_handler(signum, frame):
        raise TimeoutError("操作超时")

    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

def tool_with_timeout(input: str) -> Dict:
    """带超时的工具"""
    try:
        with timeout(5):  # 5 秒超时
            result = slow_operation(input)
        return {"success": True, "data": result}
    except TimeoutError:
        return {"success": False, "error": "操作超时"}
```

---

## 最小验证

### 验证目标
- ✅ 理解工具定义的契约
- ✅ 能够定义参数校验
- ✅ 能够标准化返回结构

### 验证步骤
1. 创建一个带 schema 的工具
2. 添加参数校验
3. 标准化返回结构
4. 测试错误场景

---

## 常见错误

### 错误 1：缺少参数校验
```python
# 错误：没有校验参数
def bad_tool(input: str):
    return input.upper()  # 如果 input 是 None 会报错

# 正确：添加校验
def good_tool(input: str):
    if input is None:
        raise ValueError("input 不能为 None")
    return input.upper()
```

### 错误 2：返回结构不统一
```python
# 错误：返回结构不统一
def inconsistent_tool(success: bool):
    if success:
        return {"data": "result"}  # 没有 success 字段
    else:
        return {"error": "error"}   # 没有 success 字段

# 正确：统一结构
def consistent_tool(success: bool):
    if success:
        return {"success": True, "data": "result", "error": None}
    else:
        return {"success": False, "data": None, "error": "error"}
```

---

## 下一步

- 📖 `notes/05_retry_and_error_handling.md` - 重试与错误处理
- 🧪 `examples/06_tool_contracts.py` - 工具契约示例

---

**记住：工具调用契约就像 API 文档，明确定义输入、输出和错误！** 📋
