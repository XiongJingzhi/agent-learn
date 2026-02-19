# Agent Skills 深度指南（Claude 官方定义版）

> 主题：基于 Claude Agent Skills 官方架构的正确理解与落地
> 时间：60-90 分钟
> 难度：⭐⭐⭐
> 前置：已了解 Level 1 的 StateGraph 和 Tool Calling 基础

---

## 学习目标

1. 明确 Agent Skill 的官方定义与边界。
2. 理解 Skill 与 Prompt、Tool、MCP 的关系。
3. 掌握 Skills 的文件系统架构与三级加载机制。
4. 能在项目中按规范设计可复用 Skill。

---

## 1) 什么是 Agent Skill（官方定义）

根据 Claude 官方文档，**Agent Skills 是模块化能力包**：
- 包含指令（instructions）
- 包含元数据（metadata）
- 可选包含资源与脚本（resources/scripts/templates）
- 在相关任务触发时由 Claude 自动使用

Skill 的核心不是“一个函数”，而是一个**目录化能力单元**。

---

## 2) Skill 与 Prompt / Tool / MCP 的关系

### Skill vs Prompt

- Prompt：会话级、一次性指令。
- Skill：可复用、文件系统持久化能力，按需加载。

结论：Prompt 适合临时指导，Skill 适合长期复用的领域能力。

### Skill vs Tool

- Tool：执行动作（API 调用、函数执行、数据库查询）。
- Skill：编排知识、流程、脚本与资源的能力包。

结论：Tool 可以是 Skill 内部的一部分，但 Skill 不等于 Tool。

### Skill vs MCP

- MCP：模型与外部能力通信的协议层。
- Skill：能力组织与加载机制（目录 + SKILL.md + 资源）。

结论：MCP 解决“怎么接”，Skill 解决“怎么组织和复用能力”。

---

## 3) Skills 的官方工作机制（重点）

官方关键点：Skills 运行在 Claude 可访问文件系统的执行环境中，Claude 按需读取文件并执行脚本。

### 三层内容、三级加载

#### Level 1：Metadata（总是加载）

来自 `SKILL.md` 的 YAML frontmatter，典型字段：

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files...
---
```

作用：让 Claude 知道“这个 Skill 存在、何时该用”。

#### Level 2：Instructions（触发时加载）

`SKILL.md` 正文里的流程说明、最佳实践、步骤指引。

作用：当用户任务匹配 Skill 描述时，Claude 才读取这部分进入上下文。

#### Level 3+：Resources / Scripts（按需加载）

Skill 目录可包含：
- 额外 markdown 指南
- 参考资料（schema、API 文档、模板）
- scripts（通过 bash 执行）

作用：只在引用时读取；脚本代码本体可不进入上下文，仅输出进入上下文。

---

## 4) 推荐目录结构

```text
my-skill/
├── SKILL.md
├── REFERENCE.md
├── WORKFLOWS.md
├── templates/
│   └── output_template.md
└── scripts/
    └── validate_input.py
```

`SKILL.md` 是入口文件，必须包含：
1. YAML 元数据（name/description）
2. 快速使用说明
3. 触发条件与边界
4. 引用资源与脚本的位置

---

## 5) SKILL.md 最小模板

```markdown
---
name: research-brief
description: Create evidence-based research briefs from user topics.
---

# Research Brief Skill

## When to use
- User asks for topic research, summary, or briefing.

## Workflow
1. Clarify topic and constraints.
2. Gather sources.
3. Synthesize findings into structured brief.
4. Validate output format.

## References
- See `REFERENCE.md` for citation rules.

## Scripts
- Run `scripts/validate_input.py` before final response.
```

---

## 6) 落地建议（基于官方机制）

### 6.1 以 Skill 作为能力组织单元

不要先从 Tool 出发，而是先定义 Skill：
- 这个 Skill 解决什么问题？
- 触发条件是什么？
- 输出结果的结构是什么？

然后再决定 Skill 内部需要哪些 Tool/MCP 能力。

### 6.2 先写 `SKILL.md`，再写实现

把 `SKILL.md` 当作 Skill 的“能力契约”。
推荐顺序：
1. 写 metadata（name/description）
2. 写触发条件（When to use）
3. 写边界（When NOT to use）
4. 写执行流程（Workflow）
5. 再补资源与脚本（References/Scripts）

### 6.3 用分层加载控制上下文成本

按官方分层机制组织内容：
- Metadata：短而准，便于正确触发
- Instructions：聚焦任务流程，不堆背景知识
- Resources/Scripts：按需引用，避免一次性塞入上下文

### 6.4 用脚本承载确定性步骤

对于确定性任务（格式校验、字段检查、规则校验），优先放在 `scripts/`。
这样可以：
- 降低模型自由发挥导致的漂移
- 提高结果稳定性
- 让验收标准可机器化执行

---

## 7) 最佳实践

1. **描述写“触发条件”，不是“能力宣言”**  
   `description` 要让模型能判断“什么时候该调用这个 Skill”。

2. **`SKILL.md` 保持短、准、可执行**  
   把长文档拆到资源文件；`SKILL.md` 只保留入口级信息。

3. **每个 Skill 只负责一个清晰结果**  
   避免“万能 Skill”，降低维护和测试复杂度。

4. **输出优先结构化**  
   让 Skill 输出可直接被后续步骤消费，而不是只给自然语言段落。

5. **明确“不适用场景”**  
   比“适用场景”同样重要，可显著减少误触发。

6. **资源按需加载，不预加载**  
   大型参考资料放外部文件，在流程中显式引用。

7. **脚本只做确定性工作**  
   把“规则判断、格式验证、静态检查”交给脚本，不交给模型猜。

8. **版本化 Skill**  
   对 `SKILL.md` 的关键变更记录版本与变更点，便于回滚与对比。

9. **把最小验证纳入日常回归**  
   任何 Skill 变更都要跑“触发-执行-输出”最小闭环验证。

10. **Skill 执行必须绑定沙盒策略**  
   任何会触发脚本、命令、文件读写的 Skill，都必须在受限执行环境中运行（路径白名单、网络策略、超时与资源限制、审计日志）。

---

## 8) 最小验证清单

1. 是否存在 `SKILL.md` 且有 YAML metadata。
2. 描述是否能明确触发场景（何时使用）。
3. 是否有可执行步骤（不是纯概念）。
4. 是否有资源/脚本并能按需引用。
5. 是否有边界说明（不适用场景）。
6. 若 Skill 会执行脚本，是否明确沙盒边界（允许路径/网络/资源/超时）。

---

## 9) 项目实战解读：`app/skills-agent-proto` 如何实现 Skill

这个仓库里的 `app/skills-agent-proto` 提供了一个完整的 Skill 运行原型，核心是“**三层加载 + 工具执行**”。

### 9.1 目录与入口

- Skill 发现与加载：`app/skills-agent-proto/src/langchain_skills/skill_loader.py`
- Tool 定义（含 `load_skill`、`bash`）：`app/skills-agent-proto/src/langchain_skills/tools.py`
- Agent 主体：`app/skills-agent-proto/src/langchain_skills/agent.py`
- 示例 Skill：`app/skills-agent-proto/.claude/skills/news-extractor/SKILL.md`

### 9.2 三层加载在代码里的对应关系

#### Level 1：元数据注入（启动时）

1. `SkillLoader.scan_skills()` 扫描 `.claude/skills/` 和 `~/.claude/skills/`。
2. 解析每个 `SKILL.md` 的 frontmatter（`name`、`description`）。
3. `build_system_prompt()` 把元数据注入 system prompt，模型知道“有哪些 skill 可用”。

#### Level 2：按需加载指令（触发时）

1. 用户请求命中某个 skill 描述。
2. 模型调用 tool：`load_skill(skill_name)`。
3. loader 读取该 skill 的 `SKILL.md` 正文 instructions 并返回。

#### Level 3：脚本执行（执行时）

1. 模型根据 instructions 决定执行命令。
2. 调用 `bash` tool 执行 `uv run .../scripts/*.py`。
3. 脚本输出进入上下文；脚本源码本体不进入上下文。

### 9.3 一次完整请求链路（以 news-extractor 为例）

1. 启动 Agent，system prompt 已含 `news-extractor` 的元数据。
2. 用户输入“提取这篇公众号文章...”
3. 模型调用：`load_skill("news-extractor")`
4. Agent 返回该 skill 的完整指令和脚本路径信息。
5. 模型调用：`bash("uv run .../extract_news.py URL")`
6. 解析输出文件（JSON/Markdown），生成最终回答。

### 9.4 你应该从这个实现学到什么

1. Skill 的本体是目录化能力包，不是单个函数。
2. Skill 与 Tool 分层后，能力组织更稳定、可扩展。
3. 三层加载能有效控制上下文成本：先元数据、再指令、最后执行输出。

## 10) 一句话总结

**Agent Skill 是可复用的目录化能力包，不是单个 Tool；它依赖文件系统与按需加载机制来实现高效、可扩展的能力复用。**

---

## 11) 项目实战解读：`app/PocketFlow` 如何实现 Skill

`app/PocketFlow` 需要分成两层来看：**框架核心层** 和 **cookbook 示例层**。

### 11.1 框架核心层：不内置 Skill 机制

- 核心代码在 `app/PocketFlow/pocketflow/__init__.py`，本质是极简图执行引擎。
- 它提供 `Node/Flow/Batch/Async/Parallel` 编排能力，但不提供官方 Skill 的自动发现、`SKILL.md` 元数据解析、按需加载协议。
- 结论：PocketFlow 核心是“编排骨架”，不是“内置 Skill runtime”。

### 11.2 示例层：用节点实现“技能路由 + 指令注入”

`app/PocketFlow/cookbook/pocketflow-agent-skills` 展示了一个轻量 Skill 模式：

1. `SelectSkill`（`nodes.py`）读取 `skills/*.md` 并按任务路由技能名。
2. `ApplySkill`（`nodes.py`）把技能 Markdown 注入提示词执行。
3. `flow.py` 用 `SelectSkill >> ApplySkill` 串联出最小技能流。

该实现本质是“**本地 Markdown 指令包 + 路由节点 + LLM 执行节点**”。

### 11.3 与 Claude 官方 Skill 的对照

相同点：
- 都把能力外置成可复用文档单元。
- 都支持按任务选择不同能力。

差异点（关键）：
- 官方 Skill：标准入口为 `SKILL.md`，强调 metadata + instructions + resources/scripts 的分层加载。
- PocketFlow cookbook：示例是自定义 `*.md` 技能文本注入，不是官方 `SKILL.md` 协议实现。
- 官方 Skill 语义包含“触发与按需加载机制”；PocketFlow 示例主要是“手写路由逻辑”。

### 11.4 你应掌握的工程结论

1. 用 PocketFlow 时，Skill 机制需要你自己在节点层实现。  
2. 如果要对齐官方 Skill，至少要补三件事：  
   - `SKILL.md` 元数据解析与发现  
   - 指令与资源的按需加载  
   - 脚本执行时的沙盒边界（路径/网络/超时/资源限制）  
3. PocketFlow 强在“最小编排抽象”，Skill 强在“能力组织与复用契约”，二者是互补关系。

---

## 参考

- Claude Docs: Agent Skills Overview  
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
