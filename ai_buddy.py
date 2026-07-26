import streamlit as st
from streamlit_mic_recorder import mic_recorder
from PIL import Image

st.set_page_config(page_title="AI Buddy", page_icon="🤖")

st.title("🤖 AI Buddy")

col1, col2, col3 = st.columns(3)
with col1:
    audio = mic_recorder(start_prompt="🎤 Start", stop_prompt="⏹️ Stop", key='mic')
with col2:
    camera_photo = st.camera_input("📷 Camera")
with col3:
    uploaded_file = st.file_uploader("📎 Upload", type=["jpg", "png"])

prompt = st.chat_input("Nenu emi cheyyali?")

if prompt:
    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write("Nenu vinnanu bro! Photo/voice unte cheppu 😊")

if audio:
    st.success("Voice record ayindi!")
if camera_photo:
    st.image(camera_photo, caption="Camera photo")
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded photo")    