import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Buddy", page_icon="🤖")

st.title("🤖 AI Buddy")
st.write("Nuvvu emaina adugu. Nenu answer ista!")

# 1. KEY NI SECRETS NUNCHI DIRECT GA TEESKOVADAM
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ Streamlit Secrets lo GROQ_API_KEY add chey bro")
    st.stop()

# 2. GROQ CLIENT CREATE CHEYADAM
client = Groq(api_key=api_key)

# 3. CHAT HISTORY SAVE CHEYADANIKI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purana chat chupinchadam
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. USER INPUT BOX
if prompt := st.chat_input("Nenu emi cheyyali?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Aloc histhunna..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful AI Buddy. Reply in Telugu if user writes in Telugu."}
                ] + st.session_state.messages,
                model="llama-3.1-8b-instant",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})