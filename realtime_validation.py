import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import pytesseract
import cv2
from google.cloud import vision
from google.oauth2 import service_account
import numpy as np

# Initialize speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return ""

# AI Chatbot using Google Gemini API
def chat_with_ai(prompt):
    genai.configure(api_key='GEMINI_API_KEY')
    response = genai.Chat().send_message(prompt)
    return response.text

# Optical Character Recognition (OCR)
def perform_ocr(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    print("Extracted Text:", text)
    return text

# Google Vision API for Image Analysis
def analyze_image(image_path):
    credentials = service_account.Credentials.from_service_account_file('YOUR_SERVICE_ACCOUNT_JSON')
    client = vision.ImageAnnotatorClient(credentials=credentials)
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    print("Detected Objects:", labels)
    return labels

# YOLO Object Detection
def yolo_object_detection(image_path):
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)
    objects = []
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                objects.append(class_id)
    print("Detected Objects (YOLO):", objects)
    return objects

# Main program loop
def main():
    while True:
        user_input = recognize_speech()
        if "exit" in user_input:
            print("Goodbye!")
            break
        elif "what is" in user_input or "who is" in user_input:
            response = chat_with_ai(user_input)
            print("AI:", response)
            speak(response)
        elif "read text from image" in user_input:
            text = perform_ocr("sample.jpg")
            speak(text)
        elif "analyze image" in user_input:
            labels = analyze_image("sample.jpg")
            speak("I see " + ", ".join(labels))
        elif "detect objects" in user_input:
            yolo_object_detection("sample.jpg")

if __name__ == "__main__":
    main()
