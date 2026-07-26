import streamlit as st

st.set_page_config(page_title="AI Buddy", page_icon="🤖", layout="centered")
st.title("🤖 AI Buddy")
st.write("Emaina adugu, nenu reply istha 😊")

# Chat history kosam
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purana messages chupinchadam
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Nenu emi cheyyali?")

if prompt:
    # User message save
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI reply - Smart replies
    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()
        
        if "world war 2" in prompt_lower or "ww2" in prompt_lower:
            reply = """**World War 2 gurinchi chinnaga** 👇

**Start**: 1939 September 1 - Germany Poland meeda attack chesindi
**End**: 1945 September 2 - Japan surrender chesindi
**Main Countries**: Allies - USA, UK, USSR | Axis - Germany, Japan, Italy
**Result**: 70 million mandhi chanipoyaru. USA atomic bomb drop chesindi Hiroshima, Nagasaki lo.

Inka detail kavala bro? Specific ga emi telusukovali?"""
        
        elif "java" in prompt_lower:
            reply = "Java code kavala? Topic cheppu bro. Eg: calculator, factorial, pattern"
        
        else:
            reply = f"Nuv '{prompt}' gurinchi adigavu. Nenu help chestha bro! Inka detail ga cheppana? 😊"
            
        st.markdown(reply)
    
    # AI reply save
    st.session_state.messages.append({"role": "assistant", "content": reply})
  
