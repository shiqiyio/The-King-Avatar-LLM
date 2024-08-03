import os
import re
import logging
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from llm import InternLM
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from gen_chroma import generate_split_docs
# from modelscope import snapshot_download
# 配置日志
log_filename = 'ragchat.log' 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
split_docs = generate_split_docs()

def load_chain(split_docs,llm):
    # 加载问答链
    # 定义 Embeddings
    # local_model_path = "./text2vec-large-chinese"
    # embeddings = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese")
    # embeddings = HuggingFaceEmbeddings(model_name=local_model_path)
    embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")
    # 向量数据库持久化路径
    persist_directory = './chroma' #根据下载好的模型的路径调整，如果路径报错就写绝对路径
    
    # 加载数据库,若本地存在则加载，不存在则创建
    if os.path.exists(persist_directory):
        print("检测到数据库，加载中...")
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        print("未检测到数据库，正在创建新的向量数据库...")
        vectordb = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        vectordb.persist()
    
    retriever = vectordb.as_retriever(search_kwargs={"k": 2})
    
    # model_id = 'hooo01/chat-huyu-ABao'
  

    # 定义一个 Prompt Template
    template = """
    **Context**（背景）：
    你是一个由十七专门训练的《全职高手》小说问答模型。可以提供准确且详细的解答，帮助用户深入了解这部小说的角色、情节和背景。
    
    **Objective**（目标）：
    回答有关《全职高手》的问题，提供有价值的见解，并确保回答基于提供的上下文信息。
    
    **Structure**（结构）：
    1. 理解问题及其背景。
    2. 查阅提供的上下文信息。
    3. 使用上下文信息优先回答问题。
    4. 如果上下文信息不足，再使用模型的通用知识。
    
    **Task**（任务）：
    回答以下问题，确保回答基于上下文信息，并在必要时参考其他知识。
    
    **Action**（行动）：
    详细阅读问题，并结合上下文信息提供准确的回答。
    
    **Result**（结果）：
    提供一个详细、准确且基于上下文的信息，以解答问题并满足用户的需求。
    
    问题: {question}
    
    上下文信息：
    ···
    {context}
    ···
    
    请根据上述框架回答问题。
"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],template=template)

    # 运行 chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm,retriever=vectordb.as_retriever(),return_source_documents=True,chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})
    
    return qa_chain

class Model_center():
    """
    存储检索问答链的对象 
    """
    def __init__(self,llm):
        # 构造函数，加载检索问答链
        
        self.llm =  llm
        self.chain = load_chain(split_docs,self.llm)

    def qa_chain_self_answer(self, question):
        """
        调用问答链进行回答，如果没有找到相关文档，则使用模型自身的回答
        """
        if not question:
            return "请勿为空。"

        try:
            # 使用检索链来获取相关文档
            result = self.chain.invoke({"query": question})         
            print(f"Debugging: Result structure => {result}")
            
            if 'result' in result:
                answer = result['result']

                return answer
            else:
                print("Error: 'result' field not found in the result.")
                return "俺目前无法提供答案，请稍后再试。"
        except Exception as e:
            # 打印更详细的错误信息，包括traceback
            import traceback
            print(f"An error occurred: {e}\n{traceback.format_exc()}")
            return "俺遇到了一些技术问题，正在修复中。"



