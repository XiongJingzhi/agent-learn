# 01. 基础练习题 - 多智能体协作

> **难度**: ⭐⭐
> **预计时间**: 60 分钟
> **题目数量**: 30 题

---

## 📋 练习说明

本练习包含 30 道基础题，涵盖多智能体协作的核心概念。

**答题方式**:
1. 选择题：选择正确答案（A/B/C/D）
2. 判断题：判断陈述是否正确（✓/✗）
3. 填空题：填写空白处的内容
4. 简答题：用简短的语言回答问题

---

## 第一部分：概念理解（10 题）

### 1. 选择题（5 题）

**1.1** 以下哪个不是多智能体系统的优势？
- A. 专业化分工
- B. 并行处理
- C. 实现简单
- D. 容错性

**答案**: C

**解析**: 多智能体系统通常比单 Agent 系统更复杂，而不是更简单。

---

**1.2** 层次化架构的主要缺点是什么？
- A. 结构不清晰
- B. Manager 成为瓶颈
- C. Agent 之间无法通信
- D. 不适合复杂任务

**答案**: B

**解析**: 层次化架构中，所有通信都经过 Manager，可能导致 Manager 成为性能瓶颈。

---

**1.3** 哪种协作模式最适合有明确处理顺序的任务？
- A. 层次化架构
- B. 扁平化架构
- C. 顺序/管道架构
- D. 图/混合架构

**答案**: C

**解析**: 顺序/管道架构专为有明确处理顺序的任务设计。

---

**1.4** 消息传递通信机制的主要优势是什么？
- A. 实时性最强
- B. 耦合度最低
- C. 实现最简单
- D. 性能最好

**答案**: B

**解析**: 消息传递完全解耦发送者和接收者，耦合度最低。

---

**1.5** 发布-订阅机制最适合什么场景？
- A. 点对点通信
- B. 广播通知
- C. 高速数据共享
- D. 强一致性要求

**答案**: B

**解析**: 发布-订阅最适合一对多的广播通知场景。

---

### 2. 判断题（5 题）

**2.1** 扁平化架构比层次化架构更难实现。 (✗)

**解析**: 扁平化架构的实现复杂度通常高于层次化架构，因为需要处理更多的分布式协调问题。题目说"更难实现"是正确的，但答案是 ✓（不是 ✗）。让我修正：
- 题目应该改为：扁平化架构比层次化架构更容易实现。 (✗)

---

**2.2** 顺序/管道架构可以并行处理多个任务。 (✗)

**解析**: 顺序/管道架构的特点就是按顺序处理，不支持并行。

---

**2.3** 共享内存通信机制需要并发控制。 (✓)

**解析**: 多个 Agent 同时访问共享内存时，需要锁等并发控制机制。

---

**2.4** 层次化架构是唯一适合多智能体系统的架构。 (✗)

**解析**: 没有唯一的"最好"架构，不同场景适合不同的架构。

---

**2.5** 图/混合架构可以包含其他所有架构的特点。 (✓)

**解析**: 图/混合架构是最灵活的，可以包含层次化、扁平化、顺序等特点。

---

## 第二部分：架构设计（10 题）

### 3. 场景分析（5 题）

**3.1** 场景：一个需要研究、写作、审核的文章生成系统

**问题**: 应该选择哪种协作模式？为什么？

**答案**: 层次化架构

**理由**:
1. 任务有明确的依赖关系（研究 → 写作 → 审核）
2. 需要中央协调者来管理流程
3. 每个阶段的专业 Agent 只需关注自己的职责

---

**3.2** 场景：一个需要 10 个专家并行分析不同角度的咨询系统

**问题**: 应该选择哪种协作模式？为什么？

**答案**: 扁平化架构

**理由**:
1. 多个专家需要并行工作
2. 专家之间地位平等
3. 需要通过协商达成共识

---

**3.3** 场景：一个数据处理流水线（清洗 → 分析 → 可视化）

**问题**: 应该选择哪种协作模式？为什么？

**答案**: 顺序/管道架构

**理由**:
1. 有明确的处理顺序
2. 上一步的输出是下一步的输入
3. 每一步专注一个任务

---

**3.4** 场景：一个需要动态路由的复杂客服系统

**问题**: 应该选择哪种协作模式？为什么？

**答案**: 图/混合架构

**理由**:
1. 复杂的多阶段任务
2. 需要根据用户请求动态路由到不同的 Agent
3. 可能需要多种协作模式

---

**3.5** 场景：一个大规模分布式系统，需要高可用性和容错性

**问题**: 应该选择哪种协作模式？为什么？

**答案**: 扁平化架构 + 分布式 RAG

**理由**:
1. 去中心化，无单点故障
2. 支持动态添加/删除 Agent
3. 适合大规模部署

---

### 4. 设计问题（5 题）

**4.1** 设计一个层次化的多智能体系统，要求：
- 1 个 Manager
- 3 个 Worker Agents
- 完成"分析市场趋势并生成报告"的任务

**答案**:
```
Manager (项目经理)
  ├─ Researcher (研究员): 收集市场数据
  ├─ Analyst (分析师): 分析数据趋势
  └─ Writer (作家): 生成分析报告
```

**流程**:
1. Manager 接收任务
2. 分配给 Researcher 收集数据
3. Researcher 完成后，Manager 分配给 Analyst 分析
4. Analyst 完成后，Manager 分配给 Writer 生成报告
5. Manager 汇总最终报告

---

**4.2** 设计一个消息传递协议，要求：
- 消息格式包含：id, from, to, type, content
- 支持回复消息
- 支持消息类型：request, response, notification

**答案**:
```python
class Message:
    def __init__(self, msg_id, from_agent, to_agent,
                 msg_type, content, reply_to=None):
        self.id = msg_id
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.type = msg_type  # request, response, notification
        self.content = content
        self.reply_to = reply_to  # 如果是回复，记录原消息ID
```

---

**4.3** 设计一个冲突解决机制，要求：
- 2 个 Agent 竞争 1 个资源
- 使用优先级队列
- 实现公平调度

**答案**:
```python
import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class Request:
    priority: int
    agent_name: str = field(compare=False)
    task: Any = field(compare=False)

class ResourceManager:
    def __init__(self):
        self.resource_available = True
        self.queue = []

    def request(self, agent_name: str, task: Any, priority: int):
        if self.resource_available:
            self.resource_available = False
            return True  # 立即获得资源
        else:
            # 加入优先级队列
            heapq.heappush(self.queue, Request(priority, agent_name, task))
            return False

    def release(self):
        if self.queue:
            # 分配给下一个等待的 Agent
            next_request = heapq.heappop(self.queue)
            return next_request.agent_name
        else:
            self.resource_available = True
            return None
```

---

**4.4** 设计一个简单的发布-订阅系统，要求：
- 支持主题订阅
- 支持消息发布
- 支持取消订阅

**答案**:
```python
from typing import Dict, List, Callable

class PubSub:
    def __init__(self):
        self.topics: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, callback: Callable):
        if topic not in self.topics:
            self.topics[topic] = []
        self.topics[topic].append(callback)

    def publish(self, topic: str, message: dict):
        if topic in self.topics:
            for callback in self.topics[topic]:
                callback(message)

    def unsubscribe(self, topic: str, callback: Callable):
        if topic in self.topics and callback in self.topics[topic]:
            self.topics[topic].remove(callback)
```

---

**4.5** 设计一个知识共享机制，要求：
- 共享基础知识库
- 每个 Agent 有本地缓存
- 支持缓存更新

**答案**:
```python
from typing import Dict, Any
import time

class SharedKnowledgeBase:
    def __init__(self):
        self.base_knowledge: Dict[str, Any] = {}
        self.last_update = 0

    def update_base(self, new_knowledge: Dict[str, Any]):
        self.base_knowledge.update(new_knowledge)
        self.last_update = time.time()

class LocalCache:
    def __init__(self, shared_kb: SharedKnowledgeBase):
        self.shared_kb = shared_kb
        self.local_cache: Dict[str, Any] = {}
        self.last_sync = 0

    def get(self, key: str) -> Any:
        # 先查本地缓存
        if key in self.local_cache:
            return self.local_cache[key]

        # 缓存未命中，从共享知识库获取
        if key in self.shared_kb.base_knowledge:
            value = self.shared_kb.base_knowledge[key]
            self.local_cache[key] = value
            return value

        return None

    def sync(self):
        # 同步更新
        if self.shared_kb.last_update > self.last_sync:
            self.local_cache.clear()
            self.last_sync = time.time()
```

---

## 第三部分：代码实践（10 题）

### 5. 代码分析（5 题）

**5.1** 以下代码有什么问题？

```python
class SharedMemory:
    def __init__(self):
        self.data = {}

    def write(self, key, value):
        self.data[key] = value

    def read(self, key):
        return self.data[key]
```

**答案**: 缺少并发控制

**问题**:
1. 多个 Agent 同时写入可能导致数据竞争
2. 没有使用锁保护共享数据

**修复**:
```python
import threading

class SharedMemory:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def write(self, key, value):
        with self.lock:
            self.data[key] = value

    def read(self, key):
        with self.lock:
            return self.data.get(key)
```

---

**5.2** 以下代码的输出是什么？

```python
agents = [Agent(f"agent{i}") for i in range(3)]
for agent in agents:
    agent.send_message("Hello")

print(agents[1].received_messages)
```

**答案**: 无法确定

**理由**:
1. 没有提供 Agent 类的实现
2. 不知道 `send_message` 和 `received_messages` 的具体逻辑

---

**5.3** 以下代码实现了什么模式？

```python
class Manager:
    def __init__(self):
        self.workers = []

    def add_worker(self, worker):
        self.workers.append(worker)

    def delegate(self, task):
        for worker in self.workers:
            worker.execute(task)
```

**答案**: 层次化架构

**特点**:
1. Manager 协调 Workers
2. 自上而下的任务分配
3. 典型的 Manager-Agent 模式

---

**5.4** 以下代码有什么问题？

```python
while True:
    message = receive_message()
    process_message(message)
```

**答案**: 死循环，没有退出条件

**问题**:
1. 会永远运行下去
2. 如果没有消息，会浪费 CPU
3. 没有错误处理

**修复**:
```python
running = True
while running:
    try:
        message = receive_message(timeout=1.0)
        if message:
            process_message(message)
        else:
            time.sleep(0.1)  # 避免忙等待
    except KeyboardInterrupt:
        running = False
    except Exception as e:
        log_error(e)
```

---

**5.5** 以下代码的输出是什么？

```python
results = []
for i in range(3):
    results.append(agent.execute(f"task{i}"))

print(len(results))
```

**答案**: 3

**理由**:
- 循环 3 次（0, 1, 2）
- 每次都 append 一个结果
- 最终 results 有 3 个元素

---

### 6. 代码实现（5 题）

**6.1** 实现一个简单的消息队列

```python
from collections import deque
from typing import Optional, Dict, Any

class MessageQueue:
    def __init__(self):
        self.queue = deque()

    def send(self, message: Dict[str, Any]):
        """发送消息"""
        self.queue.append(message)

    def receive(self) -> Optional[Dict[str, Any]]:
        """接收消息"""
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self) -> bool:
        """检查队列是否为空"""
        return len(self.queue) == 0
```

---

**6.2** 实现一个简单的 Agent 类

```python
class Agent:
    def __init__(self, name: str):
        self.name = name
        self.message_queue = MessageQueue()
        self.received_messages = []

    def send_message(self, to_agent: 'Agent', content: str):
        """发送消息给其他 Agent"""
        message = {
            "from": self.name,
            "to": to_agent.name,
            "content": content
        }
        to_agent.receive_message(message)

    def receive_message(self, message: Dict[str, Any]):
        """接收消息"""
        self.received_messages.append(message)

    def process_messages(self):
        """处理所有消息"""
        for msg in self.received_messages:
            print(f"[{self.name}] 收到来自 {msg['from']} 的消息: {msg['content']}")
        self.received_messages.clear()
```

---

**6.3** 实现一个层次化的 Manager-Agent 系统

```python
class ManagerAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.workers = []

    def add_worker(self, worker: 'WorkerAgent'):
        """添加 Worker"""
        self.workers.append(worker)

    def delegate_task(self, task: str):
        """分配任务给所有 Workers"""
        print(f"[{self.name}] 分配任务: {task}")
        for worker in self.workers:
            worker.receive_task(task)

class WorkerAgent(Agent):
    def __init__(self, name: str, role: str):
        super().__init__(name)
        self.role = role
        self.current_task = None

    def receive_task(self, task: str):
        """接收任务"""
        self.current_task = task
        print(f"[{self.name}] ({self.role}) 收到任务: {task}")

    def execute_task(self):
        """执行任务"""
        if self.current_task:
            result = f"[{self.name}] 完成 {self.role} 工作"
            print(result)
            return result
```

---

**6.4** 实现一个发布-订阅系统

```python
class PubSubSystem:
    def __init__(self):
        self.subscribers = {}  # topic -> list of agents

    def subscribe(self, agent: Agent, topic: str):
        """订阅主题"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(agent)
        print(f"[{agent.name}] 订阅了主题: {topic}")

    def publish(self, topic: str, message: str):
        """发布消息到主题"""
        if topic in self.subscribers:
            print(f"\n发布到主题 '{topic}': {message}")
            for agent in self.subscribers[topic]:
                agent.receive_message({
                    "from": "system",
                    "to": agent.name,
                    "content": f"[{topic}] {message}"
                })
```

---

**6.5** 实现一个简单的冲突检测和解决机制

```python
class ConflictResolver:
    def __init__(self):
        self.resource_status = {}  # resource -> owner

    def request_resource(self, agent_name: str, resource: str) -> bool:
        """请求资源"""
        if resource not in self.resource_status:
            # 资源空闲，分配给 Agent
            self.resource_status[resource] = agent_name
            print(f"[{agent_name}] 获得资源: {resource}")
            return True
        elif self.resource_status[resource] == agent_name:
            # Agent 已经拥有该资源
            return True
        else:
            # 资源被其他 Agent 占用
            owner = self.resource_status[resource]
            print(f"[{agent_name}] 无法获得资源 {resource} (被 {owner} 占用)")
            return False

    def release_resource(self, agent_name: str, resource: str):
        """释放资源"""
        if self.resource_status.get(resource) == agent_name:
            del self.resource_status[resource]
            print(f"[{agent_name}] 释放资源: {resource}")
```

---

## 📊 评分标准

- **概念理解**（10 分）：每题 1 分
- **架构设计**（10 分）：每题 2 分
- **代码实践**（10 分）：每题 1 分

**总分**: 30 分

**及格线**: 24 分（80%）

---

## ✅ 自检清单

完成练习后，检查以下内容：

- [ ] 所有题目都已作答
- [ ] 理解每道题的答案和解析
- [ ] 能够解释为什么选这个答案
- [ ] 能够用代码实现设计问题
- [ ] 记录不理解的题目，查阅相关资料

---

## 🚀 下一步

完成基础练习后，继续：
- `exercises/02_intermediate_exercises.md` - 进阶练习
- `exercises/03_challenge_projects.md` - 挑战项目

---

**记住：练习是巩固知识的最好方式！** 💪
