import numpy as np
import streamlit as st
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]

# from langchain.chat_models import ChatOpenAI
# chat_model - ChatOpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

st.set_page_config(
    page_title="방탈출"
)
st.header("금옥여고의 비밀")
# st.subheader("맛보기")

def chat_response(word):
    with st.chat_message("assistant"):
        st.markdown(word)

# chat_response("안녕")
# chat_response("게임을 시작하고 싶으면 시작 이라고 외쳐봐")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "내 이름은 정근이라고 해"},
        {"role": "assistant", "content": "방탈출 챗봇"},
        {"role": "user", "content": "나는 금옥여자고등학교 학생이야"}
        ]

for message in st.session_state.messages[3:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("what is up?")

valid = True

if prompt == "1234":
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.messages.append({"role": "user", "content":prompt})

    with st.chat_message("assistant"):
        st.markdown("정답입니다")
                
    st.session_state.messages.append({"role": "assistant", "content":"정답입니다"})
    valid = False

if prompt and valid:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content":prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content":full_response})

print(st.session_state.messages)
