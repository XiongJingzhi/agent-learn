# Chain of Thought (思维链) 推理

> **目标**: 掌握 CoT 推理的原理和实现
> **预计时间**: 40 分钟
> **难度**: ⭐⭐⭐

---

## 什么是 CoT？

Chain of Thought (CoT) 是一种提示策略，通过让模型显式地展示推理步骤来提高复杂问题的解决能力。

**类比**：CoT 就像**数学题的解题过程**，不仅要答案，还要写出每一步的推理。

---

## 为什么需要 CoT？

**问题 1：直接回答错误**
```
问题: "Roger 有 5 个网球。他又买了 2 罐网球。每罐有 3 个球。
现在他总共有多少个网球？"

直接回答: "11 个" ❌ 错误
```

**问题 2：推理过程不透明**
```
问题: "如果 3x + 5 = 20，x 是多少？"

直接回答: "x = 5"
但是怎么得到的结果？不清楚。
```

**CoT 解决方案**：
```
问题: "Roger 有 5 个网球。他又买了 2 罐网球。每罐有 3 个球。
现在他总共有多少个网球？"

CoT 推理:
"Roger 从 5 个球开始。
2 罐 × 3 个/罐 = 6 个球。
5 + 6 = 11 个球。"
✅ 正确
```

---

## CoT 的核心原理

### 原理 1：显式推理

将隐式的推理过程显式化。

**示例**：
```python
class CoTReasoner:
    """CoT 推理器"""

    def reason(self, query: str) -> str:
        """使用 CoT 推理"""
        # 1. 生成推理步骤
        reasoning_steps = self._generate_steps(query)

        # 2. 基于步骤得出结论
        conclusion = self._derive_conclusion(reasoning_steps)

        # 3. 组合完整回答
        return self._format_answer(reasoning_steps, conclusion)
```

---

### 原理 2：逐步分解

将复杂问题分解为简单的步骤。

**示例**：
```
问题: "如果 A > B, B > C, 那么 A 和 C 的关系？"

步骤 1: 理解条件
- A > B 表示 A 大于 B
- B > C 表示 B 大于 C

步骤 2: 应用传递性
- 如果 A > B 且 B > C
- 根据传递性，A > C

步骤 3: 得出结论
- A 大于 C
```

---

## CoT 提示策略

### 策略 1：零样本 CoT (Zero-Shot CoT)

直接在问题后添加"让我们一步步思考"。

```python
def zero_shot_cot_prompt(query: str) -> str:
    """零样本 CoT 提示"""
    return f"""{query}

让我们一步步思考。"""
```

**示例**：
```
用户: "如果 3x + 5 = 20，x 是多少？"

提示: "如果 3x + 5 = 20，x 是多少？

让我们一步步思考。"

模型回答:
"步骤 1: 我需要解方程 3x + 5 = 20
步骤 2: 减去 5：3x = 15
步骤 3: 除以 3：x = 5
答案: x = 5"
```

---

### 策略 2：少样本 CoT (Few-Shot CoT)

提供几个推理示例。

```python
def few_shot_cot_prompt(query: str) -> str:
    """少样本 CoT 提示"""
    examples = """
Q: "Roger 有 5 个球，买了 2 罐（每罐 3 个），总共有多少个？"
A: "Roger 从 5 个球开始。2 罐 × 3 = 6 个球。5 + 6 = 11。答案是 11。"

Q: "餐厅有 23 个苹果，如果用掉 20 个做午餐，又买了 6 个，现在有多少个？"
A: "开始有 23 个，用掉 20 个剩 3 个。买 6 个后变成 9 个。答案是 9。"
"""

    return f"""{examples}

Q: "{query}"
A: """
```

---

### 策略 3：自动 CoT (Auto-CoT)

自动生成推理步骤。

```python
class AutoCoT:
    """自动 CoT"""

    def __init__(self):
        self.question_bank = []

    def generate_reasoning(self, question: str) -> List[str]:
        """生成推理步骤"""
        # 1. 识别问题类型
        question_type = self._classify_question(question)

        # 2. 选择推理模板
        template = self._get_template(question_type)

        # 3. 填充具体内容
        steps = self._fill_template(template, question)

        return steps

    def _classify_question(self, question: str) -> str:
        """分类问题"""
        if "计算" in question or "+" in question or "-" in question:
            return "math"
        elif "推理" in question or "因为" in question:
            return "logic"
        else:
            return "general"

    def _get_template(self, question_type: str) -> List[str]:
        """获取推理模板"""
        templates = {
            "math": [
                "识别数值和运算",
                "按顺序计算",
                "验证结果"
            ],
            "logic": [
                "分析前提条件",
                "应用逻辑规则",
                "得出结论"
            ],
            "general": [
                "理解问题",
                "收集信息",
                "分析综合",
                "得出答案"
            ]
        }
        return templates.get(question_type, templates["general"])

    def _fill_template(self, template: List[str], question: str) -> List[str]:
        """填充模板"""
        # 简化：直接返回模板
        # 实际应用中应该根据问题填充
        return template
```

---

## CoT 实现示例

### 实现 1：数学问题 CoT

```python
class MathCoT:
    """数学问题 CoT 推理"""

    def solve(self, problem: str) -> str:
        """解决数学问题"""
        print(f"\n[问题] {problem}")

        # 提取数字和运算
        numbers = self._extract_numbers(problem)
        operations = self._identify_operations(problem)

        print(f"[提取信息] 数字: {numbers}, 运算: {operations}")

        # 生成推理步骤
        steps = []
        running_value = numbers[0] if numbers else 0

        steps.append(f"从 {running_value} 开始")

        for i, (num, op) in enumerate(zip(numbers[1:], operations), 1):
            if op == "+":
                running_value += num
                steps.append(f"加上 {num} 得到 {running_value}")
            elif op == "-":
                running_value -= num
                steps.append(f"减去 {num} 得到 {running_value}")
            elif op == "*":
                running_value *= num
                steps.append(f"乘以 {num} 得到 {running_value}")
            elif op == "/":
                running_value /= num
                steps.append(f"除以 {num} 得到 {running_value}")

        steps.append(f"最终答案是 {running_value}")

        # 打印推理过程
        print("\n[推理过程]")
        for step in steps:
            print(f"  {step}")

        return "\n".join(steps)

    def _extract_numbers(self, problem: str) -> List[float]:
        """提取数字"""
        import re
        numbers = re.findall(r'\d+\.?\d*', problem)
        return [float(n) for n in numbers]

    def _identify_operations(self, problem: str) -> List[str]:
        """识别运算"""
        operations = []
        if "+" in problem:
            operations.append("+")
        if "-" in problem:
            operations.append("-")
        if "*" in problem or "乘" in problem:
            operations.append("*")
        if "/" in problem or "除" in problem:
            operations.append("/")
        return operations


# 使用示例
math_cot = MathCoT()
result = math_cot.solve("Roger 有 5 个球，又买了 2 罐（每罐 3 个），总共有多少个？")
```

---

### 实现 2：逻辑推理 CoT

```python
class LogicCoT:
    """逻辑推理 CoT"""

    def reason(self, problem: str) -> str:
        """逻辑推理"""
        print(f"\n[问题] {problem}")

        steps = []

        # 步骤 1: 理解前提
        steps.append("步骤 1: 理解前提条件")
        premises = self._extract_premises(problem)
        for premise in premises:
            steps.append(f"  - {premise}")

        # 步骤 2: 应用推理规则
        steps.append("\n步骤 2: 应用推理规则")
        rule = self._identify_rule(problem)
        steps.append(f"  - 使用规则: {rule}")

        # 步骤 3: 得出结论
        steps.append("\n步骤 3: 得出结论")
        conclusion = self._derive_conclusion(premises, rule)
        steps.append(f"  - 结论: {conclusion}")

        # 打印推理过程
        print("\n[推理过程]")
        for step in steps:
            print(step)

        return "\n".join(steps)

    def _extract_premises(self, problem: str) -> List[str]:
        """提取前提"""
        # 简化：按逗号分割
        parts = problem.split(",")
        return [p.strip() for p in parts if p.strip()]

    def _identify_rule(self, problem: str) -> str:
        """识别推理规则"""
        if "大于" in problem or ">" in problem:
            return "传递性（如果 A > B 且 B > C，则 A > C）"
        elif "等于" in problem or "=" in problem:
            return "等量代换"
        else:
            return "一般推理"

    def _derive_conclusion(self, premises: List[str], rule: str) -> str:
        """推导结论"""
        # 简化：基于规则生成结论
        if "传递性" in rule:
            return "根据传递性，第一个元素大于最后一个元素"
        elif "等量代换" in rule:
            return "根据等量代换，它们相等"
        else:
            return "基于前提和规则，得出结论"
```

---

## CoT 的优缺点

### 优点

1. **提高准确率**：复杂问题准确率提升 10-30%
2. **可解释性**：推理过程透明
3. **调试友好**：可以定位错误步骤

### 缺点

1. **成本高**：需要更多 tokens
2. **速度慢**：生成推理步骤需要时间
3. **可能出错**：推理链中的错误会传播

---

## CoT 最佳实践

### 实践 1：选择合适的问题类型

**适合 CoT**：
- 数学问题
- 逻辑推理
- 多步骤计算

**不适合 CoT**：
- 简单事实查询
- 创意写作
- 情感分析

---

### 实践 2：控制推理链长度

```python
def optimize_cot_length(problem: str) -> int:
    """优化 CoT 长度"""
    complexity = estimate_complexity(problem)

    if complexity < 0.3:
        return 3  # 简单问题：3 步
    elif complexity < 0.7:
        return 5  # 中等问题：5 步
    else:
        return 8  # 复杂问题：最多 8 步
```

---

### 实践 3：验证推理步骤

```python
def validate_cot(steps: List[str]) -> bool:
    """验证 CoT 步骤"""
    # 检查 1: 步骤数量合理
    if len(steps) < 2 or len(steps) > 10:
        return False

    # 检查 2: 每步都有内容
    if any(not step.strip() for step in steps):
        return False

    # 检查 3: 最后一步是结论
    if not any(keyword in steps[-1] for keyword in ["答案", "结论", "因此"]):
        return False

    return True
```

---

## 最小验证

- [ ] 理解 CoT 的原理
- [ ] 能够实现零样本 CoT
- [ ] 能够实现少样本 CoT
- [ ] 能够优化 CoT 性能

---

## 下一步

- 📖 `notes/14_tree_of_thoughts.md` - Tree of Thoughts
- 🧪 `examples/04_reasoning_comparison.py` - 推理对比示例

---

**记住：CoT 就像解题过程，把思考步骤写出来，答案更准确！** 🧠
