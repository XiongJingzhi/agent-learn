# 06. 环境检查练习题 - Level 0

> **对应 Note**: `notes/06_environment_check_guide.md`
> **对应 Example**: `examples/06_environment_check.py`
> **目标**: 测试你对 Agent 开发环境配置的理解

---

## 📊 练习统计

- **总题数**: 25 题
- **选择题**: 10 题
- **填空题**: 5 题
- **简答题**: 5 题
- **实操题**: 5 题
- **预计时间**: 35 分钟

---

## 🎯 选择题（1-10）

### 第 1 部分：环境检查（1-5）

**Q1. Agent 开发的最低 Python 版本要求是：**

A. Python 3.6+
B. Python 3.7+
C. Python 3.8+
D. Python 3.10+

**答案**: C

---

**Q2. 检查 Python 版本的命令是：**

A. python --version
B. python --info
C. python version
D. python -v

**答案**: A

---

**Q3. 以下哪个不是 LangChain 的核心包？**

A. langchain
B. langgraph
C. langchain-openai
D. langchain-extra

**答案**: D

**解析**: langchain-extra 不是官方核心包。

---

**Q4. 安装 Python 包的命令是：**

A. python install package
B. pip install package
C. python get package
D. pip package install

**答案**: B

---

**Q5. 检查已安装包的版本，应该使用：**

A. pip list
B. pip show package
C. pip info package
D. pip version package

**答案**: B

**解析**: pip show 可以显示包的详细信息，包括版本。

---

### 第 2 部分：环境配置（6-10）

**Q6. 创建虚拟环境的命令是：**

A. python venv venv
B. python -m venv venv
C. venv create
D. virtualenv create

**答案**: B

---

**Q7. 激活虚拟环境的命令（Linux/Mac）是：**

A. source venv/activate
B. source venv/bin/activate
C. venv/bin/activate
D. activate venv

**答案**: B

---

**Q8. .env 文件的主要作用是：**

A. 存储代码
B. 存储环境变量
C. 存储日志
D. 存储配置

**答案**: B

---

**Q9. OpenAI API 密钥的环境变量名是：**

A. API_KEY
B. OPENAI_KEY
C. OPENAI_API_KEY
D. AI_API_KEY

**答案**: C

---

**Q10. 使用 python-dotenv 加载 .env 文件的函数是：**

A. load_env()
B. load_dotenv()
C. read_dotenv()
D. parse_dotenv()

**答案**: B

---

## 🔤 填空题（11-15）

**Q11. 虚拟环境可以隔离不同项目的 _______。**

**答案**: 依赖（或依赖包）

---

**Q12. 在虚拟环境中，pip 安装的包会保存在 _______ 目录中。**

**答案**: venv（或虚拟环境目录）

---

**Q13. 导入 langchain 时，如果出现 ModuleNotFoundError，说明 _______。**

**答案**: 包未安装（或 langchain 未安装）

---

**Q14. OpenAI API 调用需要设置 _______ 环境变量。**

**答案**: OPENAI_API_KEY

---

**Q15. requirements.txt 文件列出了项目所需的 _______。**

**答案**: 所有依赖包（或依赖）

---

## 📝 简答题（16-20）

**Q16. 为什么需要使用虚拟环境？**

**答案**:
1. **隔离依赖**：不同项目的依赖不会相互冲突
2. **版本控制**：可以为不同项目使用不同版本的包
3. **环境干净**：保持全局 Python 环境的整洁
4. **便于管理**：可以轻松删除或重建环境
5. **团队协作**：确保团队成员使用相同的环境

---

**Q17. 环境检查的主要步骤有哪些？**

**答案**:
1. 检查 Python 版本（3.8+）
2. 检查 pip 版本
3. 检查核心包是否已安装（langchain, langgraph 等）
4. 检查环境变量是否已设置（OPENAI_API_KEY）
5. 运行测试代码验证环境

---

**Q18. 如何设置 OpenAI API 密钥？**

**答案**:
有三种方法：

1. **直接设置（临时）**：
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

2. **使用 .env 文件（推荐）**：
   创建 .env 文件：
   ```
   OPENAI_API_KEY=your-api-key
   ```
   然后在代码中加载：
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

3. **在代码中设置**：
   ```python
   import os
   os.environ['OPENAI_API_KEY'] = 'your-api-key'
   ```

---

**Q19. requirements.txt 的格式是什么？**

**答案**:
requirements.txt 每行一个包，格式如下：

```
# 基本格式
package_name

# 指定版本
package_name==1.0.0

# 版本范围
package_name>=1.0.0
package_name~=1.0.0

# 从 GitHub 安装
git+https://github.com/user/repo.git

# 包含额外内容
package-name[extra]
```

示例：
```
langchain>=0.1.0
langgraph>=0.1.0
langchain-openai>=0.0.1
python-dotenv>=1.0.0
```

---

**Q20. 如何验证环境配置是否正确？**

**答案**:
可以运行以下测试代码：

```python
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试导入
try:
    from langchain_openai import ChatOpenAI
    print("✅ langchain-openai 导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")

# 测试 API 密钥
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print(f"✅ OPENAI_API_KEY 已设置")

    # 测试调用
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        response = llm.invoke("Hello!")
        print(f"✅ API 调用成功")
    except Exception as e:
        print(f"⚠️ API 调用失败: {e}")
else:
    print("❌ OPENAI_API_KEY 未设置")
```

---

## 💡 实操题（21-25）

**Q21. 创建一个 requirements.txt 文件**

**要求**: 包含以下包：
- langchain (>= 0.1.0)
- langgraph (>= 0.1.0)
- langchain-openai (>= 0.0.1)
- python-dotenv (>= 1.0.0)

**答案**:
```
langchain>=0.1.0
langgraph>=0.1.0
langchain-openai>=0.0.1
python-dotenv>=1.0.0
```

---

**Q22. 创建一个 .env 文件**

**要求**: 包含以下环境变量：
- OPENAI_API_KEY
- LANGCHAIN_API_KEY (可选)
- LANGCHAIN_TRACING_V2 (可选)

**答案**:
```env
# OpenAI API
OPENAI_API_KEY=sk-your-api-key-here

# LangChain (可选)
LANGCHAIN_API_KEY=lsv2-your-api-key-here
LANGCHAIN_TRACING_V2=true
```

---

**Q23. 写一个环境检查脚本**

**要求**:
1. 检查 Python 版本
2. 检查核心包是否已安装
3. 检查 OPENAI_API_KEY 是否已设置

**答案**:
```python
import sys
import os
from typing import List, Tuple

def check_python_version(min_version: Tuple[int, int] = (3, 8)) -> bool:
    """检查 Python 版本"""
    current = sys.version_info[:2]
    if current >= min_version:
        print(f"✅ Python 版本：{'.'.join(map(str, current))}")
        return True
    else:
        print(f"❌ Python 版本过低：{'.'.join(map(str, current))} < {'.'.join(map(str, min_version))}")
        return False

def check_packages(packages: List[str]) -> bool:
    """检查包是否已安装"""
    all_installed = True
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            all_installed = False
    return all_installed

def check_env_vars() -> bool:
    """检查环境变量"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY 已设置（长度：{len(api_key)}）")
        return True
    else:
        print("❌ OPENAI_API_KEY 未设置")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("Agent 开发环境检查")
    print("=" * 50)
    print()

    # 检查 Python 版本
    python_ok = check_python_version()
    print()

    # 检查包
    packages = ["langchain", "langgraph", "langchain_openai", "dotenv"]
    packages_ok = check_packages(packages)
    print()

    # 检查环境变量
    env_ok = check_env_vars()
    print()

    # 总结
    print("=" * 50)
    if python_ok and packages_ok and env_ok:
        print("✅ 环境检查全部通过！")
    else:
        print("❌ 环境检查未通过，请修复问题")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

---

**Q24. 写一个一键安装脚本的命令序列**

**要求**: 从零开始搭建 Agent 开发环境

**答案**:
```bash
# 1. 检查 Python 版本
python --version

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境（Linux/Mac）
source venv/bin/activate

# 3. 激活虚拟环境（Windows）
# venv\Scripts\activate

# 4. 升级 pip
pip install --upgrade pip

# 5. 安装依赖
pip install langchain langgraph langchain-openai python-dotenv

# 6. 验证安装
python -c "import langchain; print(langchain.__version__)"
python -c "import langgraph; print('LangGraph installed')"

# 7. 创建 .env 文件
echo "OPENAI_API_KEY=your-api-key" > .env

# 8. 运行测试
python test_environment.py
```

---

**Q25. 写一个完整的环境检查和修复脚本**

**答案**:
```python
import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd: List[str]) -> Tuple[bool, str]:
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def check_and_fix_environment():
    """检查并修复环境"""
    print("🔍 Agent 开发环境检查与修复")
    print("=" * 50)
    print()

    issues = []
    fixes = []

    # 1. 检查 Python 版本
    print("1. 检查 Python 版本...")
    if sys.version_info < (3, 8):
        issues.append("Python 版本过低")
        fixes.append("请升级 Python 到 3.8 或更高版本")
    else:
        print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print()

    # 2. 检查虚拟环境
    print("2. 检查虚拟环境...")
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print(f"   ✅ 在虚拟环境中：{sys.prefix}")
    else:
        issues.append("未使用虚拟环境")
        fixes.append("建议创建虚拟环境：python -m venv venv && source venv/bin/activate")
    print()

    # 3. 检查包
    print("3. 检查核心包...")
    packages = {
        "langchain": "langchain",
        "langgraph": "langgraph",
        "langchain_openai": "langchain-openai",
        "dotenv": "python-dotenv"
    }

    for module, package in packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            issues.append(f"{package} 未安装")
            fixes.append(f"安装：pip install {package}")
    print()

    # 4. 检查 .env 文件
    print("4. 检查 .env 文件...")
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ .env 文件存在")
    else:
        issues.append(".env 文件不存在")
        fixes.append("创建 .env 文件并设置 OPENAI_API_KEY")
    print()

    # 5. 检查环境变量
    print("5. 检查环境变量...")
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print(f"   ✅ OPENAI_API_KEY 已设置（长度：{len(api_key)}）")
    else:
        issues.append("OPENAI_API_KEY 未设置")
        fixes.append("在 .env 文件中设置 OPENAI_API_KEY=your-key")
    print()

    # 总结
    print("=" * 50)
    if not issues:
        print("✅ 环境检查全部通过！")
    else:
        print(f"⚠️  发现 {len(issues)} 个问题：")
        print()
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        print()
        print("建议的修复方法：")
        print()
        for i, fix in enumerate(fixes, 1):
            print(f"{i}. {fix}")
    print("=" * 50)

if __name__ == "__main__":
    check_and_fix_environment()
```

---

## 🎯 学习建议

1. **先阅读 note**: `notes/06_environment_check_guide.md`
2. **再运行 example**: `examples/06_environment_check.py`
3. **最后完成练习**: 本练习题

---

## ✅ 完成标准

- [ ] 完成 10 道选择题
- [ ] 完成 5 道填空题
- [ ] 完成 5 道简答题
- [ ] 完成 5 道实操题
- [ ] 正确率 >= 80%
- [ ] 成功搭建开发环境
- [ ] 通过环境检查脚本
- [ ] 能够运行基本的 Agent 代码

---

**恭喜完成 Level 0 所有练习！** 🎉

**下一步**: 完成 `projects/00_hello_project.md` 🚀
