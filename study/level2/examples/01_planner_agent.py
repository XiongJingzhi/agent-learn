"""
示例 01: Planning Agent 完整示例

演示 PER (Planner-Executor-Reflector) 架构的完整实现

作者：Senior Developer
日期：2026-02-19
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time

# ===== 数据结构 =====

@dataclass
class Task:
    """任务定义"""
    id: str
    type: str  # 'search', 'calculate', 'llm_query'
    description: str
    dependencies: List[str]
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None

@dataclass
class ExecutionPlan:
    """执行计划"""
    tasks: List[Task]
    dag: Dict[str, List[str]]  # adjacency list
    estimated_steps: int

@dataclass
class ExecutionContext:
    """执行上下文"""
    task_results: Dict[str, Any]
    current_step: int
    errors: List[str]

@dataclass
class Reflection:
    """反思结果"""
    completeness: float  # 0.0 - 1.0
    issues: List[str]
    next_action: str  # 'finish', 'replan', 'continue'
    suggestions: List[str]

# ===== Planner =====

class Planner:
    """规划器：分解任务并制定计划"""

    def plan(self, input: str, available_tools: List[str]) -> ExecutionPlan:
        """制定执行计划"""
        print(f"\n[规划器] 分析输入: {input}")

        # 分析任务类型
        if "搜索" in input and "总结" in input:
            tasks = self._create_search_tasks()
        elif "计算" in input:
            tasks = self._create_calculation_tasks()
        else:
            tasks = self._create_simple_tasks(input)

        # 构建 DAG
        dag = self._build_dag(tasks)

        plan = ExecutionPlan(
            tasks=tasks,
            dag=dag,
            estimated_steps=len(tasks)
        )

        print(f"[规划器] 制定计划: {plan.estimated_steps} 个任务")
        self._print_plan(plan)

        return plan

    def _create_search_tasks(self) -> List[Task]:
        """创建搜索任务"""
        return [
            Task(
                id="search_docs",
                type="search",
                description="搜索 LangGraph 官方文档",
                dependencies=[]
            ),
            Task(
                id="search_examples",
                type="search",
                description="搜索 LangGraph 示例代码",
                dependencies=[]
            ),
            Task(
                id="extract_features",
                type="llm_query",
                description="提取关键特性",
                dependencies=["search_docs", "search_examples"]
            ),
            Task(
                id="summarize",
                type="llm_query",
                description="总结核心要点",
                dependencies=["extract_features"]
            )
        ]

    def _create_calculation_tasks(self) -> List[Task]:
        """创建计算任务"""
        return [
            Task(
                id="calc_basic",
                type="calculate",
                description="计算基础统计（平均值、中位数）",
                dependencies=[]
            ),
            Task(
                id="calc_advanced",
                type="calculate",
                description="计算高级指标（方差、标准差）",
                dependencies=["calc_basic"]
            ),
            Task(
                id="analyze_trend",
                type="llm_query",
                description="分析趋势",
                dependencies=["calc_advanced"]
            )
        ]

    def _create_simple_tasks(self, input: str) -> List[Task]:
        """创建简单任务"""
        return [
            Task(
                id="process",
                type="llm_query",
                description=f"处理: {input}",
                dependencies=[]
            )
        ]

    def _build_dag(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """构建 DAG"""
        dag = {}
        for task in tasks:
            dag[task.id] = task.dependencies
        return dag

    def _print_plan(self, plan: ExecutionPlan):
        """打印计划"""
        print("\n[计划详情]")
        for task in plan.tasks:
            deps = task.dependencies or ["无"]
            print(f"  {task.id}: {task.description}")
            print(f"    类型: {task.type}")
            print(f"    依赖: {', '.join(deps)}")

# ===== Executor =====

class Executor:
    """执行器：执行任务并维护状态"""

    def __init__(self):
        self.context = ExecutionContext(
            task_results={},
            current_step=0,
            errors=[]
        )

    def execute(self, plan: ExecutionPlan) -> ExecutionContext:
        """执行计划"""
        print(f"\n[执行器] 开始执行 {plan.estimated_steps} 个任务")

        # 拓扑排序
        execution_order = self._topological_sort(plan.dag)

        # 执行任务
        for task_id in execution_order:
            task = next(t for t in plan.tasks if t.id == task_id)

            if self._can_execute(task, plan):
                print(f"\n  [执行] {task.id}")
                print(f"    描述: {task.description}")

                task.status = "in_progress"

                try:
                    result = self._execute_task(task, self.context)
                    task.result = result
                    task.status = "completed"

                    self.context.task_results[task.id] = result
                    print(f"    ✓ 完成: {result}")

                except Exception as e:
                    task.status = "failed"
                    error_msg = f"{task.id} 失败: {str(e)}"
                    self.context.errors.append(error_msg)
                    print(f"    ✗ 失败: {error_msg}")

            else:
                print(f"\n  [跳过] {task.id} - 依赖未满足")

        self.context.current_step = len([
            t for t in plan.tasks if t.status == "completed"
        ])

        print(f"\n[执行器] 完成: {self.context.current_step}/{plan.estimated_steps} 个任务")
        return self.context

    def _can_execute(self, task: Task, plan: ExecutionPlan) -> bool:
        """检查任务是否可以执行"""
        # 检查所有依赖是否完成
        for dep_id in task.dependencies:
            dep_task = next((t for t in plan.tasks if t.id == dep_id), None)
            if not dep_task or dep_task.status != "completed":
                return False
        return True

    def _execute_task(self, task: Task, context: ExecutionContext) -> str:
        """执行单个任务"""
        if task.type == "search":
            return f"找到相关信息: {task.description}"
        elif task.type == "calculate":
            return f"计算完成: {task.description}"
        elif task.type == "llm_query":
            return f"LLM 处理: {task.description}"
        else:
            return f"执行完成: {task.description}"

    def _topological_sort(self, dag: Dict[str, List[str]]) -> List[str]:
        """拓扑排序"""
        sorted_tasks = []
        visited = set()

        def visit(node):
            if node in visited:
                return
            visited.add(node)

            for dep in dag.get(node, []):
                visit(dep)

            sorted_tasks.append(node)

        for node in dag.keys():
            visit(node)

        return sorted_tasks

# ===== Reflector =====

class Reflector:
    """反思器：评估结果并决定下一步"""

    def reflect(self, input: str, context: ExecutionContext, plan: ExecutionPlan) -> Reflection:
        """反思执行结果"""
        print(f"\n[反思器] 评估执行结果")

        # 计算完成度
        completed_count = sum(
            1 for t in plan.tasks
            if t.status == "completed"
        )
        total_count = len(plan.tasks)
        completeness = completed_count / total_count if total_count > 0 else 0

        # 识别问题
        issues = []
        if context.errors:
            issues.extend(context.errors)

        failed_tasks = [t.id for t in plan.tasks if t.status == "failed"]
        if failed_tasks:
            issues.append(f"失败的任务: {', '.join(failed_tasks)}")

        # 判断下一步
        if completeness >= 0.9:
            next_action = "finish"
        elif completeness >= 0.5 or not issues:
            next_action = "continue"
        else:
            next_action = "replan"

        # 生成建议
        suggestions = []
        if next_action == "replan":
            suggestions.append("考虑调整任务顺序")
        if issues:
            suggestions.append(f"解决以下问题: {issues}")

        reflection = Reflection(
            completeness=completeness,
            issues=issues,
            next_action=next_action,
            suggestions=suggestions
        )

        print(f"[反思器] 完成度: {completeness:.2f}")
        print(f"[反思器] 问题: {issues}")
        print(f"[反思器] 下一步: {next_action}")

        return reflection

# ===== PER Agent =====

class PERAgent:
    """PER Agent: 整合 Planner、Executor、Reflector"""

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.reflector = Reflector()
        self.max_iterations = 3

    def run(self, input: str) -> str:
        """运行 PER Agent"""
        print("=" * 70)
        print("PER Agent 示例")
        print("=" * 70)
        print(f"输入: {input}\n")

        for iteration in range(self.max_iterations):
            print(f"\n{'=' * 70}")
            print(f"迭代 {iteration + 1}/{self.max_iterations}")
            print('=' * 70)

            # 1. 规划
            plan = self.planner.plan(input, ["search", "calculate"])

            # 2. 执行
            context = self.executor.execute(plan)

            # 3. 反思
            reflection = self.reflector.reflect(input, context, plan)

            # 4. 判断下一步
            if reflection.next_action == "finish":
                print(f"\n{'=' * 70}")
                print("任务完成！")
                print("=" * 70)
                return self._generate_final_answer(context)

            elif reflection.next_action == "replan":
                print(f"\n{'=' * 70}")
                print("重新规划...")
                print("=" * 70)
                input = self._update_input(input, reflection.suggestions)

        return "达到最大迭代次数"

    def _generate_final_answer(self, context: ExecutionContext) -> str:
        """生成最终答案"""
        results = list(context.task_results.values())
        return f"基于执行结果的答案: {', '.join(results)}"

    def _update_input(self, input: str, suggestions: List[str]) -> str:
        """更新输入"""
        return f"{input}（注：{', '.join(suggestions)}）"


# ===== 运行示例 =====

def main():
    """主函数"""
    agent = PERAgent()

    # 示例 1：搜索并总结
    print("\n【示例 1】搜索并总结 LangGraph 信息")
    result1 = agent.run("搜索并总结 LangGraph 的核心特性")
    print(f"\n最终结果: {result1}\n")

    # 示例 2：计算并分析
    print("\n【示例 2】计算并分析数据")
    result2 = agent.run("计算一组数据的统计信息并分析趋势")
    print(f"\n最终结果: {result2}\n")


if __name__ == "__main__":
    main()
