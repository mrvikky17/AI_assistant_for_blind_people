import pytesseract
from PIL import Image
import pyttsx3
import cv2
import os
import requests
import json
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
tts_engine = pyttsx3.init()

def ocr_from_image(image_path):
    """Extracts text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        print(f"📝 Extracted Text: {extracted_text.strip()}")
        speak(extracted_text)
        return extracted_text.strip()
    except Exception as e:
        print(f"❌ OCR Error: {e}")
        return None

def capture_image():
    """Captures an image using the webcam and saves it."""
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    cam.release()
    
    if result:
        img_path = "captured_image.jpg"
        cv2.imwrite(img_path, image)
        print("✅ Image Captured Successfully!")
        return img_path
    else:
        print("❌ Failed to capture image.")
        return None

def upload_image():
    """Opens a file dialog to upload an image from the system."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp;*.tiff")]
    )
    
    if file_path:
        print(f"✅ Selected Image: {file_path}")
        return file_path
    else:
        print("❌ No image selected.")
        return None

def describe_image(image_path):
    """Generates a description of the image using Google Cloud Vision API."""
    if not GOOGLE_CLOUD_API_KEY:
        print("❌ Missing GOOGLE_CLOUD_API_KEY in .env file.")
        return None

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        vision_api_url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_CLOUD_API_KEY}"
        request_body = {
            "requests": [{
                "image": {"content": image_data.decode("latin1")},  # Encoding fix
                "features": [{"type": "LABEL_DETECTION"}]
            }]
        }
        
        response = requests.post(vision_api_url, json=request_body)
        result = response.json()

        if "responses" in result and result["responses"]:
            labels = result["responses"][0].get("labelAnnotations", [])
            description = ", ".join([label["description"] for label in labels[:5]])
            print(f"📷 Image Description: {description}")
            speak(f"The image contains {description}")
            return description
        else:
            print("❌ No description found.")
            return None
    except Exception as e:
        print(f"❌ Image Description Error: {e}")
        return None

def speak(text):
    """Converts text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

if __name__ == "__main__":
    print("Choose an input method:")
    print("1️⃣ Capture Image (Camera)")
    print("2️⃣ Select Image from System")
    choice = input("Enter choice (1/2): ").strip()

    image_path = None
    if choice == "1":
        image_path = capture_image()
    elif choice == "2":
        image_path = upload_image()
    else:
        print("❌ Invalid choice.")
        exit()

    if image_path and os.path.exists(image_path):
        extracted_text = ocr_from_image(image_path)
        image_description = describe_image(image_path)
        
        # Combine extracted text & description for better context
        if extracted_text and image_description:
            combined_output = f"📝 Extracted Text: {extracted_text}.\n📷 Image Description: {image_description}."
            speak(combined_output)
    else:
        print("❌ Image file not found.")