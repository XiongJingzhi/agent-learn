# 任务分解 DAG

> **目标**: 掌握如何将复杂任务分解为可执行的 DAG
> **预计时间**: 50 分钟
> **难度**: ⭐⭐⭐

---

## 什么是任务分解 DAG？

DAG（Directed Acyclic Graph，有向无环图）是一种任务依赖关系表示：
- **节点（Node）**: 表示一个任务
- **边（Edge）**: 表示任务间的依赖关系
- **无环（Acyclic）**: 没有循环依赖，避免死锁

**类比**：DAG 就像**项目管理中的甘特图**，清晰地表示任务的前后依赖关系。

---

## 为什么需要 DAG？

**问题 1：任务依赖**
- 某些任务必须在其他任务完成后才能开始
- 例如：必须先"搜索信息"，才能"总结信息"

**问题 2：并行执行**
- 没有依赖关系的任务可以并行执行
- 例如："搜索 A" 和 "搜索 B" 可以同时进行

**问题 3：执行顺序**
- DAG 提供了拓扑排序，确定执行顺序

---

## DAG 数据结构

### 表示方式 1：邻接表

```python
from typing import Dict, List

class TaskDAG:
    """任务 DAG（邻接表表示）"""

    def __init__(self):
        self.graph: Dict[str, List[str]] = {}  # 邻接表
        self.tasks: Dict[str, Dict] = {}          # 任务信息

    def add_task(self, task_id: str, task_info: Dict):
        """添加任务"""
        self.tasks[task_id] = task_info
        if task_id not in self.graph:
            self.graph[task_id] = []

    def add_dependency(self, from_task: str, to_task: str):
        """添加依赖：from_task 必须在 to_task 之前完成"""
        if to_task not in self.graph[from_task]:
            self.graph[from_task].append(to_task)

    def get_ready_tasks(self) -> List[str]:
        """获取可以执行的任务（没有未完成的前置任务）"""
        # 计算每个任务的入度（前置任务数）
        in_degree = {}
        for task in self.tasks:
            in_degree[task] = 0

        for from_task, to_tasks in self.graph.items():
            for to_task in to_tasks:
                in_degree[to_task] += 1

        # 返回入度为 0 的任务
        return [task for task, degree in in_degree.items() if degree == 0]

# 使用示例
dag = TaskDAG()

# 添加任务
dag.add_task("search_A", {"type": "search", "query": "A"})
dag.add_task("search_B", {"type": "search", "query": "B"})
dag.add_task("combine", {"type": "combine", "sources": ["A", "B"]})

# 添加依赖
dag.add_dependency("search_A", "combine")  # A 必须在 combine 之前
dag.add_dependency("search_B", "combine")  # B 必须在 combine 之前

# 获取可执行任务
ready = dag.get_ready_tasks()
print(f"可执行任务: {ready}")  # ["search_A", "search_B"]
```

---

### 表示方式 2：边列表

```python
class EdgeListDAG:
    """任务 DAG（边列表表示）"""

    def __init__(self):
        self.edges = []  # (from_task, to_task) 列表
        self.nodes = set()

    def add_task(self, task_id: str):
        """添加任务节点"""
        self.nodes.add(task_id)

    def add_dependency(self, from_task: str, to_task: str):
        """添加依赖边"""
        self.edges.append((from_task, to_task))

    def topological_sort(self) -> List[str]:
        """拓扑排序：返回执行顺序"""
        # 简化的拓扑排序实现
        sorted_tasks = []
        visited = set()

        def visit(task):
            if task in visited:
                return
            visited.add(task)

            # 先访问依赖的任务
            for (from_task, to_task) in self.edges:
                if to_task == task:
                    visit(from_task)

            sorted_tasks.append(task)

        for task in self.nodes:
            visit(task)

        return sorted_tasks
```

---

## 任务分解策略

### 策略 1：水平分解

将任务按功能模块分解。

**示例**：
```
任务：创建一个个人财务助手

分解为：
1. 记账功能
2. 预算功能
3. 投资功能
4. 报表功能
```

**适用场景**：任务包含多个独立的功能模块

---

### 策略 2：垂直分解

将任务按处理流程分解。

**示例**：
```
任务：搜索并总结 LangGraph 的信息

分解为：
1. 搜索 LangGraph 文档
2. 提取关键特性
3. 总结核心要点
```

**适用场景**：任务有明确的处理流程

---

### 策略 3：混合分解

结合水平和垂直分解。

**示例**：
```
任务：构建一个数据分析 Agent

分解为：
1. 数据获取阶段
   - 连接数据库
   - 执行查询
   - 验证数据

2. 数据处理阶段
   - 清洗数据
   - 转换格式
   - 计算指标

3. 结果展示阶段
   - 生成图表
   - 导出报告
```

**适用场景**：复杂的系统工程

---

## 完整示例：任务分解与执行

```python
from typing import Dict, List

class TaskDecomposer:
    """任务分解器"""

    def decompose(self, input: str) -> List[Dict]:
        """分解任务为 DAG"""
        print(f"\n[任务分解] 输入: {input}")

        # 分析任务类型
        if "搜索" in input and "总结" in input:
            return self._decompose_search_and_summarize(input)
        elif "计算" in input and "分析" in input:
            return self._decompose_calculate_and_analyze(input)
        else:
            return self._decompose_simple(input)

    def _decompose_search_and_summarize(self, input: str) -> List[Dict]:
        """分解：搜索并总结"""
        tasks = [
            {
                "id": "task_1",
                "type": "search",
                "description": "搜索 LangGraph 文档",
                "dependencies": []
            },
            {
                "id": "task_2",
                "type": "search",
                "description": "搜索 LangGraph 示例",
                "dependencies": []
            },
            {
                "id": "task_3",
                "type": "extract",
                "description": "提取关键特性",
                "dependencies": ["task_1", "task_2"]  # 依赖前两个任务
            },
            {
                "id": "task_4",
                "type": "summarize",
                "description": "总结核心要点",
                "dependencies": ["task_3"]
            }
        ]

        self._print_dag(tasks)
        return tasks

    def _decompose_calculate_and_analyze(self, input: str) -> List[Dict]:
        """分解：计算并分析"""
        tasks = [
            {
                "id": "task_1",
                "type": "calculate",
                "description": "计算基础统计",
                "dependencies": []
            },
            {
                "id": "task_2",
                "type": "calculate",
                "description": "计算高级指标",
                "dependencies": ["task_1"]
            },
            {
                "id": "task_3",
                "type": "analyze",
                "description": "分析结果",
                "dependencies": ["task_2"]
            }
        ]

        self._print_dag(tasks)
        return tasks

    def _decompose_simple(self, input: str) -> List[Dict]:
        """分解：简单任务"""
        tasks = [
            {
                "id": "task_1",
                "type": "process",
                "description": f"处理: {input}",
                "dependencies": []
            }
        ]

        self._print_dag(tasks)
        return tasks

    def _print_dag(self, tasks: List[Dict]):
        """打印 DAG 结构"""
        print("\n[DAG 结构]")
        for task in tasks:
            deps = task.get("dependencies", [])
            deps_str = " -> ".join(deps) + " -> " if deps else ""
            print(f"  {deps_str}{task['id']}: {task['description']}")


class DAGExecutor:
    """DAG 执行器"""

    def execute(self, tasks: List[Dict]) -> Dict:
        """执行 DAG"""
        print("\n[DAG 执行]")

        # 构建邻接表
        graph = {}
        for task in tasks:
            graph[task['id']] = task.get('dependencies', [])

        # 拓扑排序
        sorted_tasks = self._topological_sort(graph)

        # 执行任务
        results = {}
        for task_id in sorted_tasks:
            task = next(t for t in tasks if t['id'] == task_id)
            print(f"\n  执行: {task_id}")
            print(f"    类型: {task['type']}")
            print(f"    描述: {task['description']}")

            # 模拟执行
            result = f"{task['type']} 的结果"
            results[task_id] = result

            print(f"    结果: {result}")

        return results

    def _topological_sort(self, graph: Dict[str, List[str]]) -> List[str]:
        """拓扑排序"""
        sorted_tasks = []
        visited = set()

        def visit(node):
            if node in visited:
                return
            visited.add(node)

            # 先访问依赖
            for dep in graph.get(node, []):
                visit(dep)

            sorted_tasks.append(node)

        for node in graph:
            visit(node)

        return sorted_tasks


# 运行示例
def main():
    print("=" * 70)
    print("任务分解 DAG 示例")
    print("=" * 70)

    decomposer = TaskDecomposer()
    executor = DAGExecutor()

    # 示例 1：搜索并总结
    print("\n【示例 1】搜索并总结")
    tasks1 = decomposer.decompose("搜索并总结 LangGraph 的信息")
    results1 = executor.execute(tasks1)

    # 示例 2：计算并分析
    print("\n\n【示例 2】计算并分析")
    tasks2 = decomposer.decompose("计算数据的平均值并分析趋势")
    results2 = executor.execute(tasks2)

    print("\n" + "=" * 70)
    print("所有任务执行完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：任务粒度

**太粗**：无法并行，无法跟踪进度
- *坏*：一个任务做所有事情

**太细**：调度开销大，管理复杂
- *坏*：每个变量声明都是一个任务

**合适**：每个任务是一个有意义的步骤
- *好*："搜索文档"、"提取信息"、"生成答案"

---

### 考虑 2：依赖关系

**避免循环依赖**：
- *坏*：A 依赖 B，B 依赖 A（死锁）

**最小化依赖**：
- *好*：只有真正需要依赖才建立依赖

**显式声明**：
- *好*：在任务定义中明确列出依赖

---

### 考虑 3：并行执行

**识别可并行任务**：
- *好*：搜索 A 和搜索 B 可以并行

**资源限制**：
- *好*：限制并行任务数量，避免资源耗尽

---

## 最小验证

- [ ] 能够设计任务 DAG
- [ ] 能够实现拓扑排序
- [ ] 能够识别可并行任务
- [ ] 能够处理依赖关系

---

## 下一步

- 📖 `notes/02_dependency_and_priority.md` - 依赖与优先级
- 🧪 `examples/02_task_decomposition.py` - 任务分解示例

---

**记住：DAG 就像项目管理中的甘特图，清晰地表示任务的前后依赖关系！** 📊
