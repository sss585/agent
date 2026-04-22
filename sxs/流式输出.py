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
        {"role": "system", "content": "你是一只猫娘，称呼我为狗修金桑麻，说完每句话要带上“喵~”，回答完我的问题会告诉我消耗了多少token，分成输入和输出，总消耗"},#系统设定
        {"role": "assistant", "content": "狗修金好，我是ai酱，喵"},  # 系统输出,即历史记录，用于丰富设定
        {"role": "user", "content": "对我表示爱意"}#用户输入


    ],
    stream=True,
    extra_body={"include_usage": True}
)

for chunk in response:#chunk：这是循环中每一次取到的单个数据包。
    print(chunk.choices[0].delta.content,
          end=' ', flush=True
    )
if hasattr(response, 'usage') and response.usage:
    print(f"\n\n--- Token统计 ---")
    print(f"输入Token: {response.usage.prompt_tokens}")
    print(f"输出Token: {response.usage.completion_tokens}")
    print(f"总消耗: {response.usage.total_tokens}")