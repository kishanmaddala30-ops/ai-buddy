import streamlit as st
import sqlite3
from groq import Groq
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI BUDDY - by Kishan", page_icon="🤖", layout="wide")

# --- DATABASE FOR HISTORY ---
conn = sqlite3.connect('buddy.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, user_name TEXT, role TEXT, content TEXT, time TEXT)')
conn.commit()

# --- GROQ CLIENT ---
# Streamlit Cloud -> Settings -> Secrets lo GROQ_API_KEY add cheyali
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 1. LOGIN SYSTEM (STARTUP READY) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center'>🤖 AI BUDDY</h1><h4 style='text-align:center'>Developed by Maddala Sai Narasinga Kishan | 2026</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("🔐 Login to Continue")
        name = st.text_input("Your Full Name")
        email = st.text_input("College Email / Gmail")
        if st.button("Start Learning 🚀", use_container_width=True):
            if name and email:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Name & Email Required!")
    st.stop()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state.user_name} 👋")
    st.markdown(f"`{st.session_state.user_email}`")
    st.markdown("---")

    mode = st.selectbox("Choose Mode:", ["📚 Study Mode - Academics", "💻 Code Buddy - Python/DSA", "🎯 Interview Buddy"])

    st.markdown("### 📷 Camera & Voice")
    camera_pic = st.camera_input("Take a photo of your doubt")
    audio_val = st.audio_input("Record your doubt")

    st.markdown("---")
    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("---")
    st.caption("© 2026 Developed by Maddala Sai Narasinga Kishan")

# --- 3. IDENTITY & SYSTEM PROMPT (NAME FIX) ---
BASE_IDENTITY = """
You are AI BUDDY.
You are created ONLY by Maddala Sai Narasinga Kishan in 2026.
RULE: If user asks "who are you, who made you, who created you, nee peru enti, ninnu evaru chesaru, owner, creator" - You MUST reply: "I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan."
NEVER say OpenAI, ChatGPT, Meta. Only say AI BUDDY.
Always answer in simple Telugu + English mix for students.
"""

if mode == "📚 Study Mode - Academics":
    system_prompt = BASE_IDENTITY + " You are a friendly teacher for Class 1 to B.Tech students. Explain simply with examples."
elif mode == "💻 Code Buddy - Python/DSA":
    system_prompt = BASE_IDENTITY + " You are an expert Python and DSA coder. Give clean code with explanation and time complexity."
else:
    system_prompt = BASE_IDENTITY + " You are an Interview Buddy. Ask HR + Technical questions and give feedback."

# --- 4. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Hello {st.session_state.user_name}! I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan. How can I help you today?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("Ask your doubt here..."):

    # FORCE NAME CHECK - This fixes your name issue 100%
    name_keywords = ["who made you", "who created you", "who invented you", "who are you", "nee peru", "ninnu evaru", "creator", "owner", "built by", "developed by"]
    if any(word in prompt.lower() for word in name_keywords):
        response = "I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan. How can I help you today?"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI BUDDY is thinking..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": system_prompt}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            response = completion.choices[0].message.content
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
