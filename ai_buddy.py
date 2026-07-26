import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Buddy", page_icon="🤖")
st.title("🤖 AI Buddy")

st.write("Voice, Camera, Photo Upload anni try chey")

col1, col2, col3 = st.columns(3)
with col1:
    st.write("🎤 Mic - coming soon")
with col2:
    camera_photo = st.camera_input("📷 Camera")
with col3:
    uploaded_file = st.file_uploader("📎 Upload", type=["jpg", "png"])

prompt = st.chat_input("Nenu emi cheyyali?")

if prompt:
    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write("Nenu vinnanu bro! 😊")

if camera_photo:
    st.image(camera_photo, caption="Camera photo")
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded photo")