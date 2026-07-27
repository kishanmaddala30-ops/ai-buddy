import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI BUDDY", page_icon="🤖")
st.title("AI BUDDY 🤖")
st.caption("Your Personal AI Assistant")
st.write("**Created & Developed by: MADDALA SAI NARASING KISHAN**")
st.divider()
# ILA CHANGE CHEY
SYSTEM_PROMPT = """You are AI BUDDY, an expert teacher and exam helper created and developed by MADDALA SAI NARASING KISHAN.

Rules:
1. First detect the class level and marks from the question. 
   - "6 Marks" or "B.Tech" = give detailed answer with headings, definition, examples, diagram.
   - "4 Marks" or "10th" = give 4-5 key points.
   - "2 Marks" or "1st to 9th" = give very simple explanation in 2-3 lines.
2. If normal doubt, explain like a friend with examples.
3. Always use this format for exams:
   **1. Definition**
   **2. Explanation / Key Points**
   **3. Example**
   **4. Exam Tip**
4. For Computer/COA questions use RTL notation like R2 ← R1
5. Answer in the same language user is using. Telugu lo adigithe Telugu lo cheppu.
6. Be detailed, clear and scoring like ChatGPT."""

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am AI Buddy 😊 How can I help you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
                messages_for_api.extend(st.session_state.messages)

                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages_for_api,
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Error: {e}" # Ippudu error direct kanipisthundi

            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("**Created & Developed by: MADDALA SAI NARASING KISHAN**")