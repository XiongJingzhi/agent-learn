# LangChain Skills Agent 快速参考指南

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| [架构分析](./langchain_skills_architecture_analysis.md) | 完整的架构和工作流程分析 |
| [流程图](./langchain_skills_workflow_diagrams.md) | Mermaid 序列图和流程图 |
| **快速参考** (本文档) | 常用命令和代码片段 |

---

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone <repo-url>
cd skills-agent-proto

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 API Key
```

### 基本使用

```bash
# 列出可用的 Skills
uv run langchain-skills --list-skills

# 显示 System Prompt
uv run langchain-skills --show-prompt

# 单次执行
uv run langchain-skills "你的问题"

# 交互式模式
uv run langchain-skills --interactive
```

---

## 💻 Python API

### 基本用法

```python
from langchain_skills import LangChainSkillsAgent

# 创建 Agent
agent = LangChainSkillsAgent()

# 同步调用
result = agent.invoke("列出当前目录的文件")
print(agent.get_last_response(result))

# 流式调用
for event in agent.stream_events("列出当前目录的文件"):
    event_type = event.get("type")
    if event_type == "text":
        print(event.get("content"), end="")
    elif event_type == "tool_call":
        print(f"\n[调用工具] {event.get('name')}")
```

### 高级配置

```python
from pathlib import Path
from langchain_skills import LangChainSkillsAgent

# 自定义配置
agent = LangChainSkillsAgent(
    model="claude-opus-4-5-20251101",      # 模型选择
    skill_paths=[                          # Skills 路径
        Path.cwd() / ".claude" / "skills",
        Path("/custom/skills/path")
    ],
    working_directory=Path.cwd(),          # 工作目录
    enable_thinking=True,                  # 启用 Extended Thinking
    thinking_budget=10000,                 # Thinking token 预算
)

# 查看发现的 Skills
skills = agent.get_discovered_skills()
for skill in skills:
    print(f"- {skill['name']}: {skill['description']}")
```

### 手动加载 Skill

```python
from langchain_skills import SkillLoader

loader = SkillLoader()

# 扫描所有 Skills
skills = loader.scan_skills()
print(f"发现 {len(skills)} 个 Skills")

# 加载特定 Skill
skill = loader.load_skill("news-extractor")
if skill:
    print(f"名称: {skill.metadata.name}")
    print(f"描述: {skill.metadata.description}")
    print(f"指令:\n{skill.instructions}")
```

---

## 🛠️ 创建自定义 Skill

### 目录结构

```
.my-skill/
├── SKILL.md          # 必需
├── scripts/          # 可选
│   └── script.py
├── references/       # 可选
│   └── doc.md
└── assets/           # 可选
    └── template.txt
```

### SKILL.md 模板

```markdown
---
name: my-skill
description: 简短描述何时使用此 skill
---

# Skill 标题

## 使用场景

当用户需要...时使用此 skill。

## 使用步骤

1. 第一步
2. 第二步
3. 第三步

## 示例

**输入**:
```
用户输入示例
```

**输出**:
```
期望输出示例
```

## 注意事项

- 重要提示
- 常见错误
```

### 示例：简单的文件处理 Skill

```markdown
---
name: file-processor
description: 批量处理文本文件，支持查找、替换、格式化等操作
---

# File Processor Skill

## 功能

此 skill 用于批量处理文本文件，支持：
- 查找并替换文本
- 格式化代码
- 提取特定行

## 使用方法

1. 使用 `glob` 工具查找目标文件
2. 使用 `read_file` 读取文件内容
3. 处理内容
4. 使用 `write_file` 写入结果

## 示例命令

```bash
# 查找所有 Python 文件
glob "**/*.py"

# 读取文件
read_file "src/main.py"

# 写入文件
write_file "output.txt" "content"
```
```

---

## 📊 工具参考

### 可用工具列表

| 工具名 | 功能 | 示例 |
|-------|------|------|
| `load_skill` | 加载 Skill 详细指令 | `load_skill("news-extractor")` |
| `bash` | 执行 shell 命令 | `bash("ls -la")` |
| `read_file` | 读取文件内容 | `read_file("file.txt")` |
| `write_file` | 写入文件 | `write_file("out.txt", "内容")` |
| `glob` | 文件模式匹配 | `glob("**/*.py")` |
| `grep` | 搜索文件内容 | `grep("TODO", ".")` |
| `edit` | 替换文件内容 | `edit("f.txt", "old", "new")` |
| `list_dir` | 列出目录内容 | `list_dir(".")` |

### 工具使用示例

#### 1. load_skill

```python
# Agent 会自动调用
load_skill("news-extractor")

# 返回
"""
# Skill: news-extractor

## Instructions
当用户需要提取新闻内容时...

## Skill Path Info
- **Skill Directory**: `/path/to/news-extractor`
- **Scripts Directory**: `/path/to/news-extractor/scripts`
"""
```

#### 2. bash

```python
# 执行命令
bash("ls -la")

# 返回
"""
[OK]

total 16
drwxr-xr-x  4 user  staff   128 Feb 14 10:00 .
drwxr-xr-x  5 user  staff   160 Feb 14 10:00 ..
-rw-r--r--  1 user  staff    50 Feb 14 10:00 file.txt
"""

# 执行失败
bash("invalid-command")

# 返回
"""
[FAILED] Exit code: 127

--- stderr ---
bash: invalid-command: command not found
"""
```

#### 3. glob

```python
# 查找 Python 文件
glob("**/*.py")

# 返回
"""
[OK]

src/main.py
src/utils.py
tests/test_main.py
"""

# 查找 Markdown 文件
glob("docs/**/*.md")

# 返回
"""
[OK]

docs/index.md
docs/guide.md
docs/api/reference.md
"""
```

#### 4. grep

```python
# 搜索 TODO
grep("TODO", ".")

# 返回
"""
[OK]

src/main.py:10: # TODO: implement feature X
src/utils.py:25: # TODO: add error handling
"""

# 搜索函数定义
grep("^def ", ".")

# 返回
"""
[OK]

src/main.py:1: def main():
src/utils.py:1: def helper():
"""
```

---

## 🔧 配置参考

### 环境变量

```bash
# .env 文件
ANTHROPIC_API_KEY=sk-ant-xxx...
ANTHROPIC_AUTH_TOKEN=sk-xxx...

# 第三方代理（可选）
ANTHROPIC_BASE_URL=https://api.example.com/anthropic

# 模型配置
CLAUDE_MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=16000

# 权限模式
PERMISSION_MODE=default  # | acceptEdits | bypassPermissions
```

### 支持的模型

#### Anthropic 模型（推荐）

| 模型 | Provider | Extended Thinking |
|------|----------|-------------------|
| `claude-sonnet-4-5-20250929` | anthropic | ✅ |
| `claude-opus-4-5-20251101` | anthropic | ✅ |
| `claude-3-5-sonnet-20241022` | anthropic | ✅ |

#### OpenAI 兼容模型

| 模型 | Provider | Extended Thinking |
|------|----------|-------------------|
| `glm-4.7` | openai | ❌ |
| `gpt-4o` | openai | ❌ |

---

## 🐛 调试技巧

### 启用调试模式

```bash
# 设置环境变量
export SKILLS_DEBUG=1

# 运行
uv run langchain-skills "你的问题"
```

**调试输出**:
```
[DEBUG] Event: AIMessageChunk
[DEBUG] Yielding: thinking
[DEBUG] Thinking: 用户想提取文章...
[DEBUG] Yielding: tool_call
[DEBUG] Tool Call: load_skill(news-extractor)
[DEBUG] Processing tool result
```

### 查看 System Prompt

```bash
uv run langchain-skills --show-prompt
```

**输出**:
```
## Available Skills

You have access to the following specialized skills:

- **news-extractor**: 新闻站点内容提取...
- **humanizer**: Remove signs of AI-generated writing...

### How to Use Skills
1. **Discover**: Review the skills list above
2. **Load**: When a user request matches a skill's description...
```

### Python 调试

```python
import logging

# 启用详细日志
logging.basicConfig(level=logging.DEBUG)

agent = LangChainSkillsAgent()

# 查看内部状态
print(f"System Prompt: {agent.get_system_prompt()}")
print(f"Discovered Skills: {agent.get_discovered_skills()}")
```

---

## 📝 常见问题

### Q1: Skill 没有被发现？

**检查**:
```bash
# 列出发现的 Skills
uv run langchain-skills --list-skills

# 检查目录结构
ls -la .claude/skills/

# 检查 SKILL.md 格式
cat .claude/skills/my-skill/SKILL.md
```

**要求**:
- SKILL.md 必须存在
- 必须包含 YAML frontmatter（`name` 和 `description`）
- Skill 目录必须在 `.claude/skills/` 下

### Q2: 工具调用失败？

**常见原因**:
1. 路径错误 → 使用绝对路径
2. 权限不足 → 检查文件权限
3. 命令不存在 → 检查命令是否安装

**解决**:
```python
# 使用绝对路径
bash("uv run /absolute/path/to/script.py")

# 检查权限
bash("ls -la /path/to/file")

# 测试命令
bash("which python3")
```

### Q3: Extended Thinking 不工作？

**检查**:
```python
# 模型是否支持
is_glm = agent.model_name.startswith("glm")
if is_glm:
    print("GLM 模型不支持 Extended Thinking")

# 温度是否正确
if agent.enable_thinking:
    print(f"温度应为 1.0，当前: {agent.temperature}")
```

### Q4: 流式输出卡住？

**可能原因**:
1. 网络问题
2. API 超时
3. 工具执行时间过长

**解决**:
```bash
# 检查网络
ping api.anthropic.com

# 设置超时（代码中）
result = subprocess.run(..., timeout=300)

# 使用更快的模型
CLAUDE_MODEL=claude-sonnet-4-5-20250929
```

---

## 🎯 最佳实践

### 1. Skill 设计

✅ **推荐**:
- 清晰的 `description`（让 LLM 知道何时使用）
- 详细的步骤说明
- 提供示例命令
- 包含错误处理

❌ **避免**:
- 模糊的描述
- 过长的指令（>10k tokens）
- 硬编码路径

### 2. 工具使用

✅ **推荐**:
```python
# 使用绝对路径
bash(f"uv run {skill_path}/script.py")

# 检查文件是否存在
bash(f"test -f {file_path} && echo 'exists'")

# 组合命令
bash("cd /path && ls -la | grep '.py'")
```

❌ **避免**:
```python
# 相对路径可能失败
bash("python script.py")

# 不检查文件直接操作
bash("rm -rf /important/path")
```

### 3. 性能优化

✅ **推荐**:
- 只在需要时加载 Skill（Level 2）
- 使用 `glob` 过滤文件而不是全部读取
- 限制输出大小（`DisplayLimits.TOOL_RESULT_MAX`）

❌ **避免**:
- 启动时加载所有 Skills
- 读取大文件（>1MB）
- 不必要的重复调用

---

## 🔗 相关资源

### 官方文档

- [LangChain 1.0 文档](https://python.langchain.com/docs/versions/introduction/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Anthropic Skills 格式](https://docs.anthropic.com/docs/build-with-claude/skills)
- [Rich 库文档](https://rich.readthedocs.io/)

### 社区资源

- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Claude Code](https://claude.ai/code)

### 示例项目

- [本项目](https://github.com/your-repo/skills-agent-proto)
- [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python)

---

## 📞 获取帮助

### 报告问题

在 GitHub 上创建 Issue，包含：
- 错误信息
- 复现步骤
- 环境信息（Python 版本、依赖版本）
- 调试日志（`SKILLS_DEBUG=1`）

### 贡献

欢迎提交 Pull Request！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

---

**最后更新**: 2026-02-14
**版本**: 0.1.0
