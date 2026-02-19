# 05. 失败模式练习题 - Level 0

> **对应 Note**: `notes/05_failure_modes_basics.md`
> **对应 Example**: `examples/05_failure_handling.py`
> **目标**: 测试你对 Agent 失败模式和错误处理的理解

---

## 📊 练习统计

- **总题数**: 25 题
- **选择题**: 10 题
- **判断题**: 5 题
- **简答题**: 5 题
- **代码题**: 5 题
- **预计时间**: 40 分钟

---

## 🎯 选择题（1-10）

### 第 1 部分：失败模式（1-5）

**Q1. 以下哪个不是 Agent 的常见失败模式？**

A. 无限循环
B. 死锁
C. 资源耗尽
D. 快速响应

**答案**: D

---

**Q2. 无限循环的主要原因不包括：**

A. 循环条件错误
B. 状态不变
C. 决策逻辑错误
D. 设置了超时

**答案**: D

**解析**: 设置超时是防止无限循环的方法，不是原因。

---

**Q3. 死锁发生的必要条件是：**

A. 单个 Agent
B. 多个 Agent 竞争资源
C. 资源无限
D. 没有锁机制

**答案**: B

---

**Q4. 幻觉（Hallucination）是指：**

A. Agent 生成不准确或虚假的回答
B. Agent 出现无限循环
C. Agent 调用工具失败
D. Agent 内存溢出

**答案**: A

---

**Q5. 以下哪种情况最可能导致资源耗尽？**

A. 设置了循环最大次数
B. 使用了内存管理
C. 无限制地分配内存
D. 使用了缓存

**答案**: C

---

### 第 2 部分：错误处理策略（6-10）

**Q6. 超时检测的主要作用是：**

A. 提高执行速度
B. 防止无限等待
C. 减少内存使用
D. 优化代码

**答案**: B

---

**Q7. 指数退避（Exponential Backoff）是指：**

A. 每次重试间隔时间相同
B. 每次重试间隔时间指数增长
C. 每次重试间隔时间减少
D. 不重试

**答案**: B

---

**Q8. 降级策略（Fallback Strategy）适用于：**

A. 主方案失败时使用备选方案
B. 提高系统性能
C. 增加功能
D. 减少代码

**答案**: A

---

**Q9. 以下哪个不是好的错误处理实践？**

A. 定义明确的异常类型
B. 记录详细的日志
C. 忽略所有错误
D. 提供友好的错误信息

**答案**: C

---

**Q10. Agent 执行器中的 `handle_parsing_errors` 参数作用是：**

A. 处理解析错误
B. 处理网络错误
C. 处理内存错误
D. 处理工具错误

**答案**: A

---

## ✅ 判断题（11-15）

**Q11. 无限循环可以通过设置循环最大次数来防止。**

**答案**: 正确

---

**Q12. 死锁只能在多线程环境中发生，单 Agent 不会出现。**

**答案**: 错误

**解析**: 多个 Agent 协作时也可能发生死锁。

---

**Q13. 重试机制应该无限重试直到成功。**

**答案**: 错误

**解析**: 应该设置最大重试次数，避免无限重试。

---

**Q14. 降级策略可以保证系统的基本可用性。**

**答案**: 正确

---

**Q15. 幻觉只能通过提高模型质量来解决，无法通过工程手段缓解。**

**答案**: 错误

**解析**: 可以通过添加知识库、验证机制、多轮确认等工程手段缓解幻觉问题。

---

## 📝 简答题（16-20）

**Q16. 列举 Agent 的 4 种常见失败模式。**

**答案**:
1. 无限循环 - Agent 卡在死循环里
2. 死锁 - 多个 Agent 互相等待
3. 资源耗尽 - 内存、API 调用次数等耗尽
4. 幻觉 - 生成不准确或虚假的信息

---

**Q17. 如何防止 Agent 出现无限循环？**

**答案**:
1. 设置循环最大次数（max_iterations）
2. 确保状态在每次循环后更新
3. 添加超时机制
4. 使用条件边明确退出条件
5. 监控循环状态，检测异常模式

---

**Q18. 什么是指数退避（Exponential Backoff）？为什么它比固定延迟更好？**

**答案**:
指数退避是一种重试策略，每次重试的间隔时间按指数增长（如：1s, 2s, 4s, 8s...）。

比固定延迟更好的原因：
1. 给系统更多恢复时间
2. 避免过度重试造成压力
3. 提高重试成功率
4. 减少不必要的资源消耗

---

**Q19. 什么是降级策略？举一个例子。**

**答案**:
降级策略是当主方案失败时，使用备选方案来保证基本功能的可用性。

例子：
- 主方案：使用高精度模型
- 降级方案：使用更快但精度略低的模型
- 如果主方案超时或失败，自动切换到降级方案

---

**Q20. 如何通过工程手段缓解 Agent 的幻觉问题？**

**答案**:
1. **添加知识库**：提供准确的信息源
2. **验证机制**：检查生成内容的准确性
3. **引用来源**：要求 Agent 标注信息来源
4. **多轮确认**：对重要信息进行确认
5. **置信度评估**：对不确定的回答添加说明
6. **人工审核**：关键内容经过人工审核

---

## 💻 代码题（21-25）

**Q21. 补充完整带超时的执行函数：**

```python
import time

def execute_with_timeout(func, timeout: int = 5):
    """带超时的执行"""
    start_time = time.______

    try:
        result = func()
        elapsed = time.______ - start_time

        if elapsed > timeout:
            print(f"警告：执行超时")
            return ______

        return result

    except ______ as e:
        print(f"执行失败：{e}")
        return None
```

**答案**:
```python
import time

def execute_with_timeout(func, timeout: int = 5):
    """带超时的执行"""
    start_time = time.time()

    try:
        result = func()
        elapsed = time.time() - start_time

        if elapsed > timeout:
            print(f"警告：执行超时")
            return None

        return result

    except Exception as e:
        print(f"执行失败：{e}")
        return None
```

---

**Q22. 补充完整重试机制：**

```python
def retry_with_backoff(func, max_retries: int = 3, backoff_factor: int = 2):
    """重试机制（指数退避）"""
    retry_count = 0
    delay = _____

    while retry_count < max_retries:
        try:
            return ______()

        except Exception as e:
            retry_count += 1

            if retry_count < max_retries:
                print(f"重试 {retry_count}/{max_retries}")
                time.sleep(_______)
                delay *= _______

    raise Exception(f"重试 {max_retries} 次后仍然失败")
```

**答案**:
```python
def retry_with_backoff(func, max_retries: int = 3, backoff_factor: int = 2):
    """重试机制（指数退避）"""
    retry_count = 0
    delay = 1

    while retry_count < max_retries:
        try:
            return func()

        except Exception as e:
            retry_count += 1

            if retry_count < max_retries:
                print(f"重试 {retry_count}/{max_retries}")
                time.sleep(delay)
                delay *= backoff_factor

    raise Exception(f"重试 {max_retries} 次后仍然失败")
```

---

**Q23. 补充完整降级策略：**

```python
def execute_with_fallback(main_func, fallback_func, operation_name: str):
    """降级策略"""
    try:
        print(f"尝试主方案：{operation_name}")
        result = ______()
        print(f"主方案成功")
        return result

    except ______ as e:
        print(f"主方案失败：{e}")
        print(f"使用降级方案：{operation_name}")

        try:
            result = ______()
            print(f"降级方案成功")
            return result

        except Exception as e2:
            print(f"降级方案也失败：{e2}")
            return ______
```

**答案**:
```python
def execute_with_fallback(main_func, fallback_func, operation_name: str):
    """降级策略"""
    try:
        print(f"尝试主方案：{operation_name}")
        result = main_func()
        print(f"主方案成功")
        return result

    except Exception as e:
        print(f"主方案失败：{e}")
        print(f"使用降级方案：{operation_name}")

        try:
            result = fallback_func()
            print(f"降级方案成功")
            return result

        except Exception as e2:
            print(f"降级方案也失败：{e2}")
            return None
```

---

**Q24. 实现一个防止无限循环的 Agent：**

```python
class SafeAgent:
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.iteration_count = 0

    def run(self, task: str):
        """执行任务"""
        self.iteration_count = 0

        while self.iteration_count < self.______:
            self.iteration_count += 1

            # 执行推理
            print(f"循环 {self.iteration_count}/{self.max_iterations}")

            # 检查是否完成
            if self.______(task):
                print("任务完成")
                return "成功"

        print("达到最大循环次数，退出")
        return "未完成（达到最大次数）"

    def is_complete(self, task: str) -> bool:
        """检查任务是否完成"""
        # 简化实现
        return "完成" in task or self.iteration_count >= 3
```

**答案**:
```python
class SafeAgent:
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.iteration_count = 0

    def run(self, task: str):
        """执行任务"""
        self.iteration_count = 0

        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1

            # 执行推理
            print(f"循环 {self.iteration_count}/{self.max_iterations}")

            # 检查是否完成
            if self.is_complete(task):
                print("任务完成")
                return "成功"

        print("达到最大循环次数，退出")
        return "未完成（达到最大次数）"

    def is_complete(self, task: str) -> bool:
        """检查任务是否完成"""
        # 简化实现
        return "完成" in task or self.iteration_count >= 3
```

---

**Q25. 实现一个带完整错误处理的工具调用：**

**要求**:
1. 超时检测（5 秒）
2. 重试机制（最多 3 次）
3. 降级策略

```python
import time

class RobustToolExecutor:
    def __init__(self):
        pass

    def execute_tool(
        self,
        tool_func,
        fallback_func=None,
        timeout: int = 5,
        max_retries: int = 3
    ):
        """执行工具，包含完整错误处理"""
        # 实现代码
        pass
```

**答案**:
```python
import time

class RobustToolExecutor:
    def __init__(self):
        pass

    def execute_tool(
        self,
        tool_func,
        fallback_func=None,
        timeout: int = 5,
        max_retries: int = 3
    ):
        """执行工具，包含完整错误处理"""
        retry_count = 0
        delay = 1

        # 重试机制
        while retry_count < max_retries:
            try:
                # 执行工具
                start_time = time.time()
                result = tool_func()
                elapsed = time.time() - start_time

                # 超时检测
                if elapsed > timeout:
                    raise TimeoutError(f"执行超时：{elapsed}秒")

                return result

            except Exception as e:
                retry_count += 1
                print(f"执行失败（第 {retry_count} 次）：{e}")

                if retry_count < max_retries:
                    print(f"等待 {delay} 秒后重试...")
                    time.sleep(delay)
                    delay *= 2  # 指数退避

        # 所有重试都失败，使用降级方案
        if fallback_func:
            print("主方案失败，使用降级方案")
            try:
                return fallback_func()
            except Exception as e:
                print(f"降级方案也失败：{e}")
                return None

        return None
```

---

## 🎯 学习建议

1. **先阅读 note**: `notes/05_failure_modes_basics.md`
2. **再运行 example**: `examples/05_failure_handling.py`
3. **最后完成练习**: 本练习题

---

## ✅ 完成标准

- [ ] 完成 10 道选择题
- [ ] 完成 5 道判断题
- [ ] 完成 5 道简答题
- [ ] 完成 5 道代码题
- [ ] 正确率 >= 80%
- [ ] 理解 4 种常见失败模式
- [ ] 掌握 3 种错误处理策略
- [ ] 能够设计健壮的 Agent 系统

---

**下一练习**: `exercises/06_environment_check_exercise.md` 🚀
