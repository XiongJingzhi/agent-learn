"""
01_babyagi_agent.py
BabyAGI 简化实现

展示任务生成、排序、执行的核心循环
"""

import os
from typing import List, Dict
from datetime import datetime

# 模拟 LLM（实际使用时替换为真实 LLM）
class MockLLM:
    def invoke(self, prompt: str) -> str:
        """模拟 LLM 调用"""
        if "创建任务" in prompt:
            return '["搜索 LangGraph 文档", "查看示例代码", "实践项目"]'
        elif "排序" in prompt:
            return '["搜索 LangGraph 文档", "查看示例代码", "实践项目"]'
        else:
            return "执行完成"

class Task:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

class BabyAGI:
    """简化的 BabyAGI 实现"""

    def __init__(self, objective: str):
        self.objective = objective
        self.llm = MockLLM()
        self.task_list = []
        self.results = []

    def run(self, max_iterations: int = 5):
        """运行 BabyAGI 循环"""

        print(f"\n🎯 目标：{self.objective}\n")

        # 初始化：创建初始任务
        self.task_list = self.create_initial_tasks()

        for iteration in range(max_iterations):
            print(f"\n{'='*50}")
            print(f"迭代 {iteration + 1}/{max_iterations}")
            print(f"{'='*50}\n")

            if not self.task_list:
                print("✓ 所有任务已完成！")
                break

            # 1. 优先级排序
            print(f"[1] 排序任务（共 {len(self.task_list)} 个）")
            self.task_list = self.prioritize_tasks()
            for i, task in enumerate(self.task_list, 1):
                print(f"  {i}. {task.name}")

            # 2. 执行第一个任务
            current_task = self.task_list[0]
            print(f"\n[2] 执行任务：{current_task.name}")
            result = self.execute_task(current_task)
            self.results.append(result)
            print(f"  → {result}")

            # 3. 创建新任务
            print(f"\n[3] 生成新任务")
            new_tasks = self.create_tasks(result)
            self.task_list.extend(new_tasks)

            # 4. 移除已完成的任务
            self.task_list = self.task_list[1:]

            print(f"\n  剩余任务：{len(self.task_list)}")

        print(f"\n{'='*50}")
        print("执行完成！")
        print(f"{'='*50}\n")

        return self.results

    def create_initial_tasks(self) -> List[Task]:
        """创建初始任务"""
        prompt = f"为目标「{self.objective}」创建初始任务"
        response = self.llm.invoke(prompt)

        # 简化：直接返回固定任务
        return [
            Task("搜索 LangGraph 文档"),
            Task("查看示例代码"),
            Task("实践项目")
        ]

    def prioritize_tasks(self) -> List[Task]:
        """排序任务优先级"""
        # 简化：直接返回原顺序
        return self.task_list

    def execute_task(self, task: Task) -> str:
        """执行任务"""
        # 简化：返回模拟结果
        return f"已完成：{task.name}"

    def create_tasks(self, result: str) -> List[Task]:
        """基于结果创建新任务"""
        # 简化：偶尔返回新任务
        if len(self.task_list) < 2:
            return [Task("深入学习高级特性")]
        return []

# 使用示例
if __name__ == "__main__":
    # 创建 BabyAGI
    baby_agi = BabyAGI(
        objective="学习 LangGraph 并构建应用"
    )

    # 运行
    results = baby_agi.run(max_iterations=3)

    print("\n📊 执行结果汇总：")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
