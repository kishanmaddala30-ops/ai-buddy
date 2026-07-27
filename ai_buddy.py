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
   **2. Explanation / Working - 5 points**
   **3. Example / RTL**
   **4. Advantages / Applications**
   **5. Exam Tip for Full Marks**

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
                    model="llama-3.1-70b-versatile",
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