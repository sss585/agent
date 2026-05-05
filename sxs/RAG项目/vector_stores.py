from langchain_chroma import Chroma
import config_data as config

class VectorStoreService:
    def __init__(self,embedding):
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config.collection_name,#表名
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):#返回向量库做成的检索器
        return self.vector_store.as_retriever(serch_kwargs={"k": config.similarity_threshold})#设置返回前一条匹配的




if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4",dashscope_api_key=config.OPENAI_API_KEY)).get_retriever()

    res = retriever.invoke("我的体重180斤，尺码推荐")
    print(res)

