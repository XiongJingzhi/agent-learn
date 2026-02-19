"""
02_autogpt_agent.py
AutoGPT 简化实现

展示规划-执行-反思循环
"""

from typing import List, Dict

class AutoGPT:
    """简化的 AutoGPT 实现"""

    def __init__(self, objective: str):
        self.objective = objective
        self.memory = []

    def run(self, max_iterations: int = 5):
        """运行 AutoGPT 循环"""

        print(f"\n🎯 目标：{self.objective}\n")

        for iteration in range(max_iterations):
            print(f"\n{'='*50}")
            print(f"迭代 {iteration + 1}/{max_iterations}")
            print(f"{'='*50}\n")

            # 1. 规划
            print("[1] 规划阶段")
            plan = self.plan()
            print(f"  计划：{plan}")

            # 2. 执行
            print(f"\n[2] 执行阶段")
            result = self.execute(plan)
            print(f"  结果：{result}")

            # 3. 反思
            print(f"\n[3] 反思阶段")
            reflection = self.reflect(result)
            print(f"  评估：{reflection['score']:.1%}")
            print(f"  建议：{reflection['suggestion']}")

            # 4. 判断是否继续
            if reflection['score'] >= 0.9:
                print("\n✓ 目标达成！")
                break

            # 5. 调整
            print(f"\n[4] 调整策略")
            self.adjust(reflection['suggestion'])

        return result

    def plan(self) -> str:
        """规划阶段"""
        # 简化：返回固定计划
        return "搜索文档 → 学习示例 → 实践项目"

    def execute(self, plan: str) -> str:
        """执行阶段"""
        # 简化：返回模拟结果
        return "已学习和实践 LangGraph 基础知识"

    def reflect(self, result: str) -> Dict:
        """反思阶段"""
        # 简化：返回模拟反思
        return {
            "score": 0.7,
            "suggestion": "需要深入学习高级特性"
        }

    def adjust(self, suggestion: str):
        """调整阶段"""
        print(f"  应用建议：{suggestion}")

# 使用示例
if __name__ == "__main__":
    autogpt = AutoGPT(
        objective="掌握 LangGraph 开发"
    )

    result = autogpt.run(max_iterations=3)
    print(f"\n最终结果：{result}")
