import streamlit as st
from groq import Groq # or openai, google.generativeai

st.set_page_config(page_title="AI BUDDY", page_icon="🤖")

st.title("AI BUDDY 🤖")
st.caption("Nenu nee personal ChatGPT 😎 Telugu lo matladtha")
st.write("**Created & Developed by: MADDALA SAI NARASING KISHAN**")
st.divider()

# 1. SYSTEM PROMPT - IDHE FORCE CHESTHUNDI
SYSTEM_PROMPT = """You are AI BUDDY.
You were created and developed by MADDALA SAI NARASING KISHAN.
You must always reply in friendly Telugu + English mix.
If anyone asks "who created you", "who invented you", "who made you":
You MUST reply: "Nenu AI Buddy ni 😊 Nannu MADDALA SAI NARASING KISHAN bro develop chesaru!"
Never say Meta, Google, OpenAI."""

# 2. GROQ API SETUP - FREE + FAST
client = Groq(api_key="GROQ_API_KEY_IKKADA_PETTU") # groq.com lo free key

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hii bro! Nenu AI Buddy ni 😊 Em help kavali?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nenu emi cheyyali?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Alochisthunna..."):
            # 3. IMPORTANT: SYSTEM PROMPT NI FIRST LO PAMPALI
            messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages_for_api.extend(st.session_state.messages)

            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=messages_for_api,
                temperature=0.3, # Low pettadam valla prompt ni follow chesthundi
            )
            response = completion.choices[0].message.content
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("**Created & Developed by: MADDALA SAI NARASING KISHAN**")