from flask import Flask, render_template, request, jsonify, session, Response
import os
from services.speech import SpeechToText
from services.speech import TextToSpeechOpenAI
from services.gpt import AiAgentGpt
from dotenv import load_dotenv
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = '1yjbw6AGpFLoRucwhfZUdB5iwRVmlj7y2npt20_JlqOpVG8R51GqSBrXjkOV'
UPLOAD_FOLDER = "media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

agents = {}
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
deepgram_key = os.getenv("DEEPGRAM_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
        agents[session["user_id"]] = AiAgentGpt(token_key=openai_key)
    elif session["user_id"] not in agents:
        agents[session["user_id"]] = AiAgentGpt(token_key=openai_key)

    audio = request.files['audio']
    file_output = f"{uuid.uuid4()}.mp3"
    path_file = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.webm")
    path_output = os.path.join(UPLOAD_FOLDER, file_output)
    audio.save(path_file)

    agent = agents[session["user_id"]]
    agent.setSystemPrompt('Ты должен отвечать очень коротко, в пару предложений')
    text  = SpeechToText(deepgram_key).responseOnlyText(path_file)
    response_text = agent.getMessagesGtp(text)
    TextToSpeechOpenAI(api_key=openai_key).createAudio(text=response_text, output_name_file=path_output)

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