import os
import google.generativeai as genai
import pyttsx3
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = model.start_chat(history=[])

tts_engine = pyttsx3.init()

def chatbot_response(user_input):
    """Get AI response and convert it to speech."""
    response = chat_session.send_message(user_input).text
    
    tts_engine.save_to_file(response, "static/response.mp3")
    tts_engine.runAndWait()

    return response
