"""
示例 04: 推理机制对比实现

演示 ReAct、CoT、ToT、Reflection 四种推理机制的实现和对比

作者：Senior Developer
日期：2026-02-19
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import copy

# ===== 基础类 =====

@dataclass
class Thought:
    """思考步骤"""
    content: str
    timestamp: int = 0

    def __str__(self):
        return self.content


@dataclass
class ReasoningResult:
    """推理结果"""
    answer: str
    reasoning_steps: List[Thought] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=defaultdict)

    def __post_init__(self):
        if not self.metadata:
            self.metadata = {}


from collections import defaultdict


# ===== ReAct 推理 =====

class ReActReasoner:
    """ReAct 推理器"""

    def __init__(self, tools: Dict[str, callable] = None):
        self.tools = tools or {}

    def reason(self, query: str, max_steps: int = 10) -> ReasoningResult:
        """使用 ReAct 循环推理"""
        print(f"\n[ReAct] 查询: {query}")
        print("=" * 60)

        steps = []
        history = []

        for step in range(max_steps):
            # 1. 思考
            thought = self._think(query, history)
            print(f"\n[步骤 {step + 1}] 思考: {thought}")

            thought_obj = Thought(content=thought)
            steps.append(thought_obj)
            history.append({"type": "thought", "content": thought})

            # 2. 判断是否完成
            if self._should_answer(thought, history):
                answer = self._generate_answer(query, history)
                print(f"[完成] 答案: {answer}\n")
                return ReasoningResult(answer=answer, reasoning_steps=steps)

            # 3. 解析行动
            action = self._parse_action(thought)
            print(f"[行动] {action['tool']}: {action['input']}")

            # 4. 执行并观察
            observation = self._execute_action(action)
            print(f"[观察] {observation}")

            history.append({
                "type": "action",
                "action": action,
                "observation": observation
            })

        return ReasoningResult(answer="达到最大步数", reasoning_steps=steps)

    def _think(self, query: str, history: List[Dict]) -> str:
        """生成思考"""
        if not history:
            return f"我需要分析查询: {query}，并决定使用什么工具"
        else:
            last_obs = history[-1].get("observation", "")
            return f"基于观察 '{last_obs}'，我可以继续或回答"

    def _should_answer(self, thought: str, history: List[Dict]) -> bool:
        """判断是否应该给出答案"""
        # 简化：如果有足够的观察，就回答
        action_count = sum(1 for h in history if h.get("type") == "action")
        return action_count >= 2 or "完成" in thought or "回答" in thought

    def _parse_action(self, thought: str) -> Dict[str, str]:
        """从思考中解析行动"""
        # 简化：循环使用不同的工具
        tools = ["search", "calculate", "lookup"]
        action_count = sum(1 for h in thought.split() if "工具" in h)
        tool_name = tools[action_count % len(tools)]
        return {"tool": tool_name, "input": thought}

    def _execute_action(self, action: Dict) -> str:
        """执行行动"""
        tool_name = action["tool"]
        if tool_name in self.tools:
            return self.tools[tool_name](action["input"])
        return f"执行 {tool_name} 的结果"

    def _generate_answer(self, query: str, history: List[Dict]) -> str:
        """生成最终答案"""
        return f"基于 {len(history)} 步推理，答案是：42"


# ===== CoT 推理 =====

class CoTReasoner:
    """Chain of Thought 推理器"""

    def reason(self, query: str) -> ReasoningResult:
        """使用思维链推理"""
        print(f"\n[CoT] 查询: {query}")
        print("=" * 60)

        # 1. 生成推理链
        reasoning_steps = self._generate_reasoning(query)

        print("\n[推理链]")
        steps = []
        for i, step_content in enumerate(reasoning_steps, 1):
            print(f"{i}. {step_content}")
            steps.append(Thought(content=step_content))

        # 2. 生成最终答案
        answer = self._generate_answer(query, reasoning_steps)
        print(f"\n[答案] {answer}\n")

        return ReasoningResult(answer=answer, reasoning_steps=steps)

    def _generate_reasoning(self, query: str) -> List[str]:
        """生成推理步骤"""
        # 根据查询类型生成不同的推理链
        if "计算" in query:
            return [
                "首先，我需要理解计算问题的要求",
                "然后，我需要识别相关的数值和运算",
                "接着，我按照运算顺序进行计算",
                "最后，我验证结果的合理性"
            ]
        elif "分析" in query:
            return [
                "首先，我需要理解分析的对象",
                "然后，我收集相关的信息和数据",
                "接着，我识别关键的模式和趋势",
                "最后，我得出结论和建议"
            ]
        else:
            return [
                "首先，我需要理解问题的核心",
                "然后，我收集相关的信息",
                "接着，我分析和综合信息",
                "最后，我得出答案"
            ]

    def _generate_answer(self, query: str, reasoning: List[str]) -> str:
        """基于推理链生成答案"""
        return f"基于上述 {len(reasoning)} 步推理，答案是：42"


# ===== ToT 推理 =====

@dataclass
class ThoughtNode:
    """思考节点"""
    content: str
    parent: Optional['ThoughtNode'] = None
    children: List['ThoughtNode'] = field(default_factory=list)
    score: float = 0.0
    depth: int = 0

    def add_child(self, content: str, score: float = 0.0) -> 'ThoughtNode':
        """添加子节点"""
        child = ThoughtNode(
            content=content,
            parent=self,
            score=score,
            depth=self.depth + 1
        )
        self.children.append(child)
        return child

    def get_path(self) -> List[str]:
        """获取从根到当前节点的路径"""
        path = []
        node = self
        while node:
            path.append(node.content)
            node = node.parent
        return list(reversed(path))

    def is_leaf(self) -> bool:
        """是否是叶子节点"""
        return len(self.children) == 0


class ToTReasoner:
    """Tree of Thoughts 推理器"""

    def __init__(self, max_branches: int = 3, max_depth: int = 3):
        self.max_branches = max_branches
        self.max_depth = max_depth

    def reason(self, query: str) -> ReasoningResult:
        """使用思维树推理"""
        print(f"\n[ToT] 查询: {query}")
        print("=" * 60)

        # 1. 构建思维树
        root = ThoughtNode(content=f"问题: {query}", depth=0)
        self._expand_tree(root)

        # 2. 评估所有路径
        leaves = self._get_leaves(root)

        print("\n[探索的路径]")
        for i, leaf in enumerate(leaves, 1):
            path = leaf.get_path()
            print(f"\n路径 {i} (分数: {leaf.score:.2f}):")
            for j, step in enumerate(path):
                indent = "  " * j
                print(f"{indent}{j+1}. {step}")

        # 3. 选择最优路径
        best_leaf = max(leaves, key=lambda n: n.score)

        # 4. 转换为推理步骤
        steps = [Thought(content=s) for s in best_leaf.get_path()]

        print(f"\n[最优答案] {best_leaf.content}\n")

        return ReasoningResult(answer=best_leaf.content, reasoning_steps=steps)

    def _expand_tree(self, node: ThoughtNode):
        """展开思维树"""
        if node.depth >= self.max_depth:
            return

        # 生成多个可能的思考
        thoughts = self._generate_thoughts(node.content, node.depth)

        # 限制分支数量
        for thought in thoughts[:self.max_branches]:
            # 评估这个思考
            score = self._evaluate_thought(thought, node.depth)

            # 添加子节点
            child = node.add_child(thought, score)

            # 递归展开
            self._expand_tree(child)

    def _generate_thoughts(self, context: str, depth: int) -> List[str]:
        """生成可能的思考"""
        if depth == 0:
            return [
                f"从角度 A 思考: {context}",
                f"从角度 B 思考: {context}",
                f"从角度 C 思考: {context}"
            ]
        elif depth == 1:
            return [
                f"分析方法 A 的可行性",
                f"分析方法 B 的可行性",
                f"分析方法 C 的可行性"
            ]
        else:
            return [
                "结论：方案 A 最优",
                "结论：方案 B 最优",
                "结论：需要更多信息"
            ]

    def _evaluate_thought(self, thought: str, depth: int) -> float:
        """评估思考的质量"""
        # 简化：基于深度和内容的启发式评分
        base_score = 0.5

        if "最优" in thought or "结论" in thought:
            base_score += 0.3
        if "可行性" in thought:
            base_score += 0.2

        # 深度越深，分数越高（假设更深层次的思考更好）
        depth_bonus = depth * 0.1

        return min(base_score + depth_bonus, 1.0)

    def _get_leaves(self, root: ThoughtNode) -> List[ThoughtNode]:
        """获取所有叶子节点"""
        leaves = []

        def traverse(node):
            if node.is_leaf():
                leaves.append(node)
            else:
                for child in node.children:
                    traverse(child)

        traverse(root)
        return leaves


# ===== Reflection 推理 =====

class ReflectionReasoner:
    """反思推理器"""

    def __init__(self, max_reflections: int = 2):
        self.max_reflections = max_reflections

    def reason(self, query: str) -> ReasoningResult:
        """使用反思推理"""
        print(f"\n[Reflection] 查询: {query}")
        print("=" * 60)

        current_answer = None
        all_steps = []

        for iteration in range(self.max_reflections + 1):
            print(f"\n{'='*60}")
            print(f"迭代 {iteration + 1}/{self.max_reflections + 1}")
            print('='*60)

            if iteration == 0:
                # 第一次：生成初步答案
                answer, steps = self._generate_initial_answer(query)
                print(f"[初步答案] {answer}")
                current_answer = answer
                all_steps.extend(steps)
            else:
                # 后续：反思并改进
                reflection = self._reflect(query, current_answer)
                print(f"[反思] {reflection}")

                improved_answer, steps = self._improve_answer(query, current_answer, reflection)
                print(f"[改进答案] {improved_answer}")

                all_steps.extend(steps)
                current_answer = improved_answer

        print(f"\n[最终答案] {current_answer}\n")

        return ReasoningResult(answer=current_answer, reasoning_steps=all_steps)

    def _generate_initial_answer(self, query: str) -> tuple[str, List[Thought]]:
        """生成初步答案"""
        steps = [
            Thought(content="理解问题的要求"),
            Thought(content="收集相关信息"),
            Thought(content="分析和综合"),
            Thought(content="得出初步结论")
        ]

        for step in steps:
            print(f"  - {step.content}")

        return "这是初步的答案：42", steps

    def _reflect(self, query: str, answer: str) -> str:
        """反思答案"""
        reflections = [
            "答案可以更详细一些",
            "需要提供更多的解释",
            "应该考虑其他可能性",
            "逻辑可以更严密"
        ]
        # 简化：循环使用不同的反思
        import random
        return random.choice(reflections)

    def _improve_answer(self, query: str, answer: str, reflection: str) -> tuple[str, List[Thought]]:
        """改进答案"""
        steps = [
            Thought(content=f"反思: {reflection}"),
            Thought(content="重新分析问题"),
            Thought(content="补充细节"),
            Thought(content="优化表达")
        ]

        for step in steps:
            print(f"  - {step.content}")

        improved = f"{answer}（根据反思'{reflection}'改进后）"
        return improved, steps


# ===== 对比和测试 =====

def compare_reasoning_mechanisms():
    """对比不同的推理机制"""
    print("=" * 70)
    print("推理机制对比")
    print("=" * 70)

    # 测试查询
    queries = [
        "计算 1+1 的结果",
        "分析这个问题并给出建议",
        "探索解决方案的可能性"
    ]

    # 创建推理器
    react_reasoner = ReActReasoner()
    cot_reasoner = CoTReasoner()
    tot_reasoner = ToTReasoner(max_branches=2, max_depth=2)
    reflection_reasoner = ReflectionReasoner(max_reflections=1)

    reasoners = {
        "ReAct": react_reasoner,
        "CoT": cot_reasoner,
        "ToT": tot_reasoner,
        "Reflection": reflection_reasoner
    }

    # 对每个查询使用不同的推理机制
    for query in queries:
        print("\n" + "=" * 70)
        print(f"查询: {query}")
        print("=" * 70)

        for name, reasoner in reasoners.items():
            try:
                result = reasoner.reason(query)
                print(f"[{name}] 最终答案: {result.answer[:100]}...")
                print(f"[{name}] 推理步骤数: {len(result.reasoning_steps)}")
            except Exception as e:
                print(f"[{name}] 错误: {e}")


def benchmark_reasoning():
    """基准测试不同推理机制"""
    print("\n" + "=" * 70)
    print("推理机制基准测试")
    print("=" * 70)

    import time

    query = "分析并解决这个问题"

    reasoners = {
        "ReAct": ReActReasoner(),
        "CoT": CoTReasoner(),
        "ToT": ToTReasoner(max_branches=2, max_depth=2),
        "Reflection": ReflectionReasoner(max_reflections=1)
    }

    results = {}

    for name, reasoner in reasoners.items():
        start = time.time()
        result = reasoner.reason(query)
        end = time.time()

        results[name] = {
            "time": end - start,
            "steps": len(result.reasoning_steps),
            "answer_length": len(result.answer)
        }

    # 打印对比结果
    print("\n[对比结果]")
    print(f"{'机制':<15} {'时间(s)':<10} {'步骤数':<10} {'答案长度':<10}")
    print("-" * 50)
    for name, metrics in results.items():
        print(f"{name:<15} {metrics['time']:<10.2f} {metrics['steps']:<10} {metrics['answer_length']:<10}")


# ===== 使用示例 =====

if __name__ == "__main__":
    # 示例 1：对比推理机制
    compare_reasoning_mechanisms()

    # 示例 2：基准测试
    benchmark_reasoning()

    print("\n" + "=" * 70)
    print("所有示例执行完成！")
    print("=" * 70)
