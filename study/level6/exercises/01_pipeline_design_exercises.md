# 流水线设计练习题

> **主题**: CI/CD 流水线设计
> **题数**: 10 题
> **时间**: 2 小时
> **难度**: ⭐⭐⭐ 中高级

---

## 练习题

### 问题 1: 基础概念

**题目**: 以下哪些是持续集成（CI）的核心实践？

A. 频繁提交代码
B. 自动化测试
C. 手动部署
D. 快速反馈

**答案**: A, B, D

**解析**:
- ✅ A: CI 要求频繁集成代码（通常每天多次）
- ✅ B: 自动化测试是 CI 的核心
- ❌ C: 手动部署是 CI 的反面，CI 强调自动化
- ✅ D: 快速反馈是 CI 的目标（通常 < 10 分钟）

---

### 问题 2: 流水线设计

**题目**: 设计一个 Python Agent 项目的 CI 流水线，包含以下步骤：

1. 代码检出
2. 安装依赖
3. 代码格式检查
4. 类型检查
5. 单元测试
6. 覆盖率报告

请用 GitHub Actions YAML 格式写出配置文件。

**答案**:
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: 安装依赖
        run: |
          pip install -r requirements.txt
          pip install black mypy pytest pytest-cov

      - name: 代码格式检查
        run: black --check .

      - name: 类型检查
        run: mypy .

      - name: 运行测试
        run: pytest --cov=. --cov-report=xml
```

**评分标准**:
- 包含所有 6 个步骤 (30%)
- 使用正确的 Action 版本 (20%)
- 依赖安装正确 (20%)
- 测试命令正确 (30%)

---

### 问题 3: 缓存优化

**题目**: 如何优化 CI 流水线以减少依赖安装时间？

**答案**:
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'  # 使用缓存

- name: 安装依赖
  run: pip install -r requirements.txt
```

**解析**:
- 使用 `cache: 'pip'` 自动缓存依赖
- 后续运行可以直接使用缓存，大幅提速

**额外加分项**:
- 使用 `requirements.txt` 的哈希作为缓存键
- 分离开发依赖和生产依赖

---

### 问题 4: 并行执行

**题目**: 如何在不同操作系统上并行运行测试？

**答案**:
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: 运行测试
        run: pytest tests/
```

**解析**:
- 使用 `matrix` 策略并行运行
- 总共 9 个并行任务（3 OS × 3 Python 版本）

---

### 问题 5: 条件执行

**题目**: 如何只在 `main` 分支上部署，其他分支只测试？

**答案**:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 运行测试
        run: pytest tests/

  deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - name: 部署
        run: echo "部署到生产环境"
```

**解析**:
- 使用 `if` 条件限制部署任务
- 使用 `needs` 确保测试通过后才部署

---

### 问题 6: 密钥管理

**题目**: 如何在 CI 中安全使用 OpenAI API 密钥？

**答案**:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 运行测试
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          pytest tests/
          # 或使用 export
          export OPENAI_API_KEY="${{ secrets.OPENAI_API_KEY }}"
          python test_agent.py
```

**解析**:
- 在 GitHub 仓库设置中添加 Secret
- 在 YAML 中通过 `${{ secrets.SECRET_NAME }}` 引用
- 不要在日志中打印密钥

---

### 问题 7: 失败快速终止

**题目**: 如何配置流水线，任何一步失败立即停止？

**答案**:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: 步骤 1
        run: echo "步骤 1"

      - name: 步骤 2
        run: exit 1  # 模拟失败

      - name: 步骤 3  # 不会执行
        if: success()  # 显式检查
        run: echo "步骤 3"
```

**解析**:
- GitHub Actions 默认任何步骤失败会终止
- 可以使用 `if: failure()` 或 `if: success()` 控制执行

---

### 问题 8: 测试矩阵

**题目**: 如何测试 Agent 在不同 LLM 上的表现？

**答案**:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        llm: ['gpt-4', 'gpt-3.5-turbo', 'claude-3-opus']

    steps:
      - name: 测试 ${{ matrix.llm }}
        env:
          LLM_MODEL: ${{ matrix.llm }}
        run: |
          pytest tests/test_agents.py \
            --llm-model=${{ matrix.llm }}
```

**解析**:
- 使用矩阵策略并行测试不同 LLM
- 每个任务使用不同的环境变量

---

### 问题 9: 制品管理

**题目**: 如何保存测试报告和覆盖率报告？

**答案**:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 运行测试
        run: |
          pytest --cov=. --cov-report=html --cov-report=xml
          mv htmlcov/ coverage-report/

      - name: 上传报告
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: |
            coverage-report/
            coverage.xml
          retention-days: 30
```

**解析**:
- 使用 `upload-artifact` Action
- 可以上传多个文件和目录
- 设置保留时间节省存储

---

### 问题 10: 性能测试

**题目**: 如何在 CI 中运行 Agent 性能测试？

**答案**:
```yaml
jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 安装依赖
        run: |
          pip install locust

      - name: 运行负载测试
        run: |
          locust -f tests/performance/locustfile.py \
            --headless \
            --users 10 \
            --spawn-rate 1 \
            --run-time 30s \
            --html performance-report.html \
            --csv performance

      - name: 上传性能报告
        uses: actions/upload-artifact@v3
        with:
          name: performance-report
          path: |
            performance-report.html
            performance_stats.csv

      - name: 检查性能阈值
        run: |
          # 检查响应时间是否超过阈值
          avg_response_time=$(python -c "
          import pandas as pd
          df = pd.read_csv('performance_stats.csv')
          print(df['Request Response Time'].mean())
          ")

          if (( $(echo "$avg_response_time > 2000" | bc -l) )); then
            echo "响应时间超过阈值: ${avg_response_time}ms"
            exit 1
          fi
```

**解析**:
- 使用 Locust 进行负载测试
- 生成 HTML 和 CSV 报告
- 检查性能指标是否符合阈值

---

## 评分标准

- **90-100%**: 优秀（完全掌握）
- **80-89%**: 良好（基本掌握）
- **70-79%**: 及格（需要复习）
- **< 70%**: 不及格（需要重新学习）

---

## 自我评估

完成练习后，请回答：

1. ✅ 能够独立设计 CI/CD 流水线
2. ✅ 理解流水线优化的方法
3. ✅ 能够处理密钥和敏感信息
4. ✅ 能够配置并行执行
5. ✅ 能够生成和保存测试报告

---

## 延伸练习

1. **优化流水线速度**: 当前流水线需要 10 分钟，如何优化到 5 分钟以内？
2. **多环境部署**: 设计支持 dev、staging、production 三个环境的流水线
3. **回滚机制**: 实现自动回滚的部署流水线

---

**完成这些练习，掌握 CI/CD 流水线设计！** 🚀
