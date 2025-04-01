import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import os

# Initialize recognizer
recognizer = sr.Recognizer()

st.image("IMG_9229.JPG", width=200)

# Supported APIs
APIS = {
    "Google Speech Recognition": "google",
    "Sphinx (Offline)": "sphinx"
}

# Supported languages (ISO 639-1 codes)
LANGUAGES = {
    "English": "en-US",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE"
}

# Flag for pause/resume
is_paused = False

def transcribe_speech(api_choice, language):
    global is_paused
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        try:
            if is_paused:
                st.warning("⏸ Speech recognition is paused.")
                return ""
            
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            st.success(" Audio captured, processing...")
            
            # Choose API
            if api_choice == "google":
                text = recognizer.recognize_google(audio, language=language)
            elif api_choice == "sphinx":
                text = recognizer.recognize_sphinx(audio, language=language)
            else:
                st.error("⚠️ Unsupported API.")
                return ""

            st.success(f"📝 Transcribed: {text}")
            return text

        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
            return ""
        except sr.RequestError as e:
            st.error(f"❌ API request failed: {e}")
            return ""
        except sr.WaitTimeoutError:
            st.warning("⏳ Listening timed out. Please try again.")
            return ""

# Text-to-Speech Function
def speak(text):
    def run_tts():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
    threading.Thread(target=run_tts, daemon=True).start()

# Save Transcription
def save_to_file(text):
    filename = "transcription.txt"
    with open(filename, "w") as file:
        file.write(text)
    st.success(f"💾 Transcription saved as {filename}")

# Pause/Resume Function
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    status = "⏸ Paused" if is_paused else "▶ Resumed"
    st.info(status)

# Streamlit UI
st.title("🎙 Erinola Speech Recognition App")

# Select API
api_choice = st.selectbox("Choose Speech Recognition API:", list(APIS.keys()))
selected_api = APIS[api_choice]

# Select Language
language_choice = st.selectbox("Choose Language:", list(LANGUAGES.keys()))
selected_language = LANGUAGES[language_choice]

# Buttons
if st.button(" Start Listening"):
    transcribed_text = transcribe_speech(selected_api, selected_language)
    if transcribed_text:
        st.session_state["transcription"] = transcribed_text

if st.button(" Save Transcription"):
    if "transcription" in st.session_state:
        save_to_file(st.session_state["transcription"])
    else:
        st.warning("⚠️ No transcription available to save.")

if st.button("Speak Transcription"):
    if "transcription" in st.session_state:
        speak(st.session_state["transcription"])
    else:
        st.warning("⚠️ No text available to speak.")

if st.button("⏸ Pause/Resume"):
    toggle_pause()
