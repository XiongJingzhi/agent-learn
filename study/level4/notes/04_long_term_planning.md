# 04. 长期规划

> **目标**: 理解自主 Agent 如何进行长期规划
> **预计时间**: 45 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 什么是长期规划？

### 定义

**长期规划（Long-term Planning）** 是指 Agent 为实现长期目标，制定的跨越多个时间步的协调策略。

> **类比**：
> - **短期规划**：决定今天吃什么
> - **长期规划**：规划未来一年的职业发展
>
> 自主 Agent 需要像规划职业生涯一样，规划如何实现长期目标。

---

## 长期规划的挑战

### 挑战 1：不确定性

**问题**：未来充满不确定性，很难准确预测

**解决方案**：
- **多方案准备**：准备多个备选方案
- **滚动规划**：定期调整规划
- **风险评估**：评估每个方案的风险

**示例**：
```python
class AdaptivePlanner:
    """自适应规划器"""

    def plan_with_uncertainty(self, goal: str):
        """在不确定性下规划"""

        # 生成多个方案
        plans = self.generate_multiple_plans(goal)

        # 评估每个方案的风险和收益
        for plan in plans:
            plan.risk = self.assess_risk(plan)
            plan.expected_value = self.estimate_value(plan)

        # 选择最优方案（考虑风险）
        best_plan = max(
            plans,
            key=lambda p: p.expected_value / (1 + p.risk)
        )

        return best_plan
```

---

### 挑战 2：目标漂移（Goal Drift）

**问题**：执行过程中可能偏离原始目标

**解决方案**：
- **定期校准**：定期检查是否偏离目标
- **里程碑检查**：设置里程碑，验证方向
- **反馈机制**：根据反馈调整方向

**示例**：
```python
class GoalTracker:
    """目标跟踪器"""

    def __init__(self, original_goal):
        self.original_goal = original_goal
        self.milestones = []
        self.deviations = []

    def check_alignment(self, current_state):
        """检查是否与目标对齐"""

        # 计算当前方向与目标的偏差
        deviation = self.calculate_deviation(
            self.original_goal,
            current_state
        )

        # 记录偏差
        self.deviations.append(deviation)

        # 如果偏差过大，发出警告
        if deviation > 0.3:
            return False, f"偏差过大：{deviation:.2f}"

        return True, "方向正确"

    def recalibrate(self):
        """重新校准方向"""

        # 基于历史偏差分析趋势
        trend = self.analyze_deviation_trend()

        # 调整后续策略
        adjustment = self.generate_adjustment(trend)

        return adjustment
```

---

### 挑战 3：资源分配

**问题**：如何在长期目标中合理分配有限资源

**解决方案**：
- **优先级排序**：高优先级任务优先分配资源
- **动态分配**：根据执行情况动态调整
- **资源监控**：实时监控资源使用情况

**示例**：
```python
class ResourceAllocator:
    """资源分配器"""

    def __init__(self, total_budget, total_time):
        self.total_budget = total_budget
        self.total_time = total_time
        self.used_budget = 0
        self.used_time = 0

    def allocate(self, tasks):
        """分配资源"""

        # 按优先级排序
        prioritized = sorted(tasks, key=lambda t: t.priority, reverse=True)

        allocations = []
        for task in prioritized:
            # 估算所需资源
            estimated_cost = self.estimate_cost(task)
            estimated_time = self.estimate_time(task)

            # 检查是否有足够资源
            if (self.used_budget + estimated_cost <= self.total_budget and
                self.used_time + estimated_time <= self.total_time):

                # 分配资源
                allocations.append({
                    "task": task,
                    "budget": estimated_cost,
                    "time": estimated_time
                })

                self.used_budget += estimated_cost
                self.used_time += estimated_time
            else:
                # 资源不足，跳过
                continue

        return allocations
```

---

## 长期规划策略

### 策略 1：里程碑规划（Milestone-based Planning）

**原理**：将长期目标分解为多个里程碑，逐步完成

**示例**：
```python
class MilestonePlanner:
    """里程碑规划器"""

    def plan(self, long_term_goal: str, time_horizon: int):
        """基于里程碑规划"""

        # 1. 分解为里程碑
        milestones = self.create_milestones(
            long_term_goal,
            time_horizon
        )

        # 2. 为每个里程碑制定计划
        plans = []
        for i, milestone in enumerate(milestones):
            # 计划当前里程碑
            plan = self.plan_milestone(
                milestone,
                previous_results=plans[i-1] if i > 0 else None
            )
            plans.append(plan)

        return plans

    def create_milestones(self, goal, time_horizon):
        """创建里程碑"""

        # 假设每个里程碑需要 1 周
        num_milestones = time_horizon  # 周数

        prompt = f"""
        目标：{goal}
        时间跨度：{num_milestones} 周

        请创建 {num_milestones} 个里程碑。
        每个里程碑应该：
        1. 有明确的交付物
        2. 可以验证完成度
        3. 逐步推进主目标

        返回格式：JSON 数组
        """

        response = llm.invoke(prompt)
        return parse_milestones(response)
```

---

### 策略 2：滚动规划（Rolling Planning）

**原理**：定期重新规划，适应新信息

**示例**：
```python
class RollingPlanner:
    """滚动规划器"""

    def __init__(self, replan_interval=7):
        self.replan_interval = replan_interval  # 天
        self.current_plan = None
        self.last_replan_time = None

    def execute_with_replanning(self, goal):
        """执行并定期重新规划"""

        # 初始规划
        self.current_plan = self.plan(goal)
        self.last_replan_time = datetime.now()

        while not self.is_goal_achieved(goal):
            # 执行当前计划
            result = self.execute_step(self.current_plan)

            # 检查是否需要重新规划
            days_since_replan = (
                datetime.now() - self.last_replan_time
            ).days

            if days_since_replan >= self.replan_interval:
                # 重新规划
                print(f"[{days_since_replan} 天后] 重新规划...")
                self.current_plan = self.replan(
                    goal,
                    self.current_plan,
                    result
                )
                self.last_replan_time = datetime.now()

    def replan(self, goal, old_plan, new_information):
        """基于新信息重新规划"""

        prompt = f"""
        目标：{goal}
        原计划：{old_plan}
        新信息：{new_information}

        请基于新信息调整计划。
        考虑：
        1. 哪些任务已完成？
        2. 哪些任务需要调整？
        3. 是否需要新任务？

        返回调整后的计划。
        """

        response = llm.invoke(prompt)
        return parse_plan(response)
```

---

### 策略 3：分层规划（Hierarchical Planning）

**原理**：不同层次有不同的规划粒度

**示例**：
```python
class HierarchicalPlanner:
    """分层规划器"""

    def __init__(self):
        self.strategic_planner = StrategicPlanner()  # 战略层
        self.tactical_planner = TacticalPlanner()    # 战术层
        self.operational_planner = OperationalPlanner()  # 操作层

    def plan(self, goal):
        """分层规划"""

        # 战略层：长期目标（月度）
        strategic_plan = self.strategic_planner.plan(
            goal,
            time_horizon="months"
        )

        # 战术层：中期目标（周度）
        tactical_plans = []
        for strategic_goal in strategic_plan.goals:
            tactical_plan = self.tactical_planner.plan(
                strategic_goal,
                time_horizon="weeks"
            )
            tactical_plans.append(tactical_plan)

        # 操作层：短期任务（日度）
        operational_plans = []
        for tactical_plan in tactical_plans:
            for tactical_goal in tactical_plan.goals:
                operational_plan = self.operational_planner.plan(
                    tactical_goal,
                    time_horizon="days"
                )
                operational_plans.append(operational_plan)

        return {
            "strategic": strategic_plan,
            "tactical": tactical_plans,
            "operational": operational_plans
        }
```

---

## 执行监控

### 进度跟踪

```python
class ProgressTracker:
    """进度跟踪器"""

    def __init__(self, milestones):
        self.milestones = milestones
        self.completed = []
        self.current = None

    def update_progress(self, result):
        """更新进度"""

        # 检查是否完成了当前里程碑
        if self.is_milestone_completed(result):
            self.completed.append(self.current)
            self.current = self.get_next_milestone()
        else:
            # 更新当前里程碑的进度
            self.update_current_progress(result)

    def get_progress_report(self):
        """生成进度报告"""

        total = len(self.milestones)
        done = len(self.completed)

        return {
            "total_milestones": total,
            "completed_milestones": done,
            "current_milestone": self.current,
            "progress_percentage": (done / total) * 100 if total > 0 else 0,
            "remaining": total - done
        }
```

---

## 最小验证

### 验证目标
- ✅ 理解长期规划的三个挑战
- ✅ 掌握三种长期规划策略
- ✅ 能够实现简单的里程碑规划

### 验证步骤
1. 选择一个长期目标（如"在 3 个月内掌握 LangGraph"）
2. 设计 3-4 个里程碑
3. 为每个里程碑制定具体计划

### 预期输出
能够为一个长期目标创建里程碑规划。

---

## 常见错误

### 错误 1：规划过于僵化

**问题**：制定计划后不再调整

**解决**：采用滚动规划，定期调整

---

### 错误 2：忽略进度跟踪

**问题**：不监控执行进度，无法及时发现偏差

**解决**：建立进度跟踪系统

---

### 错误 3：里程碑设置不合理

**问题**：里程碑太大或太小

**解决**：里程碑应该是 1-2 周可完成的

---

## 下一步

- 📖 `notes/05_self_reflection.md` - 自我反思
- 🧪 `examples/02_autogpt_agent.py` - AutoGPT 示例

---

**记住：长期规划就像登山，既要看到山顶，也要关注脚下的每一步！** ⛰️🚶
