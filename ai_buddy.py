import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="AI Buddy", page_icon="🤖")

st.title("🤖 AI Buddy")
st.write("Emaina adugu, nenu ChatGPT laga reply istha 😎")

# 1. API Key Input
api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_... tho start avvadi")

if api_key:
    client = Groq(api_key=api_key)
    
    # 2. Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 3. Previous messages chupinchadam
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. New message input
    if prompt := st.chat_input("Nenu emi cheyyali?"):
        # User message ni save cheyi
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 5. AI Reply
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are AI Buddy. Always reply in English language in a friendly way."}
                        ] + st.session_state.messages,
                        model="llama-3.1-8b-instant", # Idi free and best model
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    reply = chat_completion.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                
                except Exception as e:
                    st.error(f"Error vachindi: {e}")
                    st.error("API Key check cheyi leda model name check cheyi")
else:
    st.info("Mundhu Groq API Key pettu bro 👆")
