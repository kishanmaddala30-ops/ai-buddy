import streamlit as st

st.set_page_config(page_title="AI Buddy", page_icon="🤖", layout="centered")
st.title("🤖 AI Buddy")
st.write("Emaina adugu, nenu reply istha 😊")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Nenu emi cheyyali?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p = prompt.lower().replace(" ", "") # space teesesta, so world war 2 = worldwar2
        
        if "worldwar2" in p or "ww2" in p:
            reply = """**World War 2 Summary** 👇

**Start**: 1939 Sep 1 - Germany Poland ni attack chesindi
**End**: 1945 Sep 2 - Japan surrender
**Allies**: USA, UK, USSR, France 
**Axis**: Germany, Italy, Japan
**Important**: Holocaust, Atomic bombs on Hiroshima & Nagasaki
**Deaths**: ~70 million mandhi

Inka em topic kavala bro?"""
        
        elif "java" in p:
            reply = "Java code kavala? Topic cheppu bro. Eg: calculator, factorial, pattern"
        
        elif "hi" in p or "hello" in p:
            reply = "Hi bro! Ela unnav? 😊 Em help kavali?"
        
        else:
            reply = f"'{prompt}' gurinchi cheppamantara? Nenu help chestha bro!"
            
        st.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
