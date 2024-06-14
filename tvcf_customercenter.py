import json
import time

import streamlit as st
import plotly.graph_objects as go

from openai import OpenAI
import toml
#######################################
# PREREQUISITES
#######################################
# Load custom secrets
with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)


st.set_page_config(
    page_title="Wanderlust",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Setting OpenAI API key and Assistant ID
client = OpenAI(api_key=secrets["openai"]["api_key"])

# Use the assistant_id from the custom secrets
assistant_id = secrets["openai"]["assistant_id"]


assistant_state = "assistant"
thread_state = "thread"
conversation_state = "conversation"
last_openai_run_state = "last_openai_run"

user_msg_input_key = "input_user_msg"

#######################################
# SESSION STATE SETUP
#######################################

# 사이드바 설정
with st.sidebar:
    st.title("TVCF 고객센터")
    # assistant_id와 thread_id 초기화
    if 'assistant_id' not in st.session_state:
        st.session_state.assistant_id = assistant_id
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = None
    if 'thread_messages' not in st.session_state:
        st.session_state.thread_messages = []
    if 'user_message' not in st.session_state:
        st.session_state.user_message = ""

    # Assistant ID 생성 버튼 옛날버전
    # if st.button("새로운 Assistant ID 생성"):
    #     assistant = client.beta.assistants.create(
    #         name="Math Tutor",
    #         instructions="A personal math tutor that answers math problems. Write and execute code to answer math questions.",
    #         tools=[{"type": "code_interpreter"}],
    #         model="gpt-4-1106-preview"
    #     )
    #     st.session_state.assistant_id = assistant.id
    #     st.success(f"Assistant ID created: {assistant.id}")



    # # Thread ID 생성 버튼 옛날버전
    # if st.button("새로운 Thread ID 생성"):
    #     thread = client.beta.threads.create()
    #     st.session_state.thread_id = thread.id
    #     st.success(f"Thread ID created: {thread.id}")

    thread_id = st.text_input("Thread ID")

    thread_btn = st.button("Create a new thread")


    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id

        st.subheader(f"Thread ID: {thread_id}" , divider="rainbow")
        st.info("You can use this thread ID to continue the conversation later.")


# 메인 채팅 영역 설정

if assistant_state not in st.session_state or st.session_state[assistant_state] is None:
    st.session_state[assistant_state] = client.beta.assistants.retrieve(assistant_id)

if thread_state not in st.session_state or st.session_state[thread_state] is None:
    st.session_state[thread_state] = client.beta.threads.create()
    st.session_state.thread_id = st.session_state[thread_state].id

if conversation_state not in st.session_state:
    st.session_state[conversation_state] = []

if last_openai_run_state not in st.session_state:
    st.session_state[last_openai_run_state] = None


def get_assistant_id():
    return st.session_state.assistant_id


def get_thread_id():
    if st.session_state.thread_id is None:
        st.session_state.thread_id = client.beta.threads.create().id
    return st.session_state.thread_id


def get_run_id():
    return st.session_state[last_openai_run_state].id


def on_text_input(status_placeholder):
    """Callback method for any chat_input value change"""
    if st.session_state[user_msg_input_key] == "":
        return

    client.beta.threads.messages.create(
        thread_id=get_thread_id(),
        role="user",
        content=st.session_state[user_msg_input_key],
    )
    st.session_state[last_openai_run_state] = client.beta.threads.runs.create(
        assistant_id=get_assistant_id(),
        thread_id=get_thread_id(),
    )

    completed = False

    # Polling
    with status_placeholder.status("Computing Assistant answer") as status_container:
        st.write(f"Launching run {get_run_id()}")

        while not completed:
            run = client.beta.threads.runs.retrieve(
                thread_id=get_thread_id(),
                run_id=get_run_id(),
            )

            if run.status == "requires_action":
                tools_output = []
                st.write(f"Will submit {tools_output}")
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=get_thread_id(),
                    run_id=get_run_id(),
                    tool_outputs=tools_output,
                )

            if run.status == "completed":
                st.write(f"Completed run {get_run_id()}")
                status_container.update(label="Assistant is done", state="complete")
                completed = True

            else:
                time.sleep(0.1)

    messages = client.beta.threads.messages.list(get_thread_id()).data
    st.session_state[conversation_state] = [
        (m.role, m.content[0].text.value.replace("【", "").replace("†source】", ""))
        for m in messages
    ]


def on_reset_thread():
    client.beta.threads.delete(get_thread_id())
    st.session_state[thread_state] = client.beta.threads.create()
    st.session_state.thread_id = st.session_state[thread_state].id
    st.session_state[conversation_state] = []
    st.session_state[last_openai_run_state] = None


#######################################
# SIDEBAR
#######################################

# with st.sidebar:
#     st.header("Debug")
#     st.write(st.session_state.to_dict())

#     st.button("Reset Thread", on_click=on_reset_thread)

#######################################
# MAIN
#######################################

st.title("TVCF 고객센터")
st.subheader(':blue[무엇이든 물어보세요!] :sunglasses:')

with st.container():
    for role, message in reversed(st.session_state[conversation_state]):
        with st.chat_message(role):
            st.write(message)
status_placeholder = st.empty()

st.chat_input(
    placeholder="Ask your question here",
    key=user_msg_input_key,
    on_submit=on_text_input,
    args=(status_placeholder,),
)
