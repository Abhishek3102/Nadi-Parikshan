# from flask import Flask, request, jsonify, render_template
# import json
# import os
# from dotenv import load_dotenv
# import speech_recognition as sr
# from gtts import gTTS
# from io import BytesIO
# import tempfile
# from huggingface_hub import InferenceClient

# load_dotenv()

# app = Flask(__name__)

# # Load Nadi Parikshan data (this remains unchanged)
# def load_nadi_data():
#     with open('nadi_data.json', 'r') as f:
#         return json.load(f)

# nadi_data = load_nadi_data()

# # Load the AI assistant model
# hf_api_token = "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"
# client = InferenceClient(
#     "mistralai/Mixtral-8x7B-Instruct-v0.1",
#     token=hf_api_token
# )

# # Function to generate AI assistant responses
# def generate_ai_response(user_input):
#     system_message = "You are an AI assistant. Answer questions clearly and concisely."

#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": user_input}
#     ]

#     response = ""
#     for message in client.chat_completion(
#             messages=messages,
#             max_tokens=150,
#             stream=True
#     ):
#         response += message.choices[0].delta.content or ""

#     return response

# # Function to generate response based on Nadi Parikshan input
# def generate_nadi_response(user_input, user_context):
#     if "nadi" in user_input.lower():
#         return "Please provide your dominant nadi (Vata, Pitta, or Kapha)."
    
#     nadi_type = user_input.strip().lower()
#     if nadi_type in nadi_data:
#         recommendations = nadi_data[nadi_type]
#         response = recommendations.get("general", "I don't have specific advice for this nadi.")
        
#         if user_context.get("gender") == "female":
#             response += f" {recommendations.get('female', '')}"
#         elif user_context.get("gender") == "male":
#             response += f" {recommendations.get('male', '')}"
        
#         return response

#     return "I'm sorry, I didn't understand that. Can you clarify?"

# # Function to transcribe audio input
# def transcribe_audio(audio_data):
#     try:
#         r = sr.Recognizer()
#         with sr.AudioFile(audio_data) as source:
#             audio = r.record(source)
#         return r.recognize_google(audio)
#     except Exception as e:
#         return f"Error transcribing audio: {str(e)}"

# # Function to convert text to speech
# def text_to_speech(text):
#     tts = gTTS(text=text, lang='en')
#     audio_bytes = BytesIO()
#     tts.write_to_fp(audio_bytes)
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# # Route to render the HTML page
# @app.route('/')
# def home():
#     return render_template('index.html')  # Make sure your HTML is named 'index.html'

# # Flask route to handle chatbot interaction
# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get("message", "")
#     user_context = request.json.get("context", {"gender": "unknown"})

#     # Determine if the message is related to Nadi Parikshan or an AI conversation
#     if "nadi" in user_input.lower():
#         response = generate_nadi_response(user_input, user_context)
#     else:
#         response = generate_ai_response(user_input)

#     return jsonify({"response": response})

# # Flask route for transcribing audio input to text
# @app.route('/transcribe', methods=['POST'])
# def transcribe():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file provided."}), 400
    
#     audio_file = request.files['audio']
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#         temp_audio.write(audio_file.read())
#         temp_audio_path = temp_audio.name

#     transcribed_text = transcribe_audio(temp_audio_path)
#     os.unlink(temp_audio_path)
#     return jsonify({"transcription": transcribed_text})

# # Flask route for converting text to speech
# @app.route('/speak', methods=['POST'])
# def speak():
#     text = request.json.get("text", "")
#     audio_data = text_to_speech(text)
#     return jsonify({"audio": audio_data.decode('latin-1')})

# # Start the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

app = Flask(__name__)

def load_nadi_data():
    with open('nadi_data.json', 'r') as f:
        return json.load(f)

nadi_data = load_nadi_data()

hf_api_token = "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"
client = InferenceClient(
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    token=hf_api_token
)

def generate_ai_response(user_input):
    system_message = "You are an AI assistant. Answer questions clearly and concisely. Answer questions related to nadi parikshan and diets, exercises and other things related to this domain only. Also the user might ask follow up questions like they followed suggestions that u gave, but it still did not work out for them and they saw no improvements. Then you ask them more questions and try to go in details of their queries and then provide context based answers. "
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]
    response = ""
    for message in client.chat_completion(
            messages=messages,
            max_tokens=250,
            stream=True
    ):
        response += message.choices[0].delta.content or ""
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    response = generate_ai_response(user_input)
    return jsonify({"response": response})

@app.route('/nadi_recommendations', methods=['POST'])
def nadi_recommendations():
    nadi = request.json.get("nadi", "").lower()
    gender = request.json.get("gender", "").lower()
    age = request.json.get("age", "").lower()
    if nadi not in nadi_data:
        return jsonify({"error": "Invalid Nadi type provided."}), 400
    recommendations = nadi_data.get(nadi, {})
    response = {
        "general": recommendations.get("general", "No general recommendations available."),
        "diet": recommendations.get("diet", {}),
        "exercise": recommendations.get("exercise", "No exercise recommendations available."),
        "common_diseases": recommendations.get("diseases", {}).get("common", "No disease data available."),
        "remedies": recommendations.get("diseases", {}).get("remedies", "No remedies available."),
        "imbalances": recommendations.get("imbalances", {}),
        "lifestyle_tips": recommendations.get("lifestyle_tips", []),
        "gender_specific": recommendations.get(gender, "No gender-specific recommendations available."),
        "age_specific": recommendations.get("age", {}).get(age, "No age-specific recommendations available.")
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)







