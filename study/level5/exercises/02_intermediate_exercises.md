# 02 进阶练习

> **主题**: Kubernetes 和 CI/CD 进阶练习
> **题数**: 30 题
> **时间**: 3 小时
> **难度**: ⭐⭐⭐

---

## Kubernetes 基础 (10 题)

### 1. Pod 和容器的关系

**问题**: 关于 Pod 和容器的关系，以下哪项是正确的？

A. Pod 只能包含一个容器
B. Pod 可以包含多个容器，它们共享网络和存储
C. Pod 是容器的运行时环境
D. Pod 和容器是同一个概念

**答案**: B

**解析**: Pod 是 Kubernetes 的最小部署单元，可以包含一个或多个容器，这些容器共享网络命名空间和存储卷。

---

### 2. Deployment 的作用

**问题**: Deployment 主要用于什么？

A. 管理无状态应用
B. 管理有状态应用
C. 管理守护进程
D. 管理定时任务

**答案**: A

**解析**: Deployment 用于管理无状态应用，提供声明式更新、回滚、扩缩容等功能。

---

### 3. Service 的类型

**问题**: 以下哪种 Service 类型会将服务暴露到集群外部？

A. ClusterIP
B. NodePort
C. LoadBalancer
D. B 和 C 都可以

**答案**: D

**解析**: NodePort 和 LoadBalancer 都可以将服务暴露到外部，LoadBalancer 还会自动创建云厂商的负载均衡器。

---

### 4. ConfigMap vs Secret

**问题**: ConfigMap 和 Secret 的主要区别是什么？

A. ConfigMap 用于配置，Secret 用于敏感信息
B. ConfigMap 是加密的，Secret 不是
C. ConfigMap 只能存储字符串，Secret 可以存储二进制
D. 没有区别

**答案**: A

**解析**: 主要用途不同，Secret 专门用于存储敏感信息（如密码、Token），且默认是 base64 编码。

---

### 5. 资源限制

**问题**: 如何为 Pod 设置资源限制？

A. 使用 resources.requests
B. 使用 resources.limits
C. 使用 resources.requests 和 resources.limits
D. 使用 resources.quota

**答案**: C

**解析**: requests 是调度时需要的最小资源，limits 是容器能使用的最大资源。

---

### 6. 健康检查

**问题**: Kubernetes 的健康检查包括哪些？

A. livenessProbe 和 readinessProbe
B. startupProbe 和 livenessProbe
C. A 和 B 都包括
D. 只有 livenessProbe

**答案**: C

**解析**: 三种探针：startupProbe（启动检查）、livenessProbe（存活检查）、readinessProbe（就绪检查）。

---

### 7. 滚动更新

**问题**: Deployment 的滚动更新策略如何配置？

A. strategy.rollingUpdate.maxUnavailable
B. strategy.rollingUpdate.maxSurge
C. A 和 B 都需要配置
D. 使用 revisionHistoryLimit

**答案**: C

**解析**: maxUnavailable 控制更新时最多不可用的 Pod 数，maxSurge 控制可以超出期望值的 Pod 数。

---

### 8. 持久化存储

**问题**: 如何在 Pod 中使用持久化存储？

A. 使用 volumeMounts 和 volumes
B. 使用 persistentVolumeClaim
C. 使用 storageClass
D. 以上都可以

**答案**: D

**解析**: 持久化存储可以通过 PV/PVC、StorageClass 动态配置等方式实现。

---

### 9. 命名空间

**问题**: Kubernetes 命名空间的作用是什么？

A. 隔离资源
B. 限制资源使用
C. A 和 B 都是
D. 只是逻辑分组

**答案**: C

**解析**: 命名空间既可以逻辑隔离资源，也可以配合 ResourceLimit 限制资源使用。

---

### 10. Ingress 的作用

**问题**: Ingress 主要用于什么？

A. 服务发现
B. 负载均衡
C. HTTP/S 路由
D. 服务网格

**答案**: C

**解析**: Ingress 用于管理外部访问，提供 HTTP/S 路由、SSL 终止、域名路由等功能。

---

## CI/CD 进阶 (10 题)

### 11. 矩阵构建

**问题**: GitHub Actions 的矩阵构建用于什么？

A. 并行运行多个配置
B. 测试多个版本
C. A 和 B 都是
D. 串行运行多个配置

**答案**: C

**解析**: 矩阵构建可以在不同配置（如 Python 版本、操作系统）下并行运行测试。

---

### 12. 缓存依赖

**问题**: GitHub Actions 中如何缓存依赖？

A. 使用 actions/cache
B. 使用环境变量
C. 使用 artifacts
D. 手动下载

**答案**: A

**解析**: actions/cache action 可以缓存依赖，加速 Workflow 运行。

---

### 13. 触发条件

**问题**: 如何配置 Workflow 只在特定文件变化时触发？

A. 使用 on.push.paths
B. 使用 on.push.paths-ignore
C. A 和 B 都可以
D. 使用 if 条件

**答案**: C

**解析**: paths 指定监听的文件，paths-ignore 指定忽略的文件。

---

### 14. 环境变量

**问题**: 如何在 GitHub Actions 中使用加密的环境变量？

A. 使用 secrets
B. 使用 env
C. 使用 vars
D. 使用配置文件

**答案**: A

**解析**: secrets 用于存储敏感信息，在 Workflow 中自动加密。

---

### 15. 条件执行

**问题**: 如何让某个步骤只在失败时执行？

A. 使用 if: failure()
B. 使用 if: success()
C. 使用 continue-on-error
D. 使用 timeout-minutes

**答案**: A

**解析**: if: failure() 使步骤仅在前面步骤失败时执行。

---

### 16. 复用 Workflow

**问题**: 如何创建可复用的 Workflow？

A. 使用 workflow_call 触发器
B. 使用 reusable workflow
C. 使用 composite action
D. A 和 B 都可以

**答案**: D

**解析**: 可以创建 reusable workflow（可复用工作流）或 composite action（组合动作）。

---

### 17. 并行任务

**问题**: 如何让两个 Job 并行运行？

A. 不设置 needs
B. 使用 needs: []
C. 使用 strategy.matrix
D. 使用 continue-on-error

**答案**: A

**解析**: 不设置 needs 或 needs 为空时，Jobs 会并行运行。

---

### 18. 串行任务

**问题**: 如何让 Job B 在 Job A 成功后运行？

A. 设置 needs: [A]
B. 设置 if: success()
C. 设置 depends: [A]
D. 设置 after: [A]

**答案**: A

**解析**: needs 定义 Job 的依赖关系。

---

### 19. 部署策略

**问题**: 蓝绿部署的特点是什么？

A. 同时运行两个版本
B. 逐步切换流量
C. 先部署到少量实例
D. 以上都不是

**答案**: A

**解析**: 蓝绿部署同时维护两个完整环境，通过切换路由实现部署。

---

### 20. 回滚策略

**问题**: Kubernetes Deployment 如何回滚？

A. kubectl rollout undo
B. kubectl deployment rollback
C. 修改镜像版本
D. 删除重建

**答案**: A

**解析**: kubectl rollout undo 可以回滚到上一个版本。

---

## 监控告警 (10 题)

### 21. Prometheus 数据模型

**问题**: Prometheus 的指标数据类型不包括？

A. Counter
B. Gauge
C. Histogram
D. Average

**答案**: D

**解析**: Prometheus 的四种指标类型是 Counter、Gauge、Histogram、Summary。

---

### 22. PromQL 查询

**问题**: 如何计算过去 5 分钟的请求速率？

A. rate(requests_total[5m])
B. increase(requests_total[5m])
C. delta(requests_total[5m])
D. avg(requests_total[5m])

**答案**: A

**解析**: rate() 计算每秒平均增长率，适合 Counter 类型。

---

### 23. 告警规则

**问题**: 以下哪个告警规则配置是正确的？

A. alert: HighErrorRate if: rate > 0.05
B. alert: HighErrorRate expr: rate(errors[5m]) > 0.05
C. alert: HighErrorRate when: rate > 0.05
D. 以上都不对

**答案**: B

**解析**: 告警规则使用 expr 字段定义 PromQL 表达式。

---

### 24. 告警持续时间

**问题**: 告警规则的 for 字段作用是什么？

A. 告警持续时间
B. 告警间隔
C. 告警超时
D. 告警延迟

**答案**: A

**解析**: for 指定条件必须持续多久才触发告警，避免瞬时波动。

---

### 25. Grafana 变量

**问题**: Grafana 仪表盘的变量用于什么？

A. 动态过滤数据
B. 简化查询
C. A 和 B 都是
D. 只是显示文本

**答案**: C

**解析**: 变量可以用于动态过滤、简化查询、创建交互式仪表盘。

---

### 26. Loki 日志查询

**问题**: Loki 的日志查询语言是？

A. LogQL
B. PromQL
C. SQL
D. Gremlin

**答案**: A

**解析**: Loki 使用 LogQL (Log Query Language) 进行日志查询。

---

### 27. 日志聚合

**问题**: Loki 的标签索引有什么特点？

A. 只索引标签，不索引内容
B. 索引所有内容
C. 只索引时间戳
D. 不建立索引

**答案**: A

**解析**: Loki 只索引标签（Label），日志内容不索引，这降低了成本。

---

### 28. 监控指标

**问题**: RED 方法不包括哪个指标？

A. Rate
B. Errors
C. Duration
D. CPU

**答案**: D

**解析**: RED 方法 = Rate（请求率）、Errors（错误率）、Duration（延迟）。

---

### 29. 监控目标

**问题**: USE 方法用于监控什么？

A. 请求处理
B. 资源使用
C. 业务指标
D. 用户体验

**答案**: B

**解析**: USE 方法 = Utilization（使用率）、Saturation（饱和度）、Errors（错误），用于监控资源。

---

### 30. SLO 定义

**问题**: SLO (Service Level Objective) 是什么？

A. 服务质量目标
B. 服务可用性目标
C. 服务性能目标
D. 以上都是

**答案**: D

**解析**: SLO 定义服务的各种质量目标，包括可用性、性能、正确性等。

---

## 实践任务

### 任务 1: 部署应用到 K8s

创建完整的 K8s 配置文件：

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      containers:
      - name: agent
        image: agent:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: agent-service
spec:
  selector:
    app: agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

**任务**: 部署到 K8s 集群并验证

### 任务 2: 配置 CI/CD

创建完整的 CI/CD Workflow：

```yaml
name: CI/CD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=.

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.REGISTRY }}/agent:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - run: |
          kubectl set image deployment/agent-app agent=${{ secrets.REGISTRY }}/agent:latest
```

**任务**: 配置并运行 CI/CD 流水线

### 任务 3: 配置监控告警

创建 Prometheus 告警规则：

```yaml
groups:
  - name: agent_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"

      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value }}s"
```

**任务**: 配置告警并测试触发

---

## 完成标准

- [ ] 完成 30 道练习题
- [ ] 正确率 >= 80%
- [ ] 完成实践任务
- [ ] 记录学习心得

---

## 学习资源

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Prometheus Querying](https://prometheus.io/docs/prometheus/latest/querying/basics/)

---

**完成时间**: ____
**得分**: ____/30
**正确率**: ____%
