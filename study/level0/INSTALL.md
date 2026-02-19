# Level 0 依赖安装指南

## 核心依赖（必须安装）

```bash
# LangChain 核心库
pip install langchain>=0.1.0

# LangChain OpenAI 集成
pip install langchain-openai>=0.0.5

# LangChain Hub（用于 Agent prompt）
pip install langchainhub>=0.1.0

# OpenAI Python SDK
pip install openai>=1.0.0
```

## 可选依赖（推荐安装）

### 用于向量存储和检索
```bash
pip install chromadb>=0.4.0
pip install sentence-transformers>=2.2.0
```

### 用于数据处理
```bash
pip install pandas>=2.0.0
pip install numpy>=1.24.0
```

### 用于网络请求
```bash
pip install requests>=2.28.0
pip install beautifulsoup4>=4.12.0
```

## 完整安装（一键安装所有）

```bash
pip install langchain langchain-openai langchainhub openai chromadb sentence-transformers pandas numpy requests beautifulsoup4
```

## 环境变量设置

### 创建 .env 文件
```bash
# 在项目根目录创建 .env 文件
cat > .env << EOF
OPENAI_API_KEY=your-api-key-here
EOF
```

### 或在命令行设置
```bash
# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# Windows (CMD)
set OPENAI_API_KEY=your-api-key-here
```

## 版本要求

- Python >= 3.9
- 推荐使用 Python 3.10 或 3.11

## 验证安装

运行以下命令验证安装：

```bash
python -c "import langchain; print(langchain.__version__)"
python -c "import openai; print('OpenAI SDK installed')"
```

## 常见问题

### Q1: 安装失败？
**A**: 尝试升级 pip：
```bash
pip install --upgrade pip
```

### Q2: 找不到模块？
**A**: 确保在正确的虚拟环境中：
```bash
which python  # Linux/Mac
where python  # Windows
```

### Q3: API Key 在哪里获取？
**A**: 访问 https://platform.openai.com/api-keys

## 成本估算

使用 Level 0 示例的预计成本（基于 gpt-3.5-turbo）：

- `07_langchain_basics.py`: ~$0.01-0.05
- `08_first_agent.py`: ~$0.02-0.10
- 总计: ~$0.10 以内

提示：可以使用更便宜的模型或本地模型来降低成本。
