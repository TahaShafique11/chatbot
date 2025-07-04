import streamlit as st
import ollama
import re

st.set_page_config(page_title="LeadBot", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: white;
        color: black;
    }
    .main {
        background-color: white;
    }
    .bubble-user {
        background-color: #a149fa;
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 80%;
        align-self: flex-end;
        text-align: right;
    }
    .bubble-bot {
        background-color: #eeeeee;
        color: black;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 80%;
        align-self: flex-start;
        text-align: left;
    }
    .chat-row {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .chat-header {
        background: #a149fa;
        color: white;
        padding: 15px;
        border-radius: 20px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    input[type="text"] {
        background-color: #a149fa !important;
        color: black !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-header">🤖 LeadBot • Online Now</div>', unsafe_allow_html=True)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    role = msg['role']
    content = msg['content']
    bubble_class = "bubble-user" if role == 'user' else "bubble-bot"
    st.markdown(f'<div class="chat-row"><div class="{bubble_class}">{content}</div></div>', unsafe_allow_html=True)

# Input field
user_input = st.chat_input("Reply to LeadBot...")

# Handle input
if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    response = ollama.chat(
        model='qwen3:1.7b',
        messages=st.session_state.messages
    )
    bot_reply = response['message']['content']
    bot_reply = re.sub(r'<think>.*?</think>', '', bot_reply, flags=re.DOTALL).strip()
    st.session_state.messages.append({'role': 'assistant', 'content': bot_reply})
    
    st.rerun()  # shows the message immediately
