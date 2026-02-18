# v3 课程映射（源文档 -> 目标章节）

## 1. 映射规则
- 以 `architect-learning-plan.md` v2 主线作为 Level 骨架
- 其它文档按四线补充：架构 / 实现 / 学习方法 / 测试
- 对冲突编号与旧路径仅保留一套 v3 编号

## 2. 主映射表

| v3 章节 | 主要来源 | 融合内容 |
|---|---|---|
| level0 | architect-learning-plan.md | Agent 基础认知、ReAct 思维 |
| level1 | architect-learning-plan.md, senior-dev-learning-plan.md | LangGraph 单 Agent 实现与工具基础 |
| level2 | architect-learning-plan.md, senior-dev-learning-plan.md | 任务规划、执行、反思与记忆系统 |
| level3 | FRAMEWORK-COMPARISON.md, NEW-FRAMEWORKS-GUIDE.md | 框架对比方法、场景选择、迁移能力 |
| level4 | architect-learning-plan.md, testing-learning-plan.md | 高级单 Agent、鲁棒性与质量策略 |
| level5 | architect-learning-plan.md, senior-dev-learning-plan.md, testing-learning-plan.md | 多 Agent 协作模式与测试 |
| level6 | architect-learning-plan.md, testing-learning-plan.md, README.md | 生产级部署、观测性、安全、CI/CD |
| level7 | architect-learning-plan.md, feynman-learning-plan.md | 前沿探索与综合项目 |

## 3. 补充来源
- `feynman-learning-plan.md`: i+1、费曼解释、类比教学、反思模板
- `FEYNMAN-UPDATE-SUMMARY.md`: 路径调整动机与框架迁移目标
- `README.md`: 快速开始、总览结构、目标用户说明

## 4. 冲突处理记录
- 已处理：`feynman-learning-plan.md` 中重复 Level 编号（Level 3/4 重复）
- 已处理：旧版 `README.md` 的 Level 0-5 主线与 v2 路径差异
- 已处理：OpenClaw/OpenCode 未确认信息，统一标记为“待确认”区
