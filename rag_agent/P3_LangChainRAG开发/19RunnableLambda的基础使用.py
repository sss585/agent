from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model="qwen3-max")
str_parser = StrOutputParser()

first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起名字，仅生成一个名字，并告知我名字，不要额外信息。"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name}，请帮我解析含义。"
)

# 函数的入参：AIMessage -> dict  ({"name": "xxx"})
# my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})
# add = lambda x, y: x + y
'''是单引号
ai_msg: ... (输入参数)
ai_msg 是这个函数的参数名。
在这个语境下，它通常代表一个 Message 对象（例如 LangChain 中的 AIMessage）。这个对象里包含了 AI 回复的所有信息（内容、角色、时间戳等）。
{"name": ai_msg.content} (返回值)
这是函数执行后的返回结果。
它创建了一个 Python 字典 {"key": "value"}。
键 (key) 是字符串 "name"。
值 (value) 是 ai_msg.content。意思是：读取 ai_msg 这个对象里的 content 属性（即 AI 说的具体文本内容），并把它赋值给字典的 "name" 字段。
'''



chain = first_prompt | model | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | model | str_parser

for chunk in chain.stream({"lastname": "曹", "gender": "女孩"}):
    print(chunk, end="", flush=True)
