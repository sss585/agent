OPENAI_API_KEY="sk-9a7479f5fe934023acc880947d0e5bee"

md5_path = "./md5.text"#md5存储路径
history_path = "./chat_history_store"

# Chroma
collection_name = "rag"#表名
persist_directory = "./chroma_db"#存储路径


# spliter
chunk_size = 1000#分片大小
chunk_overlap = 100#上下文重叠大小
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]#分割符号
max_split_char_number = 1000        # 文本分割的阈值

#
similarity_threshold = 1            # 检索返回匹配的文档数量

embedding_model_name = "text-embedding-v4"#向量模型,不能和聊天模型混用
chat_model_name = "qwen3-max"#LLM，輸錯同上報錯url

session_config = {#会话的配置文件
        "configurable": {
            "session_id": "user_001",
        }
    }
