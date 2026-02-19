# Agent Learn

一个以 Agent 工程能力为核心的学习型仓库。

当前仓库有两条主线：
- `plan/`：学习计划与方法论（为什么学、学什么、如何评估）
- `study/`：可执行教程（按 Level 拆分的 notes/exercises/projects/checklists）

`app/` 为综合案例区，不纳入主学习大纲必修路径。

## 1. 学习架构总览

### 1.1 两层架构

1. 计划层（Plan Layer）
- 目录：`plan/`
- 作用：定义学习目标、角色分工、能力演进路线
- 核心文件：
  - `plan/architect-learning-plan.md`
  - `plan/senior-dev-learning-plan.md`
  - `plan/testing-learning-plan.md`
  - `plan/testing-expert-learning-plan.md`
  - `plan/feynman-learning-plan.md`
  - `plan/feynman-mentor-learning-plan.md`

2. 执行层（Study Layer）
- 目录：`study/`
- 作用：把计划落地成逐级教程、练习和项目交付
- 核心文件：
  - `study/README.md`
  - `study/CURRICULUM-MAPPING.md`
  - `study/STYLE-GUIDE.md`

### 1.2 Level 化执行模型（当前为 Level 0-6）

每个 Level 使用统一结构：
- `README.md`：本级目标与范围
- `PROGRESS.md`：阶段推进计划
- `notes/`：知识点拆分
- `exercises/`：基础/进阶/挑战练习
- `projects/`：Capstone 项目
- `checklists/completion.md`：验收清单

## 2. 学习大纲（Level 0-6）

### Level 0：认知地图
- 目标：建立 Agent 基础认知、ReAct 循环、失败模式意识
- 重点：概念边界、最小工具集、基础环境检查
- 入口：`study/level0/README.md`

### Level 1：单 Agent 实践（LangGraph）
- 目标：实现可运行的单 Agent（状态、节点、路由、工具、短期记忆）
- 重点：节点边界、工具契约、重试与错误处理
- 入口：`study/level1/README.md`

### Level 2：任务规划型 Agent
- 目标：掌握 Planner/Executor/Reflector 架构与重规划机制
- 重点：DAG 拆解、依赖优先级、回滚恢复、可追踪日志
- 入口：`study/level2/README.md`

### Level 3：框架对比与选型
- 目标：形成框架对比、决策与迁移能力
- 重点：方法论、概念映射、选型树、迁移手册、待确认项管理
- 入口：`study/level3/README.md`

### Level 4：高级单 Agent 优化
- 目标：在质量、性能、成本之间做可验证优化
- 重点：记忆分层、Grep vs RAG、并行与缓存、性能基线
- 入口：`study/level4/README.md`

### Level 5：生产系统能力
- 目标：将 Agent 推进到可部署、可监控、可回滚
- 重点：部署策略、CI/CD、可观测性、安全与故障处理
- 入口：`study/level5/README.md`

### Level 6：生产级测试体系
- 目标：建立持续质量保证与发布门禁体系
- 重点：自动化测试、A/B 测试、监控与质量门禁
- 入口：`study/level6/README.md`

## 3. 角色视角与文件映射

### Architect（架构）
- 关注：系统分层、协作模式、生产架构
- 计划来源：`plan/architect-learning-plan.md`
- 在 study 的体现：Level 2-5 架构决策与项目交付

### Senior Dev（实现）
- 关注：框架落地、工具开发、工程实践
- 计划来源：`plan/senior-dev-learning-plan.md`
- 在 study 的体现：Level 1-4 的实现与优化主线

### Testing / Testing Expert（质量）
- 关注：测试策略、覆盖率、回归与质量门禁
- 计划来源：
  - `plan/testing-learning-plan.md`
  - `plan/testing-expert-learning-plan.md`
- 在 study 的体现：Level 2-6 的练习、项目验收、checklist

### Feynman / Feynman Mentor（学习方法）
- 关注：i+1、费曼复述、类比与反思
- 计划来源：
  - `plan/feynman-learning-plan.md`
  - `plan/feynman-mentor-learning-plan.md`
- 在 study 的体现：每个 notes 文档中的解释、验证和复盘要求

## 4. 推荐执行顺序

1. 先读计划层：
   - `plan/architect-learning-plan.md`
   - `plan/senior-dev-learning-plan.md`
   - `plan/testing-learning-plan.md`
2. 再进执行层：从 `study/level0` 按顺序到 `study/level6`
3. 每个 Level 固定流程：
   - `README.md` -> `PROGRESS.md` -> `notes/` -> `exercises/` -> `projects/` -> `checklists/completion.md`

## 5. 环境准备

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 6. 目录边界说明

- `study/`：主学习路径（本 README 的核心对象）
- `plan/`：学习设计来源与方法论
- `app/`：综合案例区（参考，不纳入主路径）
