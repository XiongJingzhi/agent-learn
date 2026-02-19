# Level 0 快速开始指南

> **从这里开始你的 Agent 学习之旅！**

---

## 🚀 第一步：环境准备

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装核心依赖
pip install langchain langchain-openai langchainhub
pip install openai

# 安装可选依赖（用于示例运行）
pip install chromadb sentence-transformers
```

### 2. 设置 API Key

```bash
# 设置 OpenAI API Key
export OPENAI_API_KEY="your-api-key-here"

# 或创建 .env 文件
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

---

## 📚 第二步：学习路径

### 推荐学习顺序

#### 阶段 1：工具基础（1-2 天）

**必学内容**：
1. ✅ `notes/07_langchain_basics.md` - LangChain 核心概念
2. ✅ `examples/07_langchain_basics.py` - 运行示例代码
3. ✅ `examples/08_first_agent.py` - 创建第一个 Agent

**学习目标**：
- 理解 LangChain 的六大组件
- 能够运行简单的 Chain 和 Agent
- 掌握 Tool 的定义和使用

**验证方式**：
```bash
# 运行示例
cd study/level0/examples
python 07_langchain_basics.py
python 08_first_agent.py
```

---

#### 阶段 2：核心概念（2-3 天）

**必学内容**：
1. ✅ `notes/00_agent_meaning.md` - Agent 的意义
2. ✅ `notes/01_react_loop_basics.md` - ReAct 循环
3. ✅ `notes/02_agent_vs_chatbot.md` - Agent vs Chatbot
4. ✅ `notes/03_state_and_feedback.md` - 状态与反馈

**学习目标**：
- 理解 Agent 的核心特征
- 掌握 ReAct 循环的四个阶段
- 理解 Agent 和 Chatbot 的区别

**验证方式**：
- 完成每个笔记的"最小验证"部分
- 用自己的话解释核心概念

---

#### 阶段 3：实践深入（2-3 天）

**必学内容**：
1. ✅ `notes/04_toolbox_minimum_set.md` - 工具箱最小集
2. ✅ `notes/05_failure_modes_basics.md` - 失败模式
3. ✅ `notes/06_environment_check_guide.md` - 环境检查
4. ✅ `examples/00-06` - 运行所有示例

**学习目标**：
- 理解 Agent 的工具组成
- 掌握基本的错误处理
- 能够检查 Agent 环境

**验证方式**：
- 修改示例代码，观察效果
- 完成基础练习题

---

#### 阶段 4：综合实践（3-5 天）

**必学内容**：
1. ✅ `exercises/01_basic_exercises.md` - 基础练习
2. ✅ `projects/00_hello_project.md` - Hello Agent 项目
3. ✅ `projects/01_capstone_project.md` - Capstone 项目

**学习目标**：
- 完成所有基础练习
- 构建第一个完整的 Agent
- 通过完成标准检查

---

## 📋 每日学习计划

### Day 1：环境搭建 + LangChain 基础

**上午（2小时）**：
- [ ] 安装所有依赖
- [ ] 设置 API Key
- [ ] 阅读快速开始指南

**下午（3小时）**：
- [ ] 阅读 `notes/07_langchain_basics.md`
- [ ] 运行 `examples/07_langchain_basics.py`
- [ ] 运行 `examples/08_first_agent.py`

**晚上（1小时）**：
- [ ] 写学习笔记
- [ ] 用自己的话解释 LangChain

---

### Day 2：Agent 核心概念

**上午（2小时）**：
- [ ] 阅读 `notes/00_agent_meaning.md`
- [ ] 阅读 `notes/01_react_loop_basics.md`

**下午（3小时）**：
- [ ] 阅读 `notes/02_agent_vs_chatbot.md`
- [ ] 阅读 `notes/03_state_and_feedback.md`
- [ ] 运行 `examples/01-03`

**晚上（1小时）**：
- [ ] 总结 Agent 核心概念
- [ ] 画出 ReAct 循环图

---

### Day 3：工具和实践

**上午（2小时）**：
- [ ] 阅读 `notes/04_toolbox_minimum_set.md`
- [ ] 阅读 `notes/05_failure_modes_basics.md`

**下午（3小时）**：
- [ ] 阅读 `notes/06_environment_check_guide.md`
- [ ] 运行 `examples/04-06`
- [ ] 完成 Hello Agent 项目

**晚上（1小时）**：
- [ ] 复盘学习内容
- [ ] 准备进入 Level 1

---

## 🎯 学习检查点

### 检查点 1：完成 LangChain 基础

**你能够**：
- [ ] 解释 LangChain 的六大组件
- [ ] 运行简单的 Chain
- [ ] 定义和使用 Tool
- [ ] 创建简单的 Agent

### 检查点 2：理解 Agent 概念

**你能够**：
- [ ] 解释什么是 Agent
- [ ] 描述 ReAct 循环的四个阶段
- [ ] 区分 Agent 和 Chatbot
- [ ] 理解状态和反馈的作用

### 检查点 3：完成实践项目

**你能够**：
- [ ] 独立创建 Agent
- [ ] 定义自定义工具
- [ ] 处理常见错误
- [ ] 优化 Agent 行为

---

## 💡 学习技巧

### 技巧 1：费曼学习法

**如何使用**：
1. 学习一个概念
2. 用简单的语言解释给"5岁孩子"听
3. 如果卡住了，回头重学
4. 简化并使用类比

**示例**：
- 不要说："Agent 是基于 LLM 的自主系统"
- 要说："Agent 就像一个智能助手，你能告诉它做什么，它会自己想办法完成"

### 技巧 2：实践驱动

**原则**：
- ✅ 先运行代码，再理解原理
- ✅ 修改代码，观察效果
- ✅ 遇到错误，学会调试
- ❌ 不要只读不练

### 技巧 3：建立知识图谱

**方法**：
- 画图展示概念之间的关系
- 用思维导图整理知识
- 写笔记连接不同概念

---

## 🔗 常用资源

### 官方文档
- [LangChain 文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [OpenAI API 文档](https://platform.openai.com/docs)

### 社区资源
- [LangChain GitHub](https://github.com/langchain-langchain/langchain)
- [LangChain 示例](https://github.com/langchain-langchain/langchain/tree/main/cookbook)

### 本项目资源
- Level 0 笔记：`study/level0/notes/`
- Level 0 示例：`study/level0/examples/`
- Level 0 练习：`study/level0/exercises/`

---

## ❓ 常见问题

### Q1: 我没有编程基础，能学吗？

**A**: 可以！Level 0 专为初学者设计，从最基础的概念开始。建议：
1. 先学习 Python 基础（1-2 天）
2. 跟随示例代码一步步运行
3. 遇到问题就问，不要害怕

### Q2: API Key 很贵，怎么办？

**A**: 有几个选项：
1. 使用便宜的模型（如 gpt-3.5-turbo）
2. 使用本地模型（通过 Ollama）
3. 只在必要时运行示例
4. 先理解概念，再实践代码

### Q3: 学习时间不够怎么办？

**A**: 根据时间调整学习计划：
- **每天 1 小时**：需要 2-3 周完成 Level 0
- **每天 2-3 小时**：需要 1-2 周完成 Level 0
- **周末集中学习**：可以在 1 个周末完成核心内容

### Q4: 遇到错误怎么办？

**A**: 按以下步骤排查：
1. 仔细阅读错误信息
2. 检查代码是否完全复制
3. 确认依赖已安装
4. 检查 API Key 是否正确
5. 查看示例代码的注释

---

## 🎉 开始学习吧！

现在你已经准备好开始学习了！

**第一步**：
```bash
cd study/level0
cat notes/07_langchain_basics.md
```

**第二步**：
```bash
cd examples
python 07_langchain_basics.py
```

**第三步**：
享受学习的乐趣，遇到问题随时回来查阅这个指南！

---

**祝你学习愉快！** 🚀📚

如有问题，欢迎查阅文档或在社区提问。
