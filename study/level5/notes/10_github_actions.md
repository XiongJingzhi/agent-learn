# 10 GitHub Actions

> **主题**: 使用 GitHub Actions 实现 CI/CD
> **时间**: 50 分钟
> **难度**: ⭐⭐⭐

---

## 学习目标

完成本笔记后，你将能够：

1. 理解 CI/CD 的概念和价值
2. 掌握 GitHub Actions 的基础语法
3. 能够配置自动化测试流水线
4. 能够配置自动化部署流水线

---

## 核心概念

### 什么是 CI/CD？

**CI (Continuous Integration - 持续集成)**
- 频繁地将代码集成到主干
- 每次集成自动运行测试
- 尽早发现集成问题

**CD (Continuous Deployment - 持续部署)**
- 自动将通过测试的代码部署到生产环境
- 减少手动操作，降低错误
- 快速交付功能给用户

### GitHub Actions 组成

```
Workflow (工作流)
  └─ Job (任务)
      └─ Step (步骤)
          └─ Action (动作)
```

**示例**:
```yaml
# Workflow
name: CI/CD Pipeline

on:
  push:
    branches: [main]

# Job
jobs:
  test:
    # Step
    steps:
      - uses: actions/checkout@v3  # Action
      - name: Run tests
        run: pytest
```

---

## Workflow 语法

### 基本结构

```yaml
# Workflow 名称
name: Build and Test

# 触发条件
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # 每天 00:00 运行

# 环境变量
env:
  PYTHON_VERSION: '3.11'

# 任务
jobs:
  # 任务 1
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### 关键字说明

| 关键字 | 说明 | 示例 |
|--------|------|------|
| `name` | Workflow 或 Job 的名称 | `name: CI Pipeline` |
| `on` | 触发条件 | `on: [push, pull_request]` |
| `env` | 环境变量 | `env: VAR=value` |
| `jobs` | 任务列表 | `jobs: { build: {...} }` |
| `runs-on` | 运行环境 | `runs-on: ubuntu-latest` |
| `steps` | 步骤列表 | `steps: [{...}]` |
| `uses` | 使用 Action | `uses: actions/checkout@v3` |
| `run` | 运行命令 | `run: pytest` |
| `with` | Action 参数 | `with: {python-version: '3.11'}` |
| `secrets` | 密钥 | `secrets: {...}` |

---

## 常用 Actions

### Checkout 代码

```yaml
- name: Checkout code
  uses: actions/checkout@v3
  with:
    fetch-depth: 0  # 获取完整历史
```

### 设置语言环境

```yaml
# Python
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'

# Node.js
- name: Set up Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '18'
    cache: 'npm'
```

### 缓存依赖

```yaml
# 缓存 pip 依赖
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# 缓存 Docker 镜像
- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-
```

---

## 完整示例

### CI 流水线

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'

jobs:
  # 代码检查
  lint:
    name: Lint
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install black flake8 mypy pylint

      - name: Run Black
        run: black --check .

      - name: Run Flake8
        run: flake8 .

      - name: Run MyPy
        run: mypy .

  # 单元测试
  test:
    name: Test
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
        run: |
          pytest \
            --cov=. \
            --cov-report=xml \
            --cov-report=html \
            --junitxml=test-results.xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results.xml
          if-no-files-found: ignore

  # 安全扫描
  security:
    name: Security Scan
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### CD 流水线

```yaml
# .github/workflows/deploy.yml
name: CD

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'tests/**'
      - 'requirements.txt'
      - 'Dockerfile'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 构建并推送 Docker 镜像
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # 部署到生产环境
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: production
      url: https://api.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster my-cluster \
            --service my-service \
            --force-new-deployment

      - name: Verify deployment
        run: |
          # 等待服务启动
          sleep 30

          # 健康检查
          curl -f https://api.example.com/health || exit 1

      - name: Notify deployment success
        if: success()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployment to production successful! 🚀'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 高级用法

### 矩阵构建

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run tests
        run: pytest
```

### 条件执行

```yaml
steps:
  - name: Deploy to production
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    run: ./deploy.sh

  - name: Run on failure
    if: failure()
    run: ./notify-failure.sh

  - name: Run on success
    if: success()
    run: ./notify-success.sh
```

### 并行和串行

```yaml
jobs:
  # 并行执行
  test-a:
    runs-on: ubuntu-latest
    steps: [...]

  test-b:
    runs-on: ubuntu-latest
    steps: [...]

  # 串行执行（依赖 test-a 和 test-b）
  deploy:
    runs-on: ubuntu-latest
    needs: [test-a, test-b]
    steps: [...]
```

### 复用 Workflow

```yaml
# .github/workflows/reusable-ci.yml
name: Reusable CI

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ inputs.python-version }}
      - run: pytest

# 调用
# .github/workflows/main.yml
name: Main CI

on: [push]

jobs:
  call-reusable:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      python-version: '3.11'
```

---

## 费曼解释

### 用简单的语言解释

**问题**: 什么是 CI/CD？

**类比**: 想象你在开餐厅：

**没有 CI/CD**:
1. 厨师每天做完一道菜，才检查味道
2. 如果味道不对，整道菜都要重做
3. 顾客等待时间长，经常吃到不好吃的菜

**有 CI**:
1. 厨师每加一个调料，就尝一下味道
2. 如果味道不对，立即调整
3. 顾客能更快吃到好吃的菜

**有 CD**:
1. 厨师做好菜，服务员自动端给顾客
2. 不需要人工操作，快速高效
3. 顾客立即能吃到新鲜菜品

**核心**: CI/CD 就是自动化检查和部署，让代码像流水线一样快速、安全地交付给用户。

---

## 最小验证

### 任务 1: 创建 CI Workflow

为项目创建 `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

**验证**: Push 代码到 GitHub，查看 Actions 运行

### 任务 2: 添加测试覆盖率

在 CI 中添加覆盖率报告：

```yaml
- name: Run tests with coverage
  run: pytest --cov=. --cov-report=xml

- name: Upload to Codecov
  uses: codecov/codecov-action@v3
```

**验证**: 检查 Codecov 上的覆盖率报告

### 任务 3: 配置自动部署

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to server
        run: |
          echo "Deploying..."
          # 添加实际的部署命令
```

**验证**: 合并到 main 分支，触发部署

---

## 常见问题

### Q1: 如何在 GitHub Actions 中使用密钥？

**A**: 在仓库设置中添加 Secret，然后在 Workflow 中引用：

```yaml
env:
  API_KEY: ${{ secrets.MY_API_KEY }}
```

### Q2: 如何调试失败的 Workflow？

**A**:
1. 查看 Actions 日志
2. 使用 `tmate` action 调试
3. 在本地使用 `act` 运行 Workflow

### Q3: GitHub Actions 免费吗？

**A**:
- **公开仓库**: 完全免费
- **私有仓库**: 每月 2000 分钟免费
- **超出部分**: 按使用量付费

---

## 总结

### 关键要点

1. **CI/CD 价值**: 快速发现错误，快速交付功能
2. **GitHub Actions**: 强大的 CI/CD 平台
3. **Workflow 核心**: jobs → steps → actions
4. **最佳实践**: 自动化一切，包括测试、构建、部署

### 下一步

- 学习部署策略
- 学习监控告警
- 学习灰度发布

---

## 参考资源

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Starter Workflows](https://github.com/actions/starter-workflows)
- [Awesome Actions](https://github.com/sdras/awesome-actions)

---

**完成时间**: ____
**验证状态**: ⏳ 待完成
