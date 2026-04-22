import os


from openai import OpenAI
from get_api import get_openai_key

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=get_openai_key(),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# noinspection PyTypeChecker
response = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},#系统设定
        {"role": "user", "content": "你是谁？"},#用户语言
    ]
)
print(response.model_dump_json())
print(response.choices[0].message.content)#json,字典{}直接用key找-->choices，
# []数组用索引[0]找到第一项，其是个字典，再从中逐级提取