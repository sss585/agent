import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
import config_data as config
#from rag_agent.P4_RAG项目案例.file_history_store import FileChatMessageHistory


#
#
def get_history(session_id):#创建历史记录的实例
    return FileChatMessageHistory(session_id,config.history_path)#对应文件夹下的对应文件

class  FileChatMessageHistory(BaseChatMessageHistory):#Base为Lang里对于管理历史记录的一个基类，也是一个标准规范
#规定必须要有 add，获取，clear等功能
    def __init__(self,session_id,storage_path):#storage储存
        self.session_id = session_id  # 会话id
        self.storage_path = storage_path    # 不同会话id的存储文件，所在的文件夹路径

        self.file_path=os.path.join(self.storage_path,"file_history.json")#根据系统拼接路径join                                                                                                                                                          os.makedirs(self.storage_path,exist_ok=True)#手动创建以保证存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)#创建文件，保证存在

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
#统一接口,@abstractmethod: 这是一个装饰器，用来标记那些必须在子类中被实现的抽象方法。
# Sequence序列 类似list、tuple
        all_messages =list(self.messages)   #已有的消息列表
        all_messages.extend(messages) #向列表在加入
        new_messages = [message_to_dict(message) for message in all_messages]#配合格式，将list中取出Base对象，挨个变为dict，自动加入
        with open(self.file_path,"w",encoding="utf-8") as f:#打开文件，之后自动关闭
            json.dump(new_messages,f)#list转成json格式并写入文件

    @property  # @property装饰器将messages方法变成成员属性用
    def messages(self) -> Sequence[BaseMessage]:
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                return messages_from_dict(json.load(f))#以json格式提取，转成message
        except FileNotFoundError:
            return []

    def clear(self):
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)#存入空白即清空


# def get_history(session_id):
#     return FileChatMessageHistory(session_id, "./chat_history")
#
#
# class FileChatMessageHistory(BaseChatMessageHistory):
#     def __init__(self, session_id, storage_path):
#         self.session_id = session_id        # 会话id
#         self.storage_path = storage_path    # 不同会话id的存储文件，所在的文件夹路径
#         # 完整的文件路径
#         self.file_path = os.path.join(self.storage_path, self.session_id)
#
#         # 确保文件夹是存在的
#         os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
#
#     def add_messages(self, messages: Sequence[BaseMessage]) -> None:
#         # Sequence序列 类似list、tuple
#         all_messages = list(self.messages)      # 已有的消息列表
#         all_messages.extend(messages)           # 新的和已有的融合成一个list
#          new_messages = [message_to_dict(message) for message in all_messages]
#         # 将数据写入文件
#         with open(self.file_path, "w", encoding="utf-8") as f:
#             json.dump(new_messages, f)
#
#         # 将数据同步写入到本地文件中
#         # 类对象写入文件 -> 一堆二进制
#         # 为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
#         # 官方message_to_dict：单个消息对象（BaseMessage类实例） -> 字典
#         # new_messages = []
#         # for message in all_messages:
#         #     d = message_to_dict(message)
#         #     new_messages.append(d)
#
#
#     @property       # @property装饰器将messages方法变成成员属性用
#     def messages(self) -> list[BaseMessage]:
#         # 当前文件内： list[字典]
#         try:
#             with open(self.file_path, "r", encoding="utf-8") as f:
#                 messages_data = json.load(f)    # 返回值就是：list[字典]
#                 return messages_from_dict(messages_data)
#         except FileNotFoundError:
#             return []
#
#     def clear(self) -> None:
#         with open(self.file_path, "w", encoding="utf-8") as f:
#             json.dump([], f)
