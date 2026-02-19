# 06. Agent 通信协议

> **主题**: 设计 Agent 之间的通信机制
> **时间**: 60 分钟
> **难度**: ⭐⭐⭐

---

## 🎯 学习目标

1. ✅ 理解为什么需要通信协议
2. ✅ 掌握 3 种主要的通信机制
3. ✅ 能够设计高效的通信协议
4. ✅ 理解每种机制的优缺点和适用场景

---

## 📚 核心概念

### 为什么需要通信协议？

**问题**: 多个 Agent 如何协作？

**答案**: 通过通信协议交换信息和协调行动

**类比**:
- 通信协议 = 语言的语法和规则
- Agent = 使用不同语言的人
- 协议让大家理解彼此

---

## 🔍 3 种通信机制详解

### 1. 消息传递（Message Passing）

#### 概念

Agent 之间通过发送和接收消息进行通信。

**类比**: 发送邮件

```
Agent A                 Agent B
  |                       |
  |  --- Message 1 --->   |
  |                       |
  |  <--- Message 2 ---   |
  |                       |
```

#### 消息格式

```python
# 标准消息格式
message = {
    "id": "unique_message_id",      # 消息 ID
    "from": "agent_a",               # 发送者
    "to": "agent_b",                 # 接收者
    "type": "request",               # 消息类型
    "content": {...},                # 消息内容
    "timestamp": 1234567890,         # 时间戳
    "reply_to": None                 # 回复的消息 ID（可选）
}
```

#### 实现

```python
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Message:
    """消息类"""
    id: str
    from_agent: str
    to_agent: str
    type: str
    content: Dict[str, Any]
    timestamp: float
    reply_to: str = None

    @classmethod
    def create(cls, from_agent: str, to_agent: str,
               type: str, content: Dict[str, Any],
               reply_to: str = None):
        """创建新消息"""
        return cls(
            id=str(uuid.uuid4()),
            from_agent=from_agent,
            to_agent=to_agent,
            type=type,
            content=content,
            timestamp=datetime.now().timestamp(),
            reply_to=reply_to
        )

class MessageBus:
    """消息总线"""

    def __init__(self):
        self.queues: Dict[str, List[Message]] = {}

    def send(self, message: Message):
        """发送消息"""
        if message.to_agent not in self.queues:
            self.queues[message.to_agent] = []
        self.queues[message.to_agent].append(message)

    def receive(self, agent_name: str) -> List[Message]:
        """接收消息"""
        messages = self.queues.get(agent_name, [])
        self.queues[agent_name] = []
        return messages

# 使用示例
bus = MessageBus()

# Agent A 发送消息给 Agent B
msg = Message.create(
    from_agent="agent_a",
    to_agent="agent_b",
    type="request",
    content={"task": "分析数据"}
)
bus.send(msg)

# Agent B 接收消息
messages = bus.receive("agent_b")
for msg in messages:
    print(f"收到来自 {msg.from_agent} 的消息: {msg.content}")
```

#### 优缺点

✅ **优点**:
- 解耦发送者和接收者
- 支持异步通信
- 易于扩展

❌ **缺点**:
- 需要消息队列
- 可能有序列化开销
- 消息顺序可能乱序

---

### 2. 共享内存（Shared Memory）

#### 概念

Agent 之间通过共享的状态空间进行通信。

**类比**: 共享白板

```
        Shared Memory
             ↑
      ┌──────┴──────┐
      |             |
   Agent A       Agent B
```

#### 状态结构

```python
# 共享状态
shared_state = {
    "agent_a": {
        "status": "working",
        "data": {...},
        "last_update": 1234567890
    },
    "agent_b": {
        "status": "idle",
        "data": {...},
        "last_update": 1234567891
    },
    "shared": {
        "counter": 0,
        "results": []
    }
}
```

#### 实现

```python
from typing import Dict, Any
import threading
import time

class SharedMemory:
    """共享内存"""

    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.lock = threading.Lock()

    def write(self, agent_name: str, key: str, value: Any):
        """写入数据"""
        with self.lock:
            if agent_name not in self.state:
                self.state[agent_name] = {}
            self.state[agent_name][key] = value
            self.state[agent_name]["last_update"] = time.time()

    def read(self, agent_name: str, key: str) -> Any:
        """读取数据"""
        with self.lock:
            if agent_name in self.state and key in self.state[agent_name]:
                return self.state[agent_name][key]
            return None

    def read_all(self) -> Dict[str, Any]:
        """读取所有数据"""
        with self.lock:
            return self.state.copy()

# 使用示例
memory = SharedMemory()

# Agent A 写入数据
memory.write("agent_a", "status", "working")
memory.write("agent_a", "progress", 50)

# Agent B 读取 Agent A 的数据
status = memory.read("agent_a", "status")
print(f"Agent A 的状态: {status}")

# Agent B 读取所有数据
all_data = memory.read_all()
print(f"所有数据: {all_data}")
```

#### 优缺点

✅ **优点**:
- 快速访问
- 实时共享
- 实现简单

❌ **缺点**:
- 需要并发控制
- 可能有竞态条件
- 难以分布式部署

---

### 3. 发布-订阅（Pub-Sub）

#### 概念

Agent 发布消息到主题，订阅者接收感兴趣的消息。

**类比**: 邮件列表或 RSS 订阅

```
        Topics
         ↑
    ┌────┴────┐
    |         |
 Publisher  Subscriber
```

#### 实现

```python
from typing import Dict, List, Callable
from collections import defaultdict

class PubSub:
    """发布-订阅系统"""

    def __init__(self):
        self.topics: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable):
        """订阅主题"""
        self.topics[topic].append(callback)

    def publish(self, topic: str, message: dict):
        """发布消息"""
        if topic in self.topics:
            for callback in self.topics[topic]:
                callback(message)

    def unsubscribe(self, topic: str, callback: Callable):
        """取消订阅"""
        if topic in self.topics and callback in self.topics[topic]:
            self.topics[topic].remove(callback)

# 使用示例
pubsub = PubSub()

# Agent A 订阅 "results" 主题
def handle_result(message):
    print(f"Agent A 收到结果: {message}")

pubsub.subscribe("results", handle_result)

# Agent B 发布结果
pubsub.publish("results", {"data": "分析完成", "score": 95})

# Agent C 也订阅 "results" 主题
def handle_result_c(message):
    print(f"Agent C 收到结果: {message}")

pubsub.subscribe("results", handle_result_c)

# Agent B 再次发布结果
pubsub.publish("results", {"data": "新的分析", "score": 88})
```

#### 优缺点

✅ **优点**:
- 完全解耦发布者和订阅者
- 支持多对多通信
- 灵活的消息过滤

❌ **缺点**:
- 消息可能丢失
- 无法保证消息顺序
- 难以追踪消息流

---

## 📊 3 种机制对比

| 特性 | 消息传递 | 共享内存 | 发布-订阅 |
|------|----------|----------|-----------|
| **耦合度** | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **实时性** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **扩展性** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **可靠性** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **复杂度** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **适用场景** | 点对点 | 高速共享 | 广播通知 |

---

## 🎓 费曼解释

### 给 5 岁孩子的解释

**Agent 通信就像人与人之间的交流方式**：

1. **消息传递** = 写信给朋友
2. **共享内存** = 大家一起在白板上画画
3. **发布-订阅** = 订阅 YouTube 频道，有新视频就通知你

### 关键要点

1. **没有最好的通信机制，只有最合适的**
2. **选择时要考虑耦合度、实时性、扩展性**
3. **可以组合使用多种通信机制**

---

## 💡 实践建议

### 如何选择通信机制？

#### 决策树

```
开始
  ↓
需要高速共享状态？
  ├─ 是 → 共享内存
  └─ 否 ↓
      需要广播通知？
        ├─ 是 → 发布-订阅
        └─ 否 → 消息传递
```

### 设计原则

1. **最小化耦合**
   - 优先使用消息传递
   - 避免直接访问共享状态

2. **处理故障**
   - 消息可能丢失
   - Agent 可能失效
   - 网络可能中断

3. **考虑性能**
   - 批量处理消息
   - 避免频繁通信
   - 使用缓存减少重复通信

---

## 🔗 相关资源

- [Message Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/)
- [Pub-Sub Pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)
- [Shared Memory Models](https://en.wikipedia.org/wiki/Shared_memory)

---

## ✅ 最小验证

### 任务

1. 实现 3 种通信机制（30 分钟）
2. 对比 3 种机制的性能（10 分钟）
3. 为以下场景选择合适的通信机制（10 分钟）:
   - 场景 1: 两个 Agent 需要频繁交换大量数据
   - 场景 2: 一个 Agent 需要通知多个 Agent 某个事件
   - 场景 3: 多个 Agent 需要协调完成一个复杂任务

### 期望输出

- [ ] 3 种机制的实现代码
- [ ] 性能对比报告
- [ ] 3 个场景的机制选择和理由

---

## 🚀 下一步

学习完本笔记后，继续学习：
- `notes/07_message_passing.md` - 深入了解消息传递
- `examples/05_message_passing.py` - 实现消息传递系统

---

**记住：通信协议是多智能体系统的基础，选择合适的机制至关重要！** 📡
