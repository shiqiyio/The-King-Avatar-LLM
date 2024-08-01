import streamlit as st
from ragchat import Model_center
from llm import InternLM

'''
通过 @st.cache_resource 装饰器，load_model 函数只会在首次调用时执行，确保模型只加载一次。随后每次用户交互时，代码将使用已加载的模型。
'''
@st.cache_resource
def load_model(model_name_or_path):
    llm = InternLM(model_path=model_name_or_path)
    model_center = Model_center(llm)
    return model_center

# 加载模型，只执行一次
model_name_or_path ='/root/share/new_models/qwen/Qwen2-7B-Instruct'
model_center = load_model(model_name_or_path)

# model_center = Model_center(llm)
if "messages" not in st.session_state:
    st.session_state["messages"] = []     
# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    st.markdown("The-King-Avatar-LLM")
    "[InternLM](https://github.com/InternLM/InternLM.git)"
    "[chat-huyu-ABao](https://github.com/shiqiyio/The-King-Avatar-LLM)"
    "感谢[chat-huyu-ABao](https://github.com/hoo01/chat-huyu-ABao.git)"

# 创建一个标题和一个副标题
st.title("The-King-Avatar-LLM")
st.caption("🚀 A streamlit chatbot powered by InternLM2_7B QLora")
    
# 遍历session_state中的所有消息，并显示在聊天界面上
for msg in st.session_state.messages:
    st.chat_message("user").write(msg["user"])
    st.chat_message("assistant").write(msg["assistant"])

# Get user input
if prompt := st.chat_input("提出任何关于《全职高手》的问题"):
    # Display user input
    st.chat_message("user").write(prompt)
        # 使用 qa_chain 生成回答
    response = model_center.qa_chain_self_answer(prompt)
    
    # 将问答结果添加到 session_state 的消息历史中
    st.session_state.messages.append({"user": prompt, "assistant": response}) 
    # 显示回答
    st.chat_message("assistant").write(response)