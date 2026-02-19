# 记忆层次设计

> **目标**: 理解如何设计 Agent 的多层次记忆系统
> **预计时间**: 40 分钟
> **难度**: ⭐⭐⭐⭐

---

## 为什么需要记忆层次？

就像人类的记忆系统一样，Agent 也需要不同层次的记忆来处理不同类型的信息：

**短期记忆（工作记忆）**：
- 当前对话的上下文
- 临时变量和中间结果
- **特点**：快速访问、容量有限、临时存储

**中期记忆（情节记忆）**：
- 重要对话摘要
- 关键决策和结果
- **特点**：选择性保存、可检索、会话级别

**长期记忆（语义记忆）**：
- 用户偏好和历史
- 知识库和文档
- **特点**：持久化、跨会话、大容量

---

## 记忆层次架构

### 架构图

```
┌─────────────────────────────────────────────────┐
│                  Agent Core                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │    短期记忆 (Short-term Memory)         │   │
│  │    - 当前对话                            │   │
│  │    - 临时变量                            │   │
│  │    - 容量: ~10-20 条消息                │   │
│  │    - 速度: 极快                          │   │
│  │    - 持久化: 否                          │   │
│  └──────────────┬──────────────────────────┘   │
│                 │ 定期摘要                      │
│                 ▼                               │
│  ┌─────────────────────────────────────────┐   │
│  │    中期记忆 (Medium-term Memory)        │   │
│  │    - 对话摘要                            │   │
│  │    - 重要决策                            │   │
│  │    - 容量: ~50-100 条摘要               │   │
│  │    - 速度: 快                            │   │
│  │    - 持久化: 会话级别                    │   │
│  └──────────────┬──────────────────────────┘   │
│                 │ 选择性归档                   │
│                 ▼                               │
│  ┌─────────────────────────────────────────┐   │
│  │    长期记忆 (Long-term Memory)          │   │
│  │    - 用户偏好                            │   │
│  │    - 知识库                              │   │
│  │    - 容量: 几乎无限                      │   │
│  │    - 速度: 中等                          │   │
│  │    - 持久化: 持久                        │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 短期记忆设计

### 特点

- **快速访问**：直接在内存中
- **自动清理**：超过容量自动淘汰最旧的消息
- **无持久化**：会话结束即清空

### 实现

```python
from typing import List, Dict, Any, Optional
from collections import deque
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    """消息"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata or {}
        }


class ShortTermMemory:
    """短期记忆（工作记忆）"""

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: deque = deque(maxlen=max_messages)

    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """添加消息"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata
        )
        self.messages.append(message)

    def get_recent_messages(self, n: int = None) -> List[Message]:
        """获取最近的消息"""
        if n is None:
            return list(self.messages)
        return list(self.messages)[-n:]

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史（用于 LLM）"""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

    def clear(self):
        """清空记忆"""
        self.messages.clear()

    def __len__(self):
        return len(self.messages)
```

---

## 中期记忆设计

### 特点

- **选择性保存**：只保存重要的信息
- **摘要压缩**：将多轮对话压缩为摘要
- **会话持久化**：当前会话期间保留

### 实现

```python
@dataclass
class Summary:
    """对话摘要"""
    summary_id: str
    content: str
    timestamp: datetime
    message_count: int  # 这个摘要覆盖了多少条消息
    importance: float  # 0.0 - 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_count": self.message_count,
            "importance": self.importance
        }


class MediumTermMemory:
    """中期记忆（情节记忆）"""

    def __init__(self, max_summaries: int = 100):
        self.max_summaries = max_summaries
        self.summaries: List[Summary] = []
        self.summary_counter = 0

    def add_summary(self,
                   content: str,
                   message_count: int,
                   importance: float = 0.5):
        """添加摘要"""
        self.summary_counter += 1
        summary = Summary(
            summary_id=f"summary_{self.summary_counter}",
            content=content,
            timestamp=datetime.now(),
            message_count=message_count,
            importance=importance
        )
        self.summaries.append(summary)

        # 如果超过容量，删除最不重要的摘要
        if len(self.summaries) > self.max_summaries:
            self.summaries.sort(key=lambda s: s.importance)
            self.summaries.pop(0)

    def get_recent_summaries(self, n: int = 5) -> List[Summary]:
        """获取最近的摘要"""
        return self.summaries[-n:]

    def get_important_summaries(self, threshold: float = 0.7) -> List[Summary]:
        """获取重要的摘要"""
        return [s for s in self.summaries if s.importance >= threshold]

    def search(self, query: str) -> List[Summary]:
        """搜索摘要（简单的关键词匹配）"""
        query_lower = query.lower()
        return [
            s for s in self.summaries
            if query_lower in s.content.lower()
        ]

    def clear(self):
        """清空记忆"""
        self.summaries = []
        self.summary_counter = 0
```

---

## 长期记忆设计

### 特点

- **持久化存储**：保存到数据库或文件
- **向量检索**：使用语义相似度搜索
- **跨会话保留**：多次会话共享

### 实现

```python
@dataclass
class MemoryItem:
    """长期记忆项"""
    memory_id: str
    content: str
    embedding: Optional[List[float]] = None  # 向量表示
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    access_count: int = 0

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "access_count": self.access_count
        }


class LongTermMemory:
    """长期记忆（语义记忆）"""

    def __init__(self, storage_path: str = "./long_term_memory.json"):
        self.storage_path = storage_path
        self.memories: Dict[str, MemoryItem] = {}
        self.memory_counter = 0
        self._load()

    def add_memory(self,
                  content: str,
                  metadata: Dict[str, Any] = None,
                  importance: float = 0.5) -> str:
        """添加记忆"""
        self.memory_counter += 1
        memory_id = f"memory_{self.memory_counter}"

        memory = MemoryItem(
            memory_id=memory_id,
            content=content,
            metadata=metadata or {},
            timestamp=datetime.now()
        )

        self.memories[memory_id] = memory
        self._save()

        return memory_id

    def get_memory(self, memory_id: str) -> Optional[MemoryItem]:
        """获取记忆"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.access_count += 1
            return memory
        return None

    def search_by_keyword(self, keyword: str) -> List[MemoryItem]:
        """关键词搜索"""
        keyword_lower = keyword.lower()
        return [
            m for m in self.memories.values()
            if keyword_lower in m.content.lower()
        ]

    def search_by_metadata(self, key: str, value: Any) -> List[MemoryItem]:
        """元数据搜索"""
        return [
            m for m in self.memories.values()
            if m.metadata.get(key) == value
        ]

    def get_frequent_memories(self, threshold: int = 5) -> List[MemoryItem]:
        """获取频繁访问的记忆"""
        return [
            m for m in self.memories.values()
            if m.access_count >= threshold
        ]

    def _save(self):
        """保存到磁盘"""
        import json
        data = {
            "counter": self.memory_counter,
            "memories": [m.to_dict() for m in self.memories.values()]
        }

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load(self):
        """从磁盘加载"""
        import json
        from pathlib import Path

        if not Path(self.storage_path).exists():
            return

        with open(self.storage_path, 'r') as f:
            data = json.load(f)

        self.memory_counter = data.get("counter", 0)

        for item_data in data.get("memories", []):
            memory = MemoryItem(
                memory_id=item_data["memory_id"],
                content=item_data["content"],
                embedding=item_data.get("embedding"),
                metadata=item_data.get("metadata", {}),
                timestamp=datetime.fromisoformat(item_data["timestamp"]),
                access_count=item_data.get("access_count", 0)
            )
            self.memories[memory_id] = memory

    def clear(self):
        """清空记忆"""
        self.memories = {}
        self.memory_counter = 0
        self._save()
```

---

## 完整示例：分层记忆系统

```python
from typing import List, Dict, Any, Optional
from datetime import datetime

class HierarchicalMemory:
    """分层记忆系统"""

    def __init__(self):
        # 三层记忆
        self.short_term = ShortTermMemory(max_messages=20)
        self.medium_term = MediumTermMemory(max_summaries=100)
        self.long_term = LongTermMemory(storage_path="./memories.json")

    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """添加消息到短期记忆"""
        self.short_term.add_message(role, content, metadata)

        # 如果短期记忆满了，创建摘要
        if len(self.short_term) >= self.short_term.max_messages:
            self._create_summary()

    def _create_summary(self):
        """创建摘要并转移到中期记忆"""
        messages = self.short_term.get_recent_messages()

        # 简化的摘要生成（实际应该使用 LLM）
        summary_content = f"包含 {len(messages)} 条消息的对话"
        importance = 0.5

        # 添加到中期记忆
        self.medium_term.add_summary(
            content=summary_content,
            message_count=len(messages),
            importance=importance
        )

        # 清空短期记忆
        self.short_term.clear()

    def archive_to_long_term(self, summary_id: str, metadata: Dict[str, Any] = None):
        """将摘要归档到长期记忆"""
        # 在中期记忆中找到摘要
        # （这里简化处理）
        summary_content = f"归档的摘要: {summary_id}"

        self.long_term.add_memory(
            content=summary_content,
            metadata=metadata or {}
        )

    def get_context(self) -> str:
        """获取完整上下文"""
        context_parts = []

        # 1. 短期记忆（最近消息）
        recent = self.short_term.get_recent_messages(n=5)
        if recent:
            context_parts.append("=== 最近消息 ===")
            for msg in recent:
                context_parts.append(f"{msg.role}: {msg.content}")

        # 2. 中期记忆（重要摘要）
        summaries = self.medium_term.get_important_summaries(threshold=0.7)
        if summaries:
            context_parts.append("\n=== 重要摘要 ===")
            for summary in summaries:
                context_parts.append(f"- {summary.content}")

        # 3. 长期记忆（频繁访问）
        frequent = self.long_term.get_frequent_memories(threshold=5)
        if frequent:
            context_parts.append("\n=== 长期记忆 ===")
            for memory in frequent:
                context_parts.append(f"- {memory.content}")

        return "\n".join(context_parts)

    def search(self, query: str) -> Dict[str, List]:
        """搜索所有层次"""
        results = {
            "short_term": [],  # 短期记忆不搜索
            "medium_term": self.medium_term.search(query),
            "long_term": self.long_term.search_by_keyword(query)
        }
        return results


# 运行示例
def main():
    print("=" * 70)
    print("分层记忆系统示例")
    print("=" * 70)

    memory_system = HierarchicalMemory()

    # 添加消息
    print("\n[添加消息到短期记忆]")
    memory_system.add_message("user", "你好，我叫张三")
    memory_system.add_message("assistant", "你好张三，很高兴认识你")
    memory_system.add_message("user", "我喜欢编程，特别是 Python")
    memory_system.add_message("assistant", "Python 是一门很棒的语言")

    # 获取上下文
    print("\n[获取上下文]")
    context = memory_system.get_context()
    print(context)

    # 归档到长期记忆
    print("\n[归档到长期记忆]")
    memory_system.archive_to_long_term(
        "user_profile",
        metadata={"type": "user_preference", "user": "张三"}
    )

    # 搜索
    print("\n[搜索]")
    results = memory_system.search("Python")
    print(f"找到 {len(results['long_term'])} 条相关记忆")


if __name__ == "__main__":
    main()
```

---

## 关键设计考虑

### 考虑 1：记忆容量

**问题**：如何设定各层记忆的容量？

**建议**：
- 短期记忆：10-20 条消息（约 2000-4000 tokens）
- 中期记忆：50-100 条摘要
- 长期记忆：根据存储资源决定

---

### 考虑 2：摘要策略

**问题**：如何生成高质量的摘要？

**方案**：
- 使用 LLM 生成摘要
- 保留关键信息（实体、事件、决策）
- 标注重要性评分

---

### 考虑 3：检索效率

**问题**：如何快速检索相关记忆？

**方案**：
- 关键词索引
- 向量相似度搜索（使用 Embeddings）
- 元数据过滤

---

## 最小验证

- [ ] 能够实现三层记忆系统
- [ ] 能够实现消息的自动流转
- [ ] 能够实现跨层搜索
- [ ] 能够持久化长期记忆

---

## 下一步

- 📖 `notes/09_memory_retrieval_strategy.md` - 记忆检索策略
- 🧪 `examples/09_memory_system.py` - 记忆系统示例

---

**记住：分层记忆就像人类的大脑，不同层次的记忆处理不同类型的信息！** 🧠
