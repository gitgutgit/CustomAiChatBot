import streamlit as st
from utils import print_messages, StreamHandler
from openai import OpenAI, AssistantEventHandler
import re  # 정규 표현식을 사용하기 위한 import
import logging  # 로그 출력을 위한 import

import os
import toml
import uuid
import time

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="TVCF 고객센터", 
    page_icon="https://www.tvcf.co.kr/images/RenewV1.1/logo.svg"  # Replace with your icon URL
)

# Hide the options menu (three dots)
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add company logo and title
st.markdown(
    """
    <style>
    .header {
        display: flex;
        align-items: center;
        padding: 10px 0;
    }
    .header img {
        height: 40px;
        margin-right: 10px;
    }
    .header h1 {
        font-size: 24px;
        margin: 0;
    }
    </style>
    <div class="header">
        <img src="https://www.tvcf.co.kr/images/RenewV1.1/logo.svg" alt="Company Logo">
        <h1>TVCF 고객센터</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Setup logging directly in the script
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

custom_spinner_css = """
<style>
.loader {
  width: 60px;
  aspect-ratio: 4;
  --c:rgba(255, 140, 0, 0.7) 90%,#0000;
  background: 
    radial-gradient(circle closest-side at left  6px top 50%,var(--c)),
    radial-gradient(circle closest-side                     ,var(--c)),
    radial-gradient(circle closest-side at right 6px top 50%,var(--c));
  background-size: 100% 100%;
  background-repeat: no-repeat;
  animation: l4 1s infinite alternate;
  position: relative;
  left: 80px;
}
@keyframes l4 {    to{width:25px;aspect-ratio: 1}
}
</style>
"""

# API KEY 설정
secrets = toml.load("api_secrets.toml")
os.environ["OPENAI_API_KEY"] = secrets["openai"]["api_key"]

# OpenAI 클라이언트 생성
client = OpenAI()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 채팅 대화기록을 저장하는 store 세션 상태 변수   
if "store" not in st.session_state:
    st.session_state["store"] = dict()

# Assistant 생성 또는 업데이트
if "assistant_id" not in st.session_state:
    assistant_id = secrets["openai"]["assistant_id"]
    st.session_state.assistant_id = assistant_id
else:
    # Update the Assistant with the vector_store_ids
    client.beta.assistants.update(
        assistant_id=st.session_state.assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [secrets["openai"]["vector_id"]]}},
    )

# Thread 생성
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# 스트리밍 중인지 여부를 저장할 변수
if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False

# 봇의 첫 인사말
if not st.session_state["messages"]:
    initial_message = "안녕하세요! TVCF 고객센터입니다. 무엇을 도와드릴까요?"
    st.session_state["messages"].append({"role": "assistant", "content": initial_message})
    # st.chat_message("assistant").write(initial_message)

# 이전 대화기록을 출력해 주는 코드
if st.session_state["messages"]:
    for chat_message in st.session_state["messages"]:
        if chat_message["role"] == "user":
            st.markdown(
                f'<div style="display: flex; align-items: center; justify-content: flex-end; margin-left: 20%;">'
                f'<div style="background-color: rgba(255, 255, 0, 0.3); padding: 5px 10px; border-radius: 10px;">{chat_message["content"]}</div>'
                f'</div>', unsafe_allow_html=True
            )
        else:
            st.chat_message(chat_message["role"]).write(chat_message["content"])

if not st.session_state.is_streaming and (user_input := st.chat_input("TVCF에 대한 궁금증을 입력하세요.")):
    # 사용자가 입력한 내용
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.markdown(
        f'<div style="display: flex; align-items: center; justify-content: flex-end; margin-left: 20%;">'
        f'<div style="background-color: rgba(255, 255, 0, 0.3); padding: 5px 10px; border-radius: 10px;">{user_input}</div>'
        f'</div>', unsafe_allow_html=True
    )

    # Thread에 메시지 추가
    message = client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    # Assistant의 아바타를 생성
    assistant_avatar = st.chat_message("assistant")

    # 아바타 아래에 스트리밍 응답을 출력할 빈 컨테이너 생성
    response_container = assistant_avatar.empty()

    # 현재 응답을 초기화
    st.session_state.current_response = ""

    # 이벤트 핸들러 정의
    class EventHandler(AssistantEventHandler):    
        def on_text_delta(self, delta, snapshot):
            st.session_state.current_response += delta.value
            clean_response = re.sub(r'.\d+:\d+†source.', '', st.session_state.current_response)
            response_container.markdown(clean_response, unsafe_allow_html=True)

    # 스트리밍 중임을 표시
    st.session_state.is_streaming = True
    
    # 스피너 표시
    spinner_container = st.empty()
    with spinner_container.container():
        st.write(custom_spinner_css, unsafe_allow_html=True)
        st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
    
    # 스트리밍
    try:
        with client.beta.threads.runs.stream(
            thread_id=st.session_state.thread_id,
            assistant_id=st.session_state.assistant_id,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()
    except Exception as e:
        logger.error(f"Error during streaming: {str(e)}")
        st.error("An error occurred while processing your request.")

    # 스피너 제거
    spinner_container.empty()

    # 스트리밍 완료
    st.session_state.is_streaming = False

    # 터미널에 원본 소스 답변과 클린 답변을 출력
    logger.info(f"User Input: {user_input}")
    clean_response = re.sub(r'.\d+:\d+†source.', '', st.session_state.current_response)
    logger.info(f"Assistant Response (Cleaned): {clean_response}")

    # 대화 내용 저장
    st.session_state["messages"].append({"role": "assistant", "content": clean_response})
