import os
import google.generativeai as genai
import requests
import json
import pyttsx3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

# Initialize Text-to-Speech Engine
tts_engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

# Configure Gemini API
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def query_gemini(question):
    """Handles general Q&A using Gemini AI."""
    response = model.generate_content(question)
    return response.text if response else "Sorry, I couldn't find an answer."

def get_news():
    """Fetches the latest news headlines."""
    if not news_api_key:
        return "News API key is missing. Please configure it in .env."
    
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        news_data = response.json()
        if news_data["status"] == "ok":
            headlines = [article["title"] for article in news_data["articles"][:5]]
            return "\n".join(headlines)
        else:
            return "Failed to fetch news."
    except Exception as e:
        return f"Error fetching news: {e}"

def get_weather(city):
    """Fetches current weather information for a given city."""
    if not weather_api_key:
        return "Weather API key is missing. Please configure it in .env."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    try:
        response = requests.get(url)
        weather_data = response.json()
        if weather_data["cod"] == 200:
            temp = weather_data["main"]["temp"]
            condition = weather_data["weather"][0]["description"]
            return f"Current weather in {city}: {temp}°C, {condition}."
        else:
            return "City not found."
    except Exception as e:
        return f"Error fetching weather: {e}"

if __name__ == "__main__":
    print("\n🤖 Instant Information Assistant")
    while True:
        print("\n1️⃣ General Q&A (Ask anything!)")
        print("2️⃣ Get Latest News")
        print("3️⃣ Get Weather Info")
        print("4️⃣ Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            question = input("🔍 Ask your question: ")
            answer = query_gemini(question)
            print(f"🤖 AI: {answer}")
            speak(answer)
        elif choice == "2":
            news = get_news()
            print(f"📰 Latest News:\n{news}")
            speak(news)
        elif choice == "3":
            city = input("🌍 Enter city name: ")
            weather_info = get_weather(city)
            print(f"🌦 {weather_info}")
            speak(weather_info)
        elif choice == "4":
            print("👋 Goodbye!")
            speak("Goodbye! Have a great day!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
