# 02. Agent vs Chatbot 练习题 - Level 0

> **对应 Note**: `notes/02_agent_vs_chatbot.md`
> **对应 Example**: `examples/03_agent_vs_chatbot.py`
> **目标**: 测试你对 Agent 和 Chatbot 区别的理解

---

## 📊 练习统计

- **总题数**: 25 题
- **选择题**: 10 题
- **判断题**: 5 题
- **简答题**: 5 题
- **代码题**: 5 题
- **预计时间**: 35 分钟

---

## 🎯 选择题（1-10）

### 第 1 部分：Chatbot 特点（1-5）

**Q1. Chatbot 的核心工作原理是：**

A. 推理 + 行动
B. 输入匹配 → 查找预设回复 → 返回回复
C. 感知 → 推理 → 执行 → 记忆
D. 观察 → 思考 → 行动 → 循环

**答案**: B

---

**Q2. 以下哪个是 Chatbot 的特点？**

A. 自主决策
B. 预定义对话
C. 推理能力
D. 学习能力

**答案**: B

---

**Q3. 基于规则的 Chatbot 的优点是：**

A. 灵活性高
B. 实现简单
C. 能理解复杂问题
D. 能自主学习

**答案**: B

---

**Q4. 基于状态的 Chatbot 比基于规则的 Chatbot 多了什么能力？**

A. 状态跟踪
B. 自主决策
C. 推理能力
D. 学习能力

**答案**: A

---

**Q5. Chatbot 最适合的场景是：**

A. 复杂任务规划
B. 规则明确的 FAQ
C. 需要推理的场景
D. 需要调用工具的场景

**答案**: B

---

### 第 2 部分：Agent 特点（6-10）

**Q6. Agent 的核心工作原理是：**

A. 输入匹配 → 查找预设回复 → 返回回复
B. 推理 + 行动的循环
C. 感知 → 记忆
D. 观察 → 循环

**答案**: B

---

**Q7. 以下哪个是 Agent 的特点？**

A. 预定义对话
B. 模式匹配
C. 自主决策
D. 固定回复

**答案**: C

---

**Q8. Agent 比 Chatbot 多了哪些能力？**

A. 推理能力和决策能力
B. 模式匹配能力
C. 状态跟踪能力
D. 预定义回复能力

**答案**: A

---

**Q9. Agent 最适合的场景是：**

A. 规则明确的 FAQ
B. 简单的问答
C. 需要推理和决策的复杂任务
D. 固定流程的处理

**答案**: C

---

**Q10. Agent 的主要缺点是：**

A. 无法处理复杂任务
B. 实现复杂，成本高
C. 只能回答预设问题
D. 缺乏灵活性

**答案**: B

---

## ✅ 判断题（11-15）

**Q11. Chatbot 可以根据上下文生成灵活的回复。**

**答案**: 错误

**解析**: Chatbot 的回复是预定义的，不能灵活生成。

---

**Q12. Agent 能够自主决策如何完成任务。**

**答案**: 正确

**解析**: Agent 的核心特性就是自主决策能力。

---

**Q13. Chatbot 一定比 Agent 差，应该总是使用 Agent。**

**答案**: 错误

**解析**: 两者各有优劣，应根据场景选择。

---

**Q14. Agent 需要 LLM 来实现推理能力。**

**答案**: 正确

**解析**: Agent 通常需要 LLM 来进行推理和决策。

---

**Q15. Chatbox 可以有状态跟踪功能。**

**答案**: 正确

**解析**: 基于状态的 Chatbot 可以有状态跟踪。

---

## 📝 简答题（16-20）

**Q16. 简述 Chatbot 的工作原理。**

**答案**: Chatbot 的工作原理是"输入匹配 → 查找预设回复 → 返回回复"。它通过关键词或模式匹配用户输入，然后查找对应的预设回复。

---

**Q17. 简述 Agent 的工作原理。**

**答案**: Agent 的工作原理是"推理 + 行动的循环"。它通过推理分析当前情况，制定行动计划，执行行动，然后观察结果，循环直到完成目标。

---

**Q18. 列举 Chatbot 的三个优点。**

**答案**:
1. 规则明确，回复可控
2. 实现简单，易于维护
3. 成本低，响应快

---

**Q19. 列举 Agent 的三个优点。**

**答案**:
1. 能够理解用户意图
2. 能够推理和决策
3. 能够调用工具完成任务
4. 能够生成灵活的回复

---

**Q20. 给出一个适合使用 Chatbot 的场景和一个适合使用 Agent 的场景。**

**答案**:
- Chatbot 场景：客户服务常见问题解答（FAQ）
- Agent 场景：智能客服，需要理解用户问题并调用不同工具

---

## 💻 代码题（21-25）

**Q21. 补充完整基于规则的 Chatbot 代码：**

```python
class RuleBasedChatbot:
    def __init__(self):
        self.rules = {
            "你好": "你好！",
            "再见": "_______"
        }

    def get_response(self, user_input: str) -> str:
        for key, value in self.______:
            if key in user_input:
                return ______

        return "抱歉，我不理解。"
```

**答案**:
```python
class RuleBasedChatbot:
    def __init__(self):
        self.rules = {
            "你好": "你好！",
            "再见": "再见！"
        }

    def get_response(self, user_input: str) -> str:
        for key, value in self.rules.items():
            if key in user_input:
                return value

        return "抱歉，我不理解。"
```

---

**Q22. 补充完整基于状态的 Chatbot 代码：**

```python
class StateBasedChatbot:
    def __init__(self):
        self.______ = "greeting"

    def get_response(self, user_input: str) -> str:
        if self.______ == "greeting":
            if "你好" in user_input:
                self.______ = "conversation"
                return "你好！"
        return "请先打招呼。"
```

**答案**:
```python
class StateBasedChatbot:
    def __init__(self):
        self.state = "greeting"

    def get_response(self, user_input: str) -> str:
        if self.state == "greeting":
            if "你好" in user_input:
                self.state = "conversation"
                return "你好！"
        return "请先打招呼。"
```

---

**Q23. 写一个简单的 Chatbot，支持以下规则：**

- 用户说"帮助" → 回复"我能帮你查询天气和计算。"
- 用户说"谢谢" → 回复"不客气！"
- 其他 → 回复"抱歉，我不理解。"

**答案**:
```python
class SimpleChatbot:
    def __init__(self):
        self.rules = {
            "帮助": "我能帮你查询天气和计算。",
            "谢谢": "不客气！"
        }

    def get_response(self, user_input: str) -> str:
        for key, value in self.rules.items():
            if key in user_input:
                return value
        return "抱歉，我不理解。"
```

---

**Q24. 以下是一个 Chatbot 的实现，找出错误并修正：**

```python
class BrokenChatbot:
    def __init__(self):
        self.rules = {"你好": "你好！"}

    def get_response(self, user_input: str) -> str:
        # 错误：使用 == 而不是 in
        if user_input == "你好":
            return self.rules["你好"]
        return "抱歉"
```

**答案**:
```python
class FixedChatbot:
    def __init__(self):
        self.rules = {"你好": "你好！"}

    def get_response(self, user_input: str) -> str:
        # 修正：使用 in 检查关键词
        if "你好" in user_input:
            return self.rules["你好"]
        return "抱歉"
```

---

**Q25. 设计一个支持状态的 Chatbot，有以下状态：**

- `greeting`: 问候阶段
- `ordering`: 点餐阶段
- `payment`: 支付阶段

**答案**:
```python
class RestaurantChatbot:
    def __init__(self):
        self.state = "greeting"
        self.order = {}

    def get_response(self, user_input: str) -> str:
        if self.state == "greeting":
            if "你好" in user_input:
                self.state = "ordering"
                return "你好！欢迎光临，请问您想点什么？"
            return "请先打招呼！"

        elif self.state == "ordering":
            if "汉堡" in user_input:
                self.order["item"] = "汉堡"
                self.state = "payment"
                return "好的，汉堡。请问您要支付多少钱？"
            return "请选择您想要的餐品。"

        elif self.state == "payment":
            return "谢谢您的支付！"
```

---

## 🎯 学习建议

1. **先阅读 note**: `notes/02_agent_vs_chatbot.md`
2. **再运行 example**: `examples/03_agent_vs_chatbot.py`
3. **最后完成练习**: 本练习题

---

## ✅ 完成标准

- [ ] 完成 10 道选择题
- [ ] 完成 5 道判断题
- [ ] 完成 5 道简答题
- [ ] 完成 5 道代码题
- [ ] 正确率 >= 80%
- [ ] 能够清晰说明 Agent 和 Chatbot 的区别

---

**下一练习**: `exercises/03_state_feedback_exercise.md` 🚀
