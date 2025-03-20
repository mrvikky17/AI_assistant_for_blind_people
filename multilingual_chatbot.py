import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from googletrans import Translator, LANGUAGES
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")
genai.configure(api_key=api_key)

# Initialize Chatbot Model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,    
    "max_output_tokens": 1000,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
chat_session = model.start_chat(history=[])

# Initialize Translator, Speech Recognition, and TTS
translator = Translator()
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to detect and translate input language
def detect_and_translate(text, target_lang="en"):
    detected_lang = translator.detect(text).lang
    translated_text = translator.translate(text, src=detected_lang, dest=target_lang).text
    return translated_text, detected_lang

# Function to translate response back to user's language
def translate_response(text, target_lang):
    return translator.translate(text, src="en", dest=target_lang).text

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
            print("❌ Could not understand.")
            return None
        except sr.RequestError:
            print("❌ Google STT service error.")
            return None
        except sr.WaitTimeoutError:
            print("⏳ No speech detected.")
            return None

# Function for Text-to-Speech (TTS)
def speak(text, lang="en"):
    tts_engine.setProperty("voice", lang)
    tts_engine.say(text)
    tts_engine.runAndWait()

# Main chatbot loop
print("\n🤖 AI Chatbot: Hello! Type or Speak. Say 'exit' to quit.")
print("🌍 Available languages:", ", ".join(list(LANGUAGES.values())))

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
        speak("Goodbye! Have a great day!", "en")
        break

    # Detect and translate input to English
    translated_input, user_lang = detect_and_translate(user_input)
    print(f"🔄 Translated to English: {translated_input}")

    # Get AI response
    response = chat_session.send_message(translated_input)
    
    # Translate response back to user's language
    final_response = translate_response(response.text, user_lang)
    print(f"🤖 AI Chatbot ({LANGUAGES[user_lang]}): {final_response}")
    
    # Speak response in user's language
    speak(final_response, user_lang)
