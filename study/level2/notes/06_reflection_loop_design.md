# 反思循环设计

> **目标**: 掌握如何设计有效的反思循环机制
> **预计时间**: 30 分钟
> **难度**: ⭐⭐⭐

---

## 什么是反思循环？

反思循环（Reflection Loop）是 Agent 在执行任务后，评估结果并决定下一步行动的过程。

**类比**：反思循环就像**写论文后的审稿过程**：
1. 写出初稿（执行）
2. 自我审查（反思）
3. 根据反馈修改（调整）
4. 重复直到满意（循环）

---

## 反思循环的组成

### 组件 1：评估指标

```python
@dataclass
class ReflectionMetrics:
    """反思指标"""
    completeness: float      # 完整度 (0.0 - 1.0)
    accuracy: float          # 准确度 (0.0 - 1.0)
    efficiency: float        # 效率 (0.0 - 1.0)
    user_satisfaction: float # 用户满意度 (0.0 - 1.0)

    def overall_score(self) -> float:
        """计算总体得分"""
        return (
            self.completeness * 0.3 +
            self.accuracy * 0.3 +
            self.efficiency * 0.2 +
            self.user_satisfaction * 0.2
        )
```

---

### 组件 2：反思触发器

```python
class ReflectionTrigger:
    """反思触发器"""

    def should_reflect(self,
                       execution_result: dict,
                       iteration: int) -> bool:
        """判断是否需要反思"""
        # 每次执行后都反思
        return True


class PeriodicReflectionTrigger(ReflectionTrigger):
    """周期性反思触发器"""

    def __init__(self, interval: int = 3):
        self.interval = interval  # 每隔 N 次执行反思一次

    def should_reflect(self,
                       execution_result: dict,
                       iteration: int) -> bool:
        return iteration % self.interval == 0
```

---

### 组件 3：反思器

```python
from typing import List, Dict, Optional

class Reflector:
    """反思器"""

    def __init__(self):
        self.reflection_history = []

    def reflect(self,
                original_input: str,
                execution_result: dict,
                iteration: int) -> dict:
        """反思执行结果"""
        print(f"\n[反思] 第 {iteration} 次反思")

        # 1. 评估结果
        metrics = self._assess_result(original_input, execution_result)

        # 2. 识别问题
        issues = self._identify_issues(execution_result, metrics)

        # 3. 判断下一步
        next_action = self._decide_next_action(metrics, issues, iteration)

        # 4. 生成建议
        suggestions = self._generate_suggestions(issues, metrics)

        reflection = {
            "iteration": iteration,
            "metrics": metrics,
            "issues": issues,
            "next_action": next_action,
            "suggestions": suggestions
        }

        self.reflection_history.append(reflection)

        # 打印反思结果
        self._print_reflection(reflection)

        return reflection

    def _assess_result(self,
                       original_input: str,
                       execution_result: dict) -> ReflectionMetrics:
        """评估结果质量"""
        # 简化的评估逻辑
        completed_tasks = sum(
            1 for r in execution_result.get("results", {}).values()
            if r.get("status") == "completed"
        )
        total_tasks = len(execution_result.get("results", {}))

        completeness = completed_tasks / total_tasks if total_tasks > 0 else 0

        # 其他指标可以根据实际情况计算
        return ReflectionMetrics(
            completeness=completeness,
            accuracy=0.9,  # 简化
            efficiency=0.8,  # 简化
            user_satisfaction=0.85  # 简化
        )

    def _identify_issues(self,
                        execution_result: dict,
                        metrics: ReflectionMetrics) -> List[str]:
        """识别问题"""
        issues = []

        # 检查完整度
        if metrics.completeness < 0.8:
            issues.append(f"完整度不足: {metrics.completeness:.2%}")

        # 检查失败任务
        failed_tasks = [
            k for k, v in execution_result.get("results", {}).items()
            if v.get("status") == "failed"
        ]
        if failed_tasks:
            issues.append(f"失败的任务: {', '.join(failed_tasks)}")

        # 检查错误
        errors = execution_result.get("errors", [])
        if errors:
            issues.extend(errors)

        return issues

    def _decide_next_action(self,
                           metrics: ReflectionMetrics,
                           issues: List[str],
                           iteration: int) -> str:
        """决定下一步行动"""
        # 如果完整度很高，可以结束
        if metrics.overall_score() >= 0.9:
            return "finish"

        # 如果有问题，需要重规划
        if issues and metrics.completeness < 0.5:
            return "replan"

        # 否则继续执行
        return "continue"

    def _generate_suggestions(self,
                             issues: List[str],
                             metrics: ReflectionMetrics) -> List[str]:
        """生成改进建议"""
        suggestions = []

        if metrics.completeness < 0.8:
            suggestions.append("考虑添加更多任务来提升完整度")

        if "失败的任务" in " ".join(issues):
            suggestions.append("分析失败原因并调整策略")

        if metrics.efficiency < 0.7:
            suggestions.append("优化任务执行顺序以提高效率")

        return suggestions

    def _print_reflection(self, reflection: dict):
        """打印反思结果"""
        metrics = reflection["metrics"]
        issues = reflection["issues"]
        next_action = reflection["next_action"]
        suggestions = reflection["suggestions"]

        print("\n[反思结果]")
        print(f"  完整度: {metrics.completeness:.2%}")
        print(f"  准确度: {metrics.accuracy:.2%}")
        print(f"  效率: {metrics.efficiency:.2%}")
        print(f"  用户满意度: {metrics.user_satisfaction:.2%}")
        print(f"  总体得分: {metrics.overall_score():.2%}")

        if issues:
            print(f"\n  发现的问题:")
            for issue in issues:
                print(f"    - {issue}")

        print(f"\n  下一步行动: {next_action}")

        if suggestions:
            print(f"\n  改进建议:")
            for suggestion in suggestions:
                print(f"    - {suggestion}")
```

---

## 反思循环策略

### 策略 1：单次反思

执行一次任务后立即反思并决定下一步。

```python
def single_reflection_loop(agent, input: str, max_iterations: int = 1):
    """单次反思循环"""
    for iteration in range(max_iterations):
        # 执行
        result = agent.run(input)

        # 反思
        reflection = agent.reflector.reflect(input, result, iteration + 1)

        # 决定下一步
        if reflection["next_action"] == "finish":
            return result

    return result
```

---

### 策略 2：迭代反思

多次执行-反思循环，逐步改进。

```python
def iterative_reflection_loop(agent, input: str, max_iterations: int = 3):
    """迭代反思循环"""
    current_input = input

    for iteration in range(max_iterations):
        print(f"\n{'='*60}")
        print(f"迭代 {iteration + 1}/{max_iterations}")
        print('='*60)

        # 执行
        result = agent.run(current_input)

        # 反思
        reflection = agent.reflector.reflect(current_input, result, iteration + 1)

        # 决定下一步
        if reflection["next_action"] == "finish":
            print(f"\n[完成] 任务完成，退出迭代")
            return result

        elif reflection["next_action"] == "replan":
            print(f"\n[重规划] 根据反思结果重新规划")
            # 根据建议调整输入
            current_input = _adjust_input(current_input, reflection["suggestions"])

        elif reflection["next_action"] == "continue":
            print(f"\n[继续] 继续执行")
            # 可以根据建议微调输入
            if reflection["suggestions"]:
                current_input = _adjust_input(current_input, reflection["suggestions"])

    print(f"\n[达到最大迭代] 达到最大迭代次数 {max_iterations}")
    return result


def _adjust_input(input: str, suggestions: List[str]) -> str:
    """根据建议调整输入"""
    # 简化版本：将建议附加到输入
    if suggestions:
        return f"{input}\n\n改进建议: {'; '.join(suggestions)}"
    return input
```

---

### 策略 3：渐进式反思

从粗到细的反思策略。

```python
def progressive_reflection_loop(agent, input: str):
    """渐进式反思循环"""

    # 阶段 1：快速评估（粗粒度）
    print("\n[阶段 1] 快速评估")
    result1 = agent.run(input)
    reflection1 = agent.reflector.reflect(input, result1, 1)

    if reflection1["metrics"].completeness >= 0.9:
        return result1

    # 阶段 2：详细分析（细粒度）
    print("\n[阶段 2] 详细分析")
    # 根据第一阶段的问题，调整输入
    adjusted_input = _adjust_input(input, reflection1["suggestions"])
    result2 = agent.run(adjusted_input)
    reflection2 = agent.reflector.reflect(adjusted_input, result2, 2)

    if reflection2["metrics"].completeness >= 0.95:
        return result2

    # 阶段 3：最终优化（精确）
    print("\n[阶段 3] 最终优化")
    final_input = _adjust_input(adjusted_input, reflection2["suggestions"])
    result3 = agent.run(final_input)

    return result3
```

---

## 完整示例：反思循环系统

```python
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ReflectionMetrics:
    """反思指标"""
    completeness: float
    accuracy: float
    efficiency: float
    user_satisfaction: float

    def overall_score(self) -> float:
        return (
            self.completeness * 0.3 +
            self.accuracy * 0.3 +
            self.efficiency * 0.2 +
            self.user_satisfaction * 0.2
        )


class ReflectionLoopSystem:
    """反思循环系统"""

    def __init__(self):
        self.reflector = Reflector()

    def run_with_reflection(self,
                           agent,
                           input: str,
                           strategy: str = "iterative",
                           max_iterations: int = 3) -> Dict[str, Any]:
        """带反思循环的执行"""

        print("="*70)
        print("反思循环执行")
        print("="*70)
        print(f"策略: {strategy}")
        print(f"最大迭代: {max_iterations}")
        print(f"输入: {input}\n")

        if strategy == "single":
            return self._single_reflection(agent, input)
        elif strategy == "iterative":
            return self._iterative_reflection(agent, input, max_iterations)
        elif strategy == "progressive":
            return self._progressive_reflection(agent, input)
        else:
            raise ValueError(f"未知策略: {strategy}")

    def _single_reflection(self, agent, input: str) -> Dict:
        """单次反思"""
        result = agent.run(input)
        reflection = self.reflector.reflect(input, result, 1)
        return result

    def _iterative_reflection(self, agent, input: str, max_iterations: int) -> Dict:
        """迭代反思"""
        current_input = input

        for iteration in range(max_iterations):
            print(f"\n{'='*60}")
            print(f"迭代 {iteration + 1}/{max_iterations}")
            print('='*60)

            # 执行
            result = agent.run(current_input)

            # 反思
            reflection = self.reflector.reflect(current_input, result, iteration + 1)

            # 决定下一步
            if reflection["next_action"] == "finish":
                print(f"\n[完成] 任务完成，退出迭代")
                return result

            elif reflection["next_action"] in ["replan", "continue"]:
                if reflection["suggestions"]:
                    print(f"\n[调整] 根据建议调整输入")
                    current_input = self._adjust_input(current_input, reflection["suggestions"])

        print(f"\n[达到最大迭代] 达到最大迭代次数 {max_iterations}")
        return result

    def _progressive_reflection(self, agent, input: str) -> Dict:
        """渐进式反思"""
        # 阶段 1：快速评估
        print("\n[阶段 1] 快速评估")
        result1 = agent.run(input)
        reflection1 = self.reflector.reflect(input, result1, 1)

        if reflection1["metrics"].completeness >= 0.9:
            return result1

        # 阶段 2：详细分析
        print("\n[阶段 2] 详细分析")
        adjusted_input = self._adjust_input(input, reflection1["suggestions"])
        result2 = agent.run(adjusted_input)
        reflection2 = self.reflector.reflect(adjusted_input, result2, 2)

        if reflection2["metrics"].completeness >= 0.95:
            return result2

        # 阶段 3：最终优化
        print("\n[阶段 3] 最终优化")
        final_input = self._adjust_input(adjusted_input, reflection2["suggestions"])
        result3 = agent.run(final_input)

        return result3

    def _adjust_input(self, input: str, suggestions: List[str]) -> str:
        """根据建议调整输入"""
        if suggestions:
            return f"{input}\n\n改进建议: {'; '.join(suggestions)}"
        return input


# 模拟 Agent
class MockAgent:
    """模拟 Agent"""

    def __init__(self):
        self.execution_count = 0

    def run(self, input: str) -> Dict:
        """运行 Agent"""
        self.execution_count += 1

        print(f"[Agent] 执行第 {self.execution_count} 次")

        # 模拟执行结果
        result = {
            "results": {
                "task_1": {"status": "completed"},
                "task_2": {"status": "completed"},
                "task_3": {"status": "completed" if self.execution_count > 1 else "pending"},
            },
            "errors": [],
            "iteration": self.execution_count
        }

        return result

    @property
    def reflector(self):
        """返回反思器"""
        if not hasattr(self, '_reflector'):
            self._reflector = Reflector()
        return self._reflector


# 运行示例
def main():
    print("="*70)
    print("反思循环系统示例")
    print("="*70)

    system = ReflectionLoopSystem()
    agent = MockAgent()

    # 示例 1：迭代反思
    print("\n\n【示例 1】迭代反思循环")
    result1 = system.run_with_reflection(
        agent,
        "搜索并总结 LangGraph 的信息",
        strategy="iterative",
        max_iterations=3
    )

    # 重置 Agent
    agent.execution_count = 0

    # 示例 2：渐进式反思
    print("\n\n【示例 2】渐进式反思循环")
    result2 = system.run_with_reflection(
        agent,
        "搜索并总结 LangGraph 的信息",
        strategy="progressive"
    )


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：反思频率

**每次都反思**：
- 优点：及时发现问题
- 缺点：开销大，可能过度优化

**周期性反思**：
- 优点：平衡开销和效果
- 缺点：可能延迟发现问题

**自适应反思**：
- 优点：根据情况调整
- 缺点：实现复杂

---

### 考虑 2：评估指标

**客观指标**：完整度、准确度、效率
- 优点：可量化
- 缺点：可能遗漏重要因素

**主观指标**：用户满意度
- 优点：反映真实需求
- 缺点：难以量化

**推荐**：结合主客观指标

---

### 考虑 3：改进建议

**具体建议**：指出具体问题和解决方案
- 优点：可操作性强
- 缺点：可能过于局限

**通用建议**：提供方向性指导
- 优点：灵活
- 缺点：可能不够具体

**推荐**：先具体后通用

---

## 最小验证

- [ ] 能够定义反思指标
- [ ] 能够实现反思器
- [ ] 能够实现至少一种反思循环策略
- [ ] 能够根据反思结果调整执行

---

## 下一步

- 📖 `notes/07_logging_and_traceability.md` - 日志与可追溯性
- 🧪 `examples/07_reflection_loop.py` - 反思循环示例

---

**记住：反思循环是持续改进的关键机制，就像论文的审稿过程！** 🔄
