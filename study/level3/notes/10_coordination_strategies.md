# 10. 协作策略设计

> **主题**: 设计有效的多智能体协作策略
> **时间**: 60 分钟
> **难度**: ⭐⭐⭐⭐

---

## 🎯 学习目标

1. ✅ 理解协作策略的设计原则
2. ✅ 掌握常见的协作模式
3. ✅ 能够设计激励机制
4. ✅ 能够实现协作协议

---

## 📚 核心概念

### 什么是协作策略？

**定义**: 一套规则和机制，用于协调多个 Agent 的行为，以实现共同目标。

**核心问题**:
- 如何分配任务？
- 如何共享信息？
- 如何解决冲突？
- 如何激励协作？

---

## 🎯 协作模式

### 模式 1: 合同网 (Contract Net)

**原理**: Manager 发布任务，Workers 竞标，Manager 选择最合适的 Worker。

```python
class ContractNetProtocol:
    """合同网协议"""

    def __init__(self):
        self.manager = None
        self.workers = []
        self.contracts = {}

    def announce_task(self, task: Task):
        """宣布任务（招标）"""
        print(f"\n[Manager] 宣布任务: {task.description}")

        bids = []
        for worker in self.workers:
            # Worker 评估自己的能力
            bid = worker.evaluate_task(task)
            if bid:
                bids.append(bid)
                print(f"  [Worker] {worker.name} 出价: {bid}")

        # Manager 选择最优出价
        if bids:
            best_bid = min(bids, key=lambda b: b.cost)
            self.award_contract(task, best_bid)

    def award_contract(self, task: Task, bid: 'Bid'):
        """授予合同"""
        print(f"\n[Manager] 授予合同给 {bid.worker.name}")
        contract = Contract(task, bid.worker, bid.cost, bid.estimated_time)
        self.contracts[task.id] = contract

        # Worker 执行任务
        result = bid.worker.execute(task)

        # 完成合同
        contract.complete(result)
        return result

class Worker:
    def evaluate_task(self, task: Task) -> Optional['Bid']:
        """评估任务并出价"""
        # 计算能力匹配度
        capability = self._calculate_capability(task)

        if capability < 0.5:
            return None  # 不投标

        # 计算成本
        cost = self._calculate_cost(task)

        # 估算时间
        estimated_time = self._estimate_time(task)

        return Bid(self, cost, estimated_time, capability)
```

**适用场景**:
- 任务可以明确描述
- Workers 有不同的能力
- 需要优化资源分配

---

### 模式 2: 黑板 (Blackboard)

**原理**: 共享的黑板空间，Agents 随时可以读写。

```python
class Blackboard:
    """黑板系统"""

    def __init__(self):
        self.data = {}
        self.sources = {}  # track who wrote what
        self.listeners = defaultdict(list)  # topic -> [callbacks]

    def write(self, agent: str, key: str, value: Any):
        """写入黑板"""
        self.data[key] = value
        self.sources[key] = agent

        print(f"[{agent}] 写入 {key}: {value}")

        # 通知监听者
        self._notify(key, value)

    def read(self, key: str) -> Any:
        """读取黑板"""
        return self.data.get(key)

    def subscribe(self, agent: str, pattern: str, callback: callable):
        """订阅黑板变化"""
        self.listeners[pattern].append((agent, callback))

    def _notify(self, key: str, value: Any):
        """通知订阅者"""
        import re
        for pattern, listeners in self.listeners.items():
            if re.match(pattern, key):
                for agent, callback in listeners:
                    callback(key, value)

# 使用示例
blackboard = Blackboard()

# Agent A 订阅所有 "research_*" 的更新
def on_research_update(key, value):
    print(f"[Agent A] 看到研究更新: {key} = {value}")

blackboard.subscribe("Agent A", "research_.*", on_research_update)

# Agent B 写入研究结果
blackboard.write("Agent B", "research_findings", "AI 很重要")
# Agent A 会自动收到通知
```

**适用场景**:
- 需要实时共享信息
- Agents 需要对变化做出反应
- 松耦合的协作

---

### 模式 3: 投票共识 (Voting Consensus)

**原理**: 通过投票达成决策。

```python
class VotingProtocol:
    """投票协议"""

    def __init__(self, agents: List[str]):
        self.agents = agents
        self.proposals = {}
        self.votes = {}

    def propose(self, agent: str, proposal_id: str, content: dict):
        """提出提案"""
        if proposal_id in self.proposals:
            return False  # 已存在

        self.proposals[proposal_id] = {
            "proposer": agent,
            "content": content,
            "timestamp": time.time()
        }
        self.votes[proposal_id] = {}

        print(f"[{agent}] 提出提案 {proposal_id}: {content}")
        return True

    def vote(self, agent: str, proposal_id: str, vote: str):
        """投票（approve/reject/abstain）"""
        if proposal_id not in self.proposals:
            return False

        self.votes[proposal_id][agent] = vote
        print(f"[{agent}] 对 {proposal_id} 投票: {vote}")

        # 检查是否所有人都投票了
        if len(self.votes[proposal_id]) == len(self.agents):
            return self._tally_votes(proposal_id)

        return None  # 还在投票中

    def _tally_votes(self, proposal_id: str) -> bool:
        """统计投票结果"""
        votes = self.votes[proposal_id]

        approve_count = sum(1 for v in votes.values() if v == "approve")
        reject_count = sum(1 for v in votes.values() if v == "reject")

        # 简单多数
        result = approve_count > reject_count

        print(f"\n[提案 {proposal_id} 投票结果]")
        print(f"  赞成: {approve_count}")
        print(f"  反对: {reject_count}")
        print(f"  结果: {'通过' if result else '否决'}")

        return result
```

**适用场景**:
- 需要集体决策
- 需要公平性
- Agents 平等

---

### 模式 4: 联邦学习 (Federated Learning)

**原理**: Agents 在本地训练，只共享模型更新。

```python
class FederatedLearning:
    """联邦学习"""

    def __init__(self):
        self.global_model = None
        self.agents = {}
        self.round = 0

    def register_agent(self, agent_id: str, local_data: List):
        """注册 Agent"""
        self.agents[agent_id] = {
            "local_data": local_data,
            "local_model": None,
            "update": None
        }

    def train_round(self):
        """训练一轮"""
        print(f"\n=== 第 {self.round} 轮训练 ===")

        # 1. 分发全局模型
        for agent_id, agent in self.agents.items():
            agent["local_model"] = copy.deepcopy(self.global_model)

        # 2. 各 Agent 本地训练
        updates = {}
        for agent_id, agent in self.agents.items():
            print(f"[{agent_id}] 本地训练...")
            update = self._local_train(agent["local_model"], agent["local_data"])
            updates[agent_id] = update

        # 3. 聚合更新（联邦平均）
        self._aggregate_updates(updates)

        self.round += 1

    def _local_train(self, model, data) -> dict:
        """本地训练"""
        # 简化：返回梯度或权重更新
        return {"gradients": self._compute_gradients(model, data)}

    def _aggregate_updates(self, updates: Dict[str, dict]):
        """聚合更新（联邦平均）"""
        n = len(updates)

        # 平均所有更新
        avg_update = {}
        for key in updates[list(updates.keys())[0]]:
            values = [update[key] for update in updates.values()]
            avg_update[key] = sum(values) / n

        # 应用到全局模型
        self._apply_update(self.global_model, avg_update)
```

**适用场景**:
- 数据隐私敏感
- 分布式数据
- 需要协作学习

---

## 💡 激励机制

### 激励设计原则

1. **贡献度量**: 如何衡量每个 Agent 的贡献？
2. **奖励分配**: 如何分配奖励？
3. **公平性**: 确保公平
4. **可持续性**: 长期维持激励

### 实例：Shapley Value

```python
def calculate_shapley_value(agents: List[str], contributions: Dict[str, float]) -> Dict[str, float]:
    """计算 Shapley Value（公平分配）"""
    from itertools import permutations

    n = len(agents)
    shapley_values = {agent: 0.0 for agent in agents}

    # 遍历所有可能的加入顺序
    for order in permutations(agents):
        # 计算边际贡献
        for i, agent in enumerate(order):
            coalition_before = set(order[:i])
            coalition_after = set(order[:i+1])

            value_before = sum(contributions.get(a, 0) for a in coalition_before)
            value_after = sum(contributions.get(a, 0) for a in coalition_after)

            marginal_contribution = value_after - value_before
            shapley_values[agent] += marginal_contribution

    # 平均化
    import math
    for agent in shapley_values:
        shapley_values[agent] /= math.factorial(n)

    return shapley_values

# 使用
agents = ["A", "B", "C"]
contributions = {
    "A": 10,
    "B": 20,
    "C": 30
}

shapley = calculate_shapley_value(agents, contributions)
print(f"Shapley Values: {shapley}")
# 输出: {'A': 10.0, 'B': 20.0, 'C': 30.0}
```

---

## 🤝 协作协议

### 协议组件

1. **协商协议** (Negotiation)
2. **承诺协议** (Commitment)
3. **协调协议** (Coordination)

### 示例：渐进式协商

```python
class NegotiationProtocol:
    """协商协议"""

    def __init__(self):
        self.negotiations = {}

    def start_negotiation(self, issue: str, participants: List[str]):
        """开始协商"""
        negotiation_id = f"{issue}_{time.time()}"
        self.negotiations[negotiation_id] = {
            "issue": issue,
            "participants": participants,
            "round": 0,
            "positions": {},  # agent -> position
            "status": "ongoing"
        }
        return negotiation_id

    def propose(self, negotiation_id: str, agent: str, position: dict):
        """提出立场"""
        if negotiation_id not in self.negotiations:
            return False

        neg = self.negotiations[negotiation_id]
        neg["positions"][agent] = position

        print(f"[{agent}] 提出立场: {position}")

        # 检查是否达成一致
        return self._check_agreement(negotiation_id)

    def _check_agreement(self, negotiation_id: str) -> bool:
        """检查是否达成一致"""
        neg = self.negotiations[negotiation_id]
        positions = list(neg["positions"].values())

        if len(positions) < len(neg["participants"]):
            return False  # 还未所有人都提出立场

        # 检查所有立场是否接近
        # 简化：检查关键项是否一致
        first_pos = positions[0]
        for pos in positions[1:]:
            for key in first_pos:
                if abs(pos[key] - first_pos[key]) > 0.1:
                    return False  # 不一致

        # 达成一致
        neg["status"] = "agreed"
        neg["agreement"] = first_pos
        print(f"\n[协商] 达成一致: {first_pos}")
        return True
```

---

## 🎓 费曼解释

### 给 5 岁孩子的解释

**协作策略就像团队合作的规则**：

1. **合同网** = 妈妈宣布任务（打扫房间），孩子竞争（我愿意做！），妈妈选择（小红最积极，小红做）

2. **黑板** = 家里的冰箱，谁都可以放东西进去，谁都可以拿东西出来

3. **投票共识** = 家里投票决定周末去哪玩，少数服从多数

4. **联邦学习** = 每个人在自己的房间学习，然后分享学习笔记，不分享课本

---

## 🔗 相关资源

- [Contract Net Protocol](https://en.wikipedia.org/wiki/Contract_net_protocol)
- [Blackboard Systems](https://en.wikipedia.org/wiki/Blackboard_system)
- [Federated Learning](https://en.wikipedia.org/wiki/Federated_learning)
- [Game Theory](https://en.wikipedia.org/wiki/Game_theory)

---

## ✅ 最小验证

### 任务

1. 实现一个简单的合同网协议（20 分钟）
2. 实现一个黑板系统（15 分钟）
3. 实现一个投票协议（15 分钟）
4. 测试协作效果（10 分钟）

### 期望输出

- [ ] 合同网协议代码
- [ ] 黑板系统代码
- [ ] 投票协议代码
- [ ] 测试结果

---

## 🚀 下一步

学习完本笔记后，继续学习：
- `notes/11_consensus_mechanisms.md` - 共识机制
- `examples/08_coordination_game.py` - 协作博弈示例

---

**记住：良好的协作策略是多智能体系统成功的关键！** 🤝
