# Level 1 Skills 内容补充报告（官方定义对齐）

> 补充日期：2025-01-19  
> 更新日期：2026-02-19  
> 状态：✅ 已对齐 Claude Agent Skills 官方定义

---

## 本次修订目标

将 Level 1 中关于 Skills 的表述从“Tools/Skills 混称”修正为官方口径：
- Skill 是目录化能力包（`SKILL.md` + 资源 + 脚本）
- Tool 是执行动作，不等于 Skill
- MCP 是协议层，不等于 Skill

---

## 修订文件

| 文件 | 调整类型 | 结果 |
|---|---|---|
| `notes/08_agent_skills_deep_dive.md` | 重写 | ✅ 已按官方架构重写 |
| `notes/09_mcp_tools_guide.md` | 补充边界说明 | ✅ 增加 MCP Tool 与 Skill 区分 |

---

## 新版 Skills 核心定义

1. Skill 是可复用能力包，而不是单个函数。
2. Skill 由文件系统目录承载，入口是 `SKILL.md`。
3. Skill 采用分层加载：
   - Metadata（总是加载）
   - Instructions（触发时加载）
   - Resources/Scripts（按需加载）
4. Tool 可被 Skill 使用，但 Tool 不构成 Skill 全部。

---

## 为什么要修订

旧版内容把 Skills 主要讲成 Tool/Function Calling 封装，容易导致：
- 设计时只关注调用，不关注能力组织
- 无法复用长期知识与模板
- 难以实现低上下文成本的按需加载

新版对齐后，学习者可以把“能力工程”与“执行动作”分层思考。

---

## 对学习路径的影响

- Level 1：从“会调工具”升级为“会设计可复用 Skill”。
- Level 2+：可在规划和协作中复用稳定 Skill 包。
- Level 5+：可把 Skill 作为生产能力单元进行治理与版本化。

---

## 参考

- Claude Docs: Agent Skills Overview  
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
