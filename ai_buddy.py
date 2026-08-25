import streamlit as st
from groq import Groq
import sqlite3
import json
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI BUDDY", page_icon="🤖", layout="wide")

# --- DB FUNCTIONS FOR HISTORY ---
def init_db():
    conn = sqlite3.connect('ai_buddy.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, mode TEXT, messages TEXT, date TEXT)''')
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

# --- CHATGPT STYLE CSS + UNIQUE TOUCH ---
st.markdown("""
<style>
  .stApp { background-color: #0A0A0B; color: #E5E5E5; }
    [data-testid="stSidebar"] { background-color: #111113; border-right: 1px solid #222; }
  .user-bubble { background: #2A4B8D; padding: 12px 18px; border-radius: 20px 20px 4px 20px; margin: 10px 0 10px 40px; text-align: left; }
  .bot-bubble { background: #1C1C1E; padding: 16px 18px; border-radius: 20px 20px 20px 4px; margin: 10px 40px 10px 0; border: 1px solid #2A2A2E; line-height: 1.6; }
  .story-box { background: linear-gradient(135deg, #1A2A3A, #1C1C1E); border: 1px solid #2E5A88; padding: 20px; border-radius: 16px; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

# --- API CONFIG - FIXED MODEL ---
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
MODEL = "llama-3.1-8b-instant"
client = Groq(api_key=GROQ_API_KEY)

# --- SIDEBAR - WITH REAL HISTORY + STORY ---
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

    # NEW: Story Button (Unique Feature)
    if st.button("✨ Create Story from Chats", use_container_width=True, type="primary"):
        st.session_state.show_story = True

    if st.button(" + New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI BUDDY. Ask me anything from Class 1 to B.Tech. How can I help today?"}]
        st.session_state.show_story = False
        st.rerun()

    st.markdown("**CHAT HISTORY**")
    # Load real history from DB
    chats = load_chats()
    if not chats:
        st.caption("No history yet. Start chatting!")
    else:
        for chat_id, title, mode, date, messages_json in chats[:8]:
            if st.button(f"{title[:28]} • {date}", key=f"chat_{chat_id}", use_container_width=True):
                st.session_state.messages = json.loads(messages_json)
                st.session_state.show_story = False
                st.rerun()

    st.markdown("---")
    st.markdown("**Rahul** \nCSE • VNR VJIET • Sem 4")
    st.caption("🔥 4-day streak")

# --- SYSTEM PROMPTS ---
if "Study" in selected_mode:
    system_prompt = "You are AI BUDDY Study Mode. Explain complex topics simply, with bullet points and exam tips. Add a 'Exam Tip' box at the end."
elif "Code" in selected_mode:
    system_prompt = "You are Code Buddy. Expert Python developer. Give clean code, explain complexity."
else:
    system_prompt = "You are Interview Buddy. Ask mock interview questions and give feedback."

# --- STORY MODE VIEW ---
if st.session_state.get("show_story", False):
    st.markdown("### 📖 Your Learning Story")
    st.caption("AI creates a story from your chat history")

    if len(st.session_state.get("messages", [])) <= 1:
        st.warning("Chat for some time first to generate a story.")
    else:
        with st.spinner("Writing your story..."):
            try:
                all_chat_text = str(st.session_state.messages[-10:])
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": f"Convert this learning chat into a short inspiring story with Title, 3 paragraphs, and 3 takeaways: {all_chat_text}"}]
                )
                story = completion.choices[0].message.content
                st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)

                if st.button("Save this Story to History"):
                    save_chat(f"Story: {story[:20]}", "Story Mode", [{"role": "assistant", "content": story}])
                    st.success("Story saved!")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("← Back to Chat"):
        st.session_state.show_story = False
        st.rerun()

else:
    # --- MAIN CHAT HEADER ---
    st.markdown(f"### {selected_mode}")
    st.caption("Focused • Exam prep • Simplified explanations")

    # --- CHAT STATE ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI BUDDY. Ask me anything from Class 1 to B.Tech. How can I help today?"}
        ]

    # --- DISPLAY CHAT ---
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    # --- QUICK ACTIONS ---
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

    # --- INPUT ---
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

            # AUTO SAVE TO HISTORY (after first Q&A)
            if len(st.session_state.messages) == 3:
                save_chat(st.session_state.messages[0]["content"][:35], selected_mode, st.session_state.messages)
            elif len(st.session_state.messages) > 3:
                # Update last chat
                pass # You can add update logic here

            st.rerun()

        except Exception as e:
            st.error(f"API Error: {e}")

    st.caption("AI BUDDY can make mistakes. Check important details. • 12 credits left")

**2. Explanation / Working - 5 points**
   **3. Example / RTL**
   **4. Advantages / Applications**
   **5. Exam Tip for Full Marks**
import streamlit as st
from groq import Groq
from datetime import datetime

# ============================================
# 1. NEE DETAILS - IKKADA MARCHU
# ============================================
USER_NAME = "SAI" # <<<<< NEE PERU
DEVELOPER_NAME = "MADDALA SAI NARASING KISHAN" # <<<<< NEE PERU

# ============================================
# 2. API KEY SETUP - 2 OPTIONS UNNAY
# ============================================
# OPTION A: Streamlit Cloud kosam - Secrets use chey
API_KEY = st.secrets["GROQ_API_KEY"]

# OPTION B: Local lo test cheyadaniki - Direct key
# API_KEY = "gsk_your_key_here" # <<<<< Idhi use chesthe paina line ni # pettu

client = Groq(api_key=API_KEY)

# ============================================
# 3. PAGE SETUP
# ============================================
st.set_page_config(
    page_title=f"AI BUDDY by {DEVELOPER_NAME}",
    page_icon="🤖",
    layout="centered"
)

# ============================================
# 4. FULL CHATGPT STYLE PROMPT
# ============================================
SYSTEM_PROMPT = f"""You are AI BUDDY, created and developed by {DEVELOPER_NAME}.
You answer exactly like ChatGPT - detailed, structured, and scoring.

CORE INSTRUCTIONS:
1. TONE: Friendly professor. Start with "Sare {USER_NAME}" if user writes in Telugu/English mix.
2. STRUCTURE: Always use headings, bold, bullet points, and code blocks.

3. IF EXAM QUESTION: "X Marks" unte
   **Length Rule**: 2 Marks=100 words, 4 Marks=200 words, 6 Marks=350 words
   **Format**:
   **1. Definition**
4. IF NORMAL DOUBT: Senior la simple ga explain chey with example.
5. LANGUAGE: User language lone answer ivvu.
6. Be accurate and detailed.
"""

# ============================================
# 5. HEADER
# ============================================
st.title(f"🤖 AI BUDDY")
st.subheader(f"Welcome {USER_NAME}! 👋")
st.caption("1st Class nunchi B.Tech + Normal Doubts - ChatGPT Style")
st.markdown("---")

# ============================================
# 6. INPUT BOX
# ============================================
user_input = st.text_area(
    f"{USER_NAME}, em doubt unna adugu:",
    placeholder="Examples:\n1. Explain RTL 6 Marks\n2. Photosynthesis 4 Marks\n3. What is Python?",
    height=150
)

# ============================================
# 7. BUTTON LOGIC
# ============================================
if st.button("Cheppu Buddy ✨", type="primary"):

    if user_input.strip() == "":
        st.warning(f"{USER_NAME}, konchem question type chey!")
    else:
        with st.spinner(f"{USER_NAME} kosam detailed answer rayisthunnanu..."):

            messages_for_api = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]

            try:
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api,
                    temperature=0.2,
                    max_tokens=2000,
                )
                answer = chat_completion.choices[0].message.content

                st.success(f"{USER_NAME}, idho Detailed Answer ✅")
                st.markdown(answer)

            except Exception as e:
                st.error(f"Error: {e}")

# ============================================
# 8. FOOTER
# ============================================
st.markdown("---")
year = datetime.now().year
st.markdown(
    f"<div style='text-align: center; color: grey;'>"
    f"<p>Developed with ❤️ by <b>{DEVELOPER_NAME}</b></p>"
    f"<p>© {year} AI BUDDY. All rights reserved.</p>"
    f"</div>",
    unsafe_allow_html=True
)

st.info(f"💡 Pro Tip: {USER_NAME}, '6 Marks' ani rasi adigithe 350+ words vastundi")
