# OpenClaw 源码剖析与实现指南

> 面向开发者与小白的 OpenClaw 实现型文档，覆盖智能体框架、通道适配器、上下文管理、状态机与 Gateway 控制面。

[![VitePress](https://img.shields.io/badge/Built%20with-VitePress-646cff?logo=vite&logoColor=white)](https://vitepress.dev)
[![Docs](https://img.shields.io/badge/Docs-236%20pages-4fc08d)](https://yeuxuan.github.io/openclaw-docs)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 📚 文档内容

| 学习主线 | 内容 | 篇数 |
|---|---|---|
| **Track 0** 安装教程 | 安装、配置、接入 AI 服务商、连接通道 | 147 篇 |
| **Track A** 完整工程主线 | CLI → Gateway → 路由 → Agent 全链路拆解 | 59 篇 |
| **Track B** AI 重点框架 | 上下文、状态机、工具策略、记忆、Hook 注入 | 22 篇 |

---

## 🚀 本地运行

```bash
git clone https://github.com/yeuxuan/openclaw-docs.git
cd openclaw-docs
npm install
npm run docs:dev
```

打开终端输出的本地地址即可预览。

## 🏗️ 构建

```bash
npm run docs:build   # 构建静态产物到 docs/.vitepress/dist/
npm run docs:preview # 本地预览构建结果
```

---

## 📁 目录说明

```
openclaw-docs/
├── docs/
│   ├── index.md                          # 首页
│   ├── tutorials/                        # Track 0：安装教程
│   │   ├── getting-started/              #   快速入门
│   │   ├── installation/                 #   安装部署
│   │   ├── gateway/                      #   网关配置
│   │   ├── channels/                     #   通道接入
│   │   ├── providers/                    #   模型 Provider
│   │   └── concepts/                     #   核心概念
│   ├── beginner-openclaw-guide/          # Track A：完整工程主线（59 篇）
│   └── beginner-openclaw-framework-focus/ # Track B：AI 核心框架（22 篇）
└── docs/.vitepress/
    └── config.mts                        # 站点配置（导航、侧边栏）
```

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=openclaw/openclaw&type=Date)](https://star-history.com/#openclaw/openclaw&Date)
