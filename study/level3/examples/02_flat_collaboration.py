"""
示例 2: 扁平化协作 (Flat Collaboration)

本示例展示如何实现一个扁平化的多智能体系统，
Agent 之间平等协作，通过直接通信完成任务。

架构：
    Agent1 ←→ Agent2 ←→ Agent3
      ↑         ↓         ↑
      ←─────────←─────────
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import threading
import time
from collections import deque


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class Message:
    """消息类"""
    id: str
    from_agent: str
    to_agent: str
    content: Dict[str, Any]
    timestamp: float
    reply_to: Optional[str] = None

    def __repr__(self):
        return f"Message({self.from_agent} → {self.to_agent}: {self.content})"


class MessageQueue:
    """消息队列"""

    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()

    def enqueue(self, message: Message):
        """入队"""
        with self.lock:
            self.queue.append(message)

    def dequeue(self) -> Optional[Message]:
        """出队"""
        with self.lock:
            if self.queue:
                return self.queue.popleft()
            return None

    def is_empty(self) -> bool:
        """检查是否为空"""
        with self.lock:
            return len(self.queue) == 0

    def size(self) -> int:
        """队列大小"""
        with self.lock:
            return len(self.queue)


# ============================================================================
# 扁平化 Agent
# ============================================================================

class FlatAgent:
    """扁平化 Agent - 平等的、可直接通信的 Agent"""

    def __init__(self, name: str, role: str, skills: List[str]):
        self.name = name
        self.role = role
        self.skills = skills

        # 消息系统
        self.message_queue = MessageQueue()
        self.known_agents: Dict[str, 'FlatAgent'] = {}

        # 状态
        self.is_running = False
        self.thread: Optional[threading.Thread] = None

        # 统计
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "tasks_completed": 0
        }

    def register_agent(self, agent: 'FlatAgent'):
        """注册其他 Agent"""
        self.known_agents[agent.name] = agent
        print(f"[{self.name}] 认识了 {agent.name}")

    def send_message(self, to_agent: str, content: Dict[str, Any], reply_to: str = None):
        """发送消息给其他 Agent"""
        if to_agent not in self.known_agents:
            print(f"[{self.name}] 错误: 不认识 {to_agent}")
            return False

        target = self.known_agents[to_agent]

        message = Message(
            id=f"{self.name}_{to_agent}_{time.time()}",
            from_agent=self.name,
            to_agent=to_agent,
            content=content,
            timestamp=time.time(),
            reply_to=reply_to
        )

        target.receive_message(message)
        self.stats["messages_sent"] += 1
        print(f"[{self.name}] → {to_agent}: {content.get('type', 'message')}")
        return True

    def receive_message(self, message: Message):
        """接收消息"""
        self.message_queue.enqueue(message)
        self.stats["messages_received"] += 1

    def process_messages(self):
        """处理消息队列"""
        while not self.message_queue.is_empty():
            message = self.message_queue.dequeue()
            if message:
                self._handle_message(message)

    def _handle_message(self, message: Message):
        """处理单个消息"""
        msg_type = message.content.get("type", "unknown")

        if msg_type == "request":
            self._handle_request(message)
        elif msg_type == "response":
            self._handle_response(message)
        elif msg_type == "notification":
            self._handle_notification(message)
        else:
            print(f"[{self.name}] 未知消息类型: {msg_type}")

    def _handle_request(self, message: Message):
        """处理请求"""
        task = message.content.get("task", "")

        # 执行任务
        result = self._execute_task(task)

        # 回复结果
        self.send_message(
            message.from_agent,
            {
                "type": "response",
                "result": result,
                "original_task": task
            },
            reply_to=message.id
        )

    def _handle_response(self, message: Message):
        """处理响应"""
        result = message.content.get("result")
        print(f"[{self.name}] 收到 {message.from_agent} 的响应: {result}")

    def _handle_notification(self, message: Message):
        """处理通知"""
        notification = message.content.get("message", "")
        print(f"[{self.name}] 收到通知: {notification}")

    def _execute_task(self, task: str) -> str:
        """执行任务"""
        print(f"[{self.name}] 执行任务: {task}")

        # 根据角色执行不同的工作
        if "研究" in self.role:
            result = self._do_research(task)
        elif "分析" in self.role:
            result = self._do_analysis(task)
        elif "写作" in self.role:
            result = self._do_writing(task)
        else:
            result = self._do_general(task)

        self.stats["tasks_completed"] += 1
        return result

    def _do_research(self, topic: str) -> str:
        """研究任务"""
        return f"[研究] 关于 {topic} 的发现: 这是一个重要的研究领域"

    def _do_analysis(self, data: str) -> str:
        """分析任务"""
        return f"[分析] 对 {data} 的分析: 数据呈上升趋势"

    def _do_writing(self, content: str) -> str:
        """写作任务"""
        return f"[写作] 基于 {content} 的文章: 内容丰富，结构清晰"

    def _do_general(self, task: str) -> str:
        """通用任务"""
        return f"[通用] 完成 {task}"

    def start(self):
        """启动 Agent"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            print(f"[{self.name}] 已启动")

    def stop(self):
        """停止 Agent"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        print(f"[{self.name}] 已停止")

    def _run_loop(self):
        """运行循环"""
        while self.is_running:
            self.process_messages()
            time.sleep(0.1)

    def get_statistics(self) -> dict:
        """获取统计信息"""
        return self.stats.copy()


# ============================================================================
# 协作机制
# ============================================================================

class CollaborationProtocol:
    """协作协议"""

    def __init__(self):
        self.proposals: Dict[str, List[Dict]] = {}  # task -> proposals
        self.votes: Dict[str, Dict[str, str]] = {}  # task -> {agent: vote}

    def propose(self, agent: str, task: str, proposal: Dict):
        """提出方案"""
        if task not in self.proposals:
            self.proposals[task] = []
        self.proposals[task].append({
            "agent": agent,
            "proposal": proposal,
            "timestamp": time.time()
        })
        print(f"[协作] {agent} 提出方案: {proposal}")

    def vote(self, agent: str, task: str, vote: str):
        """投票"""
        if task not in self.votes:
            self.votes[task] = {}
        self.votes[task][agent] = vote
        print(f"[协作] {agent} 投票: {vote}")

    def get_consensus(self, task: str) -> Optional[str]:
        """获取共识"""
        if task not in self.votes:
            return None

        votes = self.votes[task]
        if not votes:
            return None

        # 统计投票
        vote_counts = {}
        for vote in votes.values():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1

        # 找出多数票
        max_votes = max(vote_counts.values())
        for vote, count in vote_counts.items():
            if count == max_votes:
                return vote

        return None


# ============================================================================
# 系统组装
# ============================================================================

def create_flat_system() -> List[FlatAgent]:
    """创建扁平化多智能体系统"""

    # 创建 Agents
    researcher = FlatAgent(
        name="研究员",
        role="研究员",
        skills=["研究", "调查", "数据收集"]
    )

    analyst = FlatAgent(
        name="分析师",
        role="分析师",
        skills=["分析", "评估", "建模"]
    )

    writer = FlatAgent(
        name="作家",
        role="作家",
        skills=["写作", "编辑", "发布"]
    )

    # 互相注册（建立连接）
    agents = [researcher, analyst, writer]

    for agent in agents:
        for other in agents:
            if agent != other:
                agent.register_agent(other)

    return agents


# ============================================================================
# 协作场景
# ============================================================================

def scenario_1_direct_collaboration():
    """场景 1: 直接协作"""
    print("\n" + "="*60)
    print("场景 1: 直接协作")
    print("="*60)

    agents = create_flat_system()

    # 启动所有 Agents
    for agent in agents:
        agent.start()

    # 研究员请求分析师协作
    researcher = agents[0]
    analyst = agents[1]

    print("\n[场景] 研究员请求分析师分析数据")
    researcher.send_message(
        analyst.name,
        {
            "type": "request",
            "task": "分析 AI 技术趋势"
        }
    )

    # 等待处理
    time.sleep(1)

    # 停止所有 Agents
    for agent in agents:
        agent.stop()

    # 显示统计
    print("\n[统计]")
    for agent in agents:
        stats = agent.get_statistics()
        print(f"{agent.name}: 发送 {stats['messages_sent']}, "
              f"接收 {stats['messages_received']}, "
              f"完成 {stats['tasks_completed']}")


def scenario_2_peer_to_peer_network():
    """场景 2: P2P 网络"""
    print("\n" + "="*60)
    print("场景 2: P2P 网络协作")
    print("="*60)

    agents = create_flat_system()

    # 启动所有 Agents
    for agent in agents:
        agent.start()

    researcher, analyst, writer = agents

    print("\n[场景] 三方协作完成项目")

    # 研究员发起项目
    print("\n[步骤 1] 研究员发起研究任务")
    researcher.send_message(
        analyst.name,
        {
            "type": "request",
            "task": "准备 AI 市场分析"
        }
    )

    time.sleep(0.5)

    # 分析师完成后，通知作家
    print("\n[步骤 2] 分析师请求作家撰写报告")
    analyst.send_message(
        writer.name,
        {
            "type": "request",
            "task": "基于市场分析撰写报告"
        }
    )

    time.sleep(0.5)

    # 作家通知所有人完成
    print("\n[步骤 3] 作家通知所有人项目完成")
    for agent in agents:
        if agent.name != writer.name:
            writer.send_message(
                agent.name,
                {
                    "type": "notification",
                    "message": "项目已完成！"
                }
            )

    time.sleep(0.5)

    # 停止所有 Agents
    for agent in agents:
        agent.stop()

    # 显示统计
    print("\n[统计]")
    for agent in agents:
        stats = agent.get_statistics()
        print(f"{agent.name}: 发送 {stats['messages_sent']}, "
              f"接收 {stats['messages_received']}, "
              f"完成 {stats['tasks_completed']}")


def scenario_3_consensus_building():
    """场景 3: 达成共识"""
    print("\n" + "="*60)
    print("场景 3: 共识构建")
    print("="*60)

    agents = create_flat_system()
    protocol = CollaborationProtocol()

    # 启动所有 Agents
    for agent in agents:
        agent.start()

    researcher, analyst, writer = agents

    task = "选择项目技术栈"

    print(f"\n[场景] 对 '{task}' 达成共识")

    # 各自提出方案
    print("\n[步骤 1] 各自提出方案")
    protocol.propose("研究员", task, {"tech": "Python", "reason": "易用性强"})
    protocol.propose("分析师", task, {"tech": "JavaScript", "reason": "生态丰富"})
    protocol.propose("作家", task, {"tech": "Python", "reason": "文档完善"})

    # 投票
    print("\n[步骤 2] 投票")
    protocol.vote("研究员", task, "Python")
    protocol.vote("分析师", task, "JavaScript")
    protocol.vote("作家", task, "Python")

    # 获取共识
    print("\n[步骤 3] 获取共识")
    consensus = protocol.get_consensus(task)
    print(f"共识结果: {consensus}")

    # 停止所有 Agents
    for agent in agents:
        agent.stop()


# ============================================================================
# 测试代码
# ============================================================================

def test_agent_communication():
    """测试 Agent 通信"""
    print("\n=== 测试 Agent 通信 ===")

    agent1 = FlatAgent("Agent1", "测试者", ["测试"])
    agent2 = FlatAgent("Agent2", "响应者", ["响应"])

    agent1.register_agent(agent2)
    agent2.register_agent(agent1)

    agent1.start()
    agent2.start()

    # 发送消息
    agent1.send_message("Agent2", {"type": "request", "task": "测试任务"})

    time.sleep(0.5)

    agent1.stop()
    agent2.stop()

    stats1 = agent1.get_statistics()
    stats2 = agent2.get_statistics()

    assert stats1["messages_sent"] == 1
    assert stats2["messages_received"] == 1
    assert stats2["tasks_completed"] == 1

    print("✓ 通信测试通过")


def test_collaboration():
    """测试协作"""
    print("\n=== 测试协作 ===")

    agents = create_flat_system()

    for agent in agents:
        agent.start()

    # 研究员发送请求
    agents[0].send_message(
        agents[1].name,
        {"type": "request", "task": "分析数据"}
    )

    time.sleep(0.5)

    for agent in agents:
        agent.stop()

    # 验证消息交换
    total_sent = sum(agent.get_statistics()["messages_sent"] for agent in agents)
    assert total_sent > 0

    print("✓ 协作测试通过")


def test_consensus():
    """测试共识"""
    print("\n=== 测试共识 ===")

    protocol = CollaborationProtocol()

    # 提出方案
    protocol.propose("Agent1", "task1", {"option": "A"})
    protocol.propose("Agent2", "task1", {"option": "B"})

    # 投票
    protocol.vote("Agent1", "task1", "A")
    protocol.vote("Agent2", "task1", "A")
    protocol.vote("Agent3", "task1", "B")

    # 获取共识
    consensus = protocol.get_consensus("task1")
    assert consensus == "A"  # A 有 2 票

    print("✓ 共识测试通过")


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序"""
    print("="*60)
    print("扁平化多智能体协作系统演示")
    print("="*60)

    # 运行场景
    scenario_1_direct_collaboration()
    scenario_2_peer_to_peer_network()
    scenario_3_consensus_building()


if __name__ == "__main__":
    main()

    # 运行测试
    test_agent_communication()
    test_collaboration()
    test_consensus()

    print("\n" + "="*60)
    print("所有测试通过！")
    print("="*60)
