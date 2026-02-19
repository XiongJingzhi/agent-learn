"""
示例 02: 任务分解 DAG 实现

演示如何将复杂任务分解为 DAG 并执行

作者：Senior Developer
日期：2026-02-19
"""

from typing import Dict, List
from dataclasses import dataclass
from collections import deque

# ===== 数据结构 =====

@dataclass
class Task:
    """任务定义"""
    id: str
    type: str
    description: str
    dependencies: List[str]
    status: str = "pending"
    result: str = None


class TaskDAG:
    """任务 DAG（邻接表表示）"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.graph: Dict[str, List[str]] = {}

    def add_task(self, task: Task):
        """添加任务"""
        self.tasks[task.id] = task
        self.graph[task.id] = task.dependencies

    def get_ready_tasks(self, completed: set) -> List[Task]:
        """获取可执行任务"""
        ready = []
        for task_id, task in self.tasks.items():
            if task.status != "pending":
                continue

            # 检查所有依赖是否完成
            if all(dep in completed for dep in task.dependencies):
                ready.append(task)

        return ready

    def topological_sort(self) -> List[str]:
        """拓扑排序"""
        in_degree = {task_id: 0 for task_id in self.tasks}

        # 计算入度
        for task_id, deps in self.graph.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[task_id] += 1

        # Kahn 算法
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            task_id = queue.popleft()
            result.append(task_id)

            # 减少依赖此任务的其他任务的入度
            for other_task_id in self.tasks:
                if task_id in self.graph[other_task_id]:
                    in_degree[other_task_id] -= 1
                    if in_degree[other_task_id] == 0:
                        queue.append(other_task_id)

        return result


class TaskExecutor:
    """任务执行器"""

    def __init__(self):
        self.completed = set()
        self.failed = set()
        self.results = {}

    def execute(self, dag: TaskDAG) -> Dict[str, str]:
        """执行 DAG"""
        print(f"\n[执行] 开始执行 {len(dag.tasks)} 个任务\n")

        while True:
            # 获取可执行任务
            ready = dag.get_ready_tasks(self.completed)

            if not ready:
                break

            # 执行所有可执行任务
            for task in ready:
                self._execute_task(task)

        # 打印结果
        self._print_results()

        return self.results

    def _execute_task(self, task: Task):
        """执行单个任务"""
        print(f"[执行] {task.id}: {task.description}")
        print(f"  类型: {task.type}")

        try:
            # 模拟执行
            result = f"{task.type} 完成"
            task.result = result
            task.status = "completed"

            self.completed.add(task.id)
            self.results[task.id] = result

            print(f"  ✓ {result}\n")

        except Exception as e:
            task.status = "failed"
            self.failed.add(task.id)

            print(f"  ✗ 失败: {e}\n")

    def _print_results(self):
        """打印执行结果"""
        print("\n[结果摘要]")
        print(f"成功: {len(self.completed)}/{len(self.completed) + len(self.failed)}")

        if self.failed:
            print(f"失败: {', '.join(self.failed)}")


# ===== 使用示例 =====

def example_search_and_summarize():
    """示例：搜索并总结"""
    print("=" * 70)
    print("示例 1：搜索并总结")
    print("=" * 70)

    dag = TaskDAG()

    # 添加任务
    dag.add_task(Task(
        id="search_docs",
        type="search",
        description="搜索文档",
        dependencies=[]
    ))

    dag.add_task(Task(
        id="search_examples",
        type="search",
        description="搜索示例",
        dependencies=[]
    ))

    dag.add_task(Task(
        id="extract_features",
        type="extract",
        description="提取特性",
        dependencies=["search_docs", "search_examples"]
    ))

    dag.add_task(Task(
        id="summarize",
        type="summarize",
        description="总结",
        dependencies=["extract_features"]
    ))

    # 执行
    executor = TaskExecutor()
    executor.execute(dag)


def example_calculate_and_analyze():
    """示例：计算并分析"""
    print("\n" + "=" * 70)
    print("示例 2：计算并分析")
    print("=" * 70)

    dag = TaskDAG()

    # 添加任务
    dag.add_task(Task(
        id="load_data",
        type="load",
        description="加载数据",
        dependencies=[]
    ))

    dag.add_task(Task(
        id="clean_data",
        type="clean",
        description="清洗数据",
        dependencies=["load_data"]
    ))

    dag.add_task(Task(
        id="calculate_stats",
        type="calculate",
        description="计算统计",
        dependencies=["clean_data"]
    ))

    dag.add_task(Task(
        id="analyze_trend",
        type="analyze",
        description="分析趋势",
        dependencies=["calculate_stats"]
    ))

    # 执行
    executor = TaskExecutor()
    executor.execute(dag)


def example_complex_pipeline():
    """示例：复杂流水线"""
    print("\n" + "=" * 70)
    print("示例 3：复杂流水线")
    print("=" * 70)

    dag = TaskDAG()

    # 阶段 1：数据准备（可并行）
    dag.add_task(Task(
        id="fetch_source_a",
        type="fetch",
        description="从来源 A 获取数据",
        dependencies=[]
    ))

    dag.add_task(Task(
        id="fetch_source_b",
        type="fetch",
        description="从来源 B 获取数据",
        dependencies=[]
    ))

    # 阶段 2：数据处理
    dag.add_task(Task(
        id="process_a",
        type="process",
        description="处理数据 A",
        dependencies=["fetch_source_a"]
    ))

    dag.add_task(Task(
        id="process_b",
        type="process",
        description="处理数据 B",
        dependencies=["fetch_source_b"]
    ))

    # 阶段 3：合并
    dag.add_task(Task(
        id="merge",
        type="merge",
        description="合并数据",
        dependencies=["process_a", "process_b"]
    ))

    # 阶段 4：输出
    dag.add_task(Task(
        id="generate_report",
        type="generate",
        description="生成报告",
        dependencies=["merge"]
    ))

    # 执行
    executor = TaskExecutor()
    executor.execute(dag)


if __name__ == "__main__":
    example_search_and_summarize()
    example_calculate_and_analyze()
    example_complex_pipeline()

    print("\n" + "=" * 70)
    print("所有示例执行完成！")
    print("=" * 70)
