import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Buddy", page_icon="🤖", layout="centered")

st.title("🤖 AI Buddy")
st.caption("Nenu nee personal ChatGPT 😎 Telugu lo matladtha")

# 1. Secret nunchi Key teeskovadam
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except KeyError:
    st.error("🚨 GROQ_API_KEY set cheyyaledu bro")
    st.info("Streamlit Settings > Secrets lo `GROQ_API_KEY = \"gsk_...\"` ani pettu")
    st.stop()
except Exception as e:
    st.error(f"Groq connect avvaledu: {e}")
    st.stop()

# 2. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # First message
    st.session_state.messages.append({"role": "assistant", "content": "Hii bro! Nenu AI Buddy ni 😄 Em help kavali?"})

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
        with st.spinner("Alocisthunnanu..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are AI Buddy. Always reply in friendly English. Use emojis and be helpful."}
                    ] + st.session_state.messages,
                    model="llama-3.1-8b-instant", # Fastest free model
                    temperature=0.7,
                    max_tokens=1024,
                )
                reply = chat_completion.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"Error vachindi: {e}")
                st.error("API Key expire ayyundochu. Kothadi create cheyi")