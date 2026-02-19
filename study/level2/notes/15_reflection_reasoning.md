# Reflection (反思) 推理

> **目标**: 掌握反思推理的原理和实现
> **预计时间**: 40 分钟
> **难度**: ⭐⭐⭐

---

## 什么是反思推理？

Reflection 是一种通过自我反思和迭代改进来提升答案质量的推理方法。

**类比**：反思推理就像**写论文的审稿过程**：
1. 写出初稿
2. 自我审查
3. 根据反馈修改
4. 重复直到满意

---

## 为什么需要反思？

### 问题 1：初稿质量有限

```
直接回答:
Q: "如何评价这个产品？"
A: "这个产品挺好的。" → 太简单，不够详细
```

### 问题 2：无法发现自身错误

```
Q: "如果 3x + 5 = 20，x 是多少？"
直接回答: "x = 5"
但过程可能有误，自己不知道
```

### 反思的解决方案

```
反思推理:
Q: "如何评价这个产品？"

初稿: "这个产品挺好的。"

反思 1: "答案太简单了。应该提供具体的优缺点。"
改进: "这个产品有好的一面：性价比高。但也有不足：功能有限。"

反思 2: "还可以补充使用场景。"
改进: "这个产品性价比高，适合预算有限的用户。虽然功能有限，但满足日常需求。"

最终答案: 更全面、更具体
```

---

## 反思的类型

### 类型 1：Self-Reflection (自我反思)

Agent 自我审查答案。

```python
class SelfReflector:
    """自我反思器"""

    def reflect(self, question: str, answer: str) -> str:
        """自我反思答案"""
        # 1. 分析答案的完整性
        completeness = self._check_completeness(answer)

        # 2. 分析答案的准确性
        accuracy = self._check_accuracy(answer)

        # 3. 生成反馈
        if completeness < 0.7:
            return "答案不够完整，需要补充更多细节"
        elif accuracy < 0.7:
            return "答案可能有误，需要验证"
        else:
            return "答案质量良好，可以考虑优化表达"

    def _check_completeness(self, answer: str) -> float:
        """检查完整性"""
        # 简化：基于长度
        if len(answer) < 50:
            return 0.5
        elif len(answer) < 100:
            return 0.7
        else:
            return 0.9

    def _check_accuracy(self, answer: str) -> float:
        """检查准确性"""
        # 简化：检查是否有具体证据
        evidence_words = ["例如", "比如", "数据显示", "研究表明"]
        has_evidence = any(word in answer for word in evidence_words)
        return 0.8 if has_evidence else 0.6
```

---

### 类型 2：Multi-Reflection (多轮反思)

进行多次反思和改进。

```python
class MultiReflectionAgent:
    """多轮反思 Agent"""

    def __init__(self, max_reflections: int = 3):
        self.max_reflections = max_reflections

    def run(self, query: str) -> str:
        """运行带反思的推理"""
        current_answer = None
        reflection_history = []

        for iteration in range(self.max_reflections + 1):
            print(f"\n=== 迭代 {iteration + 1} ===")

            if iteration == 0:
                # 第一次：生成初始答案
                current_answer = self._generate_answer(query, None)
                print(f"[初始答案] {current_answer}")

            else:
                # 后续：反思并改进
                reflection = self._reflect(query, current_answer, reflection_history)
                print(f"[反思] {reflection}")

                improved_answer = self._improve(query, current_answer, reflection)
                print(f"[改进答案] {improved_answer}")

                # 检查是否满意
                if self._is_satisfied(improved_answer, reflection):
                    print("\n[满意] 达到质量要求")
                    return improved_answer

                current_answer = improved_answer
                reflection_history.append(reflection)

        return current_answer

    def _generate_answer(self, query: str, previous_reflection: str) -> str:
        """生成答案"""
        return f"对'{query}'的回答：这是初步的答案。"

    def _reflect(self, query: str, answer: str, history: List[str]) -> str:
        """反思答案"""
        reflections = [
            "答案可以更详细",
            "需要提供更多证据",
            "逻辑可以更严密",
            "表达可以更清晰"
        ]
        # 简化：循环使用
        import random
        return random.choice(reflections)

    def _improve(self, query: str, answer: str, reflection: str) -> str:
        """改进答案"""
        return f"{answer}（根据反思'{reflection}'改进后）"

    def _is_satisfied(self, answer: str, reflection: str) -> bool:
        """判断是否满意"""
        # 简化：基于长度
        return len(answer) > 100
```

---

### 类型 3：Critique-Revise (批评-修订)

使用外部批评指导改进。

```python
class CritiqueReviseAgent:
    """批评-修订 Agent"""

    def run(self, query: str) -> str:
        """运行批评-修订循环"""
        draft = self._generate_draft(query)

        for iteration in range(3):
            print(f"\n=== 迭代 {iteration + 1} ===")

            # 生成批评
            critique = self._generate_critique(query, draft)
            print(f"[批评] {critique}")

            # 检查是否需要修订
            if not self._needs_revision(critique):
                print("[满意] 无需进一步修订")
                return draft

            # 修订
            draft = self._revise(query, draft, critique)
            print(f"[修订] {draft}")

        return draft

    def _generate_draft(self, query: str) -> str:
        """生成初稿"""
        return f"关于'{query}'的初稿"

    def _generate_critique(self, query: str, draft: str) -> str:
        """生成批评"""
        # 简化：分析初稿的问题
        issues = []

        if len(draft) < 50:
            issues.append("太简短")
        if "例如" not in draft:
            issues.append("缺少例子")
        if "因此" not in draft and "所以" not in draft:
            issues.append("缺少逻辑连接")

        return "、".join(issues) if issues else "质量良好"

    def _needs_revision(self, critique: str) -> bool:
        """判断是否需要修订"""
        return "质量良好" not in critique

    def _revise(self, query: str, draft: str, critique: str) -> str:
        """修订初稿"""
        # 根据批评修订
        if "简短" in critique:
            draft += " 详细来说，这个问题的背景是..."

        if "例子" in critique:
            draft += " 例如，在实际应用中..."

        if "逻辑" in critique:
            draft = "因此，" + draft

        return draft
```

---

## 反思的质量评估

### 评估维度 1：完整性

答案是否回答了问题的所有方面？

```python
def check_completeness(question: str, answer: str) -> float:
    """检查完整性"""
    # 提取问题中的关键点
    question_points = extract_key_points(question)

    # 检查答案是否覆盖
    covered = sum(1 for point in question_points if point in answer)

    return covered / len(question_points) if question_points else 0.5
```

---

### 评估维度 2：准确性

答案的事实是否正确？

```python
def check_accuracy(answer: str) -> float:
    """检查准确性"""
    # 检查是否有模糊表述
    vague_words = ["可能", "也许", "大概", "应该"]
    vague_count = sum(1 for word in vague_words if word in answer)

    # 检查是否有确定性表述
    certain_words = ["确实", "肯定", "明确", "证明"]
    certain_count = sum(1 for word in certain_words if word in answer)

    # 计算准确性得分
    total = vague_count + certain_count
    if total == 0:
        return 0.5

    return certain_count / total
```

---

### 评估维度 3：清晰度

答案是否易于理解？

```python
def check_clarity(answer: str) -> float:
    """检查清晰度"""
    # 检查句子长度
    sentences = answer.split("。")
    avg_length = sum(len(s) for s in sentences) / len(sentences)

    # 检查是否有结构
    has_structure = any(marker in answer for marker in ["首先", "其次", "最后", "一、", "二、"])

    # 检查是否有连接词
    connectors = ["因为", "所以", "但是", "然而", "因此"]
    has_connectors = any(conn in answer for conn in connectors)

    # 计算清晰度
    score = 0.0
    if avg_length < 50:
        score += 0.3
    if has_structure:
        score += 0.4
    if has_connectors:
        score += 0.3

    return score
```

---

## 完整示例：反思 Agent

```python
from typing import List, Dict, Tuple

class ReflectionAgent:
    """反思 Agent"""

    def __init__(self, max_reflections: int = 2):
        self.max_reflections = max_reflections

    def run(self, query: str) -> Tuple[str, List[Dict]]:
        """运行反思循环"""
        print("=" * 70)
        print("反思推理")
        print("=" * 70)
        print(f"查询: {query}\n")

        current_answer = None
        history = []

        for iteration in range(self.max_reflections + 1):
            print(f"\n{'='*60}")
            print(f"迭代 {iteration + 1}/{self.max_reflections + 1}")
            print('='*60)

            if iteration == 0:
                # 生成初始答案
                current_answer = self._generate_initial(query)
                print(f"[初始答案] {current_answer}")

            else:
                # 反思
                reflection = self._reflect(query, current_answer)
                print(f"[反思] {reflection}")

                # 改进
                improved_answer = self._improve(query, current_answer, reflection)
                print(f"[改进] {improved_answer}")

                # 评估
                quality = self._evaluate(query, improved_answer)
                print(f"[质量] 完整性: {quality['completeness']:.2f}, "
                      f"准确性: {quality['accuracy']:.2f}, "
                      f"清晰度: {quality['clarity']:.2f}")

                # 记录历史
                history.append({
                    "iteration": iteration,
                    "answer": improved_answer,
                    "reflection": reflection,
                    "quality": quality
                })

                # 检查是否满意
                if all(score >= 0.7 for score in quality.values()):
                    print("\n[满意] 答案质量达标")
                    current_answer = improved_answer
                    break

                current_answer = improved_answer

        print(f"\n[最终答案] {current_answer}")
        return current_answer, history

    def _generate_initial(self, query: str) -> str:
        """生成初始答案"""
        return f"关于'{query}'的初步回答：这是一个复杂的问题，需要从多个角度分析。"

    def _reflect(self, query: str, answer: str) -> str:
        """反思答案"""
        reflections = []

        if len(answer) < 100:
            reflections.append("答案太简短，需要扩充内容")

        if "例如" not in answer and "比如" not in answer:
            reflections.append("缺少具体例子")

        if "第一" not in answer and "首先" not in answer:
            reflections.append("缺少结构化组织")

        if not reflections:
            return "答案质量良好"

        return "、".join(reflections)

    def _improve(self, query: str, answer: str, reflection: str) -> str:
        """改进答案"""
        improved = answer

        if "简短" in reflection:
            improved += " 从更详细的角度来看，这个问题涉及多个方面，包括技术、经济和社会影响。"

        if "例子" in reflection:
            improved += " 例如，在技术方面，我们需要考虑实现的可行性和成本。"

        if "结构" in reflection:
            improved = "首先，" + improved + " 其次，我们还需要考虑长期的影响。"

        return improved

    def _evaluate(self, query: str, answer: str) -> Dict[str, float]:
        """评估答案质量"""
        return {
            "completeness": check_completeness(query, answer),
            "accuracy": check_accuracy(answer),
            "clarity": check_clarity(answer)
        }


# 辅助函数
def extract_key_points(question: str) -> List[str]:
    """提取关键点"""
    # 简化：按逗号分割
    return [p.strip() for p in question.split("、") if p.strip()]

def check_completeness(question: str, answer: str) -> float:
    """检查完整性"""
    question_points = extract_key_points(question)
    covered = sum(1 for point in question_points if point in answer)
    return covered / len(question_points) if question_points else 0.5

def check_accuracy(answer: str) -> float:
    """检查准确性"""
    certain_words = ["确实", "肯定", "明确"]
    return sum(0.3 for word in certain_words if word in answer) + 0.1

def check_clarity(answer: str) -> float:
    """检查清晰度"""
    score = 0.0
    if len(answer.split("。")[0]) < 50:
        score += 0.3
    if "首先" in answer or "第一" in answer:
        score += 0.4
    if "因此" in answer or "所以" in answer:
        score += 0.3
    return score


# 使用示例
if __name__ == "__main__":
    agent = ReflectionAgent(max_reflections=2)

    query = "如何提高工作效率？"
    answer, history = agent.run(query)

    print("\n" + "=" * 70)
    print("反思历史")
    print("=" * 70)
    for item in history:
        print(f"\n迭代 {item['iteration']}:")
        print(f"  反思: {item['reflection']}")
        print(f"  质量: {item['quality']}")
