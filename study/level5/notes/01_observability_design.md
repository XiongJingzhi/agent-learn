# 01 可观测性设计

> **主题**: 设计生产级系统的可观测性方案
> **时间**: 50 分钟
> **难度**: ⭐⭐⭐⭐

---

## 学习目标

完成本笔记后，你将能够：

1. 理解可观测性的三大支柱
2. 能够设计监控方案
3. 能够选择合适的监控工具
4. 能够定义关键指标

---

## 核心概念

### 什么是可观测性？

**可观测性（Observability）**是指通过观察系统的外部输出，推断系统内部状态的能力。

**可观测性 vs 监控**:
- **监控**: 检查预定义的指标和告警
- **可观测性**: 主动探索和理解系统状态

> "Monitoring is asking 'is it okay?', Observability is asking 'what's happening?'"

---

### 三大支柱

#### 1. 日志（Logs）

**定义**: 离散事件的记录，带时间戳的文本信息。

**特点**:
- 描述"发生了什么"
- 丰富的上下文信息
- 适合排查问题

**日志级别**:
```python
DEBUG    - 详细的信息，用于调试
INFO     - 一般的信息，记录关键操作
WARNING  - 警告信息，不影响运行
ERROR    - 错误信息，需要关注
CRITICAL - 严重错误，需要立即处理
```

**最佳实践**:
```python
# ✅ 好的日志
logger.info("User login", extra={
    "user_id": user.id,
    "ip": request.remote_addr,
    "user_agent": request.headers.get("User-Agent"),
    "timestamp": datetime.now().isoformat()
})

# ❌ 不好的日志
logger.info("User logged in")  # 缺少上下文
```

**结构化日志**:
```json
{
  "level": "info",
  "message": "Agent tool called",
  "timestamp": "2024-01-15T10:30:00Z",
  "context": {
    "agent_id": "agent-123",
    "tool_name": "web_search",
    "arguments": {"query": "Python tutorial"},
    "duration_ms": 1234,
    "success": true
  }
}
```

#### 2. 指标（Metrics）

**定义**: 数值化的测量数据，通常是时间序列数据。

**特点**:
- 描述"系统状态如何"
- 可聚合、可计算
- 适合监控和告警

**指标类型**:

1. **Counter（计数器）**: 只增不减的值
   - 示例：API 请求总数、错误总数
   - 用途：统计速率、总量

2. **Gauge（仪表）**: 可增可减的值
   - 示例：当前内存使用、活跃连接数
   - 用途：当前状态

3. **Histogram（直方图）**: 分布情况
   - 示例：请求延迟分布、响应大小分布
   - 用途：P50、P95、P99 延迟

**关键指标示例**:
```python
from prometheus_client import Counter, Histogram, Gauge

# 请求数
request_count = Counter(
    'agent_requests_total',
    'Total number of agent requests',
    ['agent_type', 'status']
)

# 请求延迟
request_duration = Histogram(
    'agent_request_duration_seconds',
    'Agent request duration',
    ['agent_type']
)

# 活跃用户
active_users = Gauge(
    'agent_active_users',
    'Number of active users'
)

# 使用
request_count.labels(agent_type='chat', status='success').inc()
request_duration.labels(agent_type='chat').observe(1.23)
```

#### 3. 追踪（Traces）

**定义**: 请求在系统中的传播路径记录。

**特点**:
- 描述"请求如何传播"
- 跨服务调用链
- 适合性能分析

**Trace 结构**:
```
Trace (请求的完整路径)
 └─ Span 1: 用户请求 → API Gateway
     ├─ Span 2: API Gateway → Agent Service
     │   ├─ Span 3: Agent → LLM API
     │   └─ Span 4: Agent → Database
     └─ Span 5: API Gateway → Cache
```

**OpenTelemetry 示例**:
```python
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor

tracer = trace.get_tracer(__name__)

@app.route("/chat")
def chat():
    with tracer.start_as_current_span("chat_handler"):
        # 处理聊天请求
        with tracer.start_as_current_span("llm_call"):
            response = call_llm()
        return response
```

---

### 监控方法论

#### RED 方法

适用于请求驱动的系统（如 API 服务）：

- **Rate（速率）**: 每秒请求数
- **Errors（错误）**: 错误率
- **Duration（延迟）**: 请求持续时间

**示例**:
```python
# Rate
requests_per_second = request_count / time_window

# Errors
error_rate = error_count / total_count

# Duration
p50_latency = percentile(latencies, 50)
p95_latency = percentile(latencies, 95)
p99_latency = percentile(latencies, 99)
```

#### USE 方法

适用于资源驱动的系统：

- **Utilization（使用率）**: 资源使用百分比
- **Saturation（饱和度）**: 资源拥塞程度
- **Errors（错误）**: 资源错误数

**示例**:
```python
# CPU
cpu_utilization = cpu_time / total_time
cpu_saturation = load_average / cpu_count

# Memory
memory_utilization = used_memory / total_memory
memory_saturation = swap_usage > 0  # 开始使用 swap

# Disk
disk_utilization = used_disk / total_disk
disk_saturation = io_wait_time_high  # IO 等待时间过长
```

#### 四大黄金信号

Google SRE 推荐的关键指标：

1. **延迟（Latency）**: 服务请求的时间
2. **流量（Traffic）**: 服务请求数量
3. **错误（Errors）**: 请求失败率
4. **饱和度（Saturation）**: 服务负载程度

---

### Agent 系统的关键指标

#### 1. 性能指标

```python
# 响应时间
agent_response_time_p50 = 0.5s   # 中位数
agent_response_time_p95 = 1.2s   # 95 分位
agent_response_time_p99 = 2.5s   # 99 分位

# 吞吐量
agent_requests_per_second = 100
agent_concurrent_users = 50
```

#### 2. 质量指标

```python
# 成功率
agent_success_rate = 98.5%

# LLM 相关
llm_tokens_per_request = 1500
llm_cost_per_request = 0.03
llm_error_rate = 0.5%

# 工具调用
tool_call_success_rate = 99%
tool_call_avg_duration = 2s
```

#### 3. 业务指标

```python
# 用户行为
daily_active_users = 1000
avg_session_duration = 300s
user_retention_rate = 65%

# 功能使用
feature_usage = {
    "web_search": 80%,    # 使用搜索功能的用户比例
    "code_interpreter": 30%,
    "file_analysis": 20%
}
```

---

## 监控工具选型

### 日志工具

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| ELK Stack | 功能强大，社区活跃 | 中大型系统 |
| Loki | 轻量级，与 Grafana 集成 | 已用 Grafana 的场景 |
| CloudWatch | AWS 原生集成 | AWS 环境 |
| Fluentd | 数据收集器 | 日志收集层 |

### 指标工具

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| Prometheus | 云原生标准，Pull 模式 | K8s 环境 |
| InfluxDB | 时序数据库，性能好 | 高频指标 |
| Datadog | SaaS 服务，易用 | 快速上手 |
| CloudWatch | AWS 原生集成 | AWS 环境 |

### 追踪工具

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| Jaeger | 开源，兼容 OpenTracing | 微服务 |
| Zipkin | 轻量级 | 简单场景 |
| Tempo | Grafana 集成 | 已用 Grafana |
| X-Ray | AWS 原生集成 | AWS 环境 |

### 一体化方案

| 方案 | 特点 | 适用场景 |
|------|------|----------|
| Grafana Stack | 开源一体化 | 自建监控 |
| Datadog | SaaS，全功能 | 快速部署 |
| New Relic | SaaS，易用 | 快速上手 |
| AWS CloudWatch | AWS 原生 | AWS 环境 |

---

## 费曼解释

### 用简单的语言解释

**问题**: 什么是可观测性？

**类比**: 想象你在开一辆车：

1. **日志**就像行车记录仪，记录了"什么时候发生了什么"
   - "10:30 右转"
   - "11:00 刹车"
   - "11:15 加速"

2. **指标**就像仪表盘，告诉你"当前状态如何"
   - 速度表：当前速度 60 km/h
   - 油量表：剩余油量 50%
   - 转速表：发动机 2000 rpm

3. **追踪**就像导航记录，告诉你"从哪里到哪里"
   - 起点 → 高速 → 出口 → 终点
   - 每段路程花了多少时间

**核心**: 可观测性就是让你"看见"系统内部发生了什么，就像开车时通过各种仪表和记录了解车的状态。

---

## 最小验证

### 任务 1: 添加结构化日志

修改一个 Agent 项目，添加结构化日志：

```python
import structlog

logger = structlog.get_logger()

def agent_run(user_input: str):
    logger.info("agent_start", input=user_input)

    # Agent 逻辑
    result = process(user_input)

    logger.info("agent_complete",
                input=user_input,
                output_length=len(result),
                duration_ms=123)
    return result
```

**验证**: 运行并检查日志输出

### 任务 2: 添加 Prometheus 指标

添加基本指标到 Agent：

```python
from prometheus_client import Counter, Histogram, start_http_server

# 定义指标
request_count = Counter('agent_requests_total', 'Total requests')
request_duration = Histogram('agent_duration_seconds', 'Request duration')

# 启动指标服务器
start_http_server(8000)

def agent_run(user_input: str):
    request_count.inc()
    with request_duration.time():
        return process(user_input)
```

**验证**: 访问 http://localhost:8000 查看指标

### 任务 3: 设计监控方案

为一个问答 Agent 设计监控方案：

1. 列出 5 个关键指标
2. 说明如何收集这些指标
3. 说明如何设置告警

**预期产出**:
- 监控方案文档（200-300 字）

---

## 常见问题

### Q1: 日志太多怎么办？

**A**: 优化日志策略：
- 使用日志级别（生产环境用 INFO+）
- 结构化日志便于过滤
- 定期归档和清理
- 使用日志采样（高流量场景）

### Q2: 指标应该多细粒度？

**A**: 平衡精度和成本：
- 关键业务指标：详细
- 系统资源指标：适中
- 调试指标：开发环境
- 避免维度爆炸（高基数问题）

### Q3: 如何选择监控工具？

**A**: 考虑因素：
1. 技术栈（K8s 用 Prometheus）
2. 团队熟悉度（学习成本）
3. 预算（开源 vs 商业）
4. 集成需求（是否与现有系统集成）

---

## 总结

### 关键要点

1. **三大支柱**：日志、指标、追踪，缺一不可
2. **选择合适的方法论**：RED、USE、四大黄金信号
3. **工具选型**：根据场景选择合适的工具
4. **从关键指标开始**：不要过度设计

### 下一步

- 学习 Prometheus 和 Grafana
- 实现日志聚合系统
- 配置告警规则

---

## 参考资源

- [Observability Engineering](https://www.oreilly.com/library/view/observability-engineering/9781492076726/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)

---

**完成时间**: ____
**验证状态**: ⏳ 待完成
