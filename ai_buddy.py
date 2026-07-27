import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI BUDDY", page_icon="🤖")
st.title("AI BUDDY 🤖")
st.caption("Your Personal AI Assistant")
st.write("**Created & Developed by: MADDALA SAI NARASING KISHAN**")
st.divider()

# ILA CHANGE CHEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"]) # <--- Secret nundi teeskuntundi

SYSTEM_PROMPT = "You are AI BUDDY. You were created and developed by MADDALA SAI NARASING KISHAN."

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
        with st.spinner("Thinking..."):
            try:
                messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
                messages_for_api.extend(st.session_state.messages)

                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages_for_api,
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Error: {e}" # Ippudu error direct kanipisthundi

            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("**Created & Developed by: MADDALA SAI NARASING KISHAN**")