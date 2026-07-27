import streamlit as st

st.set_page_config(page_title="AI BUDDY", page_icon="🤖", layout="wide")

st.title("AI BUDDY 🤖")
st.caption("Your Personal AI Assistant")
st.write("**Created & Developed by: MADDALA SAI NARASING KISHAN**")
st.divider()

# SYSTEM PROMPT - ENGLISH ONLY
SYSTEM_PROMPT = """
You are AI BUDDY, a friendly AI Assistant.
You were created and developed by MADDALA SAI NARASING KISHAN.
Always reply in English only. Be helpful, clear, and professional.
If anyone asks "Who created you", "Who is your founder", "Who made you":
ALWAYS reply exactly: "I am AI BUDDY. I was created and developed by MADDALA SAI NARASING KISHAN."
Do not mention Google, OpenAI, or any other company.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am AI Buddy 😊\nHow can I help you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            
            # Direct answer for founder question
            if any(word in prompt.lower() for word in ["created", "founder", "made", "developer"]):
                response = "I am AI BUDDY. I was created and developed by MADDALA SAI NARASING KISHAN."
            else:
                # Replace this with your actual LLM API call
                response = f"You asked: '{prompt}'. This is where your LLM API response will come."
            
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("**Created & Developed by: MADDALA SAI NARASING KISHAN**")
st.markdown("Hosted with Streamlit | AI BUDDY v1.3")