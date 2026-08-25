import streamlit as st
from groq import Groq
import sqlite3
import json
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI BUDDY", page_icon="🤖", layout="wide")

# --- DB FOR HISTORY ---
def init_db():
    conn = sqlite3.connect('ai_buddy.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  mode TEXT,
                  messages TEXT,
                  date TEXT)''')
    conn.commit()
    conn.close()

def save_chat(title, mode, messages):
    conn = sqlite3.connect('ai_buddy.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO chats (title, mode, messages, date) VALUES (?,?,?,?)",
              (title, mode, json.dumps(messages), datetime.now().strftime("%d %b, %I:%M %p")))
    conn.commit()
    conn.close()

def load_chats():
    conn = sqlite3.connect('ai_buddy.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT id, title, mode, date, messages FROM chats ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# --- CSS ---
st.markdown("""
<style>
 .stApp { background-color: #0A0A0B; color: #E5E5E5; }
  [data-testid="stSidebar"] { background-color: #111113; border-right: 1px solid #222; }
 .user-bubble { background: #2A4B8D; padding: 12px 18px; border-radius: 20px 20px 4px 20px; margin: 10px 0 10px 40px; text-align: left; }
 .bot-bubble { background: #1C1C1E; padding: 16px 18px; border-radius: 20px 20px 20px 4px; margin: 10px 40px 10px 0; border: 1px solid #2A2A2E; line-height: 1.6; }
 .story-box { background: #1C1C1E; border: 1px solid #3A5A8A; padding: 20px; border-radius: 16px; }
</style>
""", unsafe_allow_html=True)

# --- GROQ CONFIG - FIXED ---
# Get free key from https://console.groq.com/keys
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
MODEL = "llama-3.1-8b-instant"
client = Groq(api_key=GROQ_API_KEY)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## AI BUDDY")
    st.caption("2026 • Premium")
    st.markdown("---")
    st.markdown("**MODES**")
    selected_mode = st.radio(
        "Modes",
        ["Study Mode - Academics", "Code Buddy - Python / DSA", "Interview Buddy"],
        label_visibility="collapsed"
    )
    st.markdown("---")

    if st.button("✨ Create Story from Chats", use_container_width=True, type="primary"):
        st.session_state.show_story = True

    if st.button(" + New Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI BUDDY. Ask me anything from Class 1 to B.Tech. How can I help today?"}
        ]
        st.session_state.show_story = False
        st.rerun()

    st.markdown("**CHAT HISTORY**")
    chats = load_chats()
    if not chats:
        st.caption("No history yet")
    else:
        for chat_id, title, mode, date, messages_json in chats[:10]:
            if st.button(f"{title[:28]}", key=f"h_{chat_id}", use_container_width=True):
                st.session_state.messages = json.loads(messages_json)
                st.session_state.show_story = False
                st.rerun()
            st.caption(f"{date} • {mode}")

    st.markdown("---")
    st.markdown("**Rahul** \nCSE • VNR VJIET • Sem 4")
    st.caption("🔥 4-day streak")

# --- SYSTEM PROMPTS - FIXED (NO SYNTAX ERROR) ---
if "Study" in selected_mode:
    system_prompt = (
        "You are AI BUDDY Study Mode. Explain complex topics simply. "
        "Use bullet points and give exam tips. "
        "Structure: 1. Definition - 2 marks, 2. Explanation / Working - 5 points, 3. Example, 4. Exam Tip. "
        "Be concise like ChatGPT."
    )
elif "Code" in selected_mode:
    system_prompt = (
        "You are Code Buddy. You are an expert Python developer. "
        "Give clean code, explain time complexity, and give optimized solution. "
        "Structure: Explanation, Code, Complexity."
    )
else:
    system_prompt = (
        "You are Interview Buddy. Ask mock interview questions and give feedback. "
        "Be friendly and supportive."
    )

# --- STORY MODE ---
if st.session_state.get("show_story", False):
    st.markdown("### 📖 Your Learning Story")
    st.caption("AI creates a story from your chat history")

    if len(st.session_state.get("messages", [])) <= 1:
        st.warning("Chat a bit more to create a story!")
    else:
        with st.spinner("Writing your story..."):
            try:
                all_chat_text = str(st.session_state.messages[-8:])
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": f"Convert this learning chat into a short inspiring story with Title, 3 paragraphs, and 3 takeaways: {all_chat_text}"}]
                )
                story = completion.choices[0].message.content
                st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)
                if st.button("Save this Story"):
                    save_chat(f"Story {datetime.now().strftime('%d %b')}", "Story Mode", [{"role": "assistant", "content": story}])
                    st.success("Saved!")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("← Back to Chat"):
        st.session_state.show_story = False
        st.rerun()

else:
    # --- MAIN CHAT ---
    st.markdown(f"### {selected_mode}")
    st.caption("Focused • Exam prep • Simplified explanations")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI BUDDY. Ask me anything from Class 1 to B.Tech. How can I help today?"}
        ]

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Give me an example"):
                st.session_state.pending_prompt = "Give me an example for this"
                st.rerun()
        with col2:
            if st.button("Make 5 MCQs"):
                st.session_state.pending_prompt = "Create 5 practice MCQs for this topic"
                st.rerun()
        with col3:
            if st.button("Create flashcards"):
                st.session_state.pending_prompt = "Create flashcards for this topic"
                st.rerun()

    prompt = st.chat_input("Ask anything... add notes, code, or voice memo")

    if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            with st.spinner("Thinking..."):
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages[-8:],
                    temperature=0.6,
                    max_tokens=1200,
                )
                response = completion.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": response})

            if len(st.session_state.messages) == 3:
                save_chat(st.session_state.messages[1]["content"][:35], selected_mode, st.session_state.messages)

            st.rerun()
        except Exception as e:
            st.error(f"API Error: {e}")
            st.info(f"Check your Groq API key. Model must be {MODEL}")

    st.caption("AI BUDDY can make mistakes. Check important details. • 12 credits left")
