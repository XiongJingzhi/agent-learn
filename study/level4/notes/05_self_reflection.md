# 05. 自我反思

> **目标**: 理解自主 Agent 如何通过自我反思改进性能
> **预计时间**: 35 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 什么是自我反思？

### 定义

**自我反思（Self-Reflection）** 是 Agent 评估自身行为、识别问题、调整策略的能力。

> **类比**：
> - **无反思**：一直按错误的方式做事
> - **有反思**：发现错误，分析原因，改进方法
>
> 就像学生考试后复盘："我哪道题做错了？为什么？下次如何避免？"

---

## 自我反思的作用

### 作用 1：评估完成度

**判断是否达成目标**

```python
def assess_completeness(objective: str, result: str) -> float:
    """评估目标完成度（0.0-1.0）"""

    prompt = f"""
    目标：{objective}
    结果：{result}

    请评估结果对目标的完成度。
    考虑因素：
    1. 是否回答了目标的所有方面
    2. 信息的完整性
    3. 结果的质量

    返回一个 0.0-1.0 之间的数字。
    """

    response = llm.invoke(prompt)
    completeness = float(response.strip())

    return completeness
```

---

### 作用 2：识别问题

**找出执行中的问题**

```python
def identify_issues(execution_trace: List[Dict]) -> List[str]:
    """识别执行中的问题"""

    prompt = f"""
    执行轨迹：
    {format_execution_trace(execution_trace)}

    请分析这次执行，识别出现的问题。
    问题类型可能包括：
    1. 工具选择错误
    2. 参数传递错误
    3. 逻辑错误
    4. 信息不足
    5. 其他问题

    返回问题列表。
    """

    response = llm.invoke(prompt)
    issues = parse_issues(response)

    return issues
```

---

### 作用 3：调整策略

**基于反思结果调整后续策略**

```python
def adjust_strategy(issues: List[str], current_strategy: Dict) -> Dict:
    """调整策略"""

    prompt = f"""
    当前策略：{current_strategy}
    发现的问题：{issues}

    请基于这些问题调整策略。
    说明：
    1. 哪些策略需要修改
    2. 如何修改
    3. 为什么这样修改

    返回调整后的策略。
    """

    response = llm.invoke(prompt)
    new_strategy = parse_strategy(response)

    return new_strategy
```

---

## 反思循环设计

### 单层反思

**简单反思：评估→调整**

```python
def simple_reflection_loop(objective, max_iterations=5):
    """简单的反思循环"""

    for iteration in range(max_iterations):
        print(f"\n=== 迭代 {iteration + 1} ===")

        # 1. 执行
        result = execute(objective)

        # 2. 反思
        completeness = assess_completeness(objective, result)

        print(f"完成度: {completeness:.2f}")

        # 3. 判断
        if completeness >= 0.9:
            print("✓ 目标达成")
            return result

        # 4. 调整
        if completeness < 0.5:
            print("× 完成度过低，调整策略")
            objective = refine_objective(objective, result)

    return result  # 返回最后一次结果
```

---

### 多层反思

**深度反思：多层评估和调整**

```python
class ReflectionLoop:
    """多层反思循环"""

    def __init__(self):
        self.reflection_history = []

    def deep_reflection(self, objective, execution_result):
        """深度反思"""

        # 第 1 层：表面评估
        surface_score = self.surface_assessment(execution_result)

        # 第 2 层：问题分析
        if surface_score < 0.8:
            issues = self.deep_analysis(execution_result)
        else:
            issues = []

        # 第 3 层：根因分析
        if issues:
            root_causes = self.root_cause_analysis(issues)
        else:
            root_causes = []

        # 第 4 层：改进建议
        improvements = self.generate_improvements(
            issues,
            root_causes
        )

        # 记录反思历史
        reflection = {
            "timestamp": datetime.now(),
            "surface_score": surface_score,
            "issues": issues,
            "root_causes": root_causes,
            "improvements": improvements
        }

        self.reflection_history.append(reflection)

        return reflection

    def surface_assessment(self, result):
        """表面评估"""
        # 快速评估结果质量
        return assess_completeness(result["objective"], result["output"])

    def deep_analysis(self, result):
        """深度分析"""
        # 详细分析执行过程
        return identify_issues(result["trace"])

    def root_cause_analysis(self, issues):
        """根因分析"""
        # 找出问题的根本原因
        prompt = f"""
        问题：{issues}

        请分析这些问题的根本原因。
        使用"5 Whys"方法：
        - 为什么会出现这个问题？
        - 为什么会导致这个原因？
        - ...（连续问5次为什么）

        返回根本原因。
        """

        response = llm.invoke(prompt)
        return parse_root_causes(response)

    def generate_improvements(self, issues, root_causes):
        """生成改进建议"""

        prompt = f"""
        问题：{issues}
        根本原因：{root_causes}

        请基于根本原因生成具体的改进建议。
        每个建议应该：
        1. 可执行
        2. 有明确步骤
        3. 能解决根本原因

        返回改进建议列表。
        """

        response = llm.invoke(prompt)
        return parse_improvements(response)
```

---

## 反思的有效性

### 如何确保反思有效？

**原则 1：基于证据**

```python
# ❌ 不好：主观判断
"我觉得这个结果不太好"

# ✓ 好：基于具体标准
"完成度只有 0.6，因为缺少 X、Y、Z 方面的信息"
```

**原则 2：可操作**

```python
# ❌ 不好：模糊建议
"下次做得更好一点"

# ✓ 好：具体建议
"下次在搜索时使用更具体的关键词，并验证信息的来源"
```

**原则 3：可验证**

```python
def verify_improvement(reflection, new_result):
    """验证改进是否有效"""

    # 对比新旧结果
    old_score = reflection["surface_score"]
    new_score = assess_completeness(new_result["objective"], new_result["output"])

    improvement = new_score - old_score

    # 记录验证结果
    reflection["verification"] = {
        "old_score": old_score,
        "new_score": new_score,
        "improvement": improvement,
        "effective": improvement > 0.1  # 提升超过 10% 视为有效
    }

    return reflection["verification"]["effective"]
```

---

## 反思记忆

### 存储反思历史

**目的**：避免重复犯错，积累经验

```python
class ReflectionMemory:
    """反思记忆"""

    def __init__(self):
        self.successes = []  # 成功经验
        self.failures = []   # 失败教训
        self.patterns = []   # 模式识别

    def store_reflection(self, reflection):
        """存储反思"""

        if reflection["surface_score"] >= 0.8:
            # 成功：存储为经验
            self.successes.append({
                "context": reflection["context"],
                "strategy": reflection["strategy"],
                "result": reflection["result"]
            })
        else:
            # 失败：存储为教训
            self.failures.append({
                "context": reflection["context"],
                "issues": reflection["issues"],
                "root_causes": reflection["root_causes"]
            })

        # 识别模式
        self.identify_patterns()

    def retrieve_relevant_lessons(self, current_context):
        """检索相关经验教训"""

        # 检索类似的成功经验
        similar_successes = self.find_similar(
            current_context,
            self.successes
        )

        # 检索类似的失败教训
        similar_failures = self.find_similar(
            current_context,
            self.failures
        )

        return {
            "successes": similar_successes,
            "failures": similar_failures
        }

    def identify_patterns(self):
        """识别成功和失败的模式"""

        # 分析成功模式的共同点
        if len(self.successes) >= 3:
            success_patterns = analyze_common_patterns(self.successes)
            self.patterns.extend([
                {"type": "success", "pattern": p}
                for p in success_patterns
            ])

        # 分析失败模式的共同点
        if len(self.failures) >= 3:
            failure_patterns = analyze_common_patterns(self.failures)
            self.patterns.extend([
                {"type": "failure", "pattern": p}
                for p in failure_patterns
            ])
```

---

## 最小验证

### 验证目标
- ✅ 理解自我反思的作用
- ✅ 能够实现简单的反思循环
- ✅ 理解多层反思的设计

### 验证步骤
1. 实现一个简单的反思函数
2. 对一个执行结果进行反思
3. 基于反思结果生成改进建议

### 预期输出
能够识别执行中的问题并给出改进建议。

---

## 常见错误

### 错误 1：反思流于形式

**问题**：只是简单判断，没有深入分析

**解决**：使用多层反思，进行根因分析

---

### 错误 2：忽略反思历史

**问题**：每次都是新的反思，不利用历史经验

**解决**：建立反思记忆，积累经验教训

---

### 错误 3：反思但不行动

**问题**：识别了问题但不改进

**解决**：确保每个反思都有对应的改进行动

---

## 下一步

- 📖 `notes/06_advanced_rag_intro.md` - 高级 RAG 简介（阶段 2）
- 🧪 `examples/01_babyagi_agent.py` - BabyAGI 示例
- ✏ `exercises/01_basic_exercises.md` - 基础练习

---

**记住：自我反思就像考试后的复盘，找出问题，分析原因，下次做得更好！** 🤔💡
