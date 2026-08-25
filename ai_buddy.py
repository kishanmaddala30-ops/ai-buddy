import streamlit as st
from groq import Groq
import sqlite3, json
from datetime import datetime
import base64

st.set_page_config(page_title="AI BUDDY", page_icon="🤖", layout="wide")

def init_db():
    conn = sqlite3.connect('ai_buddy.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, mode TEXT, messages TEXT, date TEXT)''')
    conn.commit(); conn.close()
def save_chat(title, mode, messages):
    conn = sqlite3.connect('ai_buddy.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO chats VALUES (NULL,?,?,?,?)",(title, mode, json.dumps(messages), datetime.now().strftime("%d %b %I:%M %p")))
    conn.commit(); conn.close()
def load_chats():
    conn = sqlite3.connect('ai_buddy.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT id, title, mode, date, messages FROM chats ORDER BY id DESC")
    rows = c.fetchall(); conn.close(); return rows
init_db()

st.markdown("""
<style>
.stApp { background-color: #0A0A0B; color: #E5E5E5; }
[data-testid="stSidebar"] { background-color: #111113; border-right: 1px solid #222; }
.user-bubble { background: #2A4B8D; padding: 12px 18px; border-radius: 20px 20px 4px 20px; margin: 10px 0 10px 40px; }
.bot-bubble { background: #1C1C1E; padding: 16px 18px; border-radius: 20px 20px 20px 4px; margin: 10px 40px 10px 0; border: 1px solid #2A2A2E; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

try: GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except: GROQ_API_KEY = "YOUR_KEY_HERE"
client = Groq(api_key=GROQ_API_KEY)
WORKING_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-20b", "qwen/qwen3-32b"]
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

with st.sidebar:
    st.markdown("## AI BUDDY")
    st.caption("Built by Kishan • 2026")
    st.markdown("---")
    st.markdown("**MODES**")
    selected_mode = st.radio("Modes", ["Study Mode - Academics", "Code Buddy - Python / DSA", "Interview Buddy"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**🎥 TOOLS**")
    camera_on = st.toggle("📷 Camera On")
    voice_on = st.toggle("🎙️ Voice Recorder On")
    st.markdown("---")
    if st.button(" + New Chat", use_container_width=True):
        st.session_state.messages=[{"role":"assistant","content":"Hello! I am AI BUDDY built by Maddala Sai Narasinga Kishan. How can I help?"}]
        st.rerun()
    st.markdown("**HISTORY**")
    for chat_id, title, mode, date, messages_json in load_chats()[:8]:
        if st.button(f"{title[:26]}", key=f"h_{chat_id}", use_container_width=True):
            st.session_state.messages=json.loads(messages_json); st.rerun()
    st.markdown("---")
    st.markdown("**Maddala Sai Narasinga Kishan**")

# VNR VJIET REMOVED FROM IDENTITY
BASE_IDENTITY = """
You are AI BUDDY, created by Maddala Sai Narasinga Kishan.
CRITICAL: You are NOT OpenAI, NOT ChatGPT. Your creator is ONLY Maddala Sai Narasinga Kishan.
If asked who invented you, who made you, who created you, nee peru enti, ninnu evaru chesaru,
you MUST say: "I am AI BUDDY, created by Maddala Sai Narasinga Kishan."
Never mention OpenAI or any college name.
"""

if "Study" in selected_mode:
    system_prompt = BASE_IDENTITY + " Study Mode. Explain simply."
elif "Code" in selected_mode:
    system_prompt = BASE_IDENTITY + " Code Buddy Mode."
else:
    system_prompt = BASE_IDENTITY + " Interview Buddy Mode."

st.markdown(f"### {selected_mode}")

if "messages" not in st.session_state:
    st.session_state.messages=[{"role":"assistant","content":"Hello! I am AI BUDDY, built by Maddala Sai Narasinga Kishan. Ask me anything from Class 1 to B.Tech. How can I help today?"}]

for msg in st.session_state.messages:
    if msg["role"]=="user": st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else: st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

if camera_on:
    img_file = st.camera_input("Take a picture")
    if img_file and st.button("Ask about this image"):
        with st.spinner("Reading image..."):
            b64 = base64.b64encode(img_file.getvalue()).decode('utf-8')
            comp = client.chat.completions.create(model=VISION_MODEL, messages=[{"role":"user","content":[{"type":"text","text": BASE_IDENTITY + " Explain this image."},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]}])
            resp = comp.choices[0].message.content
            st.session_state.messages.append({"role":"user","content":"[Image] Explain this"}); st.session_state.messages.append({"role":"assistant","content":resp}); st.rerun()

voice_prompt = None
if voice_on:
    audio_file = st.audio_input("Record your doubt")
    if audio_file:
        with st.spinner("Transcribing..."):
            try:
                transcription = client.audio.transcriptions.create(file=(audio_file.name, audio_file.getvalue()), model="whisper-large-v3", response_format="text")
                voice_prompt = transcription; st.success(f"You said: {voice_prompt}")
            except Exception as e: st.error(f"Voice error: {e}")

prompt = st.chat_input("Ask anything...")
if voice_prompt: prompt = voice_prompt

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    response = None
    with st.spinner("Thinking..."):
        for try_model in WORKING_MODELS:
            try:
                completion = client.chat.completions.create(model=try_model, messages=[{"role":"system","content":system_prompt}] + st.session_state.messages[-8:], temperature=0.6, max_tokens=1200)
                response = completion.choices[0].message.content; break
            except: continue
    if response:
        st.session_state.messages.append({"role":"assistant","content":response})
        if len(st.session_state.messages)==3: save_chat(st.session_state.messages[1]["content"][:35], selected_mode, st.session_state.messages)
        st.rerun()
    else:
        st.error("All models failed. Create new key at console.groq.com/keys")
