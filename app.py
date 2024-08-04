import streamlit as st
from ragchat import Model_center
from llm import InternLM
from tts import text_to_speech
import os

def on_btn_click():
    del st.session_state.messages
    # del st.session_state.audio_file

def on_btn_click_tts(response):
    try:
        # 转换文本为语音
        print("准备转换为音频...")
        text_to_speech(response)
        
        audio_file = './data/result.mp3'
        if os.path.exists(audio_file):
            st.session_state.audio_file = audio_file  # 将音频文件路径存储在会话状态中
        else:
            st.error("音频文件未生成或路径错误")
    except Exception as e:
        st.error(f"处理语音时发生错误: {e}")

@st.cache_resource
def load_model(model_name_or_path):
    llm = InternLM(model_path=model_name_or_path)
    model_center = Model_center(llm)
    return model_center

model_name_or_path = './quanzhigaoshou'

if not os.path.exists(model_name_or_path):

    os.system('apt install git')
    os.system('apt install git-lfs')
    os.system(f'git clone https://code.openxlab.org.cn/shiqiyioo/quanzhigaoshou.git {model_name_or_path}')
    os.system(f'cd {model_name_or_path} && git lfs pull')
    print("模型下载完成")

# model_name_or_path = '/root/share/model_repos/internlm-chat-7b'
model_center = load_model(model_name_or_path)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

with st.sidebar:
    st.markdown("The-King-Avatar-LLM")
    st.markdown("[InternLM](https://github.com/InternLM/InternLM.git)")
    st.markdown("[chat-huyu-ABao](https://github.com/shiqiyio/The-King-Avatar-LLM)")
    st.markdown("感谢[chat-huyu-ABao](https://github.com/hoo01/chat-huyu-ABao.git)")
    st.button('Clear Chat History', on_click=on_btn_click)

st.title("The-King-Avatar-LLM")
st.caption("🚀 一个由 InternLM2_7B QLora 支持的 Streamlit 聊天机器人")

for msg in st.session_state.messages:
    st.chat_message("user").write(msg["user"])
    st.chat_message("assistant").write(msg["assistant"])

if prompt := st.chat_input("提出任何关于《全职高手》的问题"):
    st.chat_message("user").write(prompt)
    response = model_center.qa_chain_self_answer(prompt)
    st.session_state.messages.append({"user": prompt, "assistant": response}) 
    st.chat_message("assistant").write(response)

    # 在响应下方添加 TTS 按钮
    st.button("语音播放", on_click=on_btn_click_tts, args=(response,))

# 如果音频文件存在，则显示音频播放器
if st.session_state.audio_file:
    st.audio(st.session_state.audio_file, format='audio/mp3')
del st.session_state.audio_file
