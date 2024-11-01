from flask import Blueprint, request, jsonify
from .ai import palm
import speech_recognition as sr
import pyttsx3

bp = Blueprint('interview', __name__)

# STT and TTS setup
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Turn state to control alternation between candidate and AI
turn_state = "candidate_turn"

def text_to_speech(text):
    """Convert text to speech and wait until finished speaking."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def speech_to_text(audio):
    """Convert audio input to text using Google STT."""
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)

@bp.route("/interview", methods=["POST"])
def interview():
    global turn_state
    req_data = request.json
    job_description = req_data.get("job_description")
    audio = req_data.get("audio")  # Audio message input from the candidate
    history = req_data.get("history", [])
    context = f"You are an AI interviewer. Job Description: {job_description}"

    if turn_state == "candidate_turn":
        candidate_response = speech_to_text(audio)
        turn_state = "ai_turn"

        ai_response = palm(candidate_response, context, history)
        history.append({"content": candidate_response, "author": "candidate"})
        history.append({"content": ai_response, "author": "AI"})

        text_to_speech(ai_response)
        
        turn_state = "candidate_turn"
        return jsonify({"response": ai_response})

    else:
        return jsonify({"error": "It's not the candidate's turn."}), 400
