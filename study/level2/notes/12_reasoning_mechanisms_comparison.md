# 推理机制对比

> **目标**: 理解不同推理机制的原理、适用场景和权衡
> **预计时间**: 40 分钟
> **难度**: ⭐⭐⭐⭐

---

## 什么是推理机制？

推理机制是 Agent 用来"思考"和"决策"的方法。不同的推理机制适用于不同类型的任务：

**类比**：推理机制就像**解决问题的方法论**：
- 简单问题：直接解决（ReAct）
- 复杂问题：分步思考（CoT）
- 超复杂问题：多路径探索（ToT）

---

## 推理机制类型

### 类型 1：ReAct (Reasoning + Acting)

**原理**：推理-行动-观察的循环

**特点**：
- 简单直观
- 实时决策
- 适合简单到中等复杂度任务

**流程**：
```
思考 → 行动 → 观察 → 思考 → 行动 → ...
```

**示例**：
```python
from typing import List, Dict, Any

class ReActAgent:
    """ReAct Agent"""

    def __init__(self, tools: List[Dict]):
        self.tools = {t["name"]: t for t in tools}

    def run(self, query: str, max_steps: int = 10) -> str:
        """运行 ReAct 循环"""
        print(f"[ReAct] 查询: {query}\n")

        history = []

        for step in range(max_steps):
            # 1. 思考：决定下一步行动
            thought = self._think(query, history)
            print(f"[步骤 {step+1}] 思考: {thought}")

            # 2. 行动：执行工具或回答
            if "回答" in thought or "完成" in thought:
                answer = self._generate_answer(query, history)
                print(f"[完成] 答案: {answer}\n")
                return answer

            # 3. 解析行动
            action = self._parse_action(thought)
            print(f"[行动] {action['tool']}: {action['input']}")

            # 4. 执行并观察
            observation = self._execute_action(action)
            print(f"[观察] {observation}\n")

            # 5. 记录历史
            history.append({
                "thought": thought,
                "action": action,
                "observation": observation
            })

        return "达到最大步数"

    def _think(self, query: str, history: List[Dict]) -> str:
        """思考下一步行动"""
        # 简化：实际应该使用 LLM
        if not history:
            return "我需要搜索相关信息来回答这个问题"
        else:
            return "我已经收集了足够信息，现在可以回答"

    def _parse_action(self, thought: str) -> Dict:
        """从思考中解析行动"""
        return {
            "tool": "search",
            "input": thought
        }

    def _execute_action(self, action: Dict) -> str:
        """执行行动"""
        return f"执行 {action['tool']} 的结果"

    def _generate_answer(self, query: str, history: List[Dict]) -> str:
        """生成最终答案"""
        return f"基于 {len(history)} 步推理，答案是：42"
```

**优点**：
- 实现简单
- 透明度高（每一步都有思考过程）
- 适合工具调用场景

**缺点**：
- 可能陷入循环
- 对复杂问题规划不足
- 依赖单一路径

---

### 类型 2：Chain of Thought (CoT)

**原理**：在给出最终答案前，先生成完整的推理链

**特点**：
- 显式推理过程
- 适合多步推理问题
- 提高复杂问题准确率

**流程**：
```
问题 → 思考步骤 1 → 思考步骤 2 → ... → 思考步骤 N → 答案
```

**示例**：
```python
class CoTAgent:
    """Chain of Thought Agent"""

    def run(self, query: str) -> str:
        """运行 CoT 推理"""
        print(f"[CoT] 查询: {query}\n")

        # 1. 生成推理链
        reasoning_steps = self._generate_reasoning(query)

        print("[推理链]")
        for i, step in enumerate(reasoning_steps, 1):
            print(f"{i}. {step}")

        # 2. 生成最终答案
        answer = self._generate_answer(query, reasoning_steps)

        print(f"\n[答案] {answer}\n")
        return answer

    def _generate_reasoning(self, query: str) -> List[str]:
        """生成推理步骤"""
        # 简化示例
        steps = [
            "首先，我需要理解问题的核心",
            "然后，我需要收集相关的信息",
            "接着，我需要分析这些信息",
            "最后，我可以得出结论"
        ]
        return steps

    def _generate_answer(self, query: str, reasoning: List[str]) -> str:
        """基于推理链生成答案"""
        return "基于上述推理，答案是：42"
```

**优点**：
- 推理过程清晰
- 适合数学、逻辑推理
- 减少错误率

**缺点**：
- 需要 LLM 支持长输出
- 推理链可能出错
- 成本较高（更多 tokens）

---

### 类型 3：Tree of Thoughts (ToT)

**原理**：探索多个可能的推理路径，选择最优解

**特点**：
- 多路径并行探索
- 支持回溯和调整
- 适合需要探索的任务

**流程**：
```
问题
├─ 路径 1 → 思考 1.1 → 思考 1.2 → 结论 1
├─ 路径 2 → 思考 2.1 → 思考 2.2 → 结论 2
└─ 路径 3 → 思考 3.1 → 思考 3.2 → 结论 3

评估 → 选择最优结论
```

**示例**：
```python
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ThoughtNode:
    """思考节点"""
    content: str
    parent: 'ThoughtNode' = None
    children: List['ThoughtNode'] = None
    score: float = 0.0

    def __post_init__(self):
        if self.children is None:
            self.children = []


class ToTAgent:
    """Tree of Thoughts Agent"""

    def __init__(self, max_branches: int = 3, max_depth: int = 3):
        self.max_branches = max_branches
        self.max_depth = max_depth

    def run(self, query: str) -> str:
        """运行 ToT 推理"""
        print(f"[ToT] 查询: {query}\n")

        # 1. 生成初始思考路径
        root = ThoughtNode(content="问题: " + query)
        self._expand_tree(root, depth=0)

        # 2. 评估所有路径
        leaves = self._get_leaves(root)
        best_leaf = max(leaves, key=lambda n: n.score)

        # 3. 返回最优路径的结论
        path = self._get_path(best_leaf)

        print("[探索的路径]")
        for i, node in enumerate(path):
            indent = "  " * i
            print(f"{indent}{i+1}. {node.content} (分数: {node.score:.2f})")

        print(f"\n[最优答案] {best_leaf.content}\n")
        return best_leaf.content

    def _expand_tree(self, node: ThoughtNode, depth: int):
        """展开思维树"""
        if depth >= self.max_depth:
            return

        # 生成多个可能的思考
        thoughts = self._generate_thoughts(node.content)

        # 限制分支数量
        for thought in thoughts[:self.max_branches]:
            child = ThoughtNode(content=thought, parent=node)
            node.children.append(child)

            # 递归展开
            self._expand_tree(child, depth + 1)

    def _generate_thoughts(self, context: str) -> List[str]:
        """生成可能的思考"""
        # 简化示例
        return [
            f"从角度 A 思考: {context}",
            f"从角度 B 思考: {context}",
            f"从角度 C 思考: {context}"
        ]

    def _get_leaves(self, root: ThoughtNode) -> List[ThoughtNode]:
        """获取所有叶子节点"""
        leaves = []

        def traverse(node):
            if not node.children:
                leaves.append(node)
            else:
                for child in node.children:
                    traverse(child)

        traverse(root)
        return leaves

    def _get_path(self, node: ThoughtNode) -> List[ThoughtNode]:
        """获取从根到节点的路径"""
        path = []
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))
```

**优点**：
- 探索多个可能性
- 可回溯和调整
- 适合创意性任务

**缺点**：
- 计算成本高
- 实现复杂
- 需要评估函数

---

### 类型 4：Reflection (反思推理)

**原理**：在给出答案后，自我反思并改进

**特点**：
- 自我纠正
- 迭代改进
- 提高答案质量

**流程**：
```
问题 → 初步答案 → 反思 → 改进答案 → （重复） → 最终答案
```

**示例**：
```python
class ReflectionAgent:
    """反思推理 Agent"""

    def __init__(self, max_reflections: int = 2):
        self.max_reflections = max_reflections

    def run(self, query: str) -> str:
        """运行反思推理"""
        print(f"[Reflection] 查询: {query}\n")

        current_answer = None

        for iteration in range(self.max_reflections + 1):
            if iteration == 0:
                # 第一次：生成初步答案
                current_answer = self._generate_answer(query, None)
                print(f"[迭代 {iteration+1}] 初步答案: {current_answer}\n")
            else:
                # 后续：反思并改进
                reflection = self._reflect(query, current_answer)
                print(f"[迭代 {iteration+1}] 反思: {reflection}")

                improved_answer = self._improve_answer(query, current_answer, reflection)
                print(f"[迭代 {iteration+1}] 改进答案: {improved_answer}\n")

                current_answer = improved_answer

        print(f"[最终答案] {current_answer}\n")
        return current_answer

    def _generate_answer(self, query: str, previous_answer: str = None) -> str:
        """生成答案"""
        if previous_answer is None:
            return "这是一个初步的答案"
        else:
            return "这是一个改进后的答案"

    def _reflect(self, query: str, answer: str) -> str:
        """反思答案"""
        return "这个答案可以更详细一些"

    def _improve_answer(self, query: str, answer: str, reflection: str) -> str:
        """改进答案"""
        return f"{answer}（根据反思改进后）"
```

**优点**：
- 自动纠错
- 提高质量
- 适合需要精炼的任务

**缺点**：
- 增加推理步骤
- 成本较高
- 可能过度反思

---

## 推理机制对比

### 对比表

| 特性 | ReAct | CoT | ToT | Reflection |
|------|-------|-----|-----|------------|
| **复杂度** | 低 | 中 | 高 | 中 |
| **成本** | 低 | 中 | 高 | 中 |
| **准确度** | 中 | 高 | 很高 | 高 |
| **适用场景** | 工具调用 | 数学/逻辑 | 创意/规划 | 写作/分析 |
| **实现难度** | 简单 | 简单 | 复杂 | 简单 |

---

### 选择决策树

```
任务类型
│
├─ 简单任务（单步工具调用）
│  └─ 使用 ReAct
│
├─ 数学/逻辑推理
│  └─ 使用 CoT
│
├─ 创意性/探索性任务
│  └─ 使用 ToT
│
└─ 需要精炼的任务（写作、分析）
   └─ 使用 Reflection
```

---

## 混合推理策略

在实际应用中，可以结合多种推理机制：

```python
class HybridReasoningAgent:
    """混合推理 Agent"""

    def __init__(self):
        self.react_agent = ReActAgent(tools=[])
        self.cot_agent = CoTAgent()
        self.reflection_agent = ReflectionAgent()

    def run(self, query: str, task_type: str) -> str:
        """根据任务类型选择推理策略"""

        if task_type == "tool_use":
            # 工具调用：使用 ReAct
            return self.react_agent.run(query)

        elif task_type == "math":
            # 数学推理：使用 CoT
            return self.cot_agent.run(query)

        elif task_type == "writing":
            # 写作任务：使用 Reflection
            return self.reflection_agent.run(query)

        else:
            # 默认：ReAct + Reflection
            initial = self.react_agent.run(query, max_steps=3)
            refined = self.reflection_agent._improve_answer(query, initial, "优化表达")
            return refined
```

---

## 关键设计考虑

### 考虑 1：成本与效果的平衡

**问题**：复杂的推理机制成本高，是否值得？

**策略**：
- 简单任务用简单机制（ReAct）
- 复杂任务才用复杂机制（ToT）
- 根据任务重要性决定

---

### 考虑 2：推理链长度

**问题**：推理链太长会出错，太短不够深

**策略**：
- CoT：通常 3-5 步足够
- ToT：深度 2-3 层，每层 2-3 个分支
- Reflection：1-2 次反思

---

### 考虑 3：评估机制

**问题**：如何评估不同推理路径的质量？

**策略**：
- 使用 LLM 打分
- 基于规则评估（如数学问题）
- 用户反馈学习

---

## 最小验证

- [ ] 能够实现 ReAct 推理
- [ ] 能够实现 CoT 推理
- [ ] 能够实现 Reflection 推理
- [ ] 能够根据任务选择合适的推理机制

---

## 下一步

- 📖 `notes/16_testing_strategy.md` - 测试策略
- 🧪 `examples/11_reasoning_comparison.py` - 推理机制对比示例

---

**记住：不同的推理机制适合不同的任务，就像不同的工具适合不同的工作！** 🧠
