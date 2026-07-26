import streamlit as st

st.set_page_config(page_title="AI Buddy", page_icon="🤖", layout="centered")
st.title("🤖 AI Buddy")
st.write("Emaina adugu, nenu reply istha 😊")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Old chat history chupinchu
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Nenu emi cheyyali?")

if prompt:
    # User message add cheyi
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI reply generate cheyi - ninna style
    reply = f"Nuv adigindi: '{prompt}' \n\nNenu help chestha bro! Inka detail ga cheppamantara? 😊"

    with st.chat_message("assistant"):
        st.markdown(reply)
    
    # AI message add cheyi
    st.session_state.messages.append({"role": "assistant", "content": reply})