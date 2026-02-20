---
title: "快速开始"
sidebarTitle: "快速开始"
---

# 快速开始

**OpenClaw 是什么？**

OpenClaw 是一个运行在你自己电脑上的 AI 助手平台。安装完成后，你可以在 Telegram、WhatsApp、Discord 等聊天软件里直接和 AI 对话——发消息、让它帮你写东西、查资料、执行任务，就像有一个随时待命的私人助手。

---

## 第一步：准备 API 密钥

OpenClaw 本身是免费的，但它需要借助第三方 AI 服务来产生智能回复。**你需要提前准备好一个 AI API 密钥。**

::: info API 提供商不限于 Anthropic
你可以自由选择任意支持的 AI 服务商，无需绑定某一家。下面列出了常见的几种选择，按需挑选即可。
:::

### 可选的 AI 提供商

| 提供商 | 模型 | 特点 | 适合人群 |
|--------|------|------|----------|
| **Anthropic（Claude）** ⭐ | Claude 3.5 / 3 系列 | 中文能力强，推理准确，官方首选 | 追求综合质量 |
| **DeepSeek** | DeepSeek-V3 / R1 | 价格极低，中文优秀，国内可直连 | 国内用户、性价比优先 |
| **OpenAI（ChatGPT）** | GPT-4o / o1 系列 | 生态成熟，插件丰富 | 已有 OpenAI 账号 |
| **Google Gemini** | Gemini 1.5 / 2.0 系列 | 多模态能力强，免费额度大 | 想免费试用 |
| **阿里云百炼（通义千问）** | Qwen-Max / Plus | 国内服务，无需翻墙，支付宝充值 | 国内用户、合规需求 |

---

### 各平台获取密钥方法

::: details Anthropic（Claude）— 官方推荐
1. 访问 [console.anthropic.com](https://console.anthropic.com)，注册并登录
2. 点击左侧菜单 **"API Keys"** → **"Create Key"**
3. 给密钥起个名字，点击确认
4. **立刻复制**这串密钥（以 `sk-ant-` 开头）——**只显示一次！**

> 需要信用卡充值，国内需要翻墙访问。
:::

::: details DeepSeek — 国内首选，超高性价比
1. 访问 [platform.deepseek.com](https://platform.deepseek.com)，注册并登录
2. 点击右上角头像 → **"API Keys"** → **"创建 API Key"**
3. 复制密钥（以 `sk-` 开头）

> 支持微信 / 支付宝充值，国内直连，价格极低。
:::

::: details OpenAI（ChatGPT）
1. 访问 [platform.openai.com](https://platform.openai.com)，支持用 **Google / Microsoft 账号 OAuth 登录**，无需单独注册
2. 点击左侧 **"API Keys"** → **"Create new secret key"**
3. 复制密钥（以 `sk-` 开头）

> 需要信用卡充值，国内需要翻墙访问。
:::

::: details Google Gemini
1. 访问 [aistudio.google.com](https://aistudio.google.com)，用 Google 账号登录
2. 点击左侧 **"Get API key"** → **"Create API key"**
3. 复制生成的密钥

> 有免费额度，国内需要翻墙访问。
:::

::: details 阿里云百炼（通义千问）
1. 访问 [bailian.console.aliyun.com](https://bailian.console.aliyun.com)，用阿里云账号登录
2. 点击右上角 **"API-KEY"** → **"创建 API-KEY"**
3. 复制密钥（以 `sk-` 开头）

> 国内直连，支持支付宝充值，有免费试用额度。
:::

---

拿到密钥后，在安装配置时填入对应字段即可。

---

## 第二步：选择安装方式

OpenClaw 提供两种安装方式，选一种适合你的就行：

### 方式一：macOS 桌面应用（图形界面）

**适合：** 不熟悉命令行的用户，或者只用 Mac 的用户

- ✅ 有可视化界面，点一点就能完成配置
- ✅ 自动管理后台服务，不用手动启动
- ❌ 仅支持 **macOS**

**下载 macOS App：**
前往 [GitHub Releases](https://github.com/openclaw/openclaw/releases) 页面，下载最新版本的 `.dmg` 文件，双击安装。

**→ [去 macOS App 首次启动指南](./onboarding)**

---

### 方式二：命令行安装（跨平台）

**适合：** 开发者，或者在 Linux / Windows 上使用的用户

- ✅ 支持 macOS、Linux、Windows
- ✅ 灵活配置，适合高级用法
- ⚠️ 需要使用终端（命令行），共 9 步，大约 10 分钟

**→ [去命令行向导安装指南](./wizard)**

---

## 安装完成后做什么？

装好之后，下一步是把你的聊天软件连接上来，这样 AI 才能接收你的消息。推荐先接 Telegram，最简单：

**→ [接入 Telegram（推荐新手，5 分钟搞定）](../channels/telegram)**

如果安装过程中遇到了问题，或者想了解更多配置：

**→ [安装后配置与常见问题](./setup)**
