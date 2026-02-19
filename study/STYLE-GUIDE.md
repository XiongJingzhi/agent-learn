# Agent 学习教程写作规范

## 目录约定
- Level 命名：`level0` 到 `level6`
- 子目录：`notes/`、`exercises/`、`projects/`、`checklists/`

## 每个 Level README 固定结构
1. 学习目标
2. 前置条件
3. 核心主题（架构/实现/学习/测试）
4. 实践任务
5. 完成标准
6. 常见误区

## 文档硬约束
- 不写 Week 拆分
- 不将 `app/` 内容作为教程必修项
- 完成标准必须可验证（行为或产物）

## 术语统一
- 使用：`Agent`、`Level`、`LangGraph`、`RAG`、`多 Agent`
- 使用：`完成标准`，避免混用“毕业标准/通过标准”
- Skill/Tool/MCP 口径：
  - `Skill`：目录化能力包（`SKILL.md` + instructions + resources/scripts），按需加载
  - `Tool`：执行动作的接口/函数（API、数据库、文件操作等）
  - `MCP`：模型与外部能力通信的协议层
  - 禁止写法：`Skill = Tool` 或“Tool 就是 Skill”

## 不确定信息标注
对于 OpenClaw/OpenCode 等外部框架，统一分区：
- 已确认：已在仓库文档中有明确依据
- 待确认：缺少稳定接口或实现边界的信息

## 提交前检查
- Level 编号连续且无重复
- 每个 Level 的四类子文档存在
- README 包含“学习目标/实践任务/完成标准”
- 全文无 Week 计划
