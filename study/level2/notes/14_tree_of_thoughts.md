# Tree of Thoughts (思维树) 推理

> **目标**: 掌握 ToT 推理的原理和实现
> **预计时间**: 50 分钟
> **难度**: ⭐⭐⭐⭐

---

## 什么是 ToT？

Tree of Thoughts (ToT) 是一种推理方法，通过探索多个可能的思维路径并选择最优解。

**类比**：ToT 就像**下棋时的思考**，不是只考虑一步，而是考虑多种可能的走法，然后选择最优的那一步。

---

## 为什么需要 ToT？

### CoT 的局限性

**问题 1：单一路径**
```
问题: "设计一个高效的学习计划"

CoT 方法:
步骤 1: 确定学习目标
步骤 2: 分配时间
步骤 3: 选择学习资源
→ 只有一种方案，可能不是最优的
```

**问题 2：无法回溯**
```
如果 CoT 的某一步错了，后续都跟着错。
无法回到之前的步骤尝试其他方案。
```

### ToT 的优势

**优势 1：多路径探索**
```
探索多个方案：
- 方案 A: 专注理论学习
- 方案 B: 理论+实践结合
- 方案 C: 项目驱动学习
→ 评估并选择最优
```

**优势 2：可以回溯**
```
方案 A 走不通？
回到分叉点，尝试方案 B。
```

---

## ToT 的核心组件

### 组件 1：Thought Generation (思考生成)

生成多个可能的思考步骤。

```python
def generate_thoughts(context: str, num_thoughts: int = 3) -> List[str]:
    """生成多个思考"""
    thoughts = []

    for i in range(num_thoughts):
        thought = f"方案 {chr(65+i)}: 从不同角度思考 {context}"
        thoughts.append(thought)

    return thoughts
```

---

### 组件 2：State Evaluation (状态评估)

评估每个思考状态的质量。

```python
def evaluate_state(state: str, criteria: Dict[str, float]) -> float:
    """评估状态得分"""
    score = 0.0

    # 准则 1: 完整性 (0-0.4)
    if "完整" in state or "详细" in state:
        score += 0.4

    # 准则 2: 可行性 (0-0.3)
    if "可行" in state or "实际" in state:
        score += 0.3

    # 准则 3: 创新性 (0-0.3)
    if "新颖" in state or "创新" in state:
        score += 0.3

    return score
```

---

### 组件 3：Search Algorithm (搜索算法)

选择搜索策略（BFS, DFS, Best-First）。

```python
from typing import List
from dataclasses import dataclass
from collections import deque

@dataclass
class ThoughtNode:
    """思考节点"""
    content: str
    parent: 'ThoughtNode' = None
    children: List['ThoughtNode'] = None
    score: float = 0.0
    depth: int = 0

    def __post_init__(self):
        if self.children is None:
            self.children = []


class ToTSearch:
    """ToT 搜索器"""

    def __init__(self, max_depth: int = 3, max_branches: int = 3):
        self.max_depth = max_depth
        self.max_branches = max_branches

    def bfs_search(self, root: ThoughtNode) -> ThoughtNode:
        """广度优先搜索"""
        queue = deque([root])

        best_node = root

        while queue:
            current = queue.popleft()

            # 如果是叶子节点，评估
            if not current.children or current.depth >= self.max_depth:
                if current.score > best_node.score:
                    best_node = current
                continue

            # 添加子节点到队列
            for child in current.children:
                queue.append(child)

        return best_node

    def dfs_search(self, root: ThoughtNode) -> ThoughtNode:
        """深度优先搜索"""
        best_node = root

        def dfs(node):
            nonlocal best_node

            # 评估当前节点
            if node.score > best_node.score:
                best_node = node

            # 递归子节点
            for child in node.children:
                dfs(child)

        dfs(root)
        return best_node

    def best_first_search(self, root: ThoughtNode) -> ThoughtNode:
        """最佳优先搜索"""
        import heapq

        # 使用最大堆
        heap = []
        heapq.heappush(heap, (-root.score, id(root), root))

        best_node = root

        while heap:
            neg_score, _, current = heapq.heappop(heap)

            # 评估
            if current.score > best_node.score:
                best_node = current

            # 添加子节点
            if current.depth < self.max_depth:
                for child in current.children:
                    heapq.heappush(heap, (-child.score, id(child), child))

        return best_node
```

---

## ToT 实现示例

### 实现 1：规划问题的 ToT

```python
class PlanningToT:
    """规划问题的 ToT 求解"""

    def __init__(self, max_depth: int = 3, max_branches: int = 3):
        self.max_depth = max_depth
        self.max_branches = max_branches
        self.searcher = ToTSearch(max_depth, max_branches)

    def solve(self, problem: str) -> str:
        """求解规划问题"""
        print(f"\n[ToT] 问题: {problem}")
        print("=" * 60)

        # 1. 创建根节点
        root = ThoughtNode(content=f"问题: {problem}", depth=0)

        # 2. 构建思维树
        self._build_tree(root)

        # 3. 搜索最优解
        best = self.searcher.best_first_search(root)

        # 4. 返回路径
        path = self._get_path(best)

        print("\n[最优路径]")
        for i, step in enumerate(path, 1):
            print(f"{i}. {step}")

        return best.content

    def _build_tree(self, node: ThoughtNode):
        """构建思维树"""
        if node.depth >= self.max_depth:
            return

        # 生成多个思考
        thoughts = self._generate_thoughts(node.content, node.depth)

        # 创建子节点
        for thought in thoughts[:self.max_branches]:
            score = self._evaluate_thought(thought, node.depth)
            child = ThoughtNode(
                content=thought,
                parent=node,
                score=score,
                depth=node.depth + 1
            )
            node.children.append(child)

            # 递归构建
            self._build_tree(child)

    def _generate_thoughts(self, context: str, depth: int) -> List[str]:
        """生成思考"""
        if depth == 0:
            return [
                "方案 A: 分解为子任务",
                "方案 B: 直接执行",
                "方案 C: 先做调研"
            ]
        elif depth == 1:
            return [
                "验证方案可行性",
                "评估所需资源",
                "识别潜在风险"
            ]
        else:
            return [
                "结论：方案可行",
                "结论：需要调整",
                "结论：风险过高"
            ]

    def _evaluate_thought(self, thought: str, depth: int) -> float:
        """评估思考"""
        score = 0.5  # 基础分

        if "方案" in thought or "可行" in thought:
            score += 0.2
        if "结论" in thought:
            score += 0.3

        return min(score, 1.0)

    def _get_path(self, node: ThoughtNode) -> List[str]:
        """获取路径"""
        path = []
        while node:
            path.append(node.content)
            node = node.parent
        return list(reversed(path))
```

---

### 实现 2：创意问题的 ToT

```python
class CreativeToT:
    """创意问题的 ToT 求解"""

    def solve_creative_problem(self, problem: str) -> Dict[str, Any]:
        """求解创意问题"""
        print(f"\n[ToT] 创意问题: {problem}")
        print("=" * 60)

        # 1. 生成多个创意方向
        directions = self._generate_directions(problem)

        print("\n[探索创意方向]")
        solutions = []

        for direction in directions:
            print(f"\n方向: {direction}")

            # 2. 对每个方向生成多个方案
            ideas = self._generate_ideas(direction)

            # 3. 评估每个方案
            for idea in ideas:
                score = self._evaluate_creativity(idea)
                print(f"  - {idea} (得分: {score:.2f})")
                solutions.append({"idea": idea, "score": score})

        # 4. 选择最优方案
        best = max(solutions, key=lambda x: x["score"])

        print(f"\n[最优方案] {best['idea']}")
        print(f"[得分] {best['score']:.2f}")

        return best

    def _generate_directions(self, problem: str) -> List[str]:
        """生成创意方向"""
        return [
            "从用户角度思考",
            "从技术角度思考",
            "从商业角度思考"
        ]

    def _generate_ideas(self, direction: str) -> List[str]:
        """生成具体想法"""
        if "用户" in direction:
            return [
                "简化用户界面",
                "增加个性化功能",
                "提供多种交互方式"
            ]
        elif "技术" in direction:
            return [
                "使用新技术优化",
                "重构架构",
                "提升性能"
            ]
        else:
            return [
                "降低成本",
                "增加收入来源",
                "扩大市场"
            ]

    def _evaluate_creativity(self, idea: str) -> float:
        """评估创意"""
        score = 0.5

        # 新颖性
        if "新" in idea or "创新" in idea:
            score += 0.2

        # 实用性
        if "优化" in idea or "提升" in idea:
            score += 0.2

        # 独特性
        if "多" in idea or "个性化" in idea:
            score += 0.1

        return min(score, 1.0)
```

---

## ToT 的搜索策略对比

### 策略 1：BFS (广度优先)

**特点**：
- 逐层探索
- 保证找到最优解（在给定深度内）
- 内存消耗大

**适用**：解空间较小，需要最优解

---

### 策略 2：DFS (深度优先)

**特点**：
- 深入探索一条路径
- 内存消耗小
- 可能错过最优解

**适用**：解空间大，需要快速找到可行解

---

### 策略 3：Best-First (最佳优先)

**特点**：
- 优先探索有希望的节点
- 平衡质量和速度
- 需要好的评估函数

**适用**：大多数场景

---

## ToT 的优缺点

### 优点

1. **探索多解**：不局限于单一思路
2. **质量更高**：从多个方案中选最优
3. **灵活调整**：可以回溯和重新选择

### 缺点

1. **计算成本高**：需要探索多条路径
2. **实现复杂**：需要设计搜索算法
3. **评估依赖**：质量取决于评估函数

---

## ToT 最佳实践

### 实践 1：控制树的规模

```python
def control_tree_size(max_nodes: int):
    """控制树的大小"""
    # 限制深度
    max_depth = 3

    # 限制分支数
    max_branches = 3

    # 总节点数 = 1 + 3 + 3² + 3³ = 40
    # 可控范围
```

---

### 实践 2：设计好的评估函数

```python
def design_evaluation_function():
    """设计评估函数"""

    # 多维度评估
    criteria = {
        "quality": 0.4,      # 质量
        "feasibility": 0.3,  # 可行性
        "novelty": 0.2,      # 新颖性
        "completeness": 0.1  # 完整性
    }

    def evaluate(state):
        score = 0.0
        for criterion, weight in criteria.items():
            score += weight * measure(state, criterion)
        return score

    return evaluate
```

---

### 实践 3：剪枝策略

```python
def prune_tree(node: ThoughtNode, threshold: float):
    """剪除低分节点"""
    if node.score < threshold:
        return True  # 剪除

    for child in node.children[:]:
        if prune_tree(child, threshold):
            node.children.remove(child)

    return False
```

---

## 最小验证

- [ ] 理解 ToT 的原理
- [ ] 能够实现基本的 ToT
- [ ] 能够选择合适的搜索策略
- [ ] 能够设计评估函数

---

## 下一步

- 📖 `notes/15_reflection_reasoning.md` - 反思推理
- 🧪 `examples/04_reasoning_comparison.py` - 推理对比示例

---

**记住：ToT 就像下棋，考虑多种可能的走法，选择最优的那一步！** ♟️
