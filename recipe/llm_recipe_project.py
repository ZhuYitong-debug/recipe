import os
import requests
import pyttsx3
import threading
import speech_recognition as sr
from dotenv import load_dotenv

# Initialize the speech engine
engine = pyttsx3.init()

# Load the API Key from the .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# Global variable for controlling speech thread
tts_thread = None

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Set the language globally
language = 'en-US'  # Default to English

def speak(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()
    global tts_thread
    tts_thread = threading.Thread(target=run_speech)
    tts_thread.start()

def stop_speech():
    engine.stop()
    print("🛑 Speech has been stopped.")

def set_speed():
    try:
        rate = int(input("Please enter the speech rate (suggested range: 120–200, default 160): "))
        engine.setProperty('rate', rate)
        print(f"✅ Speech rate has been set to {rate}")
    except:
        print("⚠️ Invalid input, using default rate.")

def set_language():
    global language
    print("\n🎧 Select speech language:")
    print("1. English")
    print("2. Chinese")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == "1":
        language = 'en-US'
        engine.setProperty('language', 'en')
        print("✅ Language set to English.")
    elif choice == "2":
        language = 'zh-CN'
        engine.setProperty('language', 'zh')
        print("✅ Language set to Chinese.")
    else:
        print("⚠️ Invalid input, using default language (English).")

def generate_recipe(ingredients, diet):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": f"""
Please generate a recipe based on the following ingredients for a {diet} diet, including:
- Dish Name
- Ingredients and amounts
- Cooking steps
Ingredients: {ingredients}
""" if language == 'en-US' else f"""
请根据以下食材生成一个符合 {diet} 饮食偏好的食谱，包含：
- 菜名
- 用料及用量
- 做法步骤
食材：{ingredients}
"""}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Request failed, status code: {response.status_code}, error: {response.text}"

def listen_for_input():
    with sr.Microphone() as source:
        print("🎙️ Please say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("🔊 Recognizing...")
            text = recognizer.recognize_google(audio, language=language)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("⚠️ Unable to understand the audio, please try again.")
            return None
        except sr.RequestError:
            print("⚠️ Speech recognition service is unavailable, please check your network connection.")
            return None

# Main program entry point
if __name__ == "__main__":
    print("🥗 Welcome to the DeepSeek AI Recipe Generator!")

    # Get ingredients and diet preference input
    ingredients = input("Enter the ingredients you have (comma separated): ")
    diet = input("Enter your diet preference (e.g., vegan, keto, low-carb): ")

    print("\n🧠 Generating recipe, please wait...\n")
    recipe = generate_recipe(ingredients, diet)
    print("✅ Here is your recipe:\n")
    print(recipe)

    while True:
        print("\n🎧 Voice control menu:")
        print("1. Set speech rate")
        print("2. Start speech")
        print("3. Stop speech")
        print("4. Enable voice input")
        print("5. Set language")
        print("6. Exit program")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            set_speed()
        elif choice == "2":
            speak(recipe)
        elif choice == "3":
            stop_speech()
        elif choice == "4":
            input_text = listen_for_input()
            if input_text:
                ingredients = input_text
                print(f"New ingredients input: {ingredients}")
                print("\n🧠 Generating new recipe, please wait...\n")
                recipe = generate_recipe(ingredients, diet)
                print("✅ Here is your new recipe:\n")
                print(recipe)
        elif choice == "5":
            set_language()
        elif choice == "6":
            stop_speech()
            print("👋 Goodbye, enjoy your meal!")
            break
        else:
            print("⚠️ Invalid input, please try again.")
