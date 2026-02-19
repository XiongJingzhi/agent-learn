# 03. 状态管理与反馈练习题 - Level 0

> **对应 Note**: `notes/03_state_and_feedback.md`
> **对应 Example**: `examples/04_state_management.py`
> **目标**: 测试你对 Agent 状态管理和反馈机制的理解

---

## 📊 练习统计

- **总题数**: 25 题
- **选择题**: 10 题
- **填空题**: 5 题
- **简答题**: 5 题
- **代码题**: 5 题
- **预计时间**: 40 分钟

---

## 🎯 选择题（1-10）

### 第 1 部分：状态类型（1-5）

**Q1. Agent 状态不包括以下哪种类型？**

A. 短期状态
B. 中期状态
C. 长期状态
D. 永久状态

**答案**: D

---

**Q2. 短期状态的特点是：**

A. 容量大，时间长
B. 容量小，时间短
C. 容量中，时间中
D. 容量无限，时间永久

**答案**: B

---

**Q3. ConversationBufferMemory 适合用于：**

A. 短期状态
B. 中期状态
C. 长期状态
D. 永久存储

**答案**: A

---

**Q4. ConversationBufferWindowMemory 的 k 参数表示：**

A. 保存所有消息
B. 保留最近 k 条消息
C. 保留最旧的 k 条消息
D. 总共保存 k 条消息

**答案**: B

---

**Q5. 长期状态通常使用什么存储？**

A. 内存
B. 数据库或向量存储
C. 文件系统
D. 缓存

**答案**: B

---

### 第 2 部分：状态更新策略（6-10）

**Q6. 直接更新策略的特点是：**

A. 保留旧值，追加新值
B. 新值覆盖旧值
C. 分层管理
D. 永久保存

**答案**: B

---

**Q7. 追加更新策略适合用于：**

A. 当前任务状态
B. 对话历史
C. 用户偏好
D. 临时计算结果

**答案**: B

---

**Q8. 反馈机制的主要作用是：**

A. 存储数据
B. 监控 Agent 行为并改进
C. 增加响应速度
D. 减少内存使用

**答案**: B

---

**Q9. 以下哪个不是反馈机制的要素？**

A. 输入
B. 行动
C. 输出
D. 成功率

**答案**: D

**解析**: 反馈机制包括输入、行动、输出和成功判断，成功率是分析结果。

---

**Q10. 状态版本号的作用是：**

A. 记录状态更新的次数
B. 标识状态的一致性
C. 控制并发访问
D. 以上都是

**答案**: D

---

## 🔤 填空题（11-15）

**Q11. Agent 状态的三种类型是：短期状态、中期状态和 _______。**

**答案**: 长期状态

---

**Q12. ConversationBufferMemory 适合保存最近的 _______ 条消息。**

**答案**: 所有（或全部）

**解析**: ConversationBufferMemory 保存所有消息，不受限制。

---

**Q13. 状态更新的三种策略是：直接更新、追加更新和 _______。**

**答案**: 分层更新（或分层管理）

---

**Q14. 反馈机制中，Agent 通过观察 _______ 来判断行动是否成功。**

**答案**: 行动结果（或输出结果）

---

**Q15. 在 LangChain 中，memory_key 参数指定了状态在 _______ 中的键名。**

**答案**: 历史记录（或对话历史）

---

## 📝 简答题（16-20）

**Q16. 简述短期状态、中期状态和长期状态的区别。**

**答案**:
- 短期状态：容量小，时间短，适合最近对话和当前任务
- 中期状态：容量中，时间中，适合对话上下文和任务进度
- 长期状态：容量大，时间长，适合用户偏好和重要历史

---

**Q17. 什么时候应该使用 ConversationBufferMemory？**

**答案**: 当需要保存完整的对话历史，且对话不会太长时使用。适合简单的对话场景。

---

**Q18. 什么时候应该使用 ConversationBufferWindowMemory？**

**答案**: 当需要限制对话历史长度，只保留最近的对话时使用。适合长时间对话场景，避免内存溢出。

---

**Q19. 简述直接更新和追加更新的区别。**

**答案**:
- 直接更新：新值覆盖旧值，适合当前任务、临时状态
- 追加更新：保留旧值，追加新值，适合对话历史、操作记录

---

**Q20. 反馈机制如何帮助 Agent 改进？**

**答案**: 反馈机制记录 Agent 的输入、行动、输出和成功情况，通过分析这些数据，可以：
1. 发现失败模式
2. 优化决策逻辑
3. 提高成功率
4. 改进用户体验

---

## 💻 代码题（21-25）

**Q21. 补充完整创建短期状态的代码：**

```python
from langchain.memory import ConversationBufferMemory

# 创建短期状态
short_term = ConversationBufferMemory(
    memory_key="______",
    return_messages=______
)

# 保存对话
short_term.______(
    {"input": "你好"},
    {"output": "你好！"}
)
```

**答案**:
```python
from langchain.memory import ConversationBufferMemory

short_term = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

short_term.save_context(
    {"input": "你好"},
    {"output": "你好！"}
)
```

---

**Q22. 补充完整创建中期状态的代码：**

```python
from langchain.memory import ConversationBufferWindowMemory

# 创建中期状态，保留最近 10 条消息
medium_term = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=______,  # 保留最近 10 条消息
    return_messages=True
)
```

**答案**: k=10

---

**Q23. 写一个状态管理器，支持直接更新和追加更新：**

```python
class StateManager:
    def __init__(self):
        self.state = {
            "current_task": "",
            "history": []
        }

    def direct_update(self, key: str, value: str) -> None:
        """直接更新"""
        # 实现代码
        pass

    def append_update(self, key: str, value: str) -> None:
        """追加更新"""
        # 实现代码
        pass
```

**答案**:
```python
class StateManager:
    def __init__(self):
        self.state = {
            "current_task": "",
            "history": []
        }

    def direct_update(self, key: str, value: str) -> None:
        """直接更新"""
        self.state[key] = value

    def append_update(self, key: str, value: str) -> None:
        """追加更新"""
        if isinstance(self.state.get(key), list):
            self.state[key].append(value)
        else:
            self.state[key] = [value]
```

---

**Q24. 写一个反馈收集器：**

```python
class FeedbackCollector:
    def __init__(self):
        self.feedback = []

    def collect(self, user_input: str, action: str, output: str, success: bool) -> None:
        """收集反馈"""
        # 实现代码
        pass

    def get_success_rate(self) -> float:
        """计算成功率"""
        # 实现代码
        pass
```

**答案**:
```python
class FeedbackCollector:
    def __init__(self):
        self.feedback = []

    def collect(self, user_input: str, action: str, output: str, success: bool) -> None:
        """收集反馈"""
        self.feedback.append({
            "user_input": user_input,
            "action": action,
            "output": output,
            "success": success
        })

    def get_success_rate(self) -> float:
        """计算成功率"""
        if not self.feedback:
            return 0.0
        success_count = sum(1 for f in self.feedback if f["success"])
        return success_count / len(self.feedback)
```

---

**Q25. 设计一个带有状态管理的简单 Agent：**

**要求**:
1. 使用短期状态保存最近 3 条消息
2. 记录操作历史
3. 提供状态查询功能

**答案**:
```python
from langchain.memory import ConversationBufferWindowMemory
from typing import List, Dict

class SimpleAgentWithState:
    def __init__(self):
        # 创建短期状态，保留最近 3 条消息
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=3,
            return_messages=True
        )

        # 操作历史
        self.action_history: List[Dict] = []

    def process(self, user_input: str) -> str:
        """处理用户输入"""
        # 简单的响应逻辑
        if "你好" in user_input:
            response = "你好！"
        elif "再见" in user_input:
            response = "再见！"
        else:
            response = f"收到：{user_input}"

        # 保存到状态
        self.memory.save_context(
            {"input": user_input},
            {"output": response}
        )

        # 记录操作
        self.action_history.append({
            "input": user_input,
            "output": response,
            "timestamp": datetime.now().isoformat()
        })

        return response

    def get_state(self) -> Dict:
        """获取当前状态"""
        history = self.memory.load_memory_variables({})
        return {
            "chat_history": history.get("chat_history", []),
            "action_count": len(self.action_history),
            "recent_actions": self.action_history[-3:]
        }
```

---

## 🎯 学习建议

1. **先阅读 note**: `notes/03_state_and_feedback.md`
2. **再运行 example**: `examples/04_state_management.py`
3. **最后完成练习**: 本练习题

---

## ✅ 完成标准

- [ ] 完成 10 道选择题
- [ ] 完成 5 道填空题
- [ ] 完成 5 道简答题
- [ ] 完成 5 道代码题
- [ ] 正确率 >= 80%
- [ ] 理解三种状态类型的区别
- [ ] 掌握状态更新策略
- [ ] 理解反馈机制的作用

---

**下一练习**: `exercises/04_toolbox_exercise.md` 🚀
