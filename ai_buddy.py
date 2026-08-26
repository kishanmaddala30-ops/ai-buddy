import streamlit as st
from groq import Groq
import extra_streamlit_components as stx
from datetime import datetime, timedelta

st.set_page_config(page_title="AI BUDDY - by Kishan", page_icon="🤖")

# Cookie Manager for Remember Login
@st.cache_resource
def get_cookie_manager():
    return stx.CookieManager()

cookie_manager = get_cookie_manager()

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY missing in Secrets!")
    st.stop()

# --- CHECK IF ALREADY LOGGED IN VIA COOKIE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Try to get cookie
try:
    saved_login = cookie_manager.get(cookie="ai_buddy_login")
    if saved_login == "true" and not st.session_state.logged_in:
        st.session_state.logged_in = True
        st.session_state.user_name = cookie_manager.get(cookie="ai_buddy_name") or "Kishan"
except:
    pass

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center'>🤖 AI BUDDY</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center'>Developed by Maddala Sai Narasinga Kishan</h4>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        st.subheader("🔐 Login")
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.button("Login & Start 🚀", use_container_width=True, type="primary"):
            if name and email:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                # Save cookie for 30 days
                cookie_manager.set("ai_buddy_login", "true", expires_at=datetime.now() + timedelta(days=30))
                cookie_manager.set("ai_buddy_name", name, expires_at=datetime.now() + timedelta(days=30))
                st.success("Login Success! Reloading...")
                st.rerun()
            else:
                st.error("Fill all fields")
    st.stop()

# --- AFTER LOGIN (Your app) ---
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state.user_name} 👋")
    if st.button("🚪 Logout", use_container_width=True):
        cookie_manager.delete("ai_buddy_login")
        cookie_manager.delete("ai_buddy_name")
        st.session_state.logged_in = False
        st.rerun()
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []

BASE = "You are AI BUDDY, developed ONLY by Maddala Sai Narasinga Kishan. Reply in ENGLISH ONLY. If asked who made you, say 'I am AI BUDDY, Developed by Maddala Sai Narasinga Kishan'."

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask your doubt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        comp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "system", "content": BASE}] + st.session_state.messages
        )
        resp = comp.choices[0].message.content
        st.markdown(resp)
        st.session_state.messages.append({"role": "assistant", "content": resp})
