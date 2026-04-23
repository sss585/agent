# langchain_community
from langchain_community.llms.tongyi import Tongyi
from get_api import get_openai_key
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是大语言模型
my_key = get_openai_key()
#print(my_key)
model = Tongyi(model="qwen-max",api_key=my_key)

messages = [
    SystemMessage(content="你是一个边塞诗人。"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，在写一首唐诗。")
]
# 调用invoke向模型提问
# res = model.invoke(input="你是谁呀能做什么？")
#
# print(res)

res = model.stream(input=messages)

for chunk in res:
    print(chunk,end="喵~",flush=True)#流式