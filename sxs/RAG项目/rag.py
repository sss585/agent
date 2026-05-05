from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import get_history
from openai import embeddings
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.globals import set_debug




def print_prompt(prompt):#输出提示词
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    print()

    return prompt

class RagService(object):#object是所有东西的基类，相当于没写
    #创造chain，包括集成模板和历史记录
    def __init__(self): #构造函数
        self.vector_store = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name,dashscope_api_key=config.OPENAI_API_KEY)#千文出的向量提取模型
        )#生成一个向量储存库的实例
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system", "并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),#将以history为键值对的历史记录放到此处
                ("user", "请回答用户提问：{input}"),

            ]

        )
        self.chat_model = ChatTongyi(model=config.chat_model_name,api_key=config.OPENAI_API_KEY)#加入模型
        self.chain=self.__get__chain()#自动生成，以便后续调用


    def __get__chain(self):#获取最后成品链,都要传入自身#可以集成到init里面
        retriever=self.vector_store.get_retriever()#获取向量储存数据库实例

        def format_docment(docs:list[Document]):#将list里的东西转换成字符串
            if not docs:
                return "无资料"

            formatted_string=""
            for doc in docs:
                formatted_string += f"文档片段:{doc.page_content}\n文档元数据{doc.metadata}\n\n"
            return formatted_string
        def show(value):
            print(f"🔍  接收到的类型: {type(value)}")
            print(f"🔍 调试内容: {value}1")
            return value

        def format_for_retriever(value:dict)->str:#提取input内容

            return value["input"]#-->dict键值对的提取方式

        def print_promptshow(full_prompt):
            print("=" * 20, full_prompt, "=" * 20)
            return full_prompt

        def format_for_prompt_template(value):#改格式
            # {input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value
        # def format_for_prompt_template(value:dict):
        #     new_value={}
        #     return value["context"]

        chain=(
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(format_for_retriever)|retriever|format_docment
            }|RunnableLambda(format_for_prompt_template)|self.prompt_template|print_prompt|self.chat_model|StrOutputParser()
            #chain中，由invoke调用，则后续全部自动调用invoke函数，自定义由lambda函数自动转换，stroutparser是个类，需要先实例化
        )


        conversation_chain=RunnableWithMessageHistory(#获得可带历史记录的加强链
            chain,
            get_history,
            input_messages_key="input",#指出用户插入处,有s，写错会自动退化
            history_messages_key="history",#指出历史记录插入处
        )
        return conversation_chain
if __name__=="__main__":#当前为主函数时

    # }#configurable"：这是 LangChain 的一个标准协议。它把“运行时配置”和“输入数据”区分开。
   #  get_history(session_id="user_001").clear()
    respose=(RagService().chain.invoke({"input":"回答我1+1=？"},config=config.session_config))#先生成类实例再调用
    #只是config，不能相信补全
    print(respose)

