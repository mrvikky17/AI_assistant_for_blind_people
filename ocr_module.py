import pytesseract
from PIL import Image
import pyttsx3
import cv2
import os

tts_engine = pyttsx3.init()

def ocr_from_image(image_path):
    """Extracts text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        print(f"Extracted Text: {extracted_text}")
        speak(extracted_text)
        return extracted_text
    except Exception as e:
        print(f"OCR Error: {e}")
        return None

def capture_image():
    """Captures an image using the webcam and saves it."""
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

def speak(text):
    """Converts text to speech."""
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
        ocr_from_image(image_path)
    else:
        print("❌ Image file not found.")
