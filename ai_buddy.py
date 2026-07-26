import streamlit as st
from streamlit_mic_recorder import mic_recorder
from PIL import Image
import io

st.set_page_config(page_title="AI Buddy", page_icon="🤖", layout="centered")

st.title("🤖 AI Buddy")
st.caption("Voice, Camera, Photo - anni untayi")

# Chat history save cheyyadaniki
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purana messages chupinchadam
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# Input options
col1, col2, col3 = st.columns(3)

with col1:
    st.write("🎤 Voice")
    audio = mic_recorder(start_prompt="Start", stop_prompt="Stop", key='mic')

with col2:
    st.write("📷 Camera")
    camera_photo = st.camera_input("Take a photo")

with col3:
    st.write("📎 Upload")
    uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

# Text input
prompt = st.chat_input("Nenu emi cheyyali?")

# Logic
user_input = None
image_data = None

if prompt:
    user_input = prompt

if audio and audio['bytes']:
    # Ikkada audio ni text ga marchali - Google Speech API kavali
    user_input = "Nenu voice message pampanu" 

if camera_photo:
    image_data = Image.open(camera_photo)
    user_input = "Nenu camera tho photo thisanu"

if uploaded_file:
    image_data = Image.open(uploaded_file)
    user_input = "Nenu oka photo upload chesanu"

# Message save + reply
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input, "image": image_data})
    with st.chat_message("user"):
        st.markdown(user_input)
        if image_data:
            st.image(image_data)

    # AI Reply - Ikkada nee AI logic pettu
    ai_reply = "Nenu mee message chusanu! Photo unte dani gurinchi cheptha 😊"
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.markdown(ai_reply)