import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="AI BUDDY - by Kishan", page_icon="🤖", layout="wide")

# --- 2. GROQ CLIENT - FIXED ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Secrets lo GROQ_API_KEY ledu bro! Streamlit Dashboard -> Settings -> Secrets lo add chey")
    st.stop()

# --- 3. LOGIN SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center'>🤖 AI BUDDY</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center'>Developed by Maddala Sai Narasinga Kishan • 2026</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        st.subheader("🔐 Login")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        if st.button("Start Learning 🚀", use_container_width=True):
            if name and email:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("Name & Email enter chey")
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f"### Hi, {st.session_state.user_name} 👋")
    st.markdown("---")
    mode = st.selectbox("Choose Mode", ["📚 Study Mode", "💻 Code Buddy", "🎯 Interview Buddy"])
    st.markdown("---")
    st.write("📷 Camera Input")
    cam = st.camera_input("Photo teesi doubt adugu")
    st.write("🎤 Voice Input")
    audio = st.audio_input("Record your doubt")
    st.markdown("---")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()
    st.caption("© 2026 Built by Kishan")

# --- 5. SYSTEM PROMPT (NAME FIX) ---
BASE_IDENTITY = "You are AI BUDDY. You are developed ONLY by Maddala Sai Narasinga Kishan in 2026. Rule: If anyone asks who made you, creator, owner, nee peru enti, you MUST reply 'I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan'. Never say OpenAI, ChatGPT, Meta."

if "Study" in mode:
    SYSTEM_PROMPT = BASE_IDENTITY + " You are a best teacher for Class 1 to B.Tech. Explain in Telugu + English mix simply."
elif "Code" in mode:
    SYSTEM_PROMPT = BASE_IDENTITY + " You are an expert Python/DSA coder. Give clean code with time complexity."
else:
    SYSTEM_PROMPT = BASE_IDENTITY + " You are Interview expert. Ask HR and technical questions."

# --- 6. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Welcome message if empty
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(f"Hello {st.session_state.user_name}! I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan. Nee doubt enti?")

# --- 7. MAIN CHAT LOGIC - ERROR FIXED HERE ---
if prompt := st.chat_input("Ask your doubt here..."):

    # Force name fix
    name_q = ["who are you", "who made you", "who created", "creator", "owner", "built by", "nee peru", "ninnu evaru chesaru"]
    if any(x in prompt.lower() for x in name_q):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        reply = "I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan."
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.stop()

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant message - THIS IS LINE 105 FIX
    with st.chat_message("assistant"):
        with st.spinner("AI BUDDY thinking..."):
            try:
                messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages:
                    messages_for_api.append({"role": m["role"], "content": m["content"]})

                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant", # <-- 100% WORKING MODEL - OLD MODEL TEESINA FIX
                    messages=messages_for_api,
                    temperature=0.7
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Groq Error: {e}")
                st.info("Solution: Groq API Key check chey, model name 'llama-3.1-8b-instant' ani unda chudu.")
