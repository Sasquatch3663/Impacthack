from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
from langdetect import detect
from serpapi import GoogleSearch
import os

app = Flask(__name__)

def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service"

def text_to_speech(text, voice_gender='female'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if voice_gender == 'female':
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()

def search_online(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY")  # Use environment variable for API key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if results.get("organic_results"):
        return results["organic_results"][0]["snippet"]
    return "No results found."

@app.route('/transcribe', methods=['POST'])
def transcribe():
    user_query = transcribe_audio()
    return jsonify({"query": user_query})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get("query")
    response = search_online(query)
    return jsonify({"response": response})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get("text")
    text_to_speech(text)
    return jsonify({"message": "Text has been spoken."})

if __name__ == "__main__":
    app.run(debug=True)
