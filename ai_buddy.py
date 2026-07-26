import streamlit as st
from streamlit_mic_recorder import mic_recorder
from PIL import Image

# BACKGROUND IMAGE
page_bg_img = '''
<style>
.stApp {
background-image: url("https://images.unsplash.com/photo-1557804506-669a67965ba0?q=80&w=1974");
background-size: cover;
background-position: center;
background-attachment: fixed;
}
.stApp h1, .stApp p, .stApp label {
    color: white;
    text-shadow: 2px 2px 4px black;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.set_page_config(page_title="AI Buddy", page_icon="🤖")
st.title("🤖 AI Buddy")

st.write("Voice, Camera, Photo Upload anni try chey")

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
    st.chat_message("assistant").write("Nenu vinnanu bro! 😊")

if audio:
    st.success("Voice record ayindi!")
if camera_photo:
    st.image(camera_photo, caption="Camera photo")
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded photo")