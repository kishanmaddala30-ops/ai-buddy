import streamlit as st
from groq import Groq
from datetime import datetime

# 1. NEE DETAILS
USER_NAME = "Nandhu" # <<<<< IKKADA NEE PERU
DEVELOPER_NAME = "MADDALA SAI NARASING KISHAN" # <<<<< IKKADA NEE PERU

# 2. Page Config
st.set_page_config(
    page_title=f"AI BUDDY by {DEVELOPER_NAME}",
    page_icon="🤖",
    layout="centered"
)

# 3. API Key - Streamlit Secrets lo petuko lekapothe direct ikkada
API_KEY = "gsk_your_key_here" # <<<<< NEE GROQ KEY IKKADA PETTU

client = Groq(api_key=API_KEY)

# 4. FULL CHATGPT STYLE SYSTEM PROMPT
SYSTEM_PROMPT = f"""You are AI BUDDY, created and developed by {DEVELOPER_NAME}.
You answer exactly like ChatGPT - detailed, structured, and scoring.

CORE INSTRUCTIONS:
1. TONE: Friendly professor. Start with "Sare {USER_NAME}" if user writes in Telugu/English mix. Be helpful, clear.
2. STRUCTURE: Always use headings, bold, bullet points, and code blocks.

3. IF EXAM QUESTION DETECTED: "X Marks" ani unte
   **Length Rule**: 2 Marks = 80-100 words, 4 Marks = 150-200 words, 6 Marks = 300-400 words
   **Format MUST be**:
   **1. Definition**
   2-3 lines clear definition

   **2. Explanation / Working**
   4-6 bullet points step by step

   **3. Example / Diagram / RTL**
   Give real example. For COA: R2 ← R1 + R3

   **4. Advantages / Applications**
   3-4 points

   **5. Exam Tip for Full Marks**
   "Diagram vesthe + Keywords highlight chesthe 100% marks vastay"

4. IF NORMAL DOUBT: Explain like a senior teaching a junior. Give example + code if needed.

5. LANGUAGE: User em language lo adigithe aa language lo ne answer ivvu.

6. QUALITY: Be accurate. Now answer the following question in full detail:"""

# 5. HEADER
st.title(f"🤖 AI BUDDY")
st.subheader(f"Welcome {USER_NAME}! 👋")
st.caption("1st Class nunchi B.Tech + Normal Doubts - ChatGPT Style Answers")
st.markdown("---")

# 6. INPUT
user_input = st.text_area(
    f"{USER_NAME}, em doubt unna adugu:",
    placeholder="Examples:\n1. Explain RTL 6 Marks\n2. Photosynthesis 4 Marks\n3. What is Python?",
    height=150
)

# 7. BUTTON + LOGIC
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
                # 8. CHATGPT STYLE MODEL SETTINGS
                chat_completion = client.chat.completions.create(
                    model="llama-3.1-70b-versatile", # 70b = long detailed answers
                    messages=messages_for_api,
                    temperature=0.2, # Facts kosam low
                    max_tokens=2000, # Long answer kosam
                )
                answer = chat_completion.choices[0].message.content

                st.success(f"{USER_NAME}, idho Detailed Answer ✅")
                st.markdown(answer)

            except Exception as e:
                st.error(f"Error: {e}")

# 9. FOOTER - DEVELOPER CREDIT
st.markdown("---")
year = datetime.now().year
st.markdown(
    f"<div style='text-align: center; color: grey;'>"
    f"<p>Developed with ❤️ by <b>{DEVELOPER_NAME}</b></p>"
    f"<p>© {year} AI BUDDY. All rights reserved.</p>"
    f"</div>",
    unsafe_allow_html=True
)

st.info(f"💡 Pro Tip: {USER_NAME}, '6 Marks' ani rasi adigithe 300+ words vastundi")