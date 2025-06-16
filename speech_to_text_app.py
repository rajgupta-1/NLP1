import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

def convert_audio_to_wav(audio_file_path):
    sound = AudioSegment.from_file(audio_file_path)
    wav_path = audio_file_path.replace(".mp3", ".wav")
    sound.export(wav_path, format="wav")
    return wav_path

def speech_to_text(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"

def main():
    st.title("🎤 Speech to Text Converter")
    st.write("Upload an MP3 or WAV file to convert speech to text.")

    uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as temp_audio:
            temp_audio.write(uploaded_file.read())
            temp_audio_path = temp_audio.name

        # Convert MP3 to WAV if needed
        if uploaded_file.type == "audio/mp3":
            wav_path = convert_audio_to_wav(temp_audio_path)
        else:
            wav_path = temp_audio_path

        st.audio(uploaded_file, format=uploaded_file.type)

        st.write("⏳ Converting...")
        text = speech_to_text(wav_path)
        st.write("✅ Converted Text:")
        st.success(text)

        # Clean up
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(wav_path) and wav_path != temp_audio_path:
            os.remove(wav_path)

if __name__ == "__main__":
    main()
