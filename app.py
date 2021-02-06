from flask import Flask, send_file
from flask import request
from classes.Seq2Seq import Seq2SeqModel
from classes.VAResponse import VAResponse
from utils.audio_worker import text_to_speech, speech_to_text
import os

from utils.intent_processing import load_additional_info
from utils.load_data import classes, ic_model, ic_tokenizer, label_encoder, seq2seq_model, seq2seq_tokenizer

app = Flask(__name__)

BASE_URL = '/va/api/v1/'
app.config['UPLOAD_PATH'] = '/temp_data/'


@app.route(BASE_URL + 'question/text', methods=['POST'])
def process_question_text():
    url_audio = request.host_url + BASE_URL[1:] + 'audio_answer'
    question = request.json['question']
    va_response = VAResponse(url_audio, question)
    return va_response.get_response()


@app.route(BASE_URL + 'question/audio', methods=['POST'])
def process_question_audio():
    for f in request.files.getlist('audio'):
        f.save(os.path.join(os.getcwd() + app.config['UPLOAD_PATH'], f.filename))
    url_audio = request.host_url + BASE_URL[1:] + 'audio_answer'
    question = speech_to_text("./temp_data/input.wav")
    va_response = VAResponse(url_audio, question)
    return va_response.get_response()


@app.route(BASE_URL + 'audio_answer', methods=['GET'])
def get_audio_answer():
    return send_file('temp_data/outputAudio.mp3')


@app.route(BASE_URL + 'test', methods=['GET'])
def test():
    result = load_additional_info('системы информатики', 'kaf_location')
    return 'test'


@app.route(BASE_URL + 'test/seq2seq', methods=['POST'])
def test_seq2seq():
    seq2seq = Seq2SeqModel(seq2seq_model, seq2seq_tokenizer, 15)
    return seq2seq.get_answer("Ты милый")


if __name__ == '__main__':
    app.run(debug=True)
