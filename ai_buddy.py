import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Buddy", layout="wide")
st.title("📚 AI Buddy - Free Version")
st.caption("Powered by Groq - Super Fast + Free")

# Groq API key free ga istharu. 1 min lo teesukovachu
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key Paste Chey", type="password", help="https://console.groq.com/keys nunchi free ga teesuko")
    if api_key: 
        st.success("Key Set Ayindi ✅")

def get_ai_explanation(topic, api_key):
    if not topic.strip(): return "⚠️ Mundhu topic type chey bro"
    if not api_key: return "⚠️ Sidebar lo Groq API key paste chey. 1 min lo free ga vastadi"

    try:
        client = Groq(api_key=api_key)
        prompt = f'Explain "{topic}" in simple English for all class. Use 3 points + 1 real life example.'
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", # Chala fast
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

user_input = st.text_area("👇 Nuvvu em nerchukovalani undi?", placeholder="Ex: Encapsulation, Photosynthesis")
if st.button("✨ Adugu AI Buddy ni"):
    with st.spinner("AI Buddy alochistundi... ⚡"):
        answer = get_ai_explanation(user_input, api_key)
        st.divider()
        st.subheader("🤖 AI Buddy Answer")
        st.markdown(answer)