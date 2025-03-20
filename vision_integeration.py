import os
import cv2
import pytesseract
import pyttsx3
import google.cloud.vision as vision
import torch
import torchvision.transforms as transforms
from PIL import Image
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
google_api_key = os.getenv("GOOGLE_CLOUD_API_KEY")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize Google Cloud Vision client
if google_api_key:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_api_key
vision_client = vision.ImageAnnotatorClient()

# Load YOLO model (for local object detection)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Function to capture image from webcam
def capture_image():
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        img_path = "captured_image.jpg"
        cv2.imwrite(img_path, image)
        print("✅ Image Captured Successfully!")
        cam.release()
        return img_path
    else:
        print("❌ Failed to capture image.")
        cam.release()
        return None

# Function for OCR (text extraction from image)
def ocr_from_image(image_path):
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        print(f"Extracted Text: {extracted_text}")
        speak(extracted_text)
        return extracted_text
    except Exception as e:
        print(f"OCR Error: {e}")
        return None

# Function to get object and scene description using Google Vision API
def google_vision_description(image_path):
    try:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = vision_client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        description = ", ".join(labels)
        print(f"🔍 Scene Description: {description}")
        speak(description)
        return description
    except Exception as e:
        print(f"Google Vision Error: {e}")
        return None

# Function to detect objects using YOLO
def yolo_object_detection(image_path):
    try:
        image = Image.open(image_path)
        transform = transforms.Compose([transforms.ToTensor()])
        img_tensor = transform(image).unsqueeze(0)
        results = model(img_tensor)
        detected_objects = results.pandas().xyxy[0]['name'].tolist()
        description = ", ".join(detected_objects)
        print(f"🛠 YOLO Detection: {description}")
        speak(description)
        return description
    except Exception as e:
        print(f"YOLO Error: {e}")
        return None

# Function to speak text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

if __name__ == "__main__":
    print("Choose input method:")
    print("1️⃣ Capture Image (Camera)")
    print("2️⃣ Upload Image")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        image_path = capture_image()
    elif choice == "2":
        image_path = input("Enter image path: ").strip()
    else:
        print("❌ Invalid choice.")
        exit()

    if image_path and os.path.exists(image_path):
        print("\nSelect Feature:")
        print("1️⃣ OCR (Extract Text from Image)")
        print("2️⃣ Google Vision (Scene/Object Detection)")
        print("3️⃣ YOLO (Local Object Detection)")
        feature_choice = input("Enter choice (1/2/3): ").strip()

        if feature_choice == "1":
            ocr_from_image(image_path)
        elif feature_choice == "2":
            google_vision_description(image_path)
        elif feature_choice == "3":
            yolo_object_detection(image_path)
        else:
            print("❌ Invalid choice.")
    else:
        print("❌ Image file not found.")
