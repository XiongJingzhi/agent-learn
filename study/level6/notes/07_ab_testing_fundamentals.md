# 07. A/B 测试基础

> **主题**: Agent 系统的 A/B 测试原理与实践
> **时间**: 60 分钟
> **难度**: ⭐⭐⭐ 中高级

---

## 🎯 学习目标

通过本节学习，你将能够：

1. ✅ 理解 A/B 测试的核心原理
2. ✅ 掌握 A/B 测试的完整流程
3. ✅ 能够设计有效的 A/B 测试实验
4. ✅ 了解统计显著性的概念

---

## 📚 什么是 A/B 测试？

### 定义

**A/B 测试** 是一种对比实验方法，将用户随机分成两组（或多组），分别展示不同版本的产品或功能，通过数据分析确定哪个版本效果更好。

### 基本原理

```
┌─────────────────────────────────────────────────────────────┐
│                    A/B 测试流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. 用户到达                                                 │
│     └─ 访问网站 / 打开 App                                   │
│          ↓                                                  │
│  2. 随机分组                                                 │
│     ├─ A 组（对照组）: 50%                                   │
│     └─ B 组（实验组）: 50%                                   │
│          ↓                                                  │
│  3. 展示不同版本                                             │
│     ├─ A 组: 看到版本 A（原版）                              │
│     └─ B 组: 看到版本 B（新版）                              │
│          ↓                                                  │
│  4. 收集数据                                                 │
│     ├─ 行为数据（点击、转化等）                              │
│     ├─ 性能数据（响应时间等）                                │
│     └─ 质量数据（满意度等）                                  │
│          ↓                                                  │
│  5. 统计分析                                                 │
│     ├─ 计算指标                                              │
│     ├─ 统计检验                                              │
│     └─ 判断显著性                                            │
│          ↓                                                  │
│  6. 做出决策                                                 │
│     ├─ B 更好 → 全面发布                                     │
│     ├─ A 更好 → 保持原版                                     │
│     └─ 无差异 → 继续测试或调整                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 A/B 测试在 Agent 系统中的应用

### 应用场景

#### 1. Prompt 优化

**场景**: 测试不同的 Prompt 模板

```python
# 版本 A: 简洁 Prompt
prompt_a = """
你是帮助用户的助手。请回答用户的问题。
问题: {question}
"""

# 版本 B: 详细 Prompt
prompt_b = """
你是一个专业的 AI 助手，擅长回答各种问题。
请提供准确、详细、友好的回答。
如果不确定，请说明。
问题: {question}
"""

# A/B 测试框架
def ab_test_prompt(user_id, question):
    group = assign_to_group(user_id)
    if group == "A":
        response = agent.run(prompt_a.format(question=question))
    else:
        response = agent.run(prompt_b.format(question=question))

    # 记录结果
    log_metrics(user_id, group, response)
    return response
```

#### 2. 工具选择策略

**场景**: 测试不同的工具路由策略

```python
# 版本 A: 基于规则的路由
def route_tools_a(query):
    if "search" in query:
        return search_tool
    elif "calculate" in query:
        return calculator_tool
    else:
        return general_tool

# 版本 B: 基于语义的路由
def route_tools_b(query):
    similarity = semantic_similarity(query, tool_descriptions)
    return max(similarity, key=similarity.get)

# A/B 测试
def ab_test_routing(user_id, query):
    group = assign_to_group(user_id)
    if group == "A":
        tool = route_tools_a(query)
    else:
        tool = route_tools_b(query)

    result = tool.run(query)
    log_metrics(user_id, group, result)
    return result
```

#### 3. 模型参数调优

**场景**: 测试不同的温度参数

```python
# 版本 A: temperature = 0.0
llm_a = ChatOpenAI(temperature=0.0)

# 版本 B: temperature = 0.7
llm_b = ChatOpenAI(temperature=0.7)

# A/B 测试
def ab_test_temperature(user_id, question):
    group = assign_to_group(user_id)
    if group == "A":
        response = llm_a.invoke(question)
    else:
        response = llm_b.invoke(question)

    # 评估质量
    quality = evaluate_quality(response)
    log_metrics(user_id, group, quality)
    return response
```

---

## 📊 关键指标设计

### 指标类型

#### 1. 性能指标

**响应时间**
```python
# 测量响应时间
import time

def measure_response_time(agent, query):
    start = time.time()
    response = agent.run(query)
    end = time.time()

    latency = end - start
    log_metric("latency", latency)
    return latency
```

**吞吐量**
```python
# 测量每秒请求数
throughput = total_requests / total_time
log_metric("throughput", throughput)
```

#### 2. 质量指标

**准确率**
```python
# 准确率 = 正确回答数 / 总回答数
accuracy = correct_answers / total_answers
log_metric("accuracy", accuracy)
```

**满意度**
```python
# 用户评分 (1-5)
satisfaction = average(user_ratings)
log_metric("satisfaction", satisfaction)
```

**转化率**
```python
# 转化率 = 完成目标的用户数 / 总用户数
conversion = conversions / total_users
log_metric("conversion", conversion)
```

#### 3. 业务指标

**用户参与度**
```python
# 平均会话长度
avg_session_length = total_interaction_time / total_sessions

# 重复使用率
retention_rate = returning_users / total_users
```

**成本指标**
```python
# 平均每次交互成本
avg_cost_per_interaction = total_cost / total_interactions

# Token 使用量
token_usage = total_tokens / total_requests
```

---

## 🔢 统计显著性

### 为什么需要统计检验？

**问题**: A 组的转化率 5%，B 组的转化率 5.5%，B 真的比 A 好吗？

**答案**: 不一定，可能是随机波动

**解决**: 使用统计检验判断差异是否显著

### 常用检验方法

#### 1. 比率检验（Chi-square test）

**适用**: 比较两个转化率

```python
from scipy.stats import chi2_contingency

# 示例：测试转化率差异
# A 组: 100 次访问，5 次转化
# B 组: 100 次访问，8 次转化

contingency_table = [
    [5, 95],   # A 组: 转化, 未转化
    [8, 92]    # B 组: 转化, 未转化
]

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"P-value: {p_value}")

if p_value < 0.05:
    print("差异显著！")
else:
    print("差异不显著")
```

#### 2. 均值检验（t-test）

**适用**: 比较两个平均值

```python
from scipy.stats import ttest_ind

# 示例：测试响应时间差异
response_time_a = [1.2, 1.5, 1.3, 1.4, 1.6]  # A 组响应时间
response_time_b = [1.1, 1.3, 1.2, 1.2, 1.4]  # B 组响应时间

t_stat, p_value = ttest_ind(response_time_a, response_time_b)

print(f"P-value: {p_value}")

if p_value < 0.05:
    print("差异显著！")
else:
    print("差异不显著")
```

### P-value 解释

**P-value**: 在假设原假设（没有差异）为真的情况下，观察到当前数据的概率

**常见阈值**:
- p < 0.01: 高度显著
- p < 0.05: 显著
- p >= 0.05: 不显著

**注意**: p < 0.05 不代表 B 一定比 A 好，只是说明差异不太可能是随机产生的

---

## 📏 最小样本量计算

### 为什么需要计算样本量？

**样本太小**: 统计效力不足，无法检测到真实差异
**样本太大**: 浪费资源，延长测试时间

### 计算公式

```python
from statsmodels.stats.power import zt_ind_solve_power

# 计算最小样本量
# 参数:
# - effect_size: 效应量（标准化差异）
# - alpha: 显著性水平（通常 0.05）
# - power: 统计效力（通常 0.8）

def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    baseline_rate: 基线转化率（如 0.05 = 5%）
    mde: 最小可检测效应（如 0.01 = 1%）
    """
    # 计算效应量
    effect_size = mde / sqrt(baseline_rate * (1 - baseline_rate))

    # 计算样本量
    sample_size = zt_ind_solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=1  # 两组相等
    )

    return int(sample_size)

# 示例
sample_size = calculate_sample_size(
    baseline_rate=0.05,  # 基线 5%
    mde=0.01  # 想检测 1% 的提升
)

print(f"每组需要 {sample_size} 个样本")
```

---

## 🎯 A/B 测试完整流程

### 步骤 1: 假设定义

**好的假设**:
```
如果使用更详细的 Prompt 模板（版本 B），
那么用户的满意度会提升 10%，
因为回答会更准确、更详细。
```

**假设要素**:
- **变量**: 明确改变什么
- **预期**: 量化预期效果
- **原因**: 说明为什么会有这个效果

### 步骤 2: 指标选择

**主要指标**:
- 直接反映目标（如：转化率、满意度）

**次要指标**:
- 辅助判断（如：响应时间、错误率）

**反向指标**:
- 确保没有恶化（如：跳出率、投诉率）

### 步骤 3: 实验设计

**随机化**:
```python
import hashlib

def assign_to_group(user_id):
    # 使用哈希确保一致性
    hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    return "A" if hash_value % 2 == 0 else "B"
```

**分层**:
```python
# 按用户类型分层
def assign_to_group_stratified(user_id, user_type):
    if user_type == "premium":
        # 高级用户单独分配
        return assign_premium_user(user_id)
    else:
        # 普通用户分配
        return assign_regular_user(user_id)
```

### 步骤 4: 数据收集

```python
class ABTestTracker:
    def __init__(self, test_name):
        self.test_name = test_name
        self.data = []

    def track(self, user_id, group, metrics):
        """记录测试数据"""
        self.data.append({
            "user_id": user_id,
            "group": group,
            "timestamp": time.time(),
            **metrics
        })

    def export(self):
        """导出数据"""
        return pd.DataFrame(self.data)

# 使用示例
tracker = ABTestTracker("prompt_optimization")
tracker.track(user_id="123", group="A", metrics={
    "response_time": 1.5,
    "satisfaction": 4.5,
    "conversion": True
})
```

### 步骤 5: 统计分析

```python
def analyze_ab_test(tracker):
    """分析 A/B 测试结果"""
    df = tracker.export()

    # 分组统计
    group_a = df[df["group"] == "A"]
    group_b = df[df["group"] == "B"]

    # 计算指标
    metrics = {}
    for metric in ["response_time", "satisfaction", "conversion"]:
        mean_a = group_a[metric].mean()
        mean_b = group_b[metric].mean()

        # 统计检验
        if metric == "conversion":
            # 比率检验
            _, p_value = chi2_test(group_a, group_b)
        else:
            # 均值检验
            _, p_value = ttest_ind(group_a[metric], group_b[metric])

        metrics[metric] = {
            "mean_a": mean_a,
            "mean_b": mean_b,
            "lift": (mean_b - mean_a) / mean_a,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    return metrics
```

### 步骤 6: 决策

```python
def make_decision(analysis_results):
    """根据分析结果做出决策"""
    significant_improvements = []
    significant_regressions = []

    for metric, result in analysis_results.items():
        if result["significant"]:
            if result["mean_b"] > result["mean_a"]:
                significant_improvements.append(metric)
            else:
                significant_regressions.append(metric)

    if significant_improvements and not significant_regressions:
        return "ADOPT_B"
    elif significant_regressions:
        return "KEEP_A"
    else:
        return "INCONCLUSIVE"
```

---

## 💡 费曼解释

### 用简单的语言解释 A/B 测试

**A/B 测试就像科学实验**：

想象你想知道哪种肥料能让植物长得更好：

1. **准备两组植物**（随机分组）
   - A 组：使用原肥料
   - B 组：使用新肥料

2. **控制其他条件**
   - 同样的阳光
   - 同样的水
   - 同样的土壤

3. **测量结果**
   - 一个月后，测量植物高度
   - A 组平均 30cm
   - B 组平均 35cm

4. **统计分析**
   - 这个差异是偶然的吗？
   - 还是肥料真的有效？

5. **做出决策**
   - 如果 B 组显著更好 → 用新肥料
   - 如果没有差异 → 继续用原肥料
   - 如果 B 组更差 → 不用新肥料

**A/B 测试就是用科学的方法，而不是凭感觉做决策**。

---

## ✅ 最小验证

### 验证 1: 理解 A/B 测试流程

**任务**: 描述 A/B 测试的 6 个步骤

**时间**: 5 分钟

**产出**:
```
1. 假设定义
2. 指标设计
3. 用户分组
4. 数据收集
5. 统计分析
6. 做出决策
```

---

### 验证 2: 计算样本量

**任务**: 计算需要的样本量

**条件**:
- 基线转化率: 5%
- 最小可检测效应: 1%
- 显著性水平: 0.05
- 统计效力: 0.8

**时间**: 10 分钟

**产出**:
```python
sample_size = calculate_sample_size(
    baseline_rate=0.05,
    mde=0.01
)
# 结果: 约 15,000 个样本/组
```

---

### 验证 3: 分析实验结果

**任务**: 判断是否显著

**数据**:
- A 组: 1000 次访问，50 次转化
- B 组: 1000 次访问，70 次转化

**时间**: 5 分钟

**产出**:
```python
# Chi-square 检验
# p < 0.05 → 显著
# 结论: B 组显著更好
```

---

## ⚠️ 常见误区

### 误区 1: 提前停止测试

**表现**: 看到 B 组领先就立即停止

**问题**: 可能是随机波动，样本不够

**解决**: 预先计算样本量，达到目标再分析

---

### 误区 2: 多重检验问题

**表现**: 同时测试多个指标，只要有一个显著就宣称成功

**问题**: 增加假阳性概率

**解决**: 使用 Bonferroni 校正

```python
# 调整显著性水平
alpha_corrected = 0.05 / num_metrics
```

---

### 误区 3: 忽视新奇效应

**表现**: B 组效果好只是因为用户好奇

**问题**: 效果是暂时的

**解决**: 进行长期测试，观察趋势

---

## 🚀 下一步

- 阅读笔记 08：指标设计
- 实践示例 05：A/B 测试框架
- 完成练习题：A/B 测试练习

---

## 📚 延伸阅读

- [Trustworthy Online Controlled Experiments (Ron Kohavi)](https://www.amazon.com/Trustworthy-Online-Controlled-Experiments-Practical/dp/1108724264)
- [A/B Testing Best Practices](https://www.optimizely.com/optimization-glossary/ab-testing/)
- [Statistics for A/B Testing](https://www.statsitics.org/ab-testing/)

---

**掌握 A/B 测试，用数据驱动决策！** 🚀
