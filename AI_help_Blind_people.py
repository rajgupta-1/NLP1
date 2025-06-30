# app.py

import streamlit as st
import pytesseract
from PIL import Image
from langdetect import detect
from gtts import gTTS
import os
import cv2
import numpy as np
import tempfile
import platform

# ---------- Helper Functions ----------

def extract_text_from_image(uploaded_image):
    # Convert to OpenCV format
    img_cv = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # OCR
    text = pytesseract.image_to_string(thresh)
    return text.strip()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def speak_text(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            # Play audio
            if platform.system() == "Windows":
                os.system(f'start {fp.name}')
            elif platform.system() == "Darwin":  # macOS
                os.system(f'afplay {fp.name}')
            else:
                os.system(f'mpg123 {fp.name}')
    except Exception as e:
        st.error(f"Text-to-Speech Error: {e}")

# ---------- Streamlit UI ----------

st.set_page_config(page_title="AI Reader for Blind", layout="centered")

st.title("👁️ AI Reader for Blind People")
st.write("Upload an image, and I will read the text out loud in its language.")

# Upload image
uploaded_image = st.file_uploader("📸 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        extracted_text = extract_text_from_image(image)

    if extracted_text:
        st.success("✅ Text Extracted:")
        st.text_area("📝 Detected Text", extracted_text, height=200)

        lang = detect_language(extracted_text)
        st.info(f"🌐 Detected Language: {lang}")

        if st.button("🔊 Read Text Aloud"):
            speak_text(extracted_text, lang)
    else:
        st.warning("No readable text found in the image.")
