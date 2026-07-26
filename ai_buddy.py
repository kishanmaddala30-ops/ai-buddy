import streamlit as st

st.set_page_config(page_title="AI Buddy", page_icon="🤖", layout="centered")
st.title("🤖 AI Buddy")
st.write("Emaina adugu, nenu reply istha 😊")

# Chat history kosam
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purana messages chupinchadam
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Nenu emi cheyyali?")

if prompt:
    # User message save
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI reply - Simple ga
    with st.chat_message("assistant"):
        reply = f"Nuv annavu: '{prompt}' \nNenu help chestha bro! Inkemaina kavala? 😊"
        st.markdown(reply)
    
    # AI reply save
    st.session_state.messages.append({"role": "assistant", "content": reply})