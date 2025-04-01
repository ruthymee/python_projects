import streamlit as st
import random
import json
import os
import speech_recognition as sr
from gtts import gTTS
from nltk.sentiment import SentimentIntensityAnalyzer
from io import BytesIO
import requests
from PIL import Image

# File to store user data
USER_DATA_FILE = 'user_data.json'

# Load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save user data
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file, indent=4)

# Initialize user data
user_data = load_user_data()

st.image("IMG_9229.JPG", width=200)

# Function to show AI Avatar
def get_ai_avatar():
    url = "https://randomuser.me/api/portraits/women/1.jpg" 
    return Image.open(BytesIO(requests.get(url).content))
    

# Function to show User Avatar
def get_user_avatar():
    url = "https://randomuser.me/api/portraits/men/1.jpg"
    return Image.open(BytesIO(requests.get(url).content))

# Joke Collection
JOKES = [
    "Why don't skeletons fight? Because they don’t have the guts!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "What do you call fake spaghetti? An impasta!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised!",
    "Parallel lines have so much in common. It’s a shame they’ll never meet!",
    "I used to play piano by ear, but now I use my hands!",
    "What do you call cheese that isn’t yours? Nacho cheese!",
    "I’m on a seafood diet. I see food, and I eat it!",
    "I asked the librarian if the library had any books on paranoia. She whispered, 'They’re right behind you.'",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats!"
]

# Welcome Audio
def welcome_voice():
    tts = gTTS(text="Welcome to Erinola Voice System", lang='en')
    tts.save("welcome.mp3")
    st.audio("welcome.mp3", format="audio/mp3", autoplay=True)

# Speech-to-text function with real-time display
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.text(f"Recognized: {text}")  # Real-time display
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Could not request results, please check your internet connection."

# Sentiment Analysis
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return "positive"
    elif score['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

# Handle user input based on personality and sentiment
def handle_user_input(user_input, personality):
    user_input = user_input.lower().strip()
    sentiment = analyze_sentiment(user_input)
    
    # Adding Go My Code responses
    gomycodes_info = {
        "about": "Go My Code is an educational platform that gathers the best tech talents in the region. We empower people by upskilling and reskilling them on digital skills through instructor-assisted, affordable, and quality training. GO MY CODE is the largest developer community in Africa and the Middle East. We train the next generation of developers and connect them with the best digital projects around the world.",
        "courses": [
            "Web Development",
            "Data Science & AI",
            "Mobile Development",
            "Game Development",
            "UX/UI Design",
            "Digital Marketing",
            "Cyber Security",
            "Cloud Computing",
            "Blockchain"
        ]
    }

    responses = {
        "friendly": {
            "greet": ["Hello, friend! How can I brighten your day? ", "Hey there! How's your day going?"],
            "bye": ["Goodbye! Stay awesome!", "See you later, take care!"],
            "neutral": "I'm here to chat! What's on your mind?",
            "positive": "That's great to hear! Keep smiling! ",
            "negative": "I'm sorry to hear that. Want to talk about it? ",
            "joke": random.choice(JOKES),
            "gomycodes_about": gomycodes_info["about"],
            "gomycodes_courses": "\n".join(gomycodes_info["courses"])
        },
        "sarcastic": {
            "greet": ["Oh great, another human to chat with. ", "Hey, what now?"],
            "bye": ["Finally, some peace! Bye! ", "Later, genius!"],
            "neutral": "Meh, let's see what you've got to say...",
            "positive": "Wow, what an incredible revelation! ",
            "negative": "Oh no, life is *so* unfair. Tell me more. ",
            "joke": random.choice(JOKES),
            "gomycodes_about": gomycodes_info["about"],
            "gomycodes_courses": "\n".join(gomycodes_info["courses"])
        },
        "professional": {
            "greet": ["Hello. How can I assist you today?", "Greetings. How may I be of service?"],
            "bye": ["Goodbye. Have a productive day!", "See you later. Stay efficient!"],
            "neutral": "I am here to provide information. How may I help?",
            "positive": "That sounds promising. Let’s build on that!",
            "negative": "I understand. Perhaps we can find a solution together.",
            "joke": random.choice(JOKES),
            "gomycodes_about": gomycodes_info["about"],
            "gomycodes_courses": "\n".join(gomycodes_info["courses"])
        }
    }
    
    # Respond to GoMyCode queries
    if "go my code" in user_input or "gomycodes" in user_input:
        if "about" in user_input or "tell me about" in user_input:
            return responses[personality]["gomycodes_about"]
        elif "courses" in user_input or "available courses" in user_input:
            return responses[personality]["gomycodes_courses"]
    
    if "hello" in user_input or "hi" in user_input:
        return random.choice(responses[personality]["greet"])
    if "bye" in user_input:
        return random.choice(responses[personality]["bye"])
    if "joke" in user_input:
        return responses[personality]["joke"]
    
    return responses[personality][sentiment]

# Chat Interface with Avatars
def chat_interface():
    st.title("Erinola Chatbot Voice & Personality")
    st.write("Choose a personality and start chatting!")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    personality = st.radio("Select Chatbot Personality:", ["friendly", "sarcastic", "professional"], index=0)
    user_input = st.text_input("You:", key="user_input")
    
    # Handle the chat and avatars
    if st.button("🎤 Speak"):
        user_input = speech_to_text()
        if user_input:
            response = handle_user_input(user_input, personality)
            st.session_state.chat_history.append(("User", user_input, get_user_avatar()))
            st.session_state.chat_history.append(("Bot", response, get_ai_avatar()))
            speak(response)
    
    if st.button("Send"):
        if user_input:
            response = handle_user_input(user_input, personality)
            st.session_state.chat_history.append(("User", user_input, get_user_avatar()))
            st.session_state.chat_history.append(("Bot", response, get_ai_avatar()))
            speak(response)
    
    for speaker, message, avatar in st.session_state.chat_history:
        if speaker == "User":
            st.image(avatar, width=40)
            st.markdown(f'**{speaker}:** {message}')
        else:
            st.image(avatar, width=40)
            st.markdown(f'**{speaker}:** {message}')

# Speak function for text-to-speech
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    st.audio("response.mp3", format="audio/mp3", autoplay=True)

# Main App
st.title("Welcome to Erinola Voice System")

# Play welcome voice when the app starts
welcome_voice()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in user_data and user_data[username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Welcome, {username}! 🎉")
                chat_interface()
            else:
                st.error("Invalid username or password.")
    with tab2:
        st.subheader("Create an Account")
        new_username = st.text_input("Enter a username")
        new_password = st.text_input("Enter a password", type="password")
        if st.button("Create Account"):
            if new_username in user_data:
                st.warning("Username already exists. Please choose a different one.")
            else:
                user_data[new_username] = {"password": new_password, "profile": {}}
                save_user_data(user_data)
                st.success("Account created successfully! Please login.")
else:
    chat_interface()
