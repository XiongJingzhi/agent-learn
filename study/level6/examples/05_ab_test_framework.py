"""
A/B 测试框架
用于 Agent 系统的 A/B 测试
"""

import hashlib
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path


class Group(Enum):
    """实验组"""
    A = "A"  # 对照组
    B = "B"  # 实验组


@dataclass
class Metrics:
    """测试指标"""
    response_time: float
    success: bool
    user_satisfaction: Optional[float] = None
    token_usage: Optional[int] = None
    error_message: Optional[str] = None


@dataclass
class ExperimentConfig:
    """实验配置"""
    name: str
    description: str
    traffic_split: float = 0.5  # A 组的流量比例（0-1）
    min_sample_size: int = 1000  # 最小样本量
    metrics: List[str] = None  # 要跟踪的指标

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = ["response_time", "success", "user_satisfaction"]


class ABTestFramework:
    """A/B 测试框架"""

    def __init__(self, config: ExperimentConfig, data_dir: str = "./ab_test_data"):
        self.config = config
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # 数据文件
        self.data_file = self.data_dir / f"{config.name}.jsonl"

        # 加载现有数据
        self.data = self._load_data()

    def assign_group(self, user_id: str) -> Group:
        """
        分配用户到实验组

        使用哈希确保同一用户始终分配到同一组
        """
        # 计算哈希值
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)

        # 根据哈希值分配组
        if (hash_value % 100) < (self.config.traffic_split * 100):
            return Group.A
        else:
            return Group.B

    def track(self, user_id: str, group: Group, metrics: Metrics):
        """记录测试数据"""
        record = {
            "user_id": user_id,
            "group": group.value,
            "timestamp": time.time(),
            "response_time": metrics.response_time,
            "success": metrics.success,
            "user_satisfaction": metrics.user_satisfaction,
            "token_usage": metrics.token_usage,
            "error_message": metrics.error_message,
        }

        # 添加到内存
        self.data.append(record)

        # 写入文件
        with open(self.data_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def _load_data(self) -> List[Dict]:
        """加载历史数据"""
        data = []
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                for line in f:
                    data.append(json.loads(line))
        return data

    def get_group_data(self, group: Group) -> List[Dict]:
        """获取指定组的数据"""
        return [d for d in self.data if d["group"] == group.value]

    def analyze(self) -> Dict:
        """
        分析测试结果

        返回统计分析结果
        """
        group_a_data = self.get_group_data(Group.A)
        group_b_data = self.get_group_data(Group.B)

        if len(group_a_data) < self.config.min_sample_size or \
           len(group_b_data) < self.config.min_sample_size:
            return {
                "status": "insufficient_data",
                "sample_size_a": len(group_a_data),
                "sample_size_b": len(group_b_data),
                "min_required": self.config.min_sample_size
            }

        # 计算指标
        analysis = {
            "status": "complete",
            "sample_size_a": len(group_a_data),
            "sample_size_b": len(group_b_data),
            "metrics": {}
        }

        # 分析每个指标
        for metric in self.config.metrics:
            if metric == "response_time":
                result = self._analyze_numerical_metric(
                    group_a_data, group_b_data, "response_time"
                )
            elif metric == "success":
                result = self._analyze_binary_metric(
                    group_a_data, group_b_data, "success"
                )
            elif metric == "user_satisfaction":
                result = self._analyze_numerical_metric(
                    group_a_data, group_b_data, "user_satisfaction"
                )
            else:
                continue

            analysis["metrics"][metric] = result

        return analysis

    def _analyze_numerical_metric(
        self,
        group_a: List[Dict],
        group_b: List[Dict],
        metric_name: str
    ) -> Dict:
        """分析数值型指标"""
        import statistics
        from scipy import stats

        # 提取数据
        values_a = [d[metric_name] for d in group_a if d[metric_name] is not None]
        values_b = [d[metric_name] for d in group_b if d[metric_name] is not None]

        # 计算统计量
        mean_a = statistics.mean(values_a)
        mean_b = statistics.mean(values_b)
        std_a = statistics.stdev(values_a) if len(values_a) > 1 else 0
        std_b = statistics.stdev(values_b) if len(values_b) > 1 else 0

        # t 检验
        t_stat, p_value = stats.ttest_ind(values_a, values_b)

        # 计算提升
        lift = (mean_b - mean_a) / mean_a if mean_a != 0 else 0

        return {
            "mean_a": mean_a,
            "mean_b": mean_b,
            "std_a": std_a,
            "std_b": std_b,
            "lift": lift,
            "lift_percentage": lift * 100,
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    def _analyze_binary_metric(
        self,
        group_a: List[Dict],
        group_b: List[Dict],
        metric_name: str
    ) -> Dict:
        """分析二元型指标（如成功率）"""
        from scipy.stats import chi2_contingency

        # 计算成功和失败的数量
        success_a = sum(1 for d in group_a if d[metric_name])
        success_b = sum(1 for d in group_b if d[metric_name])
        fail_a = len(group_a) - success_a
        fail_b = len(group_b) - success_b

        # 构建列联表
        contingency_table = [
            [success_a, fail_a],
            [success_b, fail_b]
        ]

        # Chi-square 检验
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)

        # 计算比率
        rate_a = success_a / len(group_a)
        rate_b = success_b / len(group_b)

        # 计算提升
        lift = (rate_b - rate_a) / rate_a if rate_a != 0 else 0

        return {
            "rate_a": rate_a,
            "rate_b": rate_b,
            "rate_percentage_a": rate_a * 100,
            "rate_percentage_b": rate_b * 100,
            "success_a": success_a,
            "success_b": success_b,
            "total_a": len(group_a),
            "total_b": len(group_b),
            "lift": lift,
            "lift_percentage": lift * 100,
            "chi_square": chi2,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    def generate_report(self) -> str:
        """生成测试报告"""
        analysis = self.analyze()

        if analysis["status"] == "insufficient_data":
            return f"""
            测试进行中...
            配置: {self.config.name}
            当前样本量:
              - A 组: {analysis['sample_size_a']}
              - B 组: {analysis['sample_size_b']}
            需要最小样本量: {analysis['min_required']}
            """

        report = f"""
        A/B 测试报告
        ============
        实验: {self.config.name}
        描述: {self.config.description}

        样本量:
          - A 组: {analysis['sample_size_a']}
          - B 组: {analysis['sample_size_b']}

        指标分析:
        """

        for metric_name, metric_data in analysis["metrics"].items():
            report += f"\n  {metric_name}:\n"

            if "mean_a" in metric_data:
                report += f"    A 组平均: {metric_data['mean_a']:.4f}\n"
                report += f"    B 组平均: {metric_data['mean_b']:.4f}\n"
            elif "rate_a" in metric_data:
                report += f"    A 组比率: {metric_data['rate_percentage_a']:.2f}%\n"
                report += f"    B 组比率: {metric_data['rate_percentage_b']:.2f}%\n"

            report += f"    提升: {metric_data['lift_percentage']:+.2f}%\n"
            report += f"    P值: {metric_data['p_value']:.4f}\n"
            report += f"    显著性: {'是' if metric_data['significant'] else '否'}\n"

        return report


# 使用示例
if __name__ == "__main__":
    # 1. 创建实验配置
    config = ExperimentConfig(
        name="prompt_optimization_v1",
        description="测试详细 Prompt 是否比简洁 Prompt 更好",
        traffic_split=0.5,
        min_sample_size=100
    )

    # 2. 初始化框架
    framework = ABTestFramework(config)

    # 3. 模拟一些测试数据
    import random

    for i in range(150):
        user_id = f"user_{i}"
        group = framework.assign_group(user_id)

        # 模拟不同组的表现
        if group == Group.A:
            # A 组：基线性能
            response_time = random.uniform(1.0, 2.0)
            success = random.random() < 0.85
            satisfaction = random.uniform(3.5, 4.5)
        else:
            # B 组：略好
            response_time = random.uniform(0.8, 1.8)
            success = random.random() < 0.90
            satisfaction = random.uniform(4.0, 4.8)

        # 记录数据
        metrics = Metrics(
            response_time=response_time,
            success=success,
            user_satisfaction=satisfaction,
            token_usage=random.randint(100, 500)
        )

        framework.track(user_id, group, metrics)

    # 4. 分析结果
    print(framework.generate_report())
