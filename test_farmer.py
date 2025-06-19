#%%writefile app.py
import streamlit as st
from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment
import os

st.set_page_config(page_title="AI Helper for Farmers", layout="centered")
st.title("🌾 AI Helper for Farmers")

st.write("Upload a crop image and describe the problem in your voice.")

# ---- Image Upload ----
uploaded_image = st.file_uploader("📷 Upload Crop Image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Crop Image", use_column_width=True)
    st.success("✅ Image uploaded successfully.")

# ---- Audio Upload ----
uploaded_audio = st.file_uploader("🎤 Upload Voice Description (MP3 or WAV)", type=["mp3", "wav"])
text_output = ""

if uploaded_audio:
    # Save the audio
    audio_path = "input_audio.wav"

    # Convert mp3 to wav if needed
    if uploaded_audio.type == "audio/mp3":
        audio = AudioSegment.from_file(uploaded_audio, format="mp3")
        audio.export(audio_path, format="wav")
    else:
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.read())

    st.audio(audio_path)

    # Transcribe using speech_recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        st.info("🎙️ Transcribing speech...")
        audio_data = recognizer.record(source)
        try:
            text_output = recognizer.recognize_google(audio_data)
            st.success("📝 Transcription Complete:")
            st.write(f"**You said:** {text_output}")
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("❌ Could not request results. Check your internet connection.")

# ---- Simple Problem Detection Logic ----
def analyze_problem(text):
    text = text.lower()
    if "yellow" in text or "leaf" in text:
        return "The crop might be suffering from nutrient deficiency. Consider checking soil nitrogen levels."
    elif "holes" in text or "insect" in text:
        return "There might be an insect infestation. Use neem oil spray or insecticide."
    elif "dry" in text or "no water" in text:
        return "The crop may be water-stressed. Ensure proper irrigation."
    else:
        return "Unable to determine problem accurately. Please consult an expert."

# ---- Show Diagnosis ----
if text_output:
    solution = analyze_problem(text_output)
    st.subheader("🩺 AI Diagnosis")
    st.write(solution)
