import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Buddy", page_icon="🤖", layout="centered")
st.title("🤖 AI Buddy")
st.write("Emaina adugu, nenu ChatGPT laga reply istha 😎")

# API key ni sidebar lo aduguthundi
api_key = st.text_input("Groq API Key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Nenu emi cheyyali?")

if prompt and api_key:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=api_key)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AI Buddy. Reply in Telugu + English mix. Be friendly and helpful."},
                    *st.session_state.messages
                ],
                model="llama3-8b-8192",
            )
            reply = chat_completion.choices[0].message.content
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

elif prompt and not api_key:
    st.warning("Paina sidebar lo Groq API Key pettu bro!")