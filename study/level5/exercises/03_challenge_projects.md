# 03 挑战项目

> **主题**: 完整的生产级 Agent 系统部署
> **时间**: 3 小时
> **难度**: ⭐⭐⭐⭐⭐
> **类型**: 综合实战

---

## 项目概述

在本次挑战中，你将完成一个**端到端的生产级 Agent 系统部署**，包括容器化、编排、CI/CD、监控和安全的完整实现。

### 项目目标

1. ✅ 容器化 Agent 应用
2. ✅ 部署到 Kubernetes 集群
3. ✅ 配置完整的 CI/CD 流水线
4. ✅ 建立监控告警体系
5. ✅ 实施安全防护措施
6. ✅ 编写完整的部署文档

---

## 挑战任务

### 任务 1: 容器化 Agent 应用 (30 分钟)

**要求**:
1. 编写优化的 Dockerfile
   - 使用多阶段构建
   - 非 root 用户运行
   - 健康检查
   - 镜像大小 < 500MB

2. 编写 docker-compose.yml
   - Agent 服务
   - PostgreSQL 数据库
   - Redis 缓存
   - Prometheus 监控

**验证**:
```bash
docker-compose up -d
docker-compose ps
curl http://localhost:8000/health
```

**产出**:
- Dockerfile
- docker-compose.yml
- 构建和运行日志

---

### 任务 2: Kubernetes 部署 (45 分钟)

**要求**:
1. 创建完整的 K8s 配置
   - Namespace
   - Deployment (3 副本)
   - Service (ClusterIP + LoadBalancer)
   - ConfigMap
   - Secret
   - HPA (自动扩缩容)
   - Ingress (域名 + HTTPS)

2. 配置资源限制
   - CPU requests: 100m, limits: 500m
   - Memory requests: 128Mi, limits: 512Mi

3. 配置健康检查
   - Liveness probe
   - Readiness probe
   - Startup probe

**验证**:
```bash
kubectl apply -f k8s/
kubectl get pods -n agent-prod
kubectl get svc -n agent-prod
kubectl get ingress -n agent-prod
```

**产出**:
- deployment.yaml
- service.yaml
- ingress.yaml
- configmap.yaml
- secret.yaml
- hpa.yaml

---

### 任务 3: CI/CD 流水线 (45 分钟)

**要求**:
1. 配置 GitHub Actions CI
   - 代码检查（black, flake8, mypy）
   - 单元测试
   - 测试覆盖率
   - 安全扫描

2. 配置 GitHub Actions CD
   - 构建并推送 Docker 镜像
   - 部署到 Kubernetes 集群
   - 健康检查验证
   - 自动回滚机制

3. 配置环境变量和密钥
   - 开发环境
   - 生产环境
   - 使用 GitHub Secrets

**验证**:
- Push 代码触发 CI
- 合并到 main 分支触发 CD
- 检查部署状态

**产出**:
- .github/workflows/ci.yml
- .github/workflows/deploy.yml
- GitHub Actions 运行日志

---

### 任务 4: 监控告警体系 (45 分钟)

**要求**:
1. 配置 Prometheus
   - 抓取 Agent 指标
   - 抓取 Kubernetes 指标
   - 抓取数据库指标
   - 配置数据保留（30天）

2. 配置告警规则
   - P0 告警：服务不可用、错误率 > 5%
   - P1 告警：高延迟、高 CPU/内存
   - P2 告警：磁盘空间、成本异常

3. 配置 Grafana 仪表盘
   - 请求速率和错误率
   - 响应时间（P50, P95, P99）
   - 资源使用（CPU, 内存）
   - LLM Token 使用和成本

4. 配置告警通知
   - Email
   - Slack（可选）

**验证**:
- 访问 Prometheus UI
- 访问 Grafana 仪表盘
- 测试告警触发

**产出**:
- prometheus.yml
- alerts.yml
- grafana-dashboard.json
- 告警通知配置

---

### 任务 5: 安全防护措施 (30 分钟)

**要求**:
1. 实施认证授权
   - JWT Token 认证
   - 基于角色的权限控制
   - Token 过期机制

2. 实施速率限制
   - 用户级别：20 req/min
   - IP 级别：100 req/min

3. 添加安全响应头
   - X-Frame-Options
   - X-Content-Type-Options
   - Strict-Transport-Security
   - Content-Security-Policy

4. 配置 HTTPS
   - Let's Encrypt 证书
   - 自动续期

**验证**:
- 测试认证流程
- 测试速率限制
- 检查安全响应头
- 验证 HTTPS 配置

**产出**:
- auth.py
- rate_limit.py
- security_middleware.py
- SSL 证书配置

---

## 验收标准

### 功能验收 (40 分)

- [ ] Agent 应用可以正常访问 (5 分)
- [ ] 响应时间 P95 < 3s (5 分)
- [ ] 并发支持 >= 50 QPS (5 分)
- [ ] 健康检查端点正常 (5 分)
- [ ] 认证授权工作正常 (10 分)
- [ ] 速率限制生效 (5 分)
- [ ] HTTPS 可以访问 (5 分)

### 技术验收 (30 分)

- [ ] Docker 镜像 < 500MB (5 分)
- [ ] K8s 部署成功 (5 分)
- [ ] 自动扩缩容工作 (5 分)
- [ ] CI/CD 流水线工作 (5 分)
- [ ] Prometheus 采集指标 (5 分)
- [ ] Grafana 仪表盘显示 (5 分)

### 质量验收 (20 分)

- [ ] 代码有类型提示 (5 分)
- [ ] 代码有文档注释 (5 分)
- [ ] 测试覆盖率 >= 70% (5 分)
- [ ] 通过安全扫描 (5 分)

### 文档验收 (10 分)

- [ ] README.md 完整 (3 分)
- [ ] DEPLOYMENT.md 详细 (3 分)
- [ ] API.md 完整 (2 分)
- [ ] 监控告警文档 (2 分)

---

## 额外挑战（可选）

### 🌟 挑战 1: 灰度发布

配置基于权重的灰度发布：
- 90% 流量到 v1
- 10% 流量到 v2
- 逐步切换流量

**加分**: 5 分

### 🌟 挑战 2: 成本优化

优化 LLM API 调用成本：
- 实现缓存策略
- 使用更小的模型
- 批量处理请求

**加分**: 5 分

### 🌟 挑战 3: 日志聚合

配置 Loki + Promtail：
- 收集应用日志
- 配置日志查询
- 创建日志仪表盘

**加分**: 5 分

---

## 时间规划

| 时间 | 任务 | 产出 |
|------|------|------|
| 0:00-0:30 | 容器化应用 | Dockerfile, docker-compose.yml |
| 0:30-1:15 | K8s 部署 | K8s 配置文件 |
| 1:15-2:00 | CI/CD 配置 | GitHub Actions workflows |
| 2:00-2:45 | 监控告警 | Prometheus, Grafana 配置 |
| 2:45-3:15 | 安全加固 | 认证、限流、HTTPS |
| 3:15-3:30 | 文档编写 | README, DEPLOYMENT |

---

## 评分标准

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100 | 优秀 | 超出预期，完成额外挑战 |
| 80-89 | 良好 | 满足所有要求，质量高 |
| 70-79 | 合格 | 满足基本要求 |
| 60-69 | 及格 | 部分要求未满足 |
| < 60 | 不及格 | 需要重新完成 |

---

## 学习资源

### 参考文档

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

### 示例配置

本项目的 `examples/` 目录提供了完整的示例配置：
- `01_docker_deployment/` - Docker 和 Compose
- `02_kubernetes_deployment/` - K8s 配置
- `04_monitoring_setup/` - Prometheus 和 Grafana
- `06_security_practices.py` - 安全实践

---

## 提交要求

### 代码仓库

1. Fork 本项目
2. 创建分支 `challenge-03`
3. 完成挑战任务
4. 提交 Pull Request

### PR 描述模板

```markdown
## 完成的任务

- [ ] 任务 1: 容器化 Agent 应用
- [ ] 任务 2: Kubernetes 部署
- [ ] 任务 3: CI/CD 流水线
- [ ] 任务 4: 监控告警体系
- [ ] 任务 5: 安全防护措施

## 额外挑战

- [ ] 挑战 1: 灰度发布
- [ ] 挑战 2: 成本优化
- [ ] 挑战 3: 日志聚合

## 产出链接

- Docker Hub 镜像:
- 部署地址:
- Grafana 仪表盘:
- 部署文档:

## 学习心得

（记录学习过程中的关键收获和遇到的问题）
```

---

## 常见问题

### Q1: 没有 Kubernetes 集群怎么办？

**A**:
- 使用 Docker Desktop 的 Kubernetes
- 使用 Kind (Kubernetes in Docker)
- 使用云服务的免费 K8s 集群

### Q2: 如何测试 CI/CD？

**A**:
- 使用 act 本地运行 GitHub Actions
- 创建测试仓库
- 使用 Pull Request 测试

### Q3: 监控数据没有显示？

**A**:
- 检查 Prometheus targets 状态
- 检查 ServiceMonitor 配置
- 检查网络策略是否允许访问

---

## 总结

这个挑战项目综合了 Level 5 的所有核心内容，完成后你将：

1. ✅ 掌握容器化部署技能
2. ✅ 理解 Kubernetes 编排
3. ✅ 能够配置 CI/CD 流水线
4. ✅ 建立监控告警体系
5. ✅ 实施安全防护措施

**开始挑战，展示你的生产级部署能力！** 🚀

---

**开始时间**: ____
**完成时间**: ____
**最终得分**: ____/100
