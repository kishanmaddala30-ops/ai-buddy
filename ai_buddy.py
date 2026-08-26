import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI BUDDY - by Kishan", page_icon="🤖", layout="wide")

# --- GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Add GROQ_API_KEY in Secrets!")
    st.stop()

# --- 1. LOGIN SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center'>🤖 AI BUDDY</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center'>Developed by Maddala Sai Narasinga Kishan • 2026</h4>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("🔐 Login to Continue")
        name = st.text_input("Enter Your Full Name", placeholder="M.S.N Kishan")
        email = st.text_input("Enter Your Email", placeholder="kishan@gmail.com")
        password = st.text_input("Password", type="password", placeholder="Any password - demo login")

        if st.button("Login & Start 🚀", use_container_width=True, type="primary"):
            if name and email and password:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Please fill all fields!")
    st.stop()

# --- 2. AFTER LOGIN ---
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state.user_name} 👋")
    st.caption(f"{st.session_state.user_email}")
    st.markdown("---")
    mode = st.selectbox("Select Mode", ["📚 Study Mode", "💻 Code Buddy", "🎯 Interview Buddy"])
    st.markdown("---")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("© 2026 Developed by Kishan")

# --- 3. SYSTEM PROMPT - ENGLISH ONLY + NAME FIX ---
BASE = "You are AI BUDDY, developed ONLY by Maddala Sai Narasinga Kishan in 2026. If user asks who made you, who are you, creator, owner, you MUST say 'I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan'. Never say OpenAI or ChatGPT. Always reply in ENGLISH ONLY."

if "Study" in mode:
    SYSTEM_PROMPT = BASE + " You are a friendly teacher. Explain simply in English."
elif "Code" in mode:
    SYSTEM_PROMPT = BASE + " You are an expert Python coder. Give clean code."
else:
    SYSTEM_PROMPT = BASE + " You are an interview coach."

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show welcome
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(f"Hello {st.session_state.user_name}! I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan. How can I help you?")

# Show history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 4. CHAT LOGIC - WORKING MODEL ---
if prompt := st.chat_input("Ask your doubt here..."):

    # Name force fix
    if any(k in prompt.lower() for k in ["who are you", "who made", "creator", "owner", "ninnu evaru"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        reply = "I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan."
        with st.chat_message("assistant"): st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-20b", # NEW WORKING MODEL
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                )
                resp = completion.choices[0].message.content
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
            except Exception as e:
                # Fallback model
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                    )
                    resp = completion.choices[0].message.content
                    st.markdown(resp)
                    st.session_state.messages.append({"role": "assistant", "content": resp})
                except Exception as e2:
                    st.error(f"Error: {e2}")
          
