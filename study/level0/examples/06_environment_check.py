"""
示例 06: 环境检查指南

演示如何检查和配置 Agent 开发环境。

作者：Senior Developer
日期：2026-02-19
"""

import sys
import subprocess
import platform
from typing import Tuple, List, Dict, Optional
from pathlib import Path

print("=" * 70)
print("Agent 开发环境检查指南")
print("=" * 70)
print()

# ============================================================================
# Part 1: 系统信息检查
# ============================================================================

print("【Part 1: 系统信息检查】")
print("-" * 70)
print()

class EnvironmentChecker:
    """环境检查器"""

    def __init__(self):
        """初始化环境检查器"""
        self.results = []
        self.warnings = []
        self.errors = []

    def log(self, message: str, level: str = "info") -> None:
        """记录日志"""
        if level == "info":
            print(f"✅ {message}")
        elif level == "warning":
            print(f"⚠️  {message}")
            self.warnings.append(message)
        elif level == "error":
            print(f"❌ {message}")
            self.errors.append(message)
        else:
            print(f"ℹ️  {message}")

        self.results.append({"level": level, "message": message})

    def check_system(self) -> None:
        """检查系统信息"""
        print("系统信息：")
        print()

        self.log(f"操作系统: {platform.system()} {platform.release()}")
        self.log(f"架构: {platform.machine()}")
        self.log(f"Python 版本: {sys.version}")
        self.log(f"Python 路径: {sys.executable}")
        print()

    def check_python_version(self, min_version: Tuple[int, int] = (3, 8)) -> bool:
        """检查 Python 版本"""
        print(f"检查 Python 版本（最低要求：{'.'.join(map(str, min_version))}）")
        print()

        current_version = sys.version_info[:2]

        if current_version >= min_version:
            self.log(f"Python 版本符合要求：{'.'.join(map(str, current_version))}")
            return True
        else:
            self.log(
                f"Python 版本过低：{'.'.join(map(str, current_version))} "
                f"< {'.'.join(map(str, min_version))}",
                level="error"
            )
            return False

    def check_pip(self) -> bool:
        """检查 pip"""
        print("检查 pip：")
        print()

        try:
            result = subprocess.run(
                ["pip", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"pip 已安装：{version}")
                return True
            else:
                self.log("pip 未正确安装", level="error")
                return False

        except Exception as e:
            self.log(f"检查 pip 失败：{e}", level="error")
            return False

    def check_package(self, package_name: str, import_name: Optional[str] = None) -> bool:
        """检查 Python 包"""
        if import_name is None:
            import_name = package_name

        try:
            __import__(import_name)
            self.log(f"{package_name} 已安装")
            return True
        except ImportError:
            self.log(f"{package_name} 未安装", level="warning")
            return False

    def check_packages(self) -> Dict[str, bool]:
        """检查核心包"""
        print("检查核心包：")
        print()

        packages = {
            "langchain": "langchain",
            "langgraph": "langgraph",
            "langchain-openai": "langchain_openai",
            "openai": "openai",
            "python-dotenv": "dotenv",
        }

        results = {}
        for display_name, import_name in packages.items():
            results[display_name] = self.check_package(display_name, import_name)

        print()
        return results

    def check_env_vars(self) -> Dict[str, bool]:
        """检查环境变量"""
        print("检查环境变量：")
        print()

        import os

        env_vars = {
            "OPENAI_API_KEY": "OpenAI API 密钥",
            "LANGCHAIN_API_KEY": "LangChain API 密钥（可选）",
            "LANGCHAIN_TRACING_V2": "LangChain 追踪（可选）"
        }

        results = {}
        for var_name, description in env_vars.items():
            value = os.environ.get(var_name)
            if value:
                # 隐藏敏感信息
                masked_value = value[:4] + "..." if len(value) > 4 else "***"
                self.log(f"{var_name}={masked_value} ({description})")
                results[var_name] = True
            else:
                self.log(f"{var_name} 未设置 ({description})", level="warning")
                results[var_name] = False

        print()
        return results

    def get_package_version(self, package_name: str) -> Optional[str]:
        """获取包版本"""
        try:
            result = subprocess.run(
                ["pip", "show", package_name],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if line.startswith("Version:"):
                        return line.split(":", 1)[1].strip()
            return None
        except:
            return None

    def print_summary(self) -> None:
        """打印检查摘要"""
        print("=" * 70)
        print("环境检查摘要")
        print("=" * 70)
        print()

        total = len(self.results)
        info = sum(1 for r in self.results if r["level"] == "info")
        warnings = len(self.warnings)
        errors = len(self.errors)

        print(f"总检查项: {total}")
        self.log(f"通过: {info}", level="info")
        if warnings > 0:
            self.log(f"警告: {warnings}", level="warning")
        if errors > 0:
            self.log(f"错误: {errors}", level="error")
        print()

        if errors > 0:
            print("❌ 环境检查未通过，请修复错误后再继续")
        elif warnings > 0:
            print("⚠️  环境检查通过，但有一些警告")
        else:
            print("✅ 环境检查全部通过！")
        print()

# 创建环境检查器
checker = EnvironmentChecker()

# 执行检查
checker.check_system()
checker.check_python_version()
checker.check_pip()
package_results = checker.check_packages()
env_results = checker.check_env_vars()

# ============================================================================
# Part 2: 安装指南
# ============================================================================

print("【Part 2: 依赖安装指南】")
print("-" * 70)
print()

print("如果某些包未安装，请运行以下命令：")
print()

print("1. 基础依赖")
print("```bash")
print("pip install langchain langgraph langchain-openai")
print("```")
print()

print("2. 可选依赖（推荐）")
print("```bash")
print("pip install python-dotenv rich")
print("```")
print()

print("3. 全部依赖（requirements.txt）")
print("```bash")
print("pip install -r requirements.txt")
print("```")
print()

# ============================================================================
# Part 3: 环境变量配置
# ============================================================================

print("【Part 3: 环境变量配置】")
print("-" * 70)
print()

print("配置环境变量：")
print()

print("方法 1: 直接设置（临时）")
print("```bash")
print("export OPENAI_API_KEY='your-api-key'")
print("```")
print()

print("方法 2: 使用 .env 文件（推荐）")
print("创建 .env 文件：")
print("```")
print("# OpenAI API")
print("OPENAI_API_KEY=your-api-key")
print()
print("# LangChain（可选）")
print("LANGCHAIN_API_KEY=your-langchain-key")
print("LANGCHAIN_TRACING_V2=true")
print("```")
print()

print("方法 3: 使用 python-dotenv 加载")
print("```python")
print("from dotenv import load_dotenv")
print("load_dotenv()  # 加载 .env 文件")
print()
print("import os")
print("api_key = os.environ.get('OPENAI_API_KEY')")
print("```")
print()

# ============================================================================
# Part 4: 创建虚拟环境
# ============================================================================

print("【Part 4: 创建虚拟环境】")
print("-" * 70)
print()

print("使用虚拟环境可以隔离项目依赖，避免冲突。")
print()

print("创建虚拟环境：")
print()
print("```bash")
print("# 创建虚拟环境")
print("python -m venv venv")
print()
print("# 激活虚拟环境")
print("# Linux/Mac:")
print("source venv/bin/activate")
print()
print("# Windows:")
print("venv\\Scripts\\activate")
print()
print("# 退出虚拟环境")
print("deactivate")
print("```")
print()

# ============================================================================
# Part 5: 快速测试
# ============================================================================

print("【Part 5: 快速测试】")
print("-" * 70)
print()

print("运行以下代码测试环境：")
print()

test_code = '''
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试导入
try:
    from langchain_openai import ChatOpenAI
    print("✅ langchain-openai 导入成功")
except ImportError as e:
    print(f"❌ langchain-openai 导入失败: {e}")

try:
    from langgraph.graph import StateGraph
    print("✅ langgraph 导入成功")
except ImportError as e:
    print(f"❌ langgraph 导入失败: {e}")

# 测试 OpenAI API
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print(f"✅ OPENAI_API_KEY 已设置（长度：{len(api_key)}）")

    # 测试调用
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        response = llm.invoke("Hello!")
        print(f"✅ OpenAI API 调用成功")
    except Exception as e:
        print(f"⚠️  OpenAI API 调用失败: {e}")
else:
    print("⚠️  OPENAI_API_KEY 未设置")
'''

print("```python")
print(test_code.strip())
print("```")
print()

# ============================================================================
# Part 6: 常见问题
# ============================================================================

print("【Part 6: 常见问题】")
print("-" * 70)
print()

faqs = [
    {
        "问题": "ImportError: No module named 'langchain'",
        "解决": "运行：pip install langchain"
    },
    {
        "问题": "OpenAI API 调用失败",
        "解决": "检查 OPENAI_API_KEY 是否正确设置，检查账户余额"
    },
    {
        "问题": "pip install 速度慢",
        "解决": "使用国内镜像：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple langchain"
    },
    {
        "问题": "Python 版本过低",
        "解决": "升级 Python 到 3.8 或更高版本"
    },
    {
        "问题": "虚拟环境激活失败",
        "解决": "检查激活脚本路径，确保使用正确的斜杠（/ 或 \\）"
    }
]

for i, faq in enumerate(faqs, 1):
    print(f"Q{i}: {faq['问题']}")
    print(f"A{i}: {faq['解决']}")
    print()

# ============================================================================
# 总结
# ============================================================================

print("【总结】")
print("-" * 70)
print()

print("环境检查步骤：")
print()
print("1. ✅ 检查系统信息（操作系统、Python 版本）")
print("2. ✅ 检查 pip 是否可用")
print("3. ✅ 检查核心包是否已安装")
print("4. ✅ 检查环境变量是否已设置")
print("5. ✅ 安装缺失的依赖")
print("6. ✅ 配置环境变量")
print("7. ✅ 运行测试代码验证")
print()

print("环境检查的重要性：")
print()
print("- 提前发现问题，避免运行时错误")
print("- 确保依赖版本兼容")
print("- 验证环境配置正确")
print("- 提高开发效率")
print()

print("=" * 70)
print("环境检查指南完成！")
print("=" * 70)

# 打印最终摘要
print()
checker.print_summary()
