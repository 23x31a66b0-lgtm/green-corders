from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import requests

app = Flask(__name__)
CORS(app)

# Question Answer
@app.route('/getanswer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get("question","").lower()

    if "yellow" in question:
        answer="Yellow leaves indicate nitrogen deficiency."
    elif "pest" in question:
        answer="Use neem oil spray to control pests."
    elif "water" in question:
        answer="Ensure balanced irrigation."
    else:
        answer="Check soil nutrients and crop health."

    return jsonify({"answer":answer})


# Image Upload
@app.route('/analyze', methods=['POST'])
def analyze_crop():

    if 'image' not in request.files:
        return jsonify({"result":"No image uploaded"})

    image=request.files['image']
    image.save(image.filename)

    return jsonify({"result":"Image received. Possible crop disease detected."})


# Voice Query
@app.route('/voice-query', methods=['POST'])
def voice_query():

    if 'audio' not in request.files:
        return jsonify({"result":"No audio uploaded"})

    audio=request.files['audio']
    audio.save("voice.wav")

    recognizer=sr.Recognizer()

    try:
        with sr.AudioFile("voice.wav") as source:
            audio_data=recognizer.record(source)
            text=recognizer.recognize_google(audio_data)

        result="You said: "+text

    except:
        result="Voice not recognized"

    return jsonify({"result":result})


# Weather Advice
@app.route('/soil', methods=['POST'])
def soil():

    data=request.get_json()
    city=data.get("city")

    if not city:
        return jsonify({"recommendation":"Enter location"})

    try:

        api_key="YOUR_API_KEY"

        weather=requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        ).json()

        temp=weather['main']['temp']

        if temp>300:
            rec="High temperature. Use soil with good water retention."
        else:
            rec="Normal temperature. Standard soil works."

    except:
        rec="Weather data unavailable"

    return jsonify({"recommendation":rec})


if __name__=="__main__":
    app.run(debug=True)