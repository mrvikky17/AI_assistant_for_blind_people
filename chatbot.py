import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check if API key is set
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

# Configure Gemini API
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1000,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session
chat_session = model.start_chat(history=[])

# Initialize Speech Recognition and TTS
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function for Speech-to-Text (STT)
def speech_to_text():
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"👤 You (Voice): {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Sorry, could not understand your voice.")
            return None
        except sr.RequestError:
            print("❌ Error connecting to Google STT.")
            return None
        except sr.WaitTimeoutError:
            print("⏳ No speech detected.")
            return None

# Function for Text-to-Speech (TTS)
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

print("\n🤖 AI Chatbot: Hello! Type or Speak. Say 'exit' to quit.")

while True:
    print("\n(1) Type your message")
    print("(2) Speak your message")
    mode = input("Choose input mode (1/2): ").strip()

    if mode == "1":
        user_input = input("👤 You (Text): ")
    elif mode == "2":
        user_input = speech_to_text()
        if not user_input:  # If voice input fails, skip to next iteration
            continue
    else:
        print("❌ Invalid choice, try again.")
        continue

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("🤖 AI Chatbot: Goodbye! Have a great day! 👋")
        speak("Goodbye! Have a great day!")
        break

    # Get AI response
    response = chat_session.send_message(user_input)
    print(f"🤖 AI Chatbot: {response.text}")
    speak(response.text)  # Convert response to speech
    
