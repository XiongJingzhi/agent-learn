# 进阶练习题 - 多智能体协作

> **难度**: ⭐⭐⭐
> **预计时间**: 90 分钟
> **题目数量**: 20 题

---

## 📋 练习说明

本练习包含 20 道进阶题，侧重于多智能体系统的设计和实现。

**答题方式**:
1. 设计题：设计系统架构或协议
2. 实现题：编写具体实现代码
3. 分析题：分析系统行为和性能
4. 调试题：找出代码问题并修复

---

## 第一部分：系统设计（5 题）

### 1. 协作模式选择

**场景**：一个需要实时处理用户查询的客服系统，要求：
- 3 个专业 Agent（售前、售后、技术支持）
- 快速响应（< 2 秒）
- 需要转接复杂问题

**问题**：
1. 应该选择哪种协作模式？为什么？
2. 画出系统架构图
3. 说明如何实现问题转接

**答案**：
1. **选择**：层次化架构 + 扁平化协作
   - **理由**：
     - 层次化：有统一的协调者（Manager）分配任务
     - 扁平化：Agent 之间可以直接转接问题
     - 混合模式满足快速响应和专业处理的需求

2. **架构图**：
```
        User
         ↓
    Manager (路由)
       / | \
  售前 售后 技术
   ↓     ↓     ↓
  [可直接转接]
```

3. **转接实现**：
```python
class ServiceAgent:
    def transfer_to(self, to_agent: str, context: dict):
        """转接到其他 Agent"""
        return {
            "type": "transfer",
            "to": to_agent,
            "context": context,
            "reason": "需要专业支持"
        }
```

---

### 2. 通信协议设计

**场景**：设计一个支持以下功能的通信协议：
- 点对点消息
- 广播消息
- 消息确认
- 错误处理

**问题**：设计消息格式和处理流程

**答案**：
```python
@dataclass
class EnhancedMessage:
    # 基础字段
    id: str
    from_agent: str
    to_agent: str  # "*" 表示广播
    content: dict
    timestamp: float

    # 控制字段
    msg_type: str  # unicast, broadcast, multicast
    require_ack: bool = False
    ack_timeout: float = 5.0
    retry_count: int = 0
    max_retries: int = 3

    # 错误处理
    error_code: str = None
    error_message: str = None

class MessageHandler:
    def handle_message(self, msg: EnhancedMessage):
        # 处理消息
        try:
            result = self._process(msg)

            # 发送确认
            if msg.require_ack:
                self.send_ack(msg.id, result)

        except Exception as e:
            # 错误处理
            self.handle_error(msg, e)

            # 重试
            if msg.retry_count < msg.max_retries:
                msg.retry_count += 1
                self.retry(msg)
```

---

### 3. 冲突解决设计

**场景**：3 个 Agent 竞争 2 个资源（资源 A 和 B）

**问题**：设计一个公平且高效的资源分配机制

**答案**：
```python
class ResourceAllocator:
    def __init__(self):
        self.resources = {
            "resource_a": None,
            "resource_b": None
        }
        self.wait_queue = []
        self.allocation_history = []

    def request(self, agent: str, preferences: List[str]):
        """请求资源"""
        # 检查偏好资源是否可用
        for resource in preferences:
            if self.resources[resource] is None:
                self.allocate(resource, agent)
                return True

        # 加入等待队列
        self.wait_queue.append((agent, preferences))
        return False

    def allocate(self, resource: str, agent: str):
        """分配资源"""
        self.resources[resource] = agent
        self.allocation_history.append({
            "resource": resource,
            "agent": agent,
            "timestamp": time.time()
        })

    def release(self, agent: str, resource: str):
        """释放资源"""
        if self.resources[resource] == agent:
            self.resources[resource] = None

            # 检查等待队列
            if self.wait_queue:
                next_agent, prefs = self.wait_queue.pop(0)
                for pref in prefs:
                    if self.resources[pref] is None:
                        self.allocate(pref, next_agent)
                        break

    def get_fairness_score(self) -> float:
        """计算公平性分数"""
        from collections import Counter
        allocations = [a["agent"] for a in self.allocation_history]
        counts = Counter(allocations)
        max_count = max(counts.values())
        min_count = min(counts.values())
        return min_count / max_count if max_count > 0 else 1.0
```

---

### 4. RAG 系统设计

**场景**：为 3 个 Agent（研究、分析、写作）设计共享 RAG 系统

**问题**：
1. 选择哪种 RAG 架构？
2. 如何处理知识更新？
3. 如何避免重复检索？

**答案**：
1. **架构选择**：混合式 RAG
   - 共享基础知识库
   - 每个 Agent 有本地缓存
   - 定期同步

2. **知识更新**：
```python
class HybridRAG:
    def __init__(self):
        self.shared_kb = SharedKnowledgeBase()
        self.local_caches = {}

    def update_knowledge(self, new_docs: List[str]):
        """更新共享知识库"""
        self.shared_kb.add_documents(new_docs)

        # 通知所有 Agent 清除缓存
        for agent in self.local_caches:
            self.local_caches[agent].clear()

    def query(self, agent: str, question: str) -> str:
        """查询"""
        # 先查本地缓存
        cache = self.local_caches.get(agent)
        if cache and question in cache:
            return cache[question]

        # 查询共享知识库
        result = self.shared_kb.query(question)

        # 更新本地缓存
        if not cache:
            cache = {}
            self.local_caches[agent] = cache
        cache[question] = result

        return result
```

3. **避免重复检索**：
```python
# 使用查询去重
class QueryDeduplicator:
    def __init__(self, ttl: float = 300):
        self.recent_queries = {}
        self.ttl = ttl

    def is_duplicate(self, query: str) -> bool:
        """检查是否重复查询"""
        if query in self.recent_queries:
            if time.time() - self.recent_queries[query] < self.ttl:
                return True
        return False

    def record_query(self, query: str):
        """记录查询"""
        self.recent_queries[query] = time.time()
```

---

### 5. 性能优化设计

**场景**：多智能体系统响应时间过长（平均 8 秒）

**问题**：分析可能的瓶颈并提出优化方案

**答案**：
**可能瓶颈**：
1. LLM 调用时间过长
2. 串行执行任务
3. 通信开销大
4. RAG 检索慢

**优化方案**：
```python
class OptimizedMultiAgentSystem:
    def __init__(self):
        self.agents = {}
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.cache = {}

    async def process_request(self, request: str):
        """并行处理请求"""
        # 1. 检查缓存
        if request in self.cache:
            return self.cache[request]

        # 2. 并行执行多个 Agent
        tasks = [
            self._run_agent(agent, request)
            for agent in self.agents.values()
        ]

        results = await asyncio.gather(*tasks)

        # 3. 聚合结果
        final_result = self.aggregate(results)

        # 4. 缓存结果
        self.cache[request] = final_result

        return final_result

    async def _run_agent(self, agent, request):
        """异步运行 Agent"""
        # 使用轻量级 LLM（如 GPT-3.5）
        # 批量处理
        # 使用流式输出
        result = await agent.aprocess(request)
        return result
```

---

## 第二部分：代码实现（10 题）

### 6. 实现消息队列

**要求**：
- 支持优先级
- 支持过期消息
- 线程安全

```python
import heapq
import threading
import time
from dataclasses import dataclass, field

@dataclass(order=True)
class PriorityMessage:
    priority: int
    expire_time: float
    message: dict = field(compare=False)

class PriorityMessageQueue:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def enqueue(self, message: dict, priority: int = 0, ttl: float = 60):
        """入队"""
        with self.lock:
            msg = PriorityMessage(
                priority=priority,
                expire_time=time.time() + ttl,
                message=message
            )
            heapq.heappush(self.queue, msg)
            self.condition.notify()

    def dequeue(self, timeout: float = None) -> Optional[dict]:
        """出队"""
        with self.condition:
            # 等待消息
            while not self.queue:
                if not self.condition.wait(timeout):
                    return None

            # 清理过期消息
            now = time.time()
            while self.queue and self.queue[0].expire_time < now:
                heapq.heappop(self.queue)

            if not self.queue:
                return None

            return heapq.heappop(self.queue).message
```

---

### 7. 实现发布-订阅系统

**要求**：
- 支持主题过滤
- 支持通配符订阅
- 支持取消订阅

```python
import re
from typing import Dict, List, Callable, Pattern

class WildcardPubSub:
    def __init__(self):
        self.subscriptions: Dict[Pattern, List[Callable]] = []

    def subscribe(self, topic_pattern: str, callback: Callable):
        """订阅主题（支持通配符）"""
        pattern = re.compile(topic_pattern.replace("*", ".*"))
        self.subscriptions.append((pattern, callback))

    def publish(self, topic: str, message: dict):
        """发布消息"""
        for pattern, callback in self.subscriptions:
            if pattern.match(topic):
                try:
                    callback(topic, message)
                except Exception as e:
                    print(f"订阅者错误: {e}")

    def unsubscribe(self, topic_pattern: str, callback: Callable):
        """取消订阅"""
        pattern = re.compile(topic_pattern.replace("*", ".*"))
        self.subscriptions = [
            (p, c) for p, c in self.subscriptions
            if not (p == pattern and c == callback)
        ]
```

---

### 8. 实现简单的共识机制

**要求**：实现多数投票共识

```python
class ConsensusMechanism:
    def __init__(self, agents: List[str]):
        self.agents = set(agents)
        self.votes: Dict[str, Dict[str, str]] = {}

    def start_voting(self, proposal_id: str, options: List[str]):
        """开始投票"""
        self.votes[proposal_id] = {
            agent: None for agent in self.agents
        }
        self.options[proposal_id] = options

    def vote(self, proposal_id: str, agent: str, choice: str):
        """投票"""
        if proposal_id in self.votes and agent in self.votes[proposal_id]:
            self.votes[proposal_id][agent] = choice

    def get_result(self, proposal_id: str) -> Optional[str]:
        """获取投票结果"""
        if proposal_id not in self.votes:
            return None

        votes = self.votes[proposal_id]

        # 检查是否所有人都投票了
        if any(v is None for v in votes.values()):
            return None

        # 统计投票
        from collections import Counter
        counts = Counter(votes.values())

        # 返回多数票
        return counts.most_common(1)[0][0]

    def has_consensus(self, proposal_id: str, threshold: float = 0.67) -> bool:
        """检查是否达成共识"""
        result = self.get_result(proposal_id)
        if not result:
            return False

        votes = self.votes[proposal_id]
        count = sum(1 for v in votes.values() if v == result)

        return count / len(votes) >= threshold
```

---

### 9. 实现分布式锁

```python
import time
import uuid
from contextlib import contextmanager

class DistributedLock:
    def __init__(self):
        self.locks: Dict[str, Dict] = {}
        self.lock = threading.Lock()

    def acquire(self, resource: str, agent: str, timeout: float = 10) -> bool:
        """获取锁"""
        start = time.time()

        while time.time() - start < timeout:
            with self.lock:
                if resource not in self.locks:
                    self.locks[resource] = {
                        "owner": agent,
                        "lock_id": str(uuid.uuid4()),
                        "acquired_at": time.time()
                    }
                    return True

                # 检查锁是否过期（TTL = 30 秒）
                lock_info = self.locks[resource]
                if time.time() - lock_info["acquired_at"] > 30:
                    del self.locks[resource]
                    continue

            time.sleep(0.1)

        return False

    def release(self, resource: str, agent: str, lock_id: str):
        """释放锁"""
        with self.lock:
            if resource in self.locks:
                lock_info = self.locks[resource]
                if (lock_info["owner"] == agent and
                    lock_info["lock_id"] == lock_id):
                    del self.locks[resource]

    @contextmanager
    def lock_context(self, resource: str, agent: str):
        """锁上下文管理器"""
        if not self.acquire(resource, agent):
            raise RuntimeError(f"无法获取资源 {resource}")

        lock_id = self.locks[resource]["lock_id"]
        try:
            yield
        finally:
            self.release(resource, agent, lock_id)
```

---

### 10. 实现结果缓存

```python
from functools import lru_cache
import hashlib
import pickle

class ResultCache:
    def __init__(self, max_size: int = 1000, ttl: float = 3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.lock = threading.Lock()

    def _make_key(self, *args, **kwargs) -> str:
        """生成缓存键"""
        data = pickle.dumps((args, sorted(kwargs.items())))
        return hashlib.md5(data).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if time.time() - item["timestamp"] < self.ttl:
                    return item["value"]
                else:
                    del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        """设置缓存"""
        with self.lock:
            # LRU 淘汰
            if len(self.cache) >= self.max_size:
                oldest = min(self.cache.items(),
                           key=lambda x: x[1]["timestamp"])
                del self.cache[oldest[0]]

            self.cache[key] = {
                "value": value,
                "timestamp": time.time()
            }

    def invalidate(self, pattern: str = None):
        """使缓存失效"""
        with self.lock:
            if pattern:
                keys_to_delete = [
                    k for k in self.cache
                    if pattern in k
                ]
                for k in keys_to_delete:
                    del self.cache[k]
            else:
                self.cache.clear()

    def cached(self, func):
        """缓存装饰器"""
        def wrapper(*args, **kwargs):
            key = self._make_key(func.__name__, *args, **kwargs)
            result = self.get(key)
            if result is None:
                result = func(*args, **kwargs)
                self.set(key, result)
            return result
        return wrapper
```

---

## 第三部分：分析和调试（5 题）

### 11. 死锁分析

**场景**：2 个 Agent 和 2 个资源

```
Agent1: 持有 Resource_A，等待 Resource_B
Agent2: 持有 Resource_B，等待 Resource_A
```

**问题**：
1. 这是什么问题？
2. 如何检测？
3. 如何解决？

**答案**：
1. **死锁**：循环等待资源

2. **检测**：
```python
class DeadlockDetector:
    def __init__(self):
        self.wait_graph = {}  # agent -> [resources it's waiting for]
        self.resource_owners = {}  # resource -> agent

    def detect_cycle(self) -> bool:
        """检测循环等待"""
        # 构建图
        graph = {}
        for agent, resources in self.wait_graph.items():
            graph[agent] = []
            for resource in resources:
                if resource in self.resource_owners:
                    owner = self.resource_owners[resource]
                    graph[agent].append(owner)

        # DFS 检测环
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True

        return False
```

3. **解决**：
- 资源排序：所有 Agent 按相同顺序申请资源
- 超时：放弃等待
- 预分配：一次性申请所有资源

---

### 12. 性能瓶颈分析

**场景**：系统处理一个请求需要 10 秒

**问题**：分析以下代码，找出瓶颈

```python
def process_request(request):
    # 步骤 1: 分析请求 (2 秒)
    analysis = analyze_request(request)

    # 步骤 2: 检索知识 (3 秒)
    knowledge = retrieve_knowledge(analysis)

    # 步骤 3: Agent1 处理 (2 秒)
    result1 = agent1.process(knowledge)

    # 步骤 4: Agent2 处理 (2 秒)
    result2 = agent2.process(knowledge)

    # 步骤 5: Agent3 处理 (1 秒)
    result3 = agent3.process(knowledge)

    # 步骤 6: 聚合结果 (无时间)
    return aggregate([result1, result2, result3])
```

**答案**：
**瓶颈分析**：
- 步骤 3-5 可以并行执行（共 5 秒）
- 步骤 2 只需要执行一次

**优化**：
```python
import asyncio

async def process_request_optimized(request):
    # 步骤 1: 分析请求 (2 秒)
    analysis = await asyncio.to_thread(analyze_request, request)

    # 步骤 2: 检索知识 (3 秒) - 只执行一次
    knowledge = await asyncio.to_thread(retrieve_knowledge, analysis)

    # 步骤 3-5: 并行执行 (max(2, 2, 1) = 2 秒)
    results = await asyncio.gather(
        asyncio.to_thread(agent1.process, knowledge),
        asyncio.to_thread(agent2.process, knowledge),
        asyncio.to_thread(agent3.process, knowledge)
    )

    # 总时间: 2 + 3 + 2 = 7 秒
    return aggregate(results)
```

---

## 📊 评分标准

- **系统设计**（25 分）：每题 5 分
- **代码实现**（50 分）：每题 5 分
- **分析调试**（25 分）：每题 5 分

**总分**: 100 分

**及格线**: 70 分

---

## ✅ 自检清单

- [ ] 所有设计题都有架构图
- [ ] 所有代码都可运行
- [ ] 所有分析都有依据
- [ ] 理解每个解决方案的权衡

---

## 🚀 下一步

完成进阶练习后，继续：
- `exercises/03_challenge_projects.md` - 挑战项目

---

**记住：进阶练习是提升能力的关键！** 💪
