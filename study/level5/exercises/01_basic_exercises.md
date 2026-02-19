# 01 基础练习

> **主题**: Docker 和基础部署练习
> **题数**: 30 题
> **时间**: 2 小时
> **难度**: ⭐⭐

---

## Docker 基础 (10 题)

### 1. Docker 核心概念

**问题**: 以下哪个不是 Docker 的核心概念？

A. 镜像 (Image)
B. 容器 (Container)
C. 虚拟机 (Virtual Machine)
D. Dockerfile

**答案**: C

**解析**: Docker 的核心概念是镜像、容器和 Dockerfile。虚拟机是完全不同的技术。

---

### 2. 镜像分层

**问题**: Docker 镜像的分层存储有什么好处？

A. 减少镜像大小
B. 加快构建速度
C. 便于复用和共享
D. 以上都是

**答案**: D

**解析**: 分层存储可以实现缓存复用、减少存储空间、加快构建和分发速度。

---

### 3. Dockerfile 指令

**问题**: 哪个指令用于设置容器启动时的默认命令？

A. RUN
B. CMD
C. ENTRYPOINT
D. EXEC

**答案**: B

**解析**: CMD 用于设置默认命令，RUN 用于构建时执行命令，ENTRYPOINT 用于配置容器启动时的入口点。

---

### 4. 多阶段构建

**问题**: 多阶段构建的主要优势是什么？

A. 加快构建速度
B. 减小最终镜像大小
C. 提高安全性
D. 简化配置

**答案**: B

**解析**: 多阶段构建可以将构建工具和依赖保留在构建阶段，最终镜像只包含运行时需要的文件。

---

### 5. 镜像优化

**问题**: 以下哪种方式不能减小镜像大小？

A. 使用 alpine 基础镜像
B. 多阶段构建
C. 在一个 RUN 指令中安装多个包
D. 使用 .dockerignore

**答案**: C

**解析**: 在一个 RUN 指令中安装多个包可以减少层数，但不会显著减小镜像大小。其他方式都能有效减小镜像。

---

### 6. 容器通信

**问题**: 两个容器如何通信？

A. 通过容器 IP
B. 通过 Docker 网络
C. 通过 docker-compose 的服务名
D. 以上都可以

**答案**: D

**解析**: 容器间可以通过多种方式通信，包括直接 IP、Docker 网络、服务名解析等。

---

### 7. 数据持久化

**问题**: 如何持久化容器中的数据？

A. 使用 VOLUME 指令
B. 使用 docker run -v 参数
C. 使用 docker-compose 的 volumes
D. 以上都可以

**答案**: D

**解析**: 数据持久化可以通过 Volume、Bind Mount 等多种方式实现。

---

### 8. 容器资源限制

**问题**: 如何限制容器的内存使用？

A. docker run --memory
B. docker run -m
C. docker-compose 的 mem_limit
D. 以上都可以

**答案**: D

**解析**: 可以通过多种方式限制容器资源，包括命令行参数和 compose 配置。

---

### 9. 健康检查

**问题**: Dockerfile 中的 HEALTHCHECK 指令有什么作用？

A. 检查容器是否启动成功
B. 定期检查容器健康状态
C. 自动重启不健康的容器
D. 记录容器日志

**答案**: B

**解析**: HEALTHCHECK 用于定期检查容器健康状态，可以通过 docker ps 查看健康状态。

---

### 10. 安全最佳实践

**问题**: 以下哪项不是 Docker 安全最佳实践？

A. 使用非 root 用户运行容器
B. 在镜像中硬编码密钥
C. 定期更新基础镜像
D. 扫描镜像漏洞

**答案**: B

**解析**: 绝不应该在镜像中硬编码密钥，应该使用环境变量或 secrets 管理敏感信息。

---

## Docker Compose (10 题)

### 11. 服务依赖

**问题**: docker-compose 中如何定义服务依赖？

A. using
B. depends_on
C. requires
D. links

**答案**: B

**解析**: depends_on 用于定义服务启动顺序和依赖关系。

---

### 12. 环境变量

**问题**: 如何在 docker-compose 中设置环境变量？

A. environment
B. env
C. env_file
D. 以上都可以

**答案**: D

**解析**: 可以通过 environment、env_file 等多种方式设置环境变量。

---

### 13. 网络配置

**问题**: docker-compose 中如何配置服务网络？

A. networks
B. net
C. network_mode
D. A 和 C 都可以

**答案**: D

**解析**: 可以定义自定义网络，也可以使用 network_mode 指定网络模式。

---

### 14. 端口映射

**问题**: 以下端口映射配置哪个是正确的？

A. ports: "8000"
B. ports: "8000:8000"
C. ports: - 8000:8000
D. B 和 C 都可以

**答案**: D

**解析**: 端口映射可以使用字符串或列表格式，格式为 "主机端口:容器端口"。

---

### 15. 数据卷

**问题**: docker-compose 中如何定义和使用数据卷？

A. volumes 顶级定义 + 服务内引用
B. 直接在服务内定义
C. 使用外部 volume
D. 以上都可以

**答案**: D

**解析**: 数据卷可以通过多种方式定义和使用。

---

### 16. 重启策略

**问题**: 哪个重启策略会在容器停止后总是重启？

A. restart: always
B. restart: unless-stopped
C. restart: on-failure
D. A 和 B 都会

**答案**: D

**解析**: always 和 unless-stopped 都会自动重启容器，区别在于手动停止时的行为。

---

### 17. 配置文件

**问题**: docker-compose 的默认配置文件名是什么？

A. docker-compose.yaml
B. docker-compose.yml
C. compose.yml
D. 以上都可以

**答案**: D

**解析**: docker-compose 会自动查找多个默认配置文件名。

---

### 18. 多环境配置

**问题**: 如何管理多环境的 docker-compose 配置？

A. 使用多个 compose 文件
B. 使用环境变量
C. 使用 override 文件
D. 以上都可以

**答案**: D

**解析**: 可以通过多种方式管理多环境配置。

---

### 19. 服务扩展

**问题**: 如何启动多个副本的服务？

A. docker-compose scale
B. docker-compose up --scale
C. deploy.replicas
D. B 和 C 都可以

**答案**: D

**解析**: 可以通过 --scale 参数或 deploy 配置来扩展服务副本数。

---

### 20. 日志管理

**问题**: 如何查看 docker-compose 服务的日志？

A. docker-compose logs
B. docker-compose logs -f
C. docker logs <container_id>
D. 以上都可以

**答案**: D

**解析**: 可以通过多种方式查看容器日志。

---

## 基础部署 (10 题)

### 21. 环境变量管理

**问题**: 以下哪种方式不适合管理敏感信息？

A. 环境变量
B. Docker secrets
C. .env 文件提交到 git
D. K8s secrets

**答案**: C

**解析**: .env 文件如果包含敏感信息，不应该提交到 git 仓库。

---

### 22. 健康检查端点

**问题**: Agent 应用应该提供什么健康检查端点？

A. /health
B. /ready
C. /live
D. 以上都应该有

**答案**: D

**解析**: 完整的健康检查应该包含健康性、就绪性和存活性检查。

---

### 23. 日志输出

**问题**: 容器化应用的日志应该输出到哪里？

A. 文件
B. 标准输出/标准错误
C. 日志服务
D. B 和 C 都可以

**答案**: D

**解析**: 容器中应该输出到 stdout/stderr，由日志驱动或服务收集。

---

### 24. 配置管理

**问题**: 应用配置应该通过什么方式管理？

A. 配置文件
B. 环境变量
C. 配置中心
D. 根据场景选择

**答案**: D

**解析**: 不同场景适合不同的配置管理方式。

---

### 25. 优雅关闭

**问题**: 如何实现容器的优雅关闭？

A. 捕获 SIGTERM 信号
B. 设置超时时间
C. 完成当前请求
D. 以上都需要

**答案**: D

**解析**: 优雅关闭需要处理信号、设置超时、完成清理工作。

---

### 26. 资源监控

**问题**: 如何监控容器的资源使用？

A. docker stats
B. docker inspect
C. Prometheus + cAdvisor
D. 以上都可以

**答案**: D

**解析**: 可以使用多种方式监控容器资源。

---

### 27. 镜像版本管理

**问题**: 生产环境应该使用哪种镜像标签？

A. latest
B. 具体版本号
C. commit hash
D. B 或 C

**答案**: D

**解析**: 生产环境应该使用可追溯的版本标签，避免使用 latest。

---

### 28. 容器安全

**问题**: 以下哪项不能提高容器安全性？

A. 扫描镜像漏洞
B. 使用非 root 用户
C. 暴露所有端口
D. 最小化镜像

**答案**: C

**解析**: 暴露所有端口会降低安全性，应该只暴露必要的端口。

---

### 29. CI/CD 集成

**问题**: Docker 在 CI/CD 中的主要作用是什么？

A. 统一构建环境
B. 简化部署流程
C. 提高部署速度
D. 以上都是

**答案**: D

**解析**: Docker 在 CI/CD 中可以统一环境、简化部署、提高速度。

---

### 30. 故障排查

**问题**: 容器启动失败时，首先应该检查什么？

A. 应用日志
B. 容器日志
C. 镜像是否正确
D. 以上都应该检查

**答案**: D

**解析**: 故障排查需要全面检查日志、配置、镜像等多个方面。

---

## 完成标准

- [ ] 完成 30 道练习题
- [ ] 正确率 >= 80%
- [ ] 能够解释每个答案
- [ ] 记录错题和知识点

---

## 学习资源

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

---

**完成时间**: ____
**得分**: ____/30
**正确率**: ____%
