from flask import Flask, send_file, Response
from flask import request
from classes.Seq2Seq import Seq2SeqModel
from classes.DialogManager import DialogManager
from constants.constants import BASE_URL
from utils.audio_worker import speech_to_text
import os
from utils.load_data import seq2seq_model, seq2seq_tokenizer
from classes.EntityExtractor import EntityExtractor

app = Flask(__name__)
app.config['UPLOAD_PATH'] = '/temp_data/'
app.config['SECRET_KEY'] = 'df458dfsd785as-1s4d5fd87-54fg45f7gdf4gd-sr7g65df4g'


@app.route(BASE_URL + 'question/text', methods=['POST'])
def process_question_text():
    question = request.json['question']
    voice = request.json['voice']
    answer_generating = request.json['generateAnswer']
    va_response = DialogManager(answer_generating=answer_generating, voice=voice)
    va_response.process_question(question)
    return va_response.get_response()


@app.route(BASE_URL + 'question/audio', methods=['POST'])
def process_question_audio():
    for f in request.files.getlist('audio'):
        f.save(os.path.join(os.getcwd() + app.config['UPLOAD_PATH'], f.filename))
    question = speech_to_text("./temp_data/input.wav")
    va_response = DialogManager(question)
    return va_response.get_response()


@app.route(BASE_URL + 'answer/audio', methods=['GET'])
def get_audio_answer():
    return send_file('temp_data/outputAudio.mp3')


@app.route(BASE_URL + 'answer/wrong', methods=['POST'])
def process_wrong_answer():
    data = request.json
    va_response = DialogManager(answer_generating=True, voice=False)
    va_response.process_wrong_answer(data)
    return va_response.get_response()


@app.route(BASE_URL + 'review', methods=['POST'])
def process_review():
    data = request.json
    return Response(status=200)


@app.route(BASE_URL + 'greeting', methods=['POST'])
def process_greeting():
    va_response = DialogManager(voice=request.json['voice'])
    va_response.greeting()
    return va_response.get_response()


@app.route(BASE_URL + 'user/greeting', methods=['POST'])
def process_user_greeting():
    va_response = DialogManager(voice=request.json['voice'])
    va_response.user_greeting(request.json)
    return va_response.get_response()


@app.route(BASE_URL + 'user/login', methods=['POST'])
def process_user_auth_response():
    va_response = DialogManager(voice=request.json['voice'])
    va_response.get_response_user_auth(request.json)
    return va_response.get_response()


@app.route(BASE_URL + 'user/logout', methods=['POST'])
def process_user_logout_response():
    va_response = DialogManager(voice=request.json['voice'])
    va_response.get_response_user_logout()
    return va_response.get_response()


@app.route(BASE_URL + 'test', methods=['GET'])
def test():
    entity_extractor = EntityExtractor()
    result = entity_extractor.extract_entity('Где находится кафедра системы информатики')
    return result


@app.route(BASE_URL + 'test/seq2seq', methods=['POST'])
def test_seq2seq():
    seq2seq = Seq2SeqModel(seq2seq_model, seq2seq_tokenizer, 15)
    return seq2seq.get_answer("Ты милый")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
