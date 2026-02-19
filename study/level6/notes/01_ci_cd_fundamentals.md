# 01. CI/CD 基础

> **主题**: 持续集成与持续部署的核心概念
> **时间**: 60 分钟
> **难度**: ⭐⭐ 中等

---

## 🎯 学习目标

通过本节学习，你将能够：

1. ✅ 理解 CI/CD 的核心概念和价值
2. ✅ 掌握 CI/CD 流水线的基本组成
3. ✅ 了解常见的 CI/CD 工具
4. ✅ 能够设计简单的 CI/CD 流程

---

## 📚 核心概念

### 什么是 CI/CD？

**CI/CD** 是 **Continuous Integration (持续集成)** 和 **Continuous Deployment (持续部署)** 的缩写。

#### 持续集成 (CI)

**定义**: 频繁地将代码集成到主干分支，每次集成都通过自动化的构建和测试来验证。

**核心实践**:
- 代码提交频繁（每天多次）
- 自动化构建
- 自动化测试
- 快速反馈（通常 < 10 分钟）
- 保持主分支始终可部署

**为什么重要**:
```python
# 没有 CI 的情况
开发者 A 提交代码 → 2天后才发现冲突 → 浪费时间

# 有 CI 的情况
开发者 A 提交代码 → CI 自动测试 → 5分钟内发现问题 → 快速修复
```

#### 持续部署 (CD)

**定义**: 代码通过所有测试后，自动部署到生产环境。

**核心实践**:
- 部署完全自动化
- 部署频繁（每天多次）
- 零停机部署
- 快速回滚能力

**为什么重要**:
```python
# 手动部署
开发完成 → 等待发布窗口 → 手动部署 → 容易出错 → 回滚困难

# 持续部署
开发完成 → 自动测试 → 自动部署 → 出问题自动回滚
```

---

## 🏗️ CI/CD 流水线架构

### 标准流水线结构

```yaml
┌─────────────────────────────────────────────────────────────┐
│                      CI/CD Pipeline                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. 触发 (Trigger)                                           │
│     ├─ Git Push                                              │
│     ├─ Pull Request                                         │
│     └─ 定时任务                                             │
│          ↓                                                  │
│  2. 检出代码 (Checkout)                                      │
│     └─ git clone                                             │
│          ↓                                                  │
│  3. 环境准备 (Setup)                                         │
│     ├─ 安装依赖                                              │
│     └─ 配置环境                                              │
│          ↓                                                  │
│  4. 代码检查 (Lint)                                          │
│     ├─ 代码风格检查                                          │
│     ├─ 安全扫描                                              │
│     └─ 依赖检查                                              │
│          ↓                                                  │
│  5. 单元测试 (Unit Test)                                     │
│     ├─ 运行测试用例                                          │
│     ├─ 代码覆盖率                                            │
│     └─ 性能测试                                              │
│          ↓                                                  │
│  6. 构建 (Build)                                             │
│     ├─ 编译代码                                              │
│     ├─ 打包 Docker 镜像                                      │
│     └─ 生成制品                                              │
│          ↓                                                  │
│  7. 集成测试 (Integration Test)                              │
│     ├─ API 测试                                              │
│     ├─ 端到端测试                                            │
│     └─ 性能测试                                              │
│          ↓                                                  │
│  8. 部署到预发布 (Staging)                                   │
│     ├─ 部署应用                                              │
│     ├─ 冒烟测试                                              │
│     └─ 手动验证（可选）                                      │
│          ↓                                                  │
│  9. 部署到生产 (Production)                                  │
│     ├─ 蓝绿部署                                              │
│     ├─ 金丝雀发布                                            │
│     └─ 监控告警                                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 关键组件

### 1. 版本控制

**Git 工作流**:
```bash
# Feature Branch Workflow
main (生产分支)
  ↑
  └─ merge
     feature/xxx (功能分支)

# GitFlow Workflow
main (生产)
  ↑
  └─ merge
     develop (开发)
       ↑
       └─ merge
          feature/xxx (功能)
          hotfix/xxx (修复)
```

### 2. 构建工具

**常用构建工具**:
- **Maven/Gradle**: Java 项目
- **npm/yarn**: Node.js 项目
- **pip**: Python 项目
- **Docker**: 容器化构建

### 3. 测试框架

**测试类型**:
```python
# 单元测试
pytest tests/unit/

# 集成测试
pytest tests/integration/

# 端到端测试
pytest tests/e2e/

# 性能测试
locust -f tests/performance/load_test.py
```

### 4. 制品管理

**制品仓库**:
- **Docker Hub**: Docker 镜像
- **Artifactory**: 通用制品
- **Nexus**: Maven/npm 包
- **PyPI**: Python 包

---

## 🛠️ 常见 CI/CD 工具

### 1. GitHub Actions

**优势**:
- 与 GitHub 深度集成
- YAML 配置简单
- 免费额度慷慨
- 市场生态丰富

**适用场景**: 中小型项目，开源项目

### 2. GitLab CI/CD

**优势**:
- GitLab 内置功能
- 完整的 DevOps 平台
- 强大的 Docker 支持
- 自托管友好

**适用场景**: 企业级项目，需要自托管

### 3. Jenkins

**优势**:
- 高度可定制
- 插件生态丰富
- 支持复杂流程
- 成熟稳定

**适用场景**: 复杂的企业级项目

### 4. CircleCI

**优势**:
- 配置简单
- 性能优秀
- Docker 支持
- 并行执行

**适用场景**: 需要快速 CI/CD 的项目

---

## 📊 CI/CD 最佳实践

### 1. 快速反馈

**原则**: 尽快发现问题

**实践**:
```yaml
# 好的做法
- 并行运行测试
- 增量测试（只测试变更部分）
- 缓存依赖

# 避免
- 串行运行所有测试
- 每次都重新安装依赖
```

### 2. 保持简洁

**原则**: 简单的流水线更可靠

**实践**:
```yaml
# 好的做法
- 每个步骤职责单一
- 步骤数量 < 10
- 失败快速终止

# 避免
- 复杂的条件逻辑
- 过多的步骤
- 隐藏的错误处理
```

### 3. 幂等性

**原则**: 多次运行结果一致

**实践**:
```python
# 好的做法
def deploy():
    version = get_current_version()
    if version != target_version:
        deploy_version(target_version)

# 避免
def deploy():
    deploy_version(target_version)  # 可能重复部署
```

### 4. 安全优先

**原则**: 保护敏感信息

**实践**:
```yaml
# 好的做法
- 使用 Secrets 管理密钥
- 最小权限原则
- 审计日志

# 避免
- 硬编码密钥
- 使用 root 权限
```

---

## 🎯 Agent 系统的 CI/CD 特殊考虑

### 1. LLM API 调用成本

**挑战**: 每次运行都可能产生 API 成本

**解决方案**:
```python
# 使用 Mock 进行测试
@pytest.fixture
def mock_llm_response():
    return {
        "content": "Test response",
        "usage": {"total_tokens": 10}
    }

# 在 CI 中使用 Mock
def test_agent_with_mock(mock_llm_response):
    response = agent.run("test input")
    assert response == "Expected output"
```

### 2. 非确定性输出

**挑战**: 相同输入可能产生不同输出

**解决方案**:
```python
# 设置种子
import random
random.seed(42)

# 使用固定的温度参数
llm = ChatOpenAI(temperature=0)

# 断言范围而非精确值
assert 0.8 < score < 0.9
```

### 3. 工具可用性测试

**挑战**: 外部工具可能不可用

**解决方案**:
```python
# 健康检查
def test_tool_availability():
    assert tool.is_available()

# 超时设置
@pytest.mark.timeout(10)
def test_tool_response():
    result = tool.run("test")
    assert result is not None
```

---

## 💡 费曼解释

### 用简单的语言解释 CI/CD

**CI/CD 就像自动化的汽车生产线**：

1. **持续集成 (CI)**：
   - 就像汽车生产线上的质量检查站
   - 每个零件（代码）经过时，自动检查是否合格
   - 发现问题立即停止生产线，快速修复

2. **持续部署 (CD)**：
   - 就像汽车组装完成后，自动运送到展厅
   - 不需要人工搬运，自动化完成
   - 如果发现问题，可以快速召回（回滚）

**没有 CI/CD 就像**：
- 手工制造汽车，每个零件都要人工检查
- 效率低，容易出错
- 发现问题时，可能已经生产了很多有问题的车

**有 CI/CD 就像**：
- 自动化生产线，效率高，质量稳定
- 发现问题立即修复，损失最小
- 可以频繁推出新车型（新功能）

---

## ✅ 最小验证

### 验证 1: 理解 CI/CD 概念

**任务**: 用自己的话解释 CI 和 CD 的区别

**时间**: 5 分钟

**产出**:
```
CI (持续集成): 频繁集成代码，自动测试，快速反馈
CD (持续部署): 代码通过测试后，自动部署到生产
```

---

### 验证 2: 设计简单流水线

**任务**: 设计一个 Python 项目的 CI 流水线

**时间**: 10 分钟

**要求**:
- 代码检查（black, flake8）
- 单元测试（pytest）
- 覆盖率报告

**产出**:
```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint
        run: flake8 .
      - name: Test
        run: pytest --cov
```

---

### 验证 3: 解释最佳实践

**任务**: 列出 3 个 CI/CD 最佳实践并解释原因

**时间**: 5 分钟

**产出**:
```
1. 快速反馈：尽早发现问题，减少浪费
2. 保持简洁：简单的流水线更可靠
3. 幂等性：多次运行结果一致，可重复
```

---

## 🚀 下一步

- 阅读笔记 02：流水线设计模式
- 实践示例 01：简单的 CI 流水线
- 完成练习题：流水线设计练习

---

## 📚 延伸阅读

- [Continuous Integration (Martin Fowler)](https://martinfowler.com/articles/continuousIntegration.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)

---

**掌握 CI/CD 基础，构建自动化测试流水线！** 🚀
