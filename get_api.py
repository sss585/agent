import os
import openai
from dotenv import load_dotenv, find_dotenv
def get_openai_key():
    _ = load_dotenv(find_dotenv())#寻找.enc文件，将其中键值对加入（临时）环境变量中
    #_是一个合法变量，但是一般作为一个占位符，表示不关心返回值
    return os.environ['OPENAI_API_KEY']#从临时变量中取出
#缩进相同即可
#print(openai.api_key = get_openai_key())
#会出错，因为python的=只是动作，没有返回值不能输出