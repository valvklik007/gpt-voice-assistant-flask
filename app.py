from distutils.log import debug
from flask import Flask, render_template, request, jsonify, session, Response
import os
from services.speech import SpeechToText
from services.speech import TextToSpeechOpenAI
from services.gpt import AiAgentGpt
from dotenv import load_dotenv
import uuid
import json
import sys

sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = '1yjbw6AGpFLoRucwhfZUdBfS#334ffff5iwRVmlj7y2npt20_JlqOpVG8R51GqSBrXjkOV'
UPLOAD_FOLDER = "media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
deepgram_key = os.getenv("DEEPGRAM_API_KEY")


def load_messages(session_id):
    path = os.path.join(SESSION_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return [{"role": "system", "content": "Ты полезный ассистент"}]

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_messages(session_id: str, messages: list):
    path = os.path.join(SESSION_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

    audio = request.files['audio']
    file_output = f"{uuid.uuid4()}.mp3"
    path_file = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.webm")
    path_output = os.path.join(UPLOAD_FOLDER, file_output)
    audio.save(path_file)

    try:
        text  = SpeechToText(deepgram_key).responseOnlyText(path_file)

        agent = AiAgentGpt(token_key=openai_key)
        mess_session = load_messages(session["user_id"])
        agent.setStoryManual(mess_session)
        agent.setSystemPrompt("Ты должен отвечать очень коротко, в пару предложений")

        response_text = agent.getMessagesGtp(text)
        save_messages(session["user_id"], agent.getMessages())

        TextToSpeechOpenAI(api_key=openai_key).createAudio(text=response_text, output_name_file=path_output)
    except:
        return jsonify({
            "error": "no result",
        })

    return jsonify({
        "text": f"Вы спросили: {text}",
        "audio_url": file_output
    })

@app.route('/get_audio/<filename>')
def get_audio(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({
            "status": "processing"
        })

    return jsonify({
        "status": "ready",
        "audio_url": f"/stream_audio/{filename}"
    })


@app.route("/stream_audio/<filename>")
def stream_audio(filename):
    print(filename)
    def generate():
        with open(os.path.join(UPLOAD_FOLDER, filename), "rb") as f:
            while chunk := f.read(4096):
                yield chunk

    return Response(generate(), mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=False)