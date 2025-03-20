import requests
import geocoder
from gtts import gTTS
import os

def get_current_location():
    """Fetches the current location using GPS."""
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng  # Returns (latitude, longitude)
    else:
        return None

def get_directions(destination, api_key):
    """Fetches directions from the current location to the destination using Google Maps API."""
    current_location = get_current_location()
    if not current_location:
        return "Unable to determine current location."
    
    origin = f"{current_location[0]},{current_location[1]}"
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    
    response = requests.get(url)
    directions = response.json()
    
    if directions["status"] == "OK":
        steps = directions["routes"][0]["legs"][0]["steps"]
        instructions = []
        for step in steps:
            instructions.append(step["html_instructions"].replace("<b>", "").replace("</b>", ""))
        return instructions
    else:
        return "Could not fetch directions. Please try again."

def provide_voice_instructions(instructions):
    """Converts text instructions to speech."""
    text = " ".join(instructions)
    tts = gTTS(text=text, lang='en')
    tts.save("directions.mp3")
    os.system("start directions.mp3")  # Change this for Mac/Linux

def indoor_navigation():
    """Placeholder for indoor navigation using Wi-Fi-based services or beacons."""
    return "Indoor navigation feature is under development. Consider using specialized SDKs."

if __name__ == "__main__":
    API_KEY = "GOOGLE_MAPS_API_KEY"  # Replace with your API Key
    destination = input("Enter your destination: ")
    directions = get_directions(destination, API_KEY)
    
    if isinstance(directions, list):
        print("\n".join(directions))
        provide_voice_instructions(directions)
    else:
        print(directions)
