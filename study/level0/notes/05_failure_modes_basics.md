# 05. 失败模式基础 - Feynman Technique

> **费曼技巧**：如果不能简单解释，说明没有真正理解。  
> **目标**：用简单的语言和类比，解释 Agent 的失败模式。

---

## 🎯 学习目标

通过本章学习，你将能够：

1. ✅ 理解 **为什么 Agent 会失败**
2. ✅ 掌握 **常见的失败模式**
3. ✅ 掌握 **失败检测和恢复策略**
4. ✅ 掌握 **错误处理最佳实践**
5. ✅ 能够用简单的语言向"资深开发"解释失败模式

---

## 📚 核心概念

### 概念 1：为什么 Agent 会失败？

> **类比**：Agent 就像一个**人**，人也会犯错，Agent 也会失败。

**Agent 失败的原因**：

1. ✅ **输入错误**：用户的输入有问题或无法理解
2. ✅ **工具失败**：工具调用失败或返回错误的结果
3. ✅ **决策错误**：Agent 的决策逻辑有问题
4. ✅ **执行错误**：执行过程中出现异常
5. ✅ **环境错误**：环境（如：API、数据库）有问题

**核心思想**：失败是不可避免的，关键是如何**检测、恢复和学习**。

---

### 概念 2：常见的失败模式

#### 1. 无限循环（Infinite Loop）

> **类比**：就像一个人**卡在死循环**里，一直重复同一个动作，永远无法停止。

**无限循环的原因**：

- ✅ **循环条件错误**：循环条件永远不会满足
- ✅ **状态不变**：Agent 的状态没有更新，导致无法退出循环
- ✅ **决策逻辑错误**：决策逻辑导致 Agent 总是选择同一个行动

**示例**：
```python
# 无限循环的 Agent
while True:
    # Agent 总是选择同一个行动
    action = "search"
    
    # 执行行动
    result = execute_action(action)
    
    # 状态不变
    state = {"action": action, "result": result}
    
    # 循环条件永远不会满足
    if result == "success":
        break
```

---

#### 2. 死锁（Deadlock）

> **类比**：就像两个人**互不谦让**，都等着对方先让路，结果谁也过不去。

**死锁的原因**：

- ✅ **资源竞争**：多个 Agent 竞争同一个资源
- ✅ **循环等待**：Agent A 等待 Agent B，Agent B 等待 Agent A
- ✅ **锁顺序错误**：锁的获取顺序不当导致死锁

**示例**：
```python
# 死锁的 Agent
class DeadlockAgent:
    """死锁 Agent"""
    
    def execute(self, resource_id: str):
        # Agent A 获取资源 1
        self.acquire_lock("resource_1")
        
        # Agent A 尝试获取资源 2，但资源 2 被 Agent B 占用
        self.acquire_lock("resource_2")  # 等待 Agent B 释放
        
        # Agent B 同时也在等待 Agent A 释放资源 1
        # 死锁！
```

---

#### 3. 资源耗尽（Resource Exhaustion）

> **类比**：就像一个人**过度使用资源**，导致资源用完，无法继续工作。

**资源耗尽的原因**：

- ✅ **内存泄漏**：Agent 不断分配内存，但不释放
- ✅ **API 调用限制**：超过 API 的调用限制，导致无法继续调用
- ✅ **数据库连接耗尽**：数据库连接用完，无法创建新连接

**示例**：
```python
# 资源耗尽的 Agent
class ResourceExhaustionAgent:
    """资源耗尽 Agent"""
    
    def execute(self, num_iterations: int):
        for i in range(num_iterations):
            # 每次都分配内存，但不释放
            data = [0] * 1000000  # 分配 10 MB 内存
            
            # API 调用限制：每分钟最多 100 次调用
            response = self.call_api()  # 超过限制，无法继续调用
```

---

#### 4. 幻觉（Hallucination）

> **类比**：就像一个人**臆想**了不存在的信息，Agent 也会生成不准确或虚假的回答。

**幻觉的原因**：

- ✅ **知识不足**：Agent 的知识库不完整或有过时信息
- ✅ **推理错误**：Agent 的推理逻辑有问题，导致错误的结论
- ✅ **输入误导**：用户的输入有误导性，导致 Agent 生成错误的回答

**示例**：
```python
# 幻觉的 Agent
class HallucinationAgent:
    """幻觉 Agent"""
    
    def generate_response(self, query: str) -> str:
        # Agent 生成不准确或虚假的回答
        # 知识库中没有相关信息，但 Agent "臆想" 了回答
        response = "根据我的知识，LangChain 是一个 LLM 框架。"
        
        # 实际上，LangChain 是一个 LLM 应用开发框架，而不是 LLM 框架
        return response
```

---

### 概念 3：失败检测和恢复策略

#### 1. 超时检测（Timeout Detection）

> **类比**：就像一个人**等待太久**，就认为任务失败了。

**超时检测的作用**：

- ✅ **设置超时时间**：为每个任务或行动设置超时时间
- ✅ **监控执行时间**：监控 Agent 的执行时间
- ✅ **超时后终止**：超过超时时间后，终止执行
- ✅ **返回错误**：返回超时错误

**示例**：
```python
import time

def execute_with_timeout(func, timeout: int):
    """超时执行"""
    start_time = time.time()
    
    try:
        # 执行函数，最多等待 timeout 秒
        result = func(timeout - (time.time() - start_time))
        return result
    except TimeoutError:
        # 超时后终止执行
        return {"error": "timeout", "message": f"执行超时：{timeout} 秒"}
```

---

#### 2. 重试机制（Retry Mechanism）

> **类比**：就像一个人**尝试多次**，直到成功或放弃。

**重试机制的作用**：

- ✅ **自动重试**：自动重试失败的任务或行动
- ✅ **指数退避**：每次重试的间隔时间指数增长
- ✅ **最大重试次数**：设置最大重试次数，避免无限重试
- ✅ **重试条件**：只有满足特定条件的错误才重试

**示例**：
```python
def retry_with_backoff(func, max_retries: int = 3, backoff_factor: int = 2):
    """重试机制（指数退避）"""
    retry_count = 0
    delay = 1
    
    while retry_count < max_retries:
        try:
            # 执行函数
            return func()
        except Exception as e:
            # 重试
            retry_count += 1
            
            # 如果还有重试次数，等待后重试
            if retry_count < max_retries:
                time.sleep(delay)
                delay *= backoff_factor  # 指数退避
    
    # 所有重试都失败，抛出异常
    raise Exception(f"重试 {max_retries} 次后仍然失败")
```

---

#### 3. 降级策略（Fallback Strategy）

> **类比**：就像一个人**无法完成任务**时，会使用备用方案。

**降级策略的作用**：

- ✅ **提供备选方案**：当主要方案失败时，使用备选方案
- ✅ **保证可用性**：即使主方案失败，也能提供基本的功能
- ✅ **用户体验**：即使主方案失败，也能给用户一个反馈

**示例**：
```python
def execute_with_fallback(main_func, fallback_func):
    """降级策略"""
    try:
        # 尝试执行主方案
        return main_func()
    except Exception as e:
        # 主方案失败，使用降级方案
        print(f"主方案失败：{e}，使用降级方案")
        return fallback_func()
```

---

### 概念 4：错误处理最佳实践

#### 1. 明确的异常类型

> **类比**：就像医生**诊断疾病**，需要明确疾病的类型才能对症下药。

**明确异常类型的作用**：

- ✅ **明确的异常类型**：为每种错误定义明确的异常类型
- ✅ **错误信息详细**：异常信息要详细，包含足够的上下文
- ✅ **便于调试**：明确的异常类型和详细的错误信息便于调试

**示例**：
```python
class AgentTimeoutError(Exception):
    """Agent 超时错误"""
    pass

class ToolExecutionError(Exception):
    """工具执行错误"""
    pass

class DecisionLogicError(Exception):
    """决策逻辑错误"""
    pass

class ResourceExhaustionError(Exception):
    """资源耗尽错误"""
    pass
```

---

#### 2. 详细的日志记录

> **类比**：就像一个人**写日记**，记录每天发生的事情，方便回顾和总结。

**详细日志记录的作用**：

- ✅ **记录执行流程**：记录 Agent 的执行流程
- ✅ **记录错误信息**：记录错误的详细信息
- ✅ **记录决策过程**：记录 Agent 的决策过程
- ✅ **便于调试和分析**：详细的日志记录便于调试和分析

**示例**：
```python
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def execute_agent():
    """执行 Agent"""
    logger.info("开始执行 Agent")
    
    try:
        # 感知
        logger.info("感知输入")
        state = perceive(input_data)
        logger.info(f"感知结果：{state}")
        
        # 推理
        logger.info("推理决策")
        decision = reason(state)
        logger.info(f"决策结果：{decision}")
        
        # 执行
        logger.info("执行决策")
        result = act(decision, state)
        logger.info(f"执行结果：{result}")
        
        return result
    except Exception as e:
        # 记录错误
        logger.error(f"Agent 执行失败：{e}", exc_info=True)
        raise
```

---

## 🔍 费曼学习检查

### 向"资深开发"解释

**假设你正在向资深开发解释 Agent 的失败模式，你能这样说吗？**

1. **为什么 Agent 会失败？**
   > "Agent 就像一个人，人也会犯错，Agent 也会失败。失败的原因有：输入错误、工具失败、决策错误、执行错误、环境错误。"

2. **常见的失败模式有哪些？**
   > "常见的失败模式有：无限循环（Agent 卡在死循环里）、死锁（Agent 互不谦让，都等待对方）、资源耗尽（Agent 过度使用资源）、幻觉（Agent 臆想不存在的信息）。"

3. **如何检测失败？**
   > "失败检测的方法有：超时检测（等待太久就认为任务失败）、异常捕获（捕获运行时异常）、状态监控（监控 Agent 的状态变化）。"

4. **如何恢复失败？**
   > "失败恢复的策略有：重试机制（自动重试失败的次数）、降级策略（主方案失败时使用备选方案）、错误处理（优雅地处理错误，给用户友好的反馈）。"

---

## 🎯 核心要点总结

### 常见的失败模式

| 失败模式 | 原因 | 解决方法 |
|----------|------|----------|
| **无限循环** | 循环条件错误、状态不变 | 设置循环最大次数、更新状态 |
| **死锁** | 资源竞争、循环等待 | 超时检测、锁顺序调整 |
| **资源耗尽** | 内存泄漏、API 限制 | 资源限制、内存管理 |
| **幻觉** | 知识不足、推理错误 | 知识库更新、验证机制 |

### 失败检测和恢复策略

| 策略 | 作用 | 适用场景 |
|------|------|----------|
| **超时检测** | 避免无限等待 | 检测无限循环、死锁 |
| **重试机制** | 自动重试失败的次数 | 网络调用、API 调用 |
| **降级策略** | 提供备选方案 | 主方案失败时使用备选方案 |

### 错误处理最佳实践

| 实践 | 说明 |
|------|------|
| **明确的异常类型** | 为每种错误定义明确的异常类型 |
| **详细的日志记录** | 记录执行流程、错误信息、决策过程 |
| **优雅的错误处理** | 优雅地处理错误，给用户友好的反馈 |

---

## 🚀 下一步

现在你已经理解了 Agent 的失败模式，让我们继续学习：

- 📖 `notes/06_environment_check_guide.md` - 环境检查指南
- 🧪 `examples/01_simple_react_agent.py` - 简单的 ReAct Agent 示例
- ✏ `exercises/00_concept_check.md` - 概念检查练习题

---

**记住：Agent 失败是不可避免的，关键是如何检测、恢复和学习！** 🚨
