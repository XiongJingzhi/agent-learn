"""
07_langchain_basics.py
LangChain 基础示例

展示 LangChain 的六大核心组件
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent

# ==================== 示例 1：Model I/O ====================

print("\n" + "="*60)
print("示例 1：Model I/O - 基础的 LLM 调用")
print("="*60 + "\n")

# 创建 LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 简单调用
message = "用一句话介绍 LangChain"
response = llm.invoke(message)

print(f"用户: {message}")
print(f"AI: {response.content}\n")


# ==================== 示例 2：Chains ====================

print("\n" + "="*60)
print("示例 2：Chains - 连接多个组件")
print("="*60 + "\n")

# 创建提示模板
prompt = ChatPromptTemplate.from_template(
    "你是一个{role}。请用简单的语言解释：{topic}"
)

# 创建 Chain
chain = LLMChain(llm=llm, prompt=prompt)

# 执行
result = chain.run(
    role="小学老师",
    topic="什么是人工智能？"
)

print(f"角色: 小学老师")
print(f"解释: {result}\n")


# ==================== 示例 3：带记忆的对话 ====================

print("\n" + "="*60)
print("示例 3：Memory - 记住对话历史")
print("="*60 + "\n")

# 创建记忆
memory = ConversationBufferMemory()

# 创建对话 Chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# 第一轮对话
print("第一轮对话：")
response1 = conversation.predict(input="我喜欢吃苹果")
print(f"用户: 我喜欢吃苹果")
print(f"AI: {response1}\n")

# 第二轮对话
print("第二轮对话：")
response2 = conversation.predict(input="我最喜欢的水果是什么？")
print(f"用户: 我最喜欢的水果是什么？")
print(f"AI: {response2}\n")

print("✓ AI 记住了你喜欢的水果！\n")


# ==================== 示例 4：Tools ====================

print("\n" + "="*60)
print("示例 4：Tools - 定义和使用工具")
print("="*60 + "\n")

# 定义工具
@tool
def calculator(expression: str) -> str:
    """计算数学表达式，如 '2 + 2' 或 '10 * 5'"""
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{str(e)}"

@tool
def get_word_length(word: str) -> str:
    """返回单词的长度"""
    return f"单词 '{word}' 有 {len(word)} 个字母"

# 使用工具
print("工具 1：计算器")
calc_result = calculator.invoke("2 + 2 * 3")
print(f"{calc_result}\n")

print("工具 2：单词长度")
length_result = get_word_length.invoke("LangChain")
print(f"{length_result}\n")


# ==================== 示例 5：Agent ====================

print("\n" + "="*60)
print("示例 5：Agent - 自主使用工具")
print("="*60 + "\n")

# 准备工具列表
tools = [calculator, get_word_length]

# 创建 Agent
# 注意：ReAct agent 需要 langchainhub 安装
try:
    from langchain import hub

    # 获取 ReAct 提示模板
    prompt = hub.pull("hwchase17/react")

    # 创建 Agent
    agent = create_react_agent(llm, tools, prompt)

    # 创建执行器
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    # 执行
    print("执行任务：计算 5 + 3，并告诉我 'Python' 这个单词有多长\n")
    result = agent_executor.invoke({
        "input": "请计算 5 + 3，然后告诉我 'Python' 这个单词有多长"
    })

    print(f"\n最终结果: {result['output']}")

except Exception as e:
    print(f"Agent 执行遇到问题: {e}")
    print("提示：确保已安装 langchainhub: pip install langchainhub\n")


# ==================== 总结 ====================

print("\n" + "="*60)
print("总结：LangChain 六大核心组件")
print("="*60 + "\n")

components = """
1. Model I/O  - 与 LLM 交互的基础接口
2. Chains     - 连接多个组件形成处理流程
3. Agents     - 自主决策并使用工具
4. Tools      - 执行具体操作的函数
5. Memory     - 保存和检索对话历史
6. Retrieval  - 从文档中检索相关信息
"""

print(components)

print("💡 提示：")
print("  - 从简单开始：先用 Model I/O 和 Chains")
print("  - 逐步进阶：学习 Agents 和 Tools")
print("  - 查阅文档：https://python.langchain.com/")
print("  - 多做实验：修改参数，观察效果\n")

print("✓ 恭喜你完成了 LangChain 基础学习！")
