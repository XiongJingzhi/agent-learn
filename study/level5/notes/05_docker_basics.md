# 05 Docker 基础

> **主题**: 掌握 Docker 容器化部署的基础知识
> **时间**: 40 分钟
> **难度**: ⭐⭐⭐

---

## 学习目标

完成本笔记后，你将能够：

1. 理解 Docker 的核心概念
2. 能够编写 Dockerfile
3. 能够构建和运行 Docker 镜像
4. 能够使用 Docker Compose 编排多容器应用

---

## 核心概念

### 什么是 Docker？

**Docker** 是一个开源的容器化平台，可以将应用及其依赖打包到一个轻量级、可移植的容器中。

**对比虚拟机**:
```
虚拟机：
┌─────────────────────────────────────┐
│         Hypervisor                  │
├──────────┬──────────┬───────────────┤
│   VM 1   │   VM 2   │    VM 3       │
│ ┌──────┐ │ ┌──────┐ │ ┌──────────┐ │
│ │Guest │ │ │Guest │ │ │  Guest   │ │
│ │ OS   │ │ │ OS   │ │ │   OS     │ │
│ ├──────┤ │ ├──────┤ │ ├──────────┤ │
│ │App 1 │ │ │App 2 │ │ │  App 3   │ │
│ └──────┘ │ └──────┘ │ └──────────┘ │
└──────────┴──────────┴───────────────┘

Docker：
┌─────────────────────────────────────┐
│         Docker Engine               │
├──────────┬──────────┬───────────────┤
│ Container│ Container│  Container    │
│ ┌──────┐ │ ┌──────┐ │ ┌──────────┐ │
│ │App 1 │ │ │App 2 │ │ │  App 3   │ │
│ └──────┘ │ └──────┘ │ └──────────┘ │
└──────────┴──────────┴───────────────┘
```

**优势**:
- **轻量级**：共享主机内核，无需完整 OS
- **快速启动**：秒级启动 vs 分钟级启动
- **环境一致**：开发、测试、生产环境一致
- **易于分发**：镜像可以在任何地方运行

---

### Docker 核心概念

#### 1. 镜像（Image）

**定义**: 只读的应用模板，包含运行应用所需的一切。

**特点**:
- 分层存储（Layered）
- 只读不可变
- 可以继承（基于基础镜像）

**示例**:
```bash
# 官方镜像
python:3.11-slim
nginx:latest
postgres:15-alpine

# 自定义镜像
my-agent:v1.0
my-agent:latest
```

#### 2. 容器（Container）

**定义**: 镜像的运行实例，可以启动、停止、删除。

**特点**:
- 可写层（在镜像之上）
- 隔离的文件系统
- 独立的进程空间

**示例**:
```bash
# 运行容器
docker run -d -p 8000:8000 my-agent:v1.0

# 查看容器
docker ps
docker logs <container_id>

# 停止容器
docker stop <container_id>
```

#### 3. Dockerfile

**定义**: 构建镜像的脚本文件。

**示例**:
```dockerfile
# 基础镜像
FROM python:3.11-slim

# 工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 编写 Dockerfile

### 基础模板

```dockerfile
# ============================================
# 阶段 1: 构建
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装依赖
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# ============================================
# 阶段 2: 运行
# ============================================
FROM python:3.11-slim

WORKDIR /app

# 从构建阶段复制依赖
COPY --from=builder /root/.local /root/.local

# 复制应用代码
COPY . .

# 设置环境变量
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 最佳实践

#### 1. 使用 .dockerignore

```text
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.git
.gitignore
venv/
.env
.venv
node_modules/
*.md
tests/
.pytest_cache/
```

**作用**: 排除不必要的文件，减少镜像大小和构建时间。

#### 2. 多阶段构建

```dockerfile
# 构建阶段
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 运行阶段
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
...
```

**优势**: 最终镜像只包含运行时需要的文件，大幅减小镜像大小。

#### 3. 利用构建缓存

```dockerfile
# ✅ 好的顺序
COPY requirements.txt .
RUN pip install -r requirements.txt  # 这层会缓存
COPY . .  # 代码变化不会影响上面的层

# ❌ 不好的顺序
COPY . .
RUN pip install -r requirements.txt  # 代码变化会重新安装依赖
```

#### 4. 最小化镜像

```dockerfile
# ✅ 使用 alpine 版本（更小）
FROM python:3.11-alpine

# ✅ 使用 slim 版本（平衡大小和兼容性）
FROM python:3.11-slim

# ❌ 避免使用完整版本
FROM python:3.11
```

#### 5. 安全性

```dockerfile
# ✅ 使用非 root 用户
RUN useradd -m appuser
USER appuser

# ✅ 不在镜像中存储敏感信息
# 使用环境变量或 secrets
ENV API_KEY=""  # 运行时传入

# ❌ 避免硬编码密钥
ENV API_KEY="sk-xxxxx"
```

---

### 常用指令

| 指令 | 说明 | 示例 |
|------|------|------|
| `FROM` | 基础镜像 | `FROM python:3.11` |
| `WORKDIR` | 工作目录 | `WORKDIR /app` |
| `COPY` | 复制文件 | `COPY . .` |
| `ADD` | 复制文件（支持 URL 和解压） | `ADD app.tar.gz /app` |
| `RUN` | 执行命令 | `RUN pip install -r requirements.txt` |
| `CMD` | 默认命令 | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | 入口点 | `ENTRYPOINT ["python"]` |
| `ENV` | 环境变量 | `ENV PORT=8000` |
| `EXPOSE` | 暴露端口 | `EXPOSE 8000` |
| `VOLUME` | 挂载点 | `VOLUME /data` |

---

## Docker Compose

### 基础配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Agent 服务
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agent
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  # 数据库
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=agent
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  # 缓存
  redis:
    image: redis:7-alpine
    restart: unless-stopped

  # 监控
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

volumes:
  postgres_data:
```

### 常用命令

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f agent

# 重启服务
docker-compose restart agent

# 停止所有服务
docker-compose down

# 查看状态
docker-compose ps

# 执行命令
docker-compose exec agent bash
```

---

## 费曼解释

### 用简单的语言解释

**问题**: 什么是 Docker？

**类比**: 想象你在搬家：

**传统方式（虚拟机）**:
- 每次搬家都要把整个房子一起搬（完整的操作系统）
- 包括家具、电器、装修（所有依赖）
- 非常重、很慢、很贵

**Docker 方式（容器）**:
- 只把你的行李打包（应用 + 依赖）
- 到了新地方找一间空房子（共享操作系统内核）
- 轻松、快速、便宜

**核心**: Docker 就像是"行李箱"，把你的应用打包好，可以在任何地方（任何服务器）运行，不用担心环境问题。

---

## 最小验证

### 任务 1: 编写 Dockerfile

为一个简单的 FastAPI Agent 编写 Dockerfile：

```python
# main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Agent!"}

# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

**任务**: 编写 Dockerfile 并构建镜像

```bash
docker build -t my-agent:v1 .
docker run -p 8000:8000 my-agent:v1
```

**验证**: 访问 http://localhost:8000

### 任务 2: 使用 Docker Compose

创建一个包含 Agent 和 Redis 的 docker-compose.yml：

```yaml
version: '3.8'
services:
  agent:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**验证**: 启动并检查服务是否正常

### 任务 3: 优化镜像大小

测量优化前后的镜像大小：

```bash
# 查看镜像大小
docker images

# 优化策略
# 1. 使用 alpine 基础镜像
# 2. 多阶段构建
# 3. 清理缓存
```

**验证**: 对比优化前后的大小

---

## 常见问题

### Q1: 容器和虚拟机有什么区别？

**A**:
- **容器**：共享主机内核，轻量级，快速启动
- **虚拟机**：完整的操作系统，重量级，慢启动

### Q2: 什么时候用 Docker，什么时候不用？

**A**:
- **适合**：微服务、CI/CD、环境一致性
- **不适合**：简单应用、桌面应用、需要硬件访问

### Q3: 如何调试 Docker 容器？

**A**:
```bash
# 查看日志
docker logs <container_id>

# 进入容器
docker exec -it <container_id> bash

# 查看容器详情
docker inspect <container_id>
```

---

## 总结

### 关键要点

1. **Docker 三大核心**：镜像、容器、Dockerfile
2. **最佳实践**：多阶段构建、缓存优化、安全加固
3. **Docker Compose**：多容器编排的利器
4. **环境一致性**：开发、测试、生产保持一致

### 下一步

- 学习 Kubernetes 部署
- 学习 CI/CD 集成
- 学习容器安全

---

## 参考资源

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**完成时间**: ____
**验证状态**: ⏳ 待完成
