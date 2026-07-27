import streamlit as st

st.set_page_config(page_title="AI BUDDY", page_icon="🤖")
st.title("AI BUDDY 🤖")
st.caption("Your Personal AI Assistant")
st.write("**Created & Developed by: MADDALA SAI NARASING KISHAN**")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am AI Buddy 😊 How can I help you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # DUMMY RESPONSE - CRASH AVVADHU
        response = f"AI Buddy here! You said: '{prompt}'\n\nI am still learning bro 😅"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("**Created & Developed by: MADDALA SAI NARASING KISHAN**")