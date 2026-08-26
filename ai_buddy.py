import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI BUDDY - by Kishan", page_icon="🤖", layout="wide")

# --- GROQ CLIENT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY Secrets lo ledu! Streamlit -> Settings -> Secrets lo add chey")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🤖 AI BUDDY")
    st.caption("Developed by Maddala Sai Narasinga Kishan • 2026")
    mode = st.selectbox("Mode", ["📚 Study Mode", "💻 Code Buddy", "🎯 Interview Buddy"])
    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.rerun()

# --- IDENTITY ---
BASE = "You are AI BUDDY, developed ONLY by Maddala Sai Narasinga Kishan in 2026. If asked who made you, say 'I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan'. Never say OpenAI/ChatGPT."

SYSTEM = BASE + " RULE: Always reply ONLY in English. Never use Telugu script. Be friendly and simple."
    if "messages" not in st.session_state
    st.session_state.messages = [{"role": "assistant", "content": "Hello m.s.n kishan! I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan. Nee doubt enti?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- CHAT ---
if prompt := st.chat_input("Ask your doubt here..."):

    # Name fix
    if any(k in prompt.lower() for k in ["who are you", "who made", "creator", "owner", "ninnu evaru"]):
        reply = "I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan."
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"): st.markdown(reply)
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # NEW MODELS LIST - Auto fallback
            models_to_try = [
                "openai/gpt-oss-20b", # NEW 2026 MODEL - FASTEST
                "llama-3.3-70b-versatile", # BACKUP 1
                "openai/gpt-oss-120b" # BACKUP 2
            ]

            response_text = None
            for model_name in models_to_try:
                try:
                    completion = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "system", "content": SYSTEM}] + st.session_state.messages
                    )
                    response_text = completion.choices[0].message.content
                    break # Success ayithe loop nundi bayataki
                except Exception as e:
                    continue # Next model try chey

            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error("Groq API Key problem bro. console.groq.com ki velli kotha API Key create chesi Secrets lo update chey.")
