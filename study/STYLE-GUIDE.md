# Agent 学习体系 v3 写作规范

## 1. 目录与命名
- Level 目录命名：`level0` 到 `level7`
- 文件命名：
  - 概览：`README.md`
  - 笔记：`notes/NN_topic.md`
  - 练习：`exercises/NN_topic_exercises.md`
  - 项目：`projects/NN_project_name.md`
  - 验收：`checklists/completion.md`

## 2. 每个 Level README 固定结构
1. 学习目标
2. 前置条件
3. 核心主题（按架构/实现/学习方法/测试四线）
4. 实践任务
5. 完成标准
6. 常见误区

约束：
- 不出现 Week 计划或周拆分
- 用可验证结果描述“完成标准”
- 任务描述尽量可执行、可检查

## 3. 术语统一
- 统一使用：`Agent`、`Level`、`LangGraph`、`RAG`
- 统一使用：`多 Agent`（不混用“多智能体”作为主称）
- 统一使用：`完成标准`（不混用“验收条件/毕业标准”）

## 4. 不确定信息写法
对未确认内容必须分区：
- 已确认：来自现有文档的可落实能力
- 待确认：需要后续补充或校验的能力

模板：
```markdown
### OpenClaw（已确认）
- ...

### OpenClaw（待确认）
- [占位] ...
```

## 5. 质量检查
提交前至少检查：
- Level 编号是否连续且不重复
- 目录链接是否有效
- 每个 Level README 是否包含“目标/任务/完成标准”
- 文档中是否出现 Week 计划
