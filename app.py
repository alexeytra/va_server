from flask import Flask, jsonify, send_file
from flask import request
from classes.IntentClassifier import IntentClassifier
from utils.AudioWorker import text_to_speech, speech_to_text
from utils.intent_processing import get_answer_from_tag, load_intents

from utils.load_data import classes, model, tokenizer, label_encoder

app = Flask(__name__)

BASE_URL = '/va/api/v1/'


@app.route(BASE_URL + 'question/text', methods=['POST'])
def process_question_text():
    response = {
        "audio_answer": request.host_url + BASE_URL[1:] + 'audio_answer'
    }
    data = request.json
    intent_classifier = IntentClassifier(classes, model, tokenizer, label_encoder)
    intent_tag = intent_classifier.get_intent(data['question'])
    data = get_answer_from_tag(intent_tag)
    if data[1] != '':
        answer = str(data[0] + data[1])
        text_to_speech(data[0])
        response['answer'] = answer
        return response
    text_to_speech(data[0])
    response['answer'] = data[0]
    return response


@app.route(BASE_URL + 'question/audio', methods=['POST'])
def process_question_audio():
    # speech_to_text("./temp_data/input.wav")
    return ''


@app.route(BASE_URL + 'audio_answer', methods=['GET'])
def get_audio_answer():
    return send_file('temp_data/outputAudio.mp3')


@app.route(BASE_URL + 'test', methods=['GET'])
def test():
    return BASE_URL[1:]


if __name__ == '__main__':
    app.run(debug=True)
