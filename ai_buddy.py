import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI BUDDY - by Kishan", page_icon="🤖", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY missing in Secrets!")
    st.stop()

# --- LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center'>🤖 AI BUDDY</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center'>Developed by Maddala Sai Narasinga Kishan • 2026</h4>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        st.subheader("🔐 Login")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        if st.button("Login & Start 🚀", use_container_width=True, type="primary"):
            if name and email:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("Enter Name & Email")
    st.stop()

# --- SIDEBAR WITH MODES ---
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state.user_name} 👋")
    st.markdown("---")
    st.subheader("🎯 Select Mode")
    mode = st.selectbox(
        "Choose your buddy",
        ["📚 Study Mode", "💻 Code Buddy", "🎯 Interview Buddy"],
        label_visibility="collapsed"
    )
    st.markdown("---")

    if mode == "📚 Study Mode":
        st.info("📖 For Class 1 to B.Tech doubts")
    elif mode == "💻 Code Buddy":
        st.info("🐍 Python, Java, DSA expert")
    else:
        st.info("💼 HR + Technical interview prep")

    st.markdown("---")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.messages = []
        st.rerun()
    st.caption("© 2026 Built by Kishan")

# --- SYSTEM PROMPT BASED ON MODE ---
BASE = "You are AI BUDDY, developed ONLY by Maddala Sai Narasinga Kishan in 2026. If asked who made you, say 'I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan'. Reply in ENGLISH ONLY."

if "Study" in mode:
    SYSTEM_PROMPT = BASE + " You are a best teacher for students from Class 1 to B.Tech. Explain in very simple English with examples."
elif "Code" in mode:
    SYSTEM_PROMPT = BASE + " You are an expert coder. Give clean Python/Java code with explanation and time complexity. You are Code Buddy."
else:
    SYSTEM_PROMPT = BASE + " You are Interview Buddy. Ask and answer HR questions, technical questions, give tips to crack interviews."

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome msg
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(f"Hello {st.session_state.user_name}! I am AI BUDDY. You selected **{mode}**. How can I help?")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Ask doubt in {mode}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"{mode} thinking..."):
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            )
            resp = completion.choices[0].message.content
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})
