import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import re


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

genai.configure(api_key=api_key)

# Set up model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1000,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat_session = model.start_chat(history=[])

# Flask App
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"reply": "I didn't receive any message."})
        
        response = chat_session.send_message(user_input)
        clean_reply = re.sub(r'\*+', '', response.text)  # Remove ** and * formatting

        return jsonify({"reply": clean_reply})

    except Exception as e:
        return jsonify({"reply": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
