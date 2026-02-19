"""
示例 1: 层次化多智能体系统 (Hierarchical Multi-Agent System)

本示例展示如何实现一个 Manager-Agent 架构的多智能体系统。
Manager 负责任务分解和协调，Worker Agents 负责具体执行。

架构：
         Manager
       /    |    \
   Researcher Writer  Critic
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class Agent:
    """Agent 类"""
    name: str
    role: str
    goal: str
    backstory: str = ""

    def __repr__(self):
        return f"Agent({self.name}, {self.role})"


@dataclass
class Task:
    """任务类"""
    description: str
    assigned_to: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None

    def to_dict(self):
        return {
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "result": self.result
        }


@dataclass
class Message:
    """消息类"""
    from_agent: str
    to_agent: str
    content: Dict[str, Any]
    msg_type: str = "task"


# ============================================================================
# Manager Agent
# ============================================================================

class ManagerAgent:
    """Manager Agent - 负责任务分解和协调"""

    def __init__(self, name: str = "Manager"):
        self.name = name
        self.workers: Dict[str, 'WorkerAgent'] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []

    def add_worker(self, worker: 'WorkerAgent'):
        """添加 Worker Agent"""
        self.workers[worker.name] = worker
        worker.set_manager(self)
        print(f"[{self.name}] 添加 Worker: {worker.name} ({worker.role})")

    def decompose_task(self, task_description: str) -> List[Task]:
        """分解任务为子任务"""
        print(f"\n[{self.name}] 正在分解任务: {task_description}")

        # 简化的任务分解逻辑
        subtasks = [
            Task(description=f"研究：{task_description}"),
            Task(description=f"写作：基于研究结果"),
            Task(description=f"审核：检查内容质量")
        ]

        for i, subtask in enumerate(subtasks):
            print(f"  [{i+1}] {subtask.description}")

        return subtasks

    def assign_tasks(self, tasks: List[Task]):
        """分配任务给合适的 Worker"""
        print(f"\n[{self.name}] 正在分配任务...")

        for task in tasks:
            # 根据任务类型分配给合适的 Worker
            if "研究" in task.description:
                worker = self.get_worker_by_role("研究员")
            elif "写作" in task.description:
                worker = self.get_worker_by_role("作家")
            elif "审核" in task.description:
                worker = self.get_worker_by_role("审核员")
            else:
                worker = None

            if worker:
                task.assigned_to = worker.name
                task.status = "assigned"
                worker.receive_task(task)
                print(f"  ✓ 任务 '{task.description[:30]}...' → {worker.name}")

    def get_worker_by_role(self, role: str) -> Optional['WorkerAgent']:
        """根据角色获取 Worker"""
        for worker in self.workers.values():
            if role in worker.role:
                return worker
        return None

    def coordinate_execution(self):
        """协调任务执行"""
        print(f"\n[{self.name}] 协调任务执行...")

        # 简化的执行逻辑：依次执行每个 Worker 的任务
        results = {}
        for worker in self.workers.values():
            print(f"\n→ 执行 {worker.name} 的任务...")
            result = worker.execute()
            if result:
                results[worker.name] = result

        return results

    def aggregate_results(self, results: Dict[str, str]) -> str:
        """汇总结果"""
        print(f"\n[{self.name}] 汇总结果...")

        final_output = "\n=== 最终输出 ===\n"
        for worker_name, result in results.items():
            final_output += f"\n[{worker_name} 的贡献]\n{result}\n"

        return final_output

    def process(self, user_input: str) -> str:
        """处理用户请求"""
        print(f"\n{'='*60}")
        print(f"[{self.name}] 收到用户请求: {user_input}")
        print(f"{'='*60}")

        # 1. 分解任务
        tasks = self.decompose_task(user_input)

        # 2. 分配任务
        self.assign_tasks(tasks)

        # 3. 协调执行
        results = self.coordinate_execution()

        # 4. 汇总结果
        final_output = self.aggregate_results(results)

        return final_output


# ============================================================================
# Worker Agent
# ============================================================================

class WorkerAgent:
    """Worker Agent - 负责具体任务执行"""

    def __init__(self, name: str, role: str, goal: str):
        self.name = name
        self.role = role
        self.goal = goal
        self.manager: Optional[ManagerAgent] = None
        self.current_task: Optional[Task] = None

    def set_manager(self, manager: ManagerAgent):
        """设置 Manager"""
        self.manager = manager

    def receive_task(self, task: Task):
        """接收任务"""
        self.current_task = task
        print(f"  [{self.name}] 收到任务: {task.description}")

    def execute(self) -> Optional[str]:
        """执行任务"""
        if not self.current_task:
            return None

        print(f"  [{self.name}] 正在执行任务...")

        # 模拟任务执行
        self.current_task.status = "in_progress"

        # 根据角色生成不同的结果
        if "研究" in self.role:
            result = self._do_research(self.current_task.description)
        elif "作家" in self.role or "写作" in self.role:
            result = self._do_writing(self.current_task.description)
        elif "审核" in self.role:
            result = self._do_review(self.current_task.description)
        else:
            result = "任务已完成"

        self.current_task.status = "completed"
        self.current_task.result = result

        return result

    def _do_research(self, topic: str) -> str:
        """研究任务"""
        return f"""
关于 {topic} 的研究成果：

1. 核心概念：这是一个重要的技术领域
2. 主要特点：具有创新性和实用性
3. 应用场景：广泛用于各种实际项目
4. 发展趋势：持续演进和优化

关键发现：该领域正处于快速发展阶段，值得深入探索。
"""

    def _do_writing(self, topic: str) -> str:
        """写作任务"""
        return f"""
基于研究的文章：

# {topic} 简介

{topic} 是一个令人兴奋的技术领域。通过深入研究和实践，
我们发现它具有巨大的潜力。

## 主要优势

- 提高效率
- 降低成本
- 改善用户体验

## 总结

{topic} 为我们提供了强大的工具和思路，值得学习和应用。
"""

    def _do_review(self, content: str) -> str:
        """审核任务"""
        return f"""
审核意见：

✓ 内容结构清晰
✓ 观点明确
✓ 逻辑连贯

建议：
- 可以增加更多实际案例
- 补充性能对比数据

总体评价：内容质量良好，可以发布。
"""

    def send_message(self, to_agent: str, message: str):
        """发送消息给其他 Agent"""
        if self.manager:
            target_worker = self.manager.workers.get(to_agent)
            if target_worker:
                print(f"  [{self.name}] → {to_agent}: {message}")


# ============================================================================
# 系统组装
# ============================================================================

def create_hierarchical_system() -> ManagerAgent:
    """创建层次化多智能体系统"""

    # 创建 Manager
    manager = ManagerAgent("项目经理")

    # 创建 Worker Agents
    researcher = WorkerAgent(
        name="研究员",
        role="研究员",
        goal="收集和分析信息"
    )

    writer = WorkerAgent(
        name="作家",
        role="作家",
        goal="撰写高质量内容"
    )

    critic = WorkerAgent(
        name="审核员",
        role="审核员",
        goal="确保内容质量"
    )

    # 将 Workers 添加到 Manager
    manager.add_worker(researcher)
    manager.add_worker(writer)
    manager.add_worker(critic)

    return manager


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序"""
    print("="*60)
    print("层次化多智能体系统演示")
    print("="*60)

    # 创建系统
    system = create_hierarchical_system()

    # 处理用户请求
    user_requests = [
        "写一篇关于人工智能的文章",
        "分析区块链技术的应用",
        "介绍云计算的基本概念"
    ]

    for i, request in enumerate(user_requests, 1):
        print(f"\n\n{'#'*60}")
        print(f"# 请求 {i}: {request}")
        print(f"{'#'*60}")

        result = system.process(request)
        print(result)

        # 重置系统状态
        for worker in system.workers.values():
            worker.current_task = None


# ============================================================================
# 测试代码
# ============================================================================

def test_basic_functionality():
    """测试基本功能"""
    print("\n\n=== 测试基本功能 ===")

    system = create_hierarchical_system()

    # 验证 Worker 注册
    assert len(system.workers) == 3
    assert "研究员" in system.workers
    assert "作家" in system.workers
    assert "审核员" in system.workers

    # 验证任务分解
    tasks = system.decompose_task("测试任务")
    assert len(tasks) == 3

    # 验证任务分配
    system.assign_tasks(tasks)
    for task in tasks:
        assert task.assigned_to is not None
        assert task.status == "assigned"

    print("✓ 基本功能测试通过")


def test_worker_execution():
    """测试 Worker 执行"""
    print("\n\n=== 测试 Worker 执行 ===")

    system = create_hierarchical_system()

    # 分配任务
    tasks = system.decompose_task("测试执行")
    system.assign_tasks(tasks)

    # 执行任务
    results = system.coordinate_execution()

    # 验证结果
    assert len(results) > 0
    assert "研究员" in results
    assert "作家" in results
    assert "审核员" in results

    print("✓ Worker 执行测试通过")


def test_full_pipeline():
    """测试完整流程"""
    print("\n\n=== 测试完整流程 ===")

    system = create_hierarchical_system()

    result = system.process("写一篇关于 Python 的文章")

    # 验证结果
    assert "研究成果" in result
    assert "基于研究的文章" in result
    assert "审核意见" in result

    print("✓ 完整流程测试通过")


# ============================================================================
# 运行入口
# ============================================================================

if __name__ == "__main__":
    # 运行演示
    main()

    # 运行测试
    test_basic_functionality()
    test_worker_execution()
    test_full_pipeline()

    print("\n\n" + "="*60)
    print("所有测试通过！")
    print("="*60)
