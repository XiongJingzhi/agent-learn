# 14 Prometheus + Grafana

> **主题**: 配置 Prometheus 和 Grafana 监控系统
> **时间**: 50 分钟
> **难度**: ⭐⭐⭐⭐

---

## 学习目标

完成本笔记后，你将能够：

1. 理解 Prometheus 的架构和数据模型
2. 掌握 PromQL 查询语言
3. 能够配置 Prometheus 抓取指标
4. 能够创建 Grafana 仪表盘
5. 能够配置告警规则

---

## Prometheus 基础

### 什么是 Prometheus？

**Prometheus** 是一个开源的监控系统和时间序列数据库。

**特点**:
- 多维数据模型
- 内置 PromQL 查询语言
- 拉取式采集（Pull）
- 服务发现
- 告警管理

### 架构

```
┌─────────────────────────────────────────────────────┐
│                   Prometheus Server                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ │
│  │ Retrieval   │  │  Storage    │  │ PromQL Engine│ │
│  │   (Scrape)  │→ │   (TSDB)    │→ │              │ │
│  └─────────────┘  └─────────────┘  └──────────────┘ │
│         ↓                                   ↓        │
│   [Targets]                          [Alertmanager]  │
└─────────────────────────────────────────────────────┘
         ↑                                           ↑
    [Exporter]                                   [Grafana]
         ↓                                           ↓
    [Applications]                             [Dashboard]
```

---

## 数据模型

### 指标类型

#### 1. Counter（计数器）

**特点**: 只增不减的值

**用途**: 请求总数、错误总数、处理的总字节数

**示例**:
```python
from prometheus_client import Counter

# 定义
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# 使用
request_count.labels(
    method='GET',
    endpoint='/api/chat',
    status='200'
).inc()

# 查询速率
rate(http_requests_total[5m])
```

#### 2. Gauge（仪表）

**特点**: 可增可减的值

**用途**: 当前温度、内存使用量、活跃连接数

**示例**:
```python
from prometheus_client import Gauge

# 定义
active_connections = Gauge(
    'http_active_connections',
    'Active HTTP connections'
)

# 使用
active_connections.set(42)

# 查询当前值
http_active_connections
```

#### 3. Histogram（直方图）

**特点**: 分布情况，可配置桶

**用途**: 请求延迟、响应大小

**示例**:
```python
from prometheus_client import Histogram

# 定义
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    buckets=[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
)

# 使用
with request_duration.time():
    # 处理请求
    process_request()

# 查询 P95 延迟
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

#### 4. Summary（摘要）

**特点**: 客户端计算分位数

**用途**: 类似 Histogram，但分位数在客户端计算

**示例**:
```python
from prometheus_client import Summary

request_duration = Summary(
    'http_request_duration_seconds',
    'HTTP request duration'
)

request_duration.observe(0.5)
```

---

## PromQL 查询

### 基础查询

```promql
# 即时值（当前值）
http_requests_total

# 带标签过滤
http_requests_total{job="agent-service", status="200"}

# 正则匹配
http_requests_total{status=~"2.."}
http_requests_total{status!~"4.."}

# 范围查询（过去 5 分钟）
http_requests_total[5m]

# 偏移量查询（一天前的数据）
http_requests_total offset 1d
```

### 操作符

#### 算术操作符

```promql
# 加法
http_requests_total + http_errors_total

# 减法
http_requests_total - http_errors_total

# 乘法
http_requests_total * 0.5

# 除法
http_errors_total / http_requests_total

# 取模
http_requests_total % 100
```

#### 比较操作符

```promql
# 等于
http_requests_total == 100

# 不等于
http_requests_total != 0

# 大于
cpu_usage > 0.8

# 小于
cpu_usage < 0.2

# 正则匹配
job =~ "agent.*"
```

#### 逻辑操作符

```promql
# 与
http_requests_total{job="agent"} and http_requests_total{status="200"}

# 或
http_requests_total{job="agent"} or http_requests_total{job="worker"}

# 非
http_requests_total and not http_requests_total{status="200"}
```

### 函数

#### rate() 和 irate()

```promql
# rate: 计算过去 5 分钟的平均速率
rate(http_requests_total[5m])

# irate: 计算瞬时速率（最后两个数据点）
irate(http_requests_total[5m])

# 适用场景：Counter 类型
rate(http_requests_total{job="agent-service"}[5m])
```

#### increase()

```promql
# 计算增量（过去一天）
increase(http_requests_total[1d])

# 适用场景：计算绝对增长
```

#### histogram_quantile()

```promql
# 计算 P95 延迟
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 计算多个服务的 P95
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job))
```

#### 聚合函数

```promql
# 求和
sum(http_requests_total)

# 按 status 求和
sum(http_requests_total) by (status)

# 最大值
max(cpu_usage)

# 最小值
min(cpu_usage)

# 平均值
avg(cpu_usage)

# 计数
count(up)

# 标准差
stddev(cpu_usage)

# 去重计数
count_distinct(user_id)
```

---

## Prometheus 配置

### 基础配置

```yaml
# prometheus.yml
global:
  # 全局抓取间隔
  scrape_interval: 15s
  # 评估规则间隔
  evaluation_interval: 15s
  # 外部标签
  external_labels:
    cluster: 'production'
    env: 'prod'

# 告警管理器
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - 'alertmanager:9093'

# 告警规则文件
rule_files:
  - '/etc/prometheus/alerts/*.yml'

# 抓取配置
scrape_configs:
  # Prometheus 自身
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Agent 服务
  - job_name: 'agent-service'
    static_configs:
      - targets: ['agent-service:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  # Kubernetes 服务发现
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### 服务发现

```yaml
# Kubernetes 服务发现
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - agent-prod
    relabel_configs:
      # 只抓取有特定注解的 Pod
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # 自定义指标路径
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      # 自定义端口
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

---

## Grafana 基础

### 什么是 Grafana？

**Grafana** 是一个开源的可视化平台，支持多种数据源。

**特点**:
- 支持多种数据源（Prometheus, Loki, Elasticsearch 等）
- 强大的仪表盘功能
- 告警通知
- 插件生态

### 仪表盘组件

#### Panel（面板）

**类型**:
- Graph（图表）
- Stat（统计）
- Table（表格）
- Heatmap（热力图）
- Gauge（仪表）
- Logs（日志）

**配置示例**:
```json
{
  "title": "Request Rate",
  "type": "graph",
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{job=\"agent-service\"}[5m]))",
      "legendFormat": "QPS"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "min": 0
    }
  }
}
```

#### Variable（变量）

**用途**: 动态过滤、简化查询

**示例**:
```json
{
  "name": "job",
  "type": "query",
  "query": "label_values(http_requests_total, job)",
  "multi": true
}
```

---

## 完整示例

### Agent 应用集成 Prometheus

```python
# main.py
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
import time

app = FastAPI()

# 定义指标
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'http_active_connections',
    'Active HTTP connections'
)

llm_tokens = Counter(
    'llm_tokens_total',
    'Total LLM tokens used'
)

llm_cost = Counter(
    'llm_cost_total',
    'Total LLM cost in USD'
)

# 中间件
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()

    # 增加活跃连接
    active_connections.inc()

    response = await call_next(request)

    # 记录请求
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    # 记录延迟
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(time.time() - start_time)

    # 减少活跃连接
    active_connections.dec()

    return response

# 指标端点
@app.get("/metrics")
async def metrics():
    return generate_latest()

# Agent 端点
@app.post("/chat")
async def chat(message: str):
    # 调用 LLM
    tokens = call_llm(message)
    cost = calculate_cost(tokens)

    # 记录指标
    llm_tokens.inc(tokens)
    llm_cost.inc(cost)

    return {"response": "..."}
```

### Grafana 仪表盘配置

```json
{
  "dashboard": {
    "title": "Agent Service Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=\"agent-service\"}[5m]))",
            "legendFormat": "QPS"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=\"agent-service\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{job=\"agent-service\"}[5m]))",
            "legendFormat": "Error Rate"
          }
        ]
      },
      {
        "title": "P95 Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job=\"agent-service\"}[5m])) by (le))",
            "legendFormat": "P95"
          }
        ]
      },
      {
        "title": "Active Connections",
        "type": "stat",
        "targets": [
          {
            "expr": "http_active_connections{job=\"agent-service\"}"
          }
        ]
      }
    ]
  }
}
```

---

## 费曼解释

### 用简单的语言解释

**问题**: Prometheus 和 Grafana 是什么？

**类比**: 想象你在管理一个餐厅：

**Prometheus** = 收银员 + 账本
- 不断记录每一笔订单（抓取指标）
- 记录每一笔收入和支出（时间序列数据）
- 可以查询历史记录（PromQL）
- 如果支出太高就报警（告警规则）

**Grafana** = 仪表盘 + 图表
- 把账本的数据可视化（图表）
- 显示实时收入趋势（实时监控）
- 比较不同时期的数据（对比分析）
- 好看又好用（美观的界面）

**核心**: Prometheus 负责收集和存储数据，Grafana 负责展示和分析数据，两者配合实现完整的监控。

---

## 最小验证

### 任务 1: 集成 Prometheus

为 FastAPI 应用添加 Prometheus 指标：

```python
from prometheus_client import Counter, Histogram, make_asgi_app

# 添加指标端点
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 定义指标
request_count = Counter('requests_total', 'Total requests', ['method', 'status'])
request_duration = Histogram('request_duration_seconds', 'Request duration')

# 使用
@app.get("/")
async def root():
    request_count.labels(method='GET', status='200').inc()
    with request_duration.time():
        return {"hello": "world"}
```

**验证**: 访问 http://localhost:8000/metrics

### 任务 2: 配置 Prometheus

创建 prometheus.yml 配置文件：

```yaml
scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['host.docker.internal:8000']
    scrape_interval: 10s
```

**验证**: 启动 Prometheus 并检查 targets

### 任务 3: 创建 Grafana 仪表盘

创建一个包含以下面板的仪表盘：
1. 请求速率
2. 错误率
3. P95 延迟

**验证**: 仪表盘显示正确数据

---

## 常见问题

### Q1: Prometheus 存储占用太大怎么办？

**A**:
- 减少数据保留时间（`--storage.tsdb.retention.time=15d`）
- 减少抓取频率
- 使用 recording rules 预聚合数据
- 配置数据限大小

### Q2: PromQL 查询太慢怎么办？

**A**:
- 使用 recording rules
- 减少查询时间范围
- 避免高基数查询
- 优化查询表达式

### Q3: 如何监控容器应用？

**A**:
- 暴露 /metrics 端口
- 配置 ServiceMonitor
- 使用 Prometheus Operator
- 配置 Pod 注解

---

## 总结

### 关键要点

1. **四种指标类型**: Counter, Gauge, Histogram, Summary
2. **PromQL 核心**: rate(), irate(), increase(), histogram_quantile()
3. **Grafana 优势**: 可视化、告警、多数据源
4. **最佳实践**: 定义清晰的指标、合理设置标签、使用仪表盘

### 下一步

- 学习告警规则
- 学习日志聚合（Loki）
- 学习分布式追踪（Tempo）

---

## 参考资源

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)

---

**完成时间**: ____
**验证状态**: ⏳ 待完成
