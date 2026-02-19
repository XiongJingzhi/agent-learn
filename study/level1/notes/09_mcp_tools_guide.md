# MCP (Model Context Protocol) 工具开发指南

> **主题**: 使用 MCP 协议开发 Agent 工具
> **时间**: 60 分钟
> **难度**: ⭐⭐⭐⭐
> **前置**: 已了解基础工具开发

---

## 🎯 学习目标

1. ✅ 理解 MCP 协议的核心概念
2. ✅ 掌握 MCP Tool 的结构
3. ✅ 能够开发自定义 MCP 工具
4. ✅ 能够集成 MCP 工具到 Agent



---

## MCP Tool 与 Agent Skill 的边界

> 本节用于避免概念混淆（基于 Claude Agent Skills 官方定义）。

- MCP Tool：协议化的“执行能力接口”。
- Agent Skill：目录化、可复用的“能力包”（通常由 `SKILL.md` + 资源 + 脚本组成）。

关系：
- Skill 可以调用 MCP Tool。
- MCP Tool 本身不等于 Skill。

实践建议：
1. 先定义 Skill 的目标、触发条件、流程。
2. 再在 Skill 内选择 MCP Tool 作为执行组件。
3. 不要把“有一个 MCP Tool”误认为“已经完成 Skill 设计”。


---

## 📚 什么是 MCP？

### 定义

**MCP (Model Context Protocol)** = 模型上下文协议

**目标**: 统一 AI 模型与工具/数据源之间的通信标准

**类比**:
- HTTP = Web 浏览器和服务器之间的协议
- MCP = AI 模型和工具之间的协议

---

### 为什么需要 MCP？

**问题**:
- 每个工具都有不同的接口
- 难以集成多个工具
- 缺乏统一标准

**MCP 的解决方案**:
```
┌─────────────────────────────────────────┐
│          MCP Protocol                  │
│  (统一的工具接口标准)                    │
└───────┬─────────────────────┬───────────┘
        │                     │
    ┌───▼────┐          ┌────▼─────┐
    │ Tool 1 │          │  Tool 2  │
    │ (任意) │          │  (任意)  │
    └────────┘          └──────────┘
```

**优势**:
1. **统一接口**: 所有工具使用相同协议
2. **易于集成**: 插件式添加工具
3. **跨框架兼容**: 不依赖特定框架
4. **类型安全**: 完整的类型定义

---

## 🔧 MCP Tool 结构

### 基础结构

```python
from mcp import Tool, ToolContext
from typing import Dict, Any, Optional

class MyMCPTool(Tool):
    """MCP 工具模板"""

    # 工具元数据
    name = "my_tool"           # 工具名称（必需）
    description = "工具描述"    # 工具功能说明（必需）
    version = "1.0.0"          # 工具版本（可选）

    def get_input_schema(self) -> Dict:
        """定义输入 Schema"""
        return {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "参数 1 说明"
                },
                "param2": {
                    "type": "integer",
                    "description": "参数 2 说明"
                }
            },
            "required": ["param1"]
        }

    def call(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None
    ) -> Dict[str, Any]:
        """执行工具"""
        param1 = arguments.get("param1")
        param2 = arguments.get("param2", 0)

        # 执行逻辑
        result = self._do_work(param1, param2)

        # 返回结果
        return {
            "success": True,
            "data": result
        }

    def _do_work(self, param1: str, param2: int) -> Any:
        """实际工作逻辑"""
        # 实现具体功能
        return f"处理 {param1}，参数 {param2}"
```

---

## 💻 实现示例

### 示例 1: 数据库查询工具

```python
import sqlite3
from typing import Dict, Any, Optional, List
from mcp import Tool, ToolContext

class DatabaseQueryTool(Tool):
    """数据库查询工具"""

    name = "database_query"
    description = "执行 SQL 查询并返回结果"
    version = "1.0.0"

    def __init__(self, db_path: str):
        """初始化"""
        super().__init__()
        self.db_path = db_path
        self.conn = None

    def get_input_schema(self) -> Dict:
        """定义输入 Schema"""
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL 查询语句"
                },
                "database": {
                    "type": "string",
                    "description": "数据库名称或路径"
                }
            },
            "required": ["query"]
        }

    def call(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None
    ) -> Dict[str, Any]:
        """执行查询"""
        query = arguments.get("query")
        database = arguments.get("database", self.db_path)

        try:
            # 连接数据库
            self.conn = sqlite3.connect(database)
            cursor = self.conn.cursor()

            # 执行查询
            cursor.execute(query)

            # 获取结果
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # 格式化结果
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))

            return {
                "success": True,
                "data": {
                    "columns": columns,
                    "rows": results,
                    "count": len(results)
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

        finally:
            if self.conn:
                self.conn.close()
```

---

### 示例 2: API 调用工具

```python
import requests
from typing import Dict, Any, Optional
from mcp import Tool, ToolContext

class APICallTool(Tool):
    """API 调用工具"""

    name = "api_call"
    description = "调用外部 HTTP API"
    version = "1.0.0"

    def __init__(self, timeout: int = 30):
        """初始化"""
        super().__init__()
        self.timeout = timeout

    def get_input_schema(self) -> Dict:
        """定义输入 Schema"""
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "API 端点 URL"
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE"],
                    "description": "HTTP 方法"
                },
                "headers": {
                    "type": "object",
                    "description": "HTTP 请求头"
                },
                "body": {
                    "type": "object",
                    "description": "请求体（POST/PUT）"
                }
            },
            "required": ["url", "method"]
        }

    def call(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None
    ) -> Dict[str, Any]:
        """执行 API 调用"""
        url = arguments["url"]
        method = arguments["method"]
        headers = arguments.get("headers", {})
        body = arguments.get("body")

        try:
            # 发送请求
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=body,
                timeout=self.timeout
            )

            # 返回结果
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.content else None,
                "headers": dict(response.headers)
            }

        except requests.Timeout:
            return {
                "success": False,
                "error": "请求超时"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

---

### 示例 3: 文件操作工具

```python
import os
import shutil
from typing import Dict, Any, Optional
from mcp import Tool, ToolContext

class FileOperationTool(Tool):
    """文件操作工具"""

    name = "file_operation"
    description = "执行文件操作：读取、写入、移动、删除"
    version = "1.0.0"

    def __init__(self, base_path: str = "."):
        """初始化"""
        super().__init__()
        self.base_path = os.path.abspath(base_path)

    def get_input_schema(self) -> Dict:
        """定义输入 Schema"""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["read", "write", "move", "delete", "list"],
                    "description": "操作类型"
                },
                "path": {
                    "type": "string",
                    "description": "文件路径（相对于 base_path）"
                },
                "content": {
                    "type": "string",
                    "description": "要写入的内容（write 操作需要）"
                },
                "destination": {
                    "type": "string",
                    "description": "目标路径（move 操作需要）"
                }
            },
            "required": ["operation", "path"]
        }

    def call(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None
    ) -> Dict[str, Any]:
        """执行文件操作"""
        operation = arguments["operation"]
        path = os.path.join(self.base_path, arguments["path"])

        try:
            if operation == "read":
                return self._read_file(path)

            elif operation == "write":
                content = arguments.get("content", "")
                return self._write_file(path, content)

            elif operation == "move":
                dest = os.path.join(self.base_path, arguments["destination"])
                return self._move_file(path, dest)

            elif operation == "delete":
                return self._delete_file(path)

            elif operation == "list":
                return self._list_directory(path)

            else:
                return {
                    "success": False,
                    "error": f"未知操作: {operation}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _read_file(self, path: str) -> Dict[str, Any]:
        """读取文件"""
        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"文件不存在: {path}"
            }

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "success": True,
            "path": path,
            "content": content,
            "size": len(content)
        }

    def _write_file(self, path: str, content: str) -> Dict[str, Any]:
        """写入文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "success": True,
            "path": path,
            "size": len(content)
        }

    def _move_file(self, src: str, dest: str) -> Dict[str, Any]:
        """移动文件"""
        shutil.move(src, dest)

        return {
            "success": True,
            "from": src,
            "to": dest
        }

    def _delete_file(self, path: str) -> Dict[str, Any]:
        """删除文件"""
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

        return {
            "success": True,
            "deleted": path
        }

    def _list_directory(self, path: str) -> Dict[str, Any]:
        """列出目录"""
        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"路径不存在: {path}"
            }

        if os.path.isfile(path):
            return {
                "success": True,
                "type": "file",
                "path": path
            }

        items = os.listdir(path)
        return {
            "success": True,
            "type": "directory",
            "path": path,
            "items": items
        }
```

---

## 🌐 MCP 服务器集成

### 创建 MCP 服务器

```python
from mcp.server import Server, ServerOptions
from mcp.types import Tool as MCPTool

# 创建 MCP 服务器
server = Server(
    name="my-mcp-server",
    version="1.0.0"
)

# 添加工具
server.add_tool(DatabaseQueryTool("./data.db"))
server.add_tool(APICallTool())
server.add_tool(FileOperationTool("./workspace"))

# 启动服务器
async def main():
    options = ServerOptions(
        host="localhost",
        port=3000
    )

    await server.start(options)

# 运行服务器
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

### 在 Agent 中使用 MCP 工具

```python
from mcp.client import Client

class MCPEnabledAgent:
    """支持 MCP 的 Agent"""

    def __init__(self, mcp_server_url: str):
        """初始化"""
        # 连接到 MCP 服务器
        self.client = Client(mcp_server_url)
        self.tools = {}

        # 加载所有工具
        self._load_tools()

    def _load_tools(self):
        """加载工具"""
        # 获取可用工具列表
        tools_list = self.client.list_tools()

        for tool_info in tools_list:
            tool_name = tool_info["name"]
            self.tools[tool_name] = {
                "description": tool_info["description"],
                "schema": tool_info["input_schema"]
            }

            print(f"加载工具: {tool_name}")

    def use_tool(self, tool_name: str, arguments: Dict) -> Any:
        """使用工具"""
        if tool_name not in self.tools:
            raise ValueError(f"未知工具: {tool_name}")

        # 调用 MCP 工具
        result = self.client.call_tool(tool_name, arguments)

        return result

    def process(self, user_request: str) -> str:
        """处理用户请求"""
        # 1. 分析请求，决定使用哪个工具
        tool_name, arguments = self._analyze_request(user_request)

        # 2. 调用工具
        result = self.use_tool(tool_name, arguments)

        # 3. 格式化返回
        return self._format_result(result)

    def _analyze_request(self, request: str) -> tuple:
        """分析请求，返回工具名和参数"""
        # 简化的分析逻辑
        request_lower = request.lower()

        if "sql" in request_lower or "查询" in request_lower:
            return "database_query", {"query": request}

        elif "api" in request_lower or "http" in request_lower:
            return "api_call", {"url": request, "method": "GET"}

        elif "文件" in request_lower or "读取" in request_lower:
            return "file_operation", {
                "operation": "read",
                "path": request.split("文件")[-1].strip()
            }

        else:
            raise ValueError("无法识别的请求类型")

    def _format_result(self, result: Dict) -> str:
        """格式化结果"""
        if result.get("success"):
            data = result.get("data")
            if isinstance(data, dict):
                return "\n".join([f"{k}: {v}" for k, v in data.items()])
            else:
                return str(data)
        else:
            return f"操作失败: {result.get('error')}"
```

---

## 🔒 安全最佳实践

### 1. 输入验证

```python
class SecureMCPTool(Tool):
    """安全的 MCP 工具"""

    def validate_input(self, arguments: Dict[str, Any]) -> bool:
        """验证输入"""
        # 检查必需参数
        required = self.get_input_schema().get("required", [])
        for param in required:
            if param not in arguments:
                raise ValueError(f"缺少必需参数: {param}")

        # 检查参数类型
        properties = self.get_input_schema().get("properties", {})
        for param, schema in properties.items():
            if param in arguments:
                value = arguments[param]
                expected_type = schema.get("type")

                if expected_type == "string" and not isinstance(value, str):
                    raise TypeError(f"{param} 必须是字符串")
                elif expected_type == "integer" and not isinstance(value, int):
                    raise TypeError(f"{param} 必须是整数")

        return True

    def call(self, arguments: Dict[str, Any], context: Optional[ToolContext] = None):
        """调用前验证"""
        self.validate_input(arguments)
        return super().call(arguments, context)
```

---

### 2. 资源限制

```python
import resource
import signal
from contextlib import contextmanager

class ResourceLimitMixin:
    """资源限制混入类"""

    @contextmanager
    def limit_resources(self, max_memory: int = 1024*1024*100,  # 100MB
                      max_time: int = 30):  # 30 秒
        """限制资源使用"""
        def timeout_handler(signum, frame):
            raise TimeoutError("操作超时")

        # 设置内存限制
        resource.setrlimit(resource.RLIMIT_AS, (max_memory, max_memory))

        # 设置时间限制
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(max_time)

        try:
            yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)


class SecureAPICallTool(APICallTool, ResourceLimitMixin):
    """安全的 API 调用工具"""

    def call(self, arguments: Dict[str, Any], context: Optional[ToolContext] = None):
        """安全调用"""
        with self.limit_resources(max_memory=50*1024*1024, max_time=10):
            return super().call(arguments, context)
```

---

### 3. 日志和审计

```python
import logging
from datetime import datetime

class AuditMixin:
    """审计混入类"""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.audit_log = []

    def log_call(self, tool_name: str, arguments: Dict, result: Any):
        """记录调用"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "arguments": arguments,
            "success": result.get("success", False)
        }

        self.audit_log.append(log_entry)

        # 日志级别根据成功与否
        if log_entry["success"]:
            self.logger.info(f"工具调用成功: {tool_name}")
        else:
            self.logger.warning(f"工具调用失败: {tool_name}, "
                             f"原因: {result.get('error')}")

    def get_audit_log(self) -> List[Dict]:
        """获取审计日志"""
        return self.audit_log.copy()


class AuditableMCPTool(SecureMCPTool, AuditMixin):
    """可审计的 MCP 工具"""

    def call(self, arguments: Dict[str, Any], context: Optional[ToolContext] = None):
        """带审计的调用"""
        try:
            result = super().call(arguments, context)
            self.log_call(self.name, arguments, result)
            return result
        except Exception as e:
            error_result = {"success": False, "error": str(e)}
            self.log_call(self.name, arguments, error_result)
            raise
```

---

## 🎓 费曼解释

### 给 5 岁孩子的解释

**MCP 就像电源插座和电器的标准**：

```
    MCP 协议 = 插座标准
    所有插座（工具）都一样
    任何电器（AI 模型）都能插上用
```

**没有 MCP 之前**：
- 每个工具都不同
- 需要专门的适配器
- 难以添加新工具

**有了 MCP 之后**：
- 所有工具都用同样的接口
- 添加新工具很容易
- AI 模型能自动使用任何工具

### 关键要点

1. **统一接口** = 所有工具有相同的"插头"
2. **自动发现** = AI 能自动知道有什么工具
3. **类型安全** = 参数和返回值有明确定义
4. **易于扩展** = 新工具只需符合 MCP 标准

---

## ✅ 最小验证

### 任务

1. 实现一个简单的 MCP Tool（20 分钟）
2. 创建 MCP 服务器并注册工具（15 分钟）
3. 在 Agent 中使用 MCP 工具（15 分钟）
4. 添加安全验证（10 分钟）

### 期望输出

- [ ] 可运行的 MCP Tool
- [ ] MCP 服务器能正常启动
- [ ] Agent 能调用 MCP 工具
- [ ] 有输入验证和日志

---

## 🔗 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP 规范](https://spec.modelcontextprotocol.io/)
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)

---

## 🚀 下一步

学习完本笔记后，继续学习：
- `examples/09_mcp_tools.py` - MCP 工具完整示例
- `notes/08_agent_skills_deep_dive.md` - Skills 深度指南

---

**记住：MCP 让工具开发标准化，让 Agent 更强大！** 🔌
