from get_api import get_openai_key
from langchain_community.embeddings import DashScopeEmbeddings
my_key = get_openai_key()
# 创建模型对象 不传model默认用的是 text-embeddings-v1
model = DashScopeEmbeddings(dashscope_api_key=my_key)

# 不用invoke stream
# embed_query、embed_documents
print(model.embed_query("我喜欢你"))#query单次转换
print(model.embed_documents(["我喜欢你", "我稀饭你", "晚上吃啥"]))#doucment([a,c,b])多个转换
#用于提取文本的向量形式