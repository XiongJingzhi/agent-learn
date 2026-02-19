# Level 5 Capstone 项目：生产级 Agent 系统部署

> **项目类型**: 综合实战项目
> **预计时间**: 12-15 小时
> **难度**: ⭐⭐⭐⭐⭐
> **团队**: 个人完成

---

## 项目目标

构建并部署一个**生产级 Agent 系统**，具备以下能力：

1. ✅ 容器化部署（Docker + Docker Compose）
2. ✅ Kubernetes 部署（可选）
3. ✅ CI/CD 流水线（GitHub Actions）
4. ✅ 监控告警系统（Prometheus + Grafana）
5. ✅ 日志聚合（Loki 或 ELK）
6. ✅ 安全防护（HTTPS + 认证授权 + 速率限制）
7. ✅ 健康检查和优雅关闭
8. ✅ 配置管理（环境变量 + ConfigMap）
9. ✅ 数据持久化（数据库 + 缓存）
10. ✅ 完整文档（部署 + 运维）

---

## 项目背景

### 业务场景

构建一个**智能客服 Agent 系统**，能够：

1. 回答常见问题（FAQ）
2. 查询订单状态
3. 处理退款请求
4. 转接人工客服

### 技术要求

- **语言**: Python 3.11+
- **框架**: FastAPI + LangChain
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **向量数据库**: Weaviate 或 Pinecone
- **LLM**: OpenAI GPT-4 或 Claude
- **部署**: Docker + Kubernetes (可选)
- **监控**: Prometheus + Grafana
- **日志**: Loki 或 ELK

---

## 核心功能

### 1. Agent 功能

#### 基础能力

```python
# FAQ 回答
- 回答产品相关问题
- 回答服务相关问题
- 回答售后相关问题

# 订单查询
- 根据订单号查询状态
- 根据用户信息查询订单

# 退款处理
- 验证退款资格
- 创建退款工单
- 通知用户退款进度

# 人工转接
- 识别需要人工处理的情况
- 创建工单
- 通知人工客服
```

#### 质量要求

- 响应时间 P95 < 3s
- 可用性 >= 99.5%
- 并发支持 >= 50 QPS

---

### 2. 监控功能

#### 指标监控

```python
# 性能指标
- 请求响应时间 (P50, P95, P99)
- 请求吞吐量 (QPS)
- 错误率

# 业务指标
- 用户满意度
- 问题解决率
- 人工转接率

# 资源指标
- CPU 使用率
- 内存使用率
- 磁盘使用率
- 网络流量
```

#### 告警规则

```python
# P0 告警（立即处理）
- 服务不可用
- 错误率 > 5%
- 响应时间 P99 > 10s

# P1 告警（快速响应）
- 错误率 > 1%
- 响应时间 P95 > 5s
- CPU > 80%

# P2 告警（计划处理）
- 磁盘使用率 > 70%
- 缓存命中率 < 80%
```

---

### 3. 安全功能

#### 认证授权

```python
# API 认证
- JWT Token 认证
- API Key 认证（内部调用）

# 权限控制
- 用户权限：只能查询自己的订单
- 管理员权限：可以查询所有订单
```

#### 安全防护

```python
# 速率限制
- 每用户每分钟 20 次
- 每 IP 每分钟 100 次

# 输入验证
- 验证所有用户输入
- 防止 SQL 注入
- 防止 XSS 攻击

# 数据加密
- HTTPS 传输
- 敏感数据加密存储
```

---

## 技术架构

### 系统架构图

```
                        ┌─────────────┐
                        │   用户请求   │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │   CDN/WAF   │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │ Load Balancer│
                        └──────┬──────┘
                               │
                    ┌──────────▼──────────┐
                    │   API Gateway       │
                    │  - 认证授权          │
                    │  - 速率限制          │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Agent Service     │
                    │  - FastAPI          │
                    │  - LangChain Agent  │
                    │  - 3 副本            │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼───────┐    ┌────────▼────────┐    ┌────────▼────────┐
│  PostgreSQL   │    │     Redis       │    │  Weaviate       │
│  (主从复制)    │    │  (主从复制)      │    │  (向量存储)      │
└───────────────┘    └─────────────────┘    └─────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  监控告警系统        │
                    │  - Prometheus       │
                    │  - Grafana          │
                    │  - Loki             │
                    └─────────────────────┘
```

---

### 技术栈

| 层次 | 技术 | 说明 |
|------|------|------|
| **应用层** | Python 3.11 | 编程语言 |
| | FastAPI | Web 框架 |
| | LangChain | Agent 框架 |
| **数据层** | PostgreSQL 15 | 关系数据库 |
| | Redis 7 | 缓存 |
| | Weaviate | 向量数据库 |
| **容器层** | Docker | 容器化 |
| | Kubernetes | 编排（可选） |
| **CI/CD** | GitHub Actions | 持续集成部署 |
| **监控** | Prometheus | 指标采集 |
| | Grafana | 可视化 |
| | Loki | 日志聚合 |
| **安全** | Let's Encrypt | SSL 证书 |
| | JWT | 认证 |

---

## 实施步骤

### Phase 1: 开发 Agent 功能 (4-5 小时)

#### 1.1 项目初始化

```bash
# 创建项目
mkdir customer-service-agent
cd customer-service-agent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install fastapi uvicorn langchain openai psycopg2 redis
```

#### 1.2 实现核心功能

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
import redis
import psycopg2

app = FastAPI(title="Customer Service Agent")

# 初始化
security = HTTPBearer()
llm = OpenAI(temperature=0)
redis_client = redis.Redis(host='redis', port=6379)
db_conn = psycopg2.connect("postgresql://user:pass@db:5432/agent")

# 工具定义
def get_faq_answer(question: str) -> str:
    """查询 FAQ 答案"""
    # 实现逻辑
    return "答案"

def get_order_status(order_id: str) -> str:
    """查询订单状态"""
    # 实现逻辑
    return "订单状态"

def create_refund(order_id: str) -> str:
    """创建退款"""
    # 实现逻辑
    return "退款已创建"

# 初始化 Agent
tools = [
    Tool(name="FAQ", func=get_faq_answer),
    Tool(name="OrderStatus", func=get_order_status),
    Tool(name="Refund", func=create_refund),
]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

@app.post("/chat")
async def chat(
    message: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """聊天接口"""
    # 验证 Token
    token = credentials.credentials
    user_id = verify_token(token)

    # 调用 Agent
    response = agent.run(message)

    return {"response": response}

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}
```

#### 1.3 添加监控

```python
# monitoring.py
from prometheus_client import Counter, Histogram, Gauge

# 指标定义
request_count = Counter('requests_total', 'Total requests', ['endpoint', 'status'])
request_duration = Histogram('request_duration_seconds', 'Request duration')
active_users = Gauge('active_users', 'Active users')

# 中间件
@app.middleware("http")
async def monitor_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    request_count.labels(
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    request_duration.observe(duration)

    return response
```

---

### Phase 2: 容器化 (2-3 小时)

#### 2.1 编写 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 非_root 用户
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2.2 编写 docker-compose.yml

```yaml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agent
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=agent
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    restart: unless-stopped

volumes:
  postgres_data:
```

---

### Phase 3: CI/CD 配置 (2-3 小时)

#### 3.1 GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=. --cov-report=html

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Push to registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USER }} --password-stdin
          docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          # 部署脚本
          kubectl set image deployment/agent app=myapp:${{ github.sha }}
          kubectl rollout status deployment/agent
```

---

### Phase 4: 监控告警 (2-3 小时)

#### 4.1 Prometheus 配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'agent'
    static_configs:
      - targets: ['agent:8000']
    metrics_path: '/metrics'
```

#### 4.2 Grafana 仪表盘

```json
{
  "dashboard": {
    "title": "Agent Service Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, request_duration_seconds_bucket)"
          }
        ]
      }
    ]
  }
}
```

#### 4.3 告警规则

```yaml
# alerts.yml
groups:
  - name: agent_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(requests_total{status=~\"5..\"}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"

      - alert: HighLatency
        expr: histogram_quantile(0.95, request_duration_seconds_bucket) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
```

---

### Phase 5: 安全加固 (1-2 小时)

#### 5.1 HTTPS 配置

```yaml
# docker-compose.yml 添加
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    restart: unless-stopped
```

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;

    location / {
        proxy_pass http://agent:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 5.2 认证授权

```python
# auth.py
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

def create_token(user_id: str) -> str:
    """创建 JWT Token"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> str:
    """验证 Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

#### 5.3 速率限制

```python
# rate_limit.py
import time
from fastapi import HTTPException

class RateLimiter:
    def __init__(self, redis_client, max_requests=20, window=60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window

    def check(self, user_id: str):
        key = f"rate_limit:{user_id}"
        current = self.redis.incr(key)

        if current == 1:
            self.redis.expire(key, self.window)

        if current > self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

# 使用
limiter = RateLimiter(redis_client)

@app.post("/chat")
async def chat(
    message: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_token(token)
    limiter.check(user_id)

    # ...
```

---

## 验收标准

### 功能验收

- [ ] Agent 能够回答 FAQ 问题
- [ ] Agent 能够查询订单状态
- [ ] Agent 能够处理退款请求
- [ ] Agent 能够转接人工客服
- [ ] 响应时间 P95 < 3s
- [ ] 并发支持 >= 50 QPS

---

### 技术验收

- [ ] 使用 Docker 部署
- [ ] 使用 Docker Compose 编排
- [ ] （可选）使用 Kubernetes 部署
- [ ] 配置 GitHub Actions CI/CD
- [ ] 配置 Prometheus 采集指标
- [ ] 配置 Grafana 仪表盘
- [ ] 配置告警规则
- [ ] 配置 HTTPS
- [ ] 实现认证授权
- [ ] 实现速率限制

---

### 质量验收

- [ ] 代码有类型提示
- [ ] 代码有文档注释
- [ ] 测试覆盖率 >= 70%
- [ ] 有完整的部署文档
- [ ] 有完整的运维手册
- [ ] 有监控仪表盘截图
- [ ] 有性能测试报告
- [ ] 有安全扫描报告

---

### 文档验收

- [ ] README.md（项目说明）
- [ ] DEPLOYMENT.md（部署文档）
- [ ] MONITORING.md（监控文档）
- [ ] API.md（API 文档）
- [ ] ARCHITECTURE.md（架构文档）

---

## 交付清单

### 代码

- [ ] 完整的应用代码
- [ ] Dockerfile
- [ ] docker-compose.yml
- [ ] Kubernetes 配置（可选）
- [ ] GitHub Actions workflow

### 文档

- [ ] README.md
- [ ] DEPLOYMENT.md
- [ ] MONITORING.md
- [ ] API.md
- [ ] ARCHITECTURE.md

### 证据

- [ ] 部署日志
- [ ] 运行截图
- [ ] 监控仪表盘截图
- [ ] 性能测试报告
- [ ] 安全扫描报告
- [ ] 测试覆盖率报告

---

## 评分标准

| 维度 | 权重 | 评分标准 |
|------|------|----------|
| **功能完整性** | 30% | 所有核心功能实现 |
| **技术实现** | 25% | 正确使用技术栈 |
| **代码质量** | 15% | 类型提示、文档、测试 |
| **监控告警** | 15% | 完整的监控体系 |
| **文档质量** | 10% | 完整清晰的文档 |
| **安全措施** | 5% | 基本安全防护 |

**总分**: 100 分

**及格**: 60 分
**良好**: 80 分
**优秀**: 90 分

---

## 时间规划

| 阶段 | 任务 | 预计时间 |
|------|------|----------|
| Phase 1 | 开发 Agent 功能 | 4-5 小时 |
| Phase 2 | 容器化 | 2-3 小时 |
| Phase 3 | CI/CD 配置 | 2-3 小时 |
| Phase 4 | 监控告警 | 2-3 小时 |
| Phase 5 | 安全加固 | 1-2 小时 |
| 总计 | - | 12-15 小时 |

---

## 参考资源

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

---

**开始日期**: ____
**完成日期**: ____
**最终得分**: ____/100
