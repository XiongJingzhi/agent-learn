"""
示例 03: 完整的记忆系统实现

演示三层记忆系统的实现和使用

作者：Senior Developer
日期：2026-02-19
"""

from typing import List, Dict, Any, Optional
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path

# ===== 数据结构 =====

@dataclass
class Message:
    """消息"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class Summary:
    """对话摘要"""
    summary_id: str
    content: str
    timestamp: datetime = None
    message_count: int = 0
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_count": self.message_count,
            "importance": self.importance,
            "tags": self.tags
        }


@dataclass
class MemoryItem:
    """长期记忆项"""
    memory_id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    access_count: int = 0
    importance: float = 0.5

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
            "access_count": self.access_count,
            "importance": self.importance
        }


# ===== 短期记忆 =====

class ShortTermMemory:
    """短期记忆（工作记忆）"""

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: deque = deque(maxlen=max_messages)

    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """添加消息"""
        message = Message(role=role, content=content, metadata=metadata)
        self.messages.append(message)
        print(f"[短期记忆] 添加消息: {role} - {content[:50]}...")

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
        print("[短期记忆] 已清空")

    def __len__(self):
        return len(self.messages)


# ===== 中期记忆 =====

class MediumTermMemory:
    """中期记忆（情节记忆）"""

    def __init__(self, max_summaries: int = 100):
        self.max_summaries = max_summaries
        self.summaries: List[Summary] = []
        self.summary_counter = 0

    def add_summary(self,
                   content: str,
                   message_count: int,
                   importance: float = 0.5,
                   tags: List[str] = None) -> str:
        """添加摘要"""
        self.summary_counter += 1
        summary = Summary(
            summary_id=f"summary_{self.summary_counter}",
            content=content,
            message_count=message_count,
            importance=importance,
            tags=tags or []
        )
        self.summaries.append(summary)

        # 如果超过容量，删除最不重要的摘要
        if len(self.summaries) > self.max_summaries:
            self.summaries.sort(key=lambda s: s.importance)
            self.summaries.pop(0)

        print(f"[中期记忆] 添加摘要: {content[:50]}... (重要性: {importance})")
        return summary.summary_id

    def get_recent_summaries(self, n: int = 5) -> List[Summary]:
        """获取最近的摘要"""
        return self.summaries[-n:]

    def get_important_summaries(self, threshold: float = 0.7) -> List[Summary]:
        """获取重要的摘要"""
        return [s for s in self.summaries if s.importance >= threshold]

    def search(self, query: str) -> List[Summary]:
        """搜索摘要（关键词匹配）"""
        query_lower = query.lower()
        return [
            s for s in self.summaries
            if query_lower in s.content.lower() or
            any(query_lower in tag.lower() for tag in s.tags)
        ]

    def clear(self):
        """清空记忆"""
        self.summaries = []
        self.summary_counter = 0


# ===== 长期记忆 =====

class LongTermMemory:
    """长期记忆（语义记忆）"""

    def __init__(self, storage_path: str = "./long_term_memory.json"):
        self.storage_path = Path(storage_path)
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
            importance=importance
        )

        self.memories[memory_id] = memory
        self._save()

        print(f"[长期记忆] 添加记忆: {content[:50]}... (ID: {memory_id})")
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
        data = {
            "counter": self.memory_counter,
            "memories": [m.to_dict() for m in self.memories.values()]
        }

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load(self):
        """从磁盘加载"""
        if not self.storage_path.exists():
            return

        with open(self.storage_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.memory_counter = data.get("counter", 0)

        for item_data in data.get("memories", []):
            memory = MemoryItem(
                memory_id=item_data["memory_id"],
                content=item_data["content"],
                embedding=item_data.get("embedding"),
                metadata=item_data.get("metadata", {}),
                timestamp=datetime.fromisoformat(item_data["timestamp"]),
                access_count=item_data.get("access_count", 0),
                importance=item_data.get("importance", 0.5)
            )
            self.memories[memory_id] = memory

    def clear(self):
        """清空记忆"""
        self.memories = {}
        self.memory_counter = 0
        self._save()


# ===== 分层记忆系统 =====

class HierarchicalMemory:
    """分层记忆系统"""

    def __init__(self,
                 short_term_size: int = 20,
                 medium_term_size: int = 100,
                 long_term_path: str = "./long_term_memory.json"):
        self.short_term = ShortTermMemory(max_messages=short_term_size)
        self.medium_term = MediumTermMemory(max_summaries=medium_term_size)
        self.long_term = LongTermMemory(storage_path=long_term_path)

    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """添加消息到短期记忆"""
        self.short_term.add_message(role, content, metadata)

        # 如果短期记忆满了，创建摘要
        if len(self.short_term) >= self.short_term.max_messages:
            self._create_summary()

    def _create_summary(self):
        """创建摘要并转移到中期记忆"""
        messages = self.short_term.get_recent_messages()

        # 简化的摘要生成
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
        summaries = self.medium_term.summaries
        summary = next((s for s in summaries if s.summary_id == summary_id), None)

        if summary:
            self.long_term.add_memory(
                content=summary.content,
                metadata=metadata or {"type": "archived_summary"},
                importance=summary.importance
            )
            print(f"[归档] 摘要 {summary_id} 已归档到长期记忆")

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
        return {
            "medium_term": self.medium_term.search(query),
            "long_term": self.long_term.search_by_keyword(query)
        }

    def print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("记忆系统统计")
        print("=" * 60)
        print(f"短期记忆: {len(self.short_term)}/{self.short_term.max_messages} 条消息")
        print(f"中期记忆: {len(self.medium_term.summaries)}/{self.medium_term.max_summaries} 条摘要")
        print(f"长期记忆: {len(self.long_term.memories)} 条记忆")
        print("=" * 60)


# ===== 使用示例 =====

def example_basic_usage():
    """示例 1：基本使用"""
    print("=" * 70)
    print("示例 1：基本使用")
    print("=" * 70)

    memory = HierarchicalMemory()

    # 添加对话
    print("\n[添加对话]")
    memory.add_message("user", "你好，我叫张三")
    memory.add_message("assistant", "你好张三，很高兴认识你")
    memory.add_message("user", "我喜欢编程，特别是 Python")
    memory.add_message("assistant", "Python 是一门很棒的语言")

    # 获取上下文
    print("\n[获取上下文]")
    context = memory.get_context()
    print(context)

    # 打印统计
    memory.print_stats()


def example_memory_flow():
    """示例 2：记忆流转"""
    print("\n" + "=" * 70)
    print("示例 2：记忆流转")
    print("=" * 70)

    memory = HierarchicalMemory(short_term_size=5)  # 设置较小容量以演示流转

    # 填满短期记忆
    print("\n[填充短期记忆]")
    for i in range(6):
        memory.add_message("user", f"消息 {i}")

    # 短期记忆满，自动创建摘要
    print("\n[短期记忆已满，创建摘要]")

    # 查看中期记忆
    print("\n[中期记忆摘要]")
    for summary in memory.medium_term.get_recent_summaries():
        print(f"- {summary.content}")

    # 归档到长期记忆
    print("\n[归档到长期记忆]")
    if memory.medium_term.summaries:
        memory.archive_to_long_term(memory.medium_term.summaries[0].summary_id)

    memory.print_stats()


def example_search():
    """示例 3：搜索记忆"""
    print("\n" + "=" * 70)
    print("示例 3：搜索记忆")
    print("=" * 70)

    memory = HierarchicalMemory()

    # 添加一些长期记忆
    print("\n[添加长期记忆]")
    memory.long_term.add_memory(
        "用户张三喜欢 Python 编程",
        metadata={"type": "user_preference", "user": "张三"}
    )
    memory.long_term.add_memory(
        "用户张三正在学习机器学习",
        metadata={"type": "user_interest", "user": "张三"}
    )
    memory.long_term.add_memory(
        "用户李四喜欢 Java 编程",
        metadata={"type": "user_preference", "user": "李四"}
    )

    # 搜索
    print("\n[搜索 'Python']")
    results = memory.search("Python")
    print(f"中期记忆: {len(results['medium_term'])} 条")
    print(f"长期记忆: {len(results['long_term'])} 条")
    for item in results['long_term']:
        print(f"  - {item.content}")

    # 按元数据搜索
    print("\n[按元数据搜索 user=张三]")
    results = memory.long_term.search_by_metadata("user", "张三")
    for item in results:
        print(f"  - {item.content}")


def example_conversation_session():
    """示例 4：完整对话会话"""
    print("\n" + "=" * 70)
    print("示例 4：完整对话会话")
    print("=" * 70)

    memory = HierarchicalMemory()

    # 模拟对话
    conversations = [
        ("user", "你好"),
        ("assistant", "你好！有什么可以帮助你的？"),
        ("user", "我想了解 LangGraph"),
        ("assistant", "LangGraph 是一个用于构建有向图的库"),
        ("user", "它有什么特点？"),
        ("assistant", "它支持状态管理、循环和条件边"),
    ]

    print("\n[对话开始]")
    for role, content in conversations:
        print(f"{role}: {content}")
        memory.add_message(role, content)

    print("\n[对话结束，获取上下文]")
    context = memory.get_context()
    print(context)

    memory.print_stats()


if __name__ == "__main__":
    example_basic_usage()
    example_memory_flow()
    example_search()
    example_conversation_session()

    print("\n" + "=" * 70)
    print("所有示例执行完成！")
    print("=" * 70)
